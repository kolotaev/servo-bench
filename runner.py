import os
import itertools
from contextlib import contextmanager

import pexpect


PROMPT = 'vagrant@test\-machine:~\$'

cmd = {
    'free-mem': "free | awk '/Mem/{print $3}'",
    'cpu-usage': "top -bn4 | grep Cpu\(s\) | awk 'NR == 4 { print $2 + $4 }'",  # get us + sys
    'wrk': 'wrk -t12 -c400 -d30s http://localhost:8081/%s',
    'cd-framework': 'cd /shared/%s',
    'docker-run': '../mule.sh -rk'
}


@contextmanager
def vagrant():
    try:
        print('Upping vagrant...')
        pexpect.run('vagrant up', timeout=300)
        child = pexpect.spawnu('vagrant ssh')
        child.expect(PROMPT)

        child.setecho(False)

        yield child
    finally:
        print('Halting vagrant...')
        pexpect.run('vagrant halt')


def selector(typ, proposed):
    print('Available %ss:' % typ)
    msg = 'Select %s(s) you want to test. Default - Run All. Type number(s) (e.g. 10 3 6):\n' % typ
    for i, x in enumerate(proposed):
        print('%d) - %s' % (i, os.path.basename(x)))
    ids = list(map(int, filter(None, input(msg).strip().split(' ')))) or list(range(len(proposed)))
    return [proposed[i] for i in ids]


def ask_suites():
    dirs = [os.path.basename(root) for root, _, filenames in os.walk(os.getcwd())
            for filename in filenames if filename == 'Dockerfile']
    apis = ['json', 'db']
    return list(itertools.product(selector('framework', dirs), selector('endpoint', apis)))


def run(s, framework, endpoint):
    wrk_cmd = cmd['wrk'] % endpoint
    cd_cmd = cmd['cd-framework'] % framework

    # cd framework's directory
    print('cd framework... ', cd_cmd)
    s.sendline(cd_cmd)
    s.expect(PROMPT)
    s.sendline('pwd')
    s.expect(framework)

    # run docker
    print('run docker... ', cmd['docker-run'])
    s.sendline(cmd['docker-run'])
    s.expect_exact('++ Launching container...')

    # get memory usage: bytes
    s.sendline('/bin/bash', [cmd['free-mem']])
    s.expect(PROMPT)
    print(s.before)

    # get cpu usage: %
    s.sendline('/bin/bash', [cmd['cpu-usage']])
    s.expect(PROMPT)
    print(s.before)

    res = pexpect.run(wrk_cmd, timeout=100000)
    print(res)

    s.sendline('exit')
    index = s.expect([pexpect.EOF, "(?i)there are stopped jobs"])
    if index == 1:
        s.sendline("exit")
        s.expect(pexpect.EOF)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    suits = ask_suites()
    with vagrant() as ssh:
        for framework, endpoint in suits:
            run(ssh, framework, endpoint)
