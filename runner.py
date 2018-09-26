import os
import re
import time
import sys
import threading
import itertools
from contextlib import contextmanager
from string import Template

import pexpect


RUN_TIME = (int(sys.argv[1]) if len(sys.argv) == 2 else 1) * 60  # in seconds
SAMPLE_NUM = 5     # time to do measurement during the period of run
SQL_SLEEP_MAX = 2  # SQL query sleep time seconds
LOOP_COUNT = 100   # Iterate times creating objects to push some CPU/Mem load
THREADS = 12       # threads number for wrk run
CONNECTIONS = 400  # connections number for wrk run

PROMPT = 'vagrant@servobench'

CMDS = {
    'free-mem': "free | awk '/Mem/{print \"___\"$3 + 0\"___\"}'",
    'cpu-usage': "top -bn3 | grep Cpu\(s\) | awk 'NR == 3 { print \"___\"$2 + $4\"___\"}'",  # get us + sys
    'wrk': 'wrk -t%d -c%d ' % (THREADS, CONNECTIONS) + '-d%ds http://localhost:8080/%s -s wrk_report.lua',
    'cd-framework': 'cd /shared/%s',
    'docker-run': '../mule.sh -rk -s %d -l %d' % (SQL_SLEEP_MAX, LOOP_COUNT)
}

# for awk-ed 'top' command output
SEARCH_PATTERN = '___([0-9]+\.?[0-9]?)___'

REPORT_FILE = 'runner-results.md'

REPORT_TEMPLATE = """
==========================
Date: $current_time
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | $framework |
| Endpoint                        | /$endpoint  |
| Requests/sec                    | $requests_per_second |
| Req. Latency (Avg.)             | $latency |
| Memory used, Mb                 | $mem_used |
| Memory used samples, kb         | $mem_samples |
| CPU used samples, %             | $cpu_samples |
| Test run time                   | $time  |
| N connections                   | $connections  |
| N threads                       | $threds  |
| N timeout-ed                    | $timeouted  |
| Data read                       | $data_read  |
| Memory occupied before run, Mb  | $mem_before_run |
==========================
"""

# Global vars
cpu_before = 0
mem_before = 0


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


def ask_suites():
    dirs = [os.path.basename(root) for root, _, filenames in os.walk(os.getcwd())
            for filename in filenames if filename == 'Dockerfile']
    apis = ['json', 'db']
    return list(itertools.product(selector('framework', dirs), selector('endpoint', apis)))


def do_report(cpu_samples, mem_samples, **kwargs):
    consumed_mem = lambda x, y: round(((sum(x) / len(x) - y) / 1000), 1)
    consumed_cpu = lambda x, y: round((sum(x) / len(x) - y), 1)
    mem_samples = list(map(int, mem_samples))
    cpu_samples = list(map(float, cpu_samples))
    print('Memory: ', mem_samples)
    print('CPU: ', cpu_samples)
    cpu_used = consumed_cpu(cpu_samples, cpu_before)
    mem_used = consumed_mem(mem_samples, mem_before)
    if mem_used < 0:
        mem_used = 0
    print('Memory used, mb: ', mem_used)
    print('CPU used, %: ', cpu_used)
    print('Doing report to file...')
    kwargs['mem_before_run'] = int(mem_before / 1000)
    kwargs['cpu_used'] = cpu_used
    kwargs['mem_used'] = mem_used
    kwargs['mem_samples'] = mem_samples
    kwargs['cpu_samples'] = cpu_samples
    kwargs['current_time'] = time.ctime()
    report = Template(REPORT_TEMPLATE).substitute(kwargs)
    with open(REPORT_FILE, "a") as f:
        f.write(report)


def run(s, framework, endpoint):
    global cpu_before, mem_before
    mem_samples = []
    cpu_samples = []
    wrk_cmd = CMDS['wrk'] % (RUN_TIME, endpoint)
    cd_cmd = CMDS['cd-framework'] % framework

    def sample_it():
        time.sleep(RUN_TIME * 0.2)

        def task():
            time.sleep(RUN_TIME * 0.6 / SAMPLE_NUM / 2)
            s.sendline(CMDS['free-mem'])
            s.expect(SEARCH_PATTERN, timeout=100)
            mem_samples.append(s.match.groups()[0])
            s.sendline(CMDS['cpu-usage'])
            s.expect(SEARCH_PATTERN, timeout=100)
            cpu_samples.append(s.match.groups()[0])

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

    # run docker
    print('run docker... ', CMDS['docker-run'])
    s.sendline(CMDS['docker-run'])
    s.expect('Launching container')
    s.expect(PROMPT)

    print('Sampling resources before run...')
    # get cpu usage: %
    s.sendline(CMDS['cpu-usage'])
    s.expect(SEARCH_PATTERN)
    cpu_before = float(s.match.groups()[0])

    # get memory usage: bytes
    s.sendline(CMDS['free-mem'])
    s.expect(SEARCH_PATTERN)
    mem_before = int(s.match.groups()[0])

    print('Mem, kb: ---->', mem_before)
    print('CPU, %:  ---->', cpu_before)

    # start background sampling thread
    t = threading.Thread(target=sample_it)
    t.start()

    # Run wrk benchmark
    print('Running wrk...')
    res = pexpect.runu(wrk_cmd, timeout=1000000)
    for l in res.splitlines():
        print(l)

    m = re.search('Running(.+?)test', res)
    run_time = m.group(1).strip() if m else 'unknown'
    m = re.search('(\d+).*threads.*?(\d+).*connections', res)
    run_threads = m.group(1).strip() if m else 'unknown'
    run_connections = m.group(2).strip() if m else 'unknown'
    m = re.search('Socket errors.*timeout.*?(\d+)', res)
    run_timeout_number = int(m.group(1).strip()) if m else 'unknown'
    m = re.search(', (.+?) read', res)
    data_read = m.group(1).strip() if m else 'unknown'
    m = re.search('Requests/sec:\W*([\.\d]+)', res)
    run_req_sec = m.group(1).strip() if m else 'unknown'
    m = re.search('Latency\W*([\.\w]+)', res)
    run_latency = m.group(1).strip() if m else 'unknown'

    print('Reporting resource measurements during benchmark...')
    do_report(cpu_samples=cpu_samples,
              mem_samples=mem_samples,
              framework=framework,
              endpoint=endpoint,
              time=run_time,
              connections=run_connections,
              threds=run_threads,
              timeouted=run_timeout_number,
              data_read=data_read,
              requests_per_second=run_req_sec,
              latency=run_latency)

    print('Exiting...')
    t.join(RUN_TIME + 60)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    suits = ask_suites()
    for f, e in suits:
        with vagrant() as ssh:
            run(ssh, f, e)
            time.sleep(60)
