import os
import sys
import time
import threading
import itertools
from contextlib import contextmanager

import pexpect


RUN_TIME = 120

PROMPT = 'vagrant@servobench'

cmd = {
    'free-mem': "free | awk '/Mem/{print \"___\"$3 + 0\"___\"}'",
    'cpu-usage': "top -bn3 | grep Cpu\(s\) | awk 'NR == 3 { print \"___\"$2 + $4\"___\"}'",  # get us + sys
    'wrk': 'wrk -t12 -c400 -d%ds http://localhost:8080/%s',
    'cd-framework': 'cd /shared/%s',
    'docker-run': '../mule.sh -rk'
}

SEARCH_PATTERN = '___([0-9]+\.?[0-9]?)___'


@contextmanager
def vagrant():
    try:
        print('Upping vagrant...')
        # pexpect.run('vagrant up', timeout=300)
        child = pexpect.spawnu('vagrant ssh')
        child.expect('Last login')

        # child.logfile_read = sys.stdout

        child.setecho(False)

        yield child
    finally:
        print('Halting vagrant...')
        # pexpect.run('vagrant halt')


@contextmanager
def counter(n):
    count = 0
    while count < n:
        try:
            yield
        except Exception as e:
            print(e)
        finally:
            count += 1


def selector(typ, proposed):
    print('Available %ss:' % typ)
    msg = 'Select %s(s) you want to test. Type number(s) (e.g. 10 3). Default: All.\n' % typ
    for i, x in enumerate(proposed):
        print('%d) - %s' % (i + 1, os.path.basename(x)))
    ids = list(map(lambda y: int(y) - 1, filter(None, input(msg).strip().split(' ')))) or list(range(len(proposed)))
    return [proposed[i] for i in ids]


def ask_suites():
    dirs = [os.path.basename(root) for root, _, filenames in os.walk(os.getcwd())
            for filename in filenames if filename == 'Dockerfile']
    apis = ['json', 'db']
    return list(itertools.product(selector('framework', dirs), selector('endpoint', apis)))


def run(s, framework, endpoint):
    mem_samples = []
    cpu_samples = []
    wrk_cmd = cmd['wrk'] % (RUN_TIME, endpoint)
    cd_cmd = cmd['cd-framework'] % framework

    def measure():
        time.sleep(20)
        with counter(5):
            time.sleep(10)
            s.sendline(cmd['free-mem'])
            s.expect(SEARCH_PATTERN, timeout=100)
            mem_samples.append(s.match.groups()[0])
            s.sendline(cmd['cpu-usage'])
            s.expect(SEARCH_PATTERN, timeout=100)
            cpu_samples.append(s.match.groups()[0])

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
    # get memory usage: bytes
    s.sendline(cmd['free-mem'])
    s.expect(SEARCH_PATTERN)
    mem_before = s.match.groups()[0]

    # get cpu usage: %
    s.sendline(cmd['cpu-usage'])
    s.expect(SEARCH_PATTERN)
    cpu_usage = s.match.groups()[0]

    print('Mem, kb: ---->', mem_before)
    print('CPU, %:  ---->', cpu_usage)

    # start background sampling thread
    t = threading.Thread(target=measure)
    t.start()

    # Run wrk benchmark
    print('Running wrk...')
    res = pexpect.runu(wrk_cmd, timeout=100000)
    for l in res.splitlines():
        print(l)

    print(mem_samples)
    print(cpu_samples)
    print('Exiting...')
    t.join(RUN_TIME + 60)
    s.sendline('exit')
    index = s.expect([pexpect.EOF, "(?i)there are stopped jobs"])
    if index == 1:
        s.sendline("exit")
        s.expect(pexpect.EOF)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    suits = ask_suites()
    with vagrant() as ssh:
        for f, e in suits:
            run(ssh, f, e)
            # time.sleep(60)
