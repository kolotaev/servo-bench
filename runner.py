import os
import sys
import time
import threading
import itertools
from contextlib import contextmanager

import pexpect


RUN_TIME = 300  # in seconds
SAMPLE_NUM = 5

PROMPT = 'vagrant@servobench'

cmd = {
    'free-mem': "free | awk '/Mem/{print \"___\"$3 + 0\"___\"}'",
    'cpu-usage': "top -bn3 | grep Cpu\(s\) | awk 'NR == 3 { print \"___\"$2 + $4\"___\"}'",  # get us + sys
    'wrk': 'wrk -t12 -c400 -d%ds http://localhost:8080/%s',
    'cd-framework': 'cd /shared/%s',
    'docker-run': '../mule.sh -rk'
}

# for awk-ed 'top' command output
SEARCH_PATTERN = '___([0-9]+\.?[0-9]?)___'

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


def do_report(cpu_samples, mem_samples):
    consumed = lambda x, y: round(((sum(x) / len(x) - y) / 1000), 1)
    mem_samples = list(map(int, mem_samples))
    cpu_samples = list(map(float, cpu_samples))
    print('Memory: ', mem_samples)
    print('CPU: ', cpu_samples)
    cpu_used = consumed(cpu_samples, cpu_before)
    mem_used = consumed(mem_samples, mem_before)
    print('Memory used, mb: ', mem_used)
    print('CPU used, %: ', cpu_used)


def run(s, framework, endpoint):
    global cpu_before, mem_before
    mem_samples = []
    cpu_samples = []
    wrk_cmd = cmd['wrk'] % (RUN_TIME, endpoint)
    cd_cmd = cmd['cd-framework'] % framework

    def sample_it():
        time.sleep(RUN_TIME * 0.2)

        def task():
            time.sleep(RUN_TIME * 0.6 / SAMPLE_NUM / 2)
            s.sendline(cmd['free-mem'])
            s.expect(SEARCH_PATTERN, timeout=100)
            mem_samples.append(s.match.groups()[0])
            s.sendline(cmd['cpu-usage'])
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
    print('run docker... ', cmd['docker-run'])
    s.sendline(cmd['docker-run'])
    s.expect('Launching container')
    s.expect(PROMPT)

    print('Sampling resources before run...')
    # get cpu usage: %
    s.sendline(cmd['cpu-usage'])
    s.expect(SEARCH_PATTERN)
    cpu_before = float(s.match.groups()[0])

    # get memory usage: bytes
    s.sendline(cmd['free-mem'])
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

    print('Reporting resource measurements during benchmark...')
    do_report(cpu_samples=cpu_samples, mem_samples=mem_samples)

    print('Exiting...')
    t.join(RUN_TIME + 60)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    suits = ask_suites()
    with vagrant() as ssh:
        for f, e in suits:
            run(ssh, f, e)
            time.sleep(60)
