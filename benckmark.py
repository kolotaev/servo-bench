import os
import re
import time
import sys
import threading
import itertools
import argparse
from contextlib import contextmanager
from string import Template
from functools import partial
from statistics import mean

import pexpect


parser = argparse.ArgumentParser(description='Run servo-bench benchmark.')
parser.add_argument('-d', '--duration', dest='RUN_TIME', nargs='?', type=int, default=60,
                    help='run wrk for N seconds (default: %(default)d)')
parser.add_argument('-t', '--threads', dest='THREADS', nargs='?', type=int, default=12,
                    help='threads number for wrk run (default: %(default)d)')
parser.add_argument('-c', '--connections', dest='CONNECTIONS', nargs='?', type=int, default=400,
                    help='connections number for wrk run (default: %(default)d)')
parser.add_argument('-S', '--samples', dest='SAMPLE_NUM', nargs='?', type=int, default=5,
                    help='times to do measurement during the period of a run (default: %(default)d)')
parser.add_argument('-s', '--sleep', dest='SQL_SLEEP_MAX', nargs='?', type=float, default=2,
                    help='SQL query sleep time seconds (default: %(default)d)')
parser.add_argument('-l', '--loop', dest='LOOP_COUNT', nargs='?', type=int, default=100,
                    help='Iterate times creating objects to push some CPU/Mem load (default: %(default)d)')
parser.add_argument('-p', '--pool', dest='POOL_SIZE', nargs='?', type=int, default=400,
                    help='Postgres pool size (default: %(default)d)')
ARGS = parser.parse_args()
globals().update(ARGS.__dict__)  # a dirty way


PROMPT = 'vagrant@servobench'

CMDS = {
    'mem-usage': "sudo python -m ps_mem | awk '/%s/{print \"___\"$7$8\"___\"}'", # substitute process name
    'cpu-usage': "top -bn1 | awk '/%s/{ SUM += $9 } END { print \"___\"SUM\"___\" }'", # substitute process name
    'wrk': 'wrk -t%d -c%d ' % (THREADS, CONNECTIONS) + '-d%ds http://localhost:8080/%s -s wrk_report.lua --timeout 10s',
    'cd-framework': 'cd /shared/%s',
    'docker-run': '../mule.sh -rk -s %d -l %d -p %d' % (SQL_SLEEP_MAX, LOOP_COUNT, POOL_SIZE)
}

REPORT_FILE_TEMPLATE = '_results/benchmark-results-%s-%dsec.md'

REPORT_TEMPLATE = """
==========================
Date: $current_time
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | $framework |
| Endpoint                        | /$endpoint  |
| Endpoint sleep sec. (if applicable) | $endpoint_sleep  |
| Requests/sec                    | $requests_per_second |
| Req. Latency (Avg.)             | $latency |
| Req. Latency (%'le - latency)   | $latency_percentiles |
| 5xx/4xx responses               | $bad_responses |
| N timeout-ed                    | $timeouted  |
| Memory used (mean), Mib         | $mem_used |
| Memory used samples, Mib        | $mem_samples |
| CPU used (mean), %              | $cpu_used |
| CPU used samples, %             | $cpu_samples |
| Test command                    | $test_command  |
| Data read                       | $data_read  |
==========================
"""

@contextmanager
def vagrant():
    try:
        print('Upping vagrant...')
        pexpect.run('vagrant up', timeout=300)
        child = pexpect.spawnu('vagrant ssh')
        child.expect('Last login')
        # child.logfile_read = sys.stdout
        child.setecho(False)
        yield child
        child.close(force=True)
    finally:
        print('Halting vagrant...')
        pexpect.run('vagrant halt', timeout=300)


def counter(cb, n):
    count = 0
    while count < n:
        try:
            cb()
        except Exception as e:
            print(e)
        finally:
            count += 1


def selector(typ, proposed):
    print('Available %ss:' % typ)
    msg = 'Select %s(s) you want to test. Type number(s) (e.g. 10 3). Default: All.\n' % typ
    for i, x in enumerate(proposed):
        print('%d) - %s' % (i + 1, os.path.basename(x)))
    ids = list(map(lambda y: int(y) - 1, filter(None, input(msg).split()))) or list(range(len(proposed)))
    return [proposed[i] for i in ids]


def ask_for_suites():
    dirs = [os.path.basename(root) for root, _, filenames in os.walk(os.getcwd())
            for filename in filenames if filename == 'processname.txt']
    apis = ['json', 'db']
    return list(itertools.product(selector('framework', dirs), selector('endpoint', apis)))


def do_report(cpu_samples, mem_samples, **kwargs):
    print('Memory: ', mem_samples)
    print('CPU: ', cpu_samples)
    mem_used = round(mean(mem_samples))
    cpu_used = round(mean(cpu_samples))
    print('Memory used, mb: ', mem_used)
    print('CPU used, %: ', cpu_used)
    print('Doing report to file...')
    kwargs['mem_used'] = mem_used
    kwargs['cpu_used'] = cpu_used
    kwargs['mem_samples'] = mem_samples
    kwargs['cpu_samples'] = cpu_samples
    kwargs['current_time'] = time.ctime()
    kwargs['endpoint_sleep'] = SQL_SLEEP_MAX
    report = Template(REPORT_TEMPLATE).substitute(kwargs)
    to_file = REPORT_FILE_TEMPLATE % (kwargs['endpoint'], SQL_SLEEP_MAX)
    with open(to_file, 'a') as f:
        f.write(report)


def run(s, framework, endpoint):
    mem_samples = []
    cpu_samples = []
    wrk_cmd = CMDS['wrk'] % (RUN_TIME, endpoint)
    wrk_warmup_cmd = CMDS['wrk'] % (30, endpoint)
    cd_cmd = CMDS['cd-framework'] % framework
    framework_processname = 'unknown'

    def sample_it(processname):
        time.sleep(RUN_TIME * 0.2)
        def task():
            time.sleep(RUN_TIME * 0.6 / SAMPLE_NUM / 2)
            s.sendline(CMDS['cpu-usage'] % processname)
            s.expect(r"___([0-9]+\.?[0-9]?)___", timeout=100)
            cpu_samples.append(float(s.match.group(1)))
            s.sendline(CMDS['mem-usage'] % processname)
            s.expect(r"___([0-9]+\.?[0-9]?)((?:M|G|K|T)i.*?)___", timeout=100)
            mem = float(s.match.group(1))
            mem_units = s.match.group(1)
            if mem_units.startswith('Ki'):
                mem /= 1024
            elif mem_units.startswith('Gi'):
                mem *= 1024
            mem_samples.append(int(mem))
        counter(task, SAMPLE_NUM)

    print('=' * 15, 'Working. %s server. %s endpoint.' % (framework.upper(), endpoint.upper()), '=' * 15)

    # set bash-prompt for further reliable checks
    s.sendline('PS1=' + PROMPT)
    s.expect(PROMPT)

    # cd framework's directory
    print('cd framework... ', cd_cmd)
    s.sendline(cd_cmd)
    s.expect(PROMPT)
    s.sendline('pwd')
    s.expect(framework)

    # get framework's processname for sampling (read it from the host machine)
    with open('./%s/processname.txt' % framework) as f:
        framework_processname = f.read().strip()

    # run framework in docker
    print('run docker... ', CMDS['docker-run'])
    s.sendline(CMDS['docker-run'])
    s.expect('Launching container')
    s.expect(PROMPT)

    # Warm-up
    print('Running wrk to warm-up...')
    pexpect.runu(wrk_warmup_cmd, timeout=1000000)

    # start background sampling thread
    t = threading.Thread(target=partial(sample_it, framework_processname))
    t.start()

    # Run wrk benchmark
    print('Running wrk benchmark...')
    res = pexpect.runu(wrk_cmd, timeout=1000000)
    for l in res.splitlines():
        print(l)

    m = re.search('Socket errors.*timeout.*?(\d+)', res)
    run_timeout_number = int(m.group(1).strip()) if m else 'unknown'
    m = re.search(', (.+?) read', res)
    data_read = m.group(1).strip() if m else 'unknown'
    m = re.search('Requests/sec:\W*([\.\d]+)', res)
    run_req_sec = m.group(1).strip() if m else 'unknown'
    m = re.search('Latency\W*([\.\w]+)', res)
    run_latency_avg = m.group(1).strip() if m else 'unknown'
    run_latencies = re.findall('Latency percentile\W*([\.\d]+)%,\W*([\.\d]+)', res)
    m = re.search('Non-2xx or 3xx responses:\W*([\.\d]+)', res)
    bad_resps = m.group(1).strip() if m else '0'

    t.join(RUN_TIME + 30)
    print('Reporting measurements made during benchmark...')
    do_report(cpu_samples=cpu_samples,
              mem_samples=mem_samples,
              framework=framework,
              endpoint=endpoint,
              test_command=wrk_cmd,
              timeouted=run_timeout_number,
              data_read=data_read,
              requests_per_second=run_req_sec,
              latency=run_latency_avg,
              latency_percentiles=run_latencies,
              bad_responses=bad_resps)
    print('Exiting...')


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    suits = ask_for_suites()
    for f, e in suits:
        with vagrant() as ssh:
            run(ssh, f, e)
            time.sleep(60)
