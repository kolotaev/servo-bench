import os
import sys
import itertools
from contextlib import contextmanager

import pexpect


PROMPT = 'vagrant@servobench'

cmd = {
    'free-mem': "free | awk '/Mem/{print $3}'",
    'cpu-usage': "top -bn4 | grep Cpu\(s\) | awk 'NR == 4 { print $2 + $4 }'",  # get us + sys
    'wrk': 'wrk -t12 -c400 -d30s -s wrk_report.lua http://localhost:8080/%s',
    'cd-framework': 'cd /shared/%s',
    'docker-run': '../mule.sh -rk'
}


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


def selector(typ, proposed):
    print('Available %ss:' % typ)
    msg = 'Select %s(s) you want to test. Type number(s) (e.g. 10 3). Default: All.\n' % typ
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

    # get memory usage: bytes
    s.sendline(cmd['free-mem'])
    s.expect(PROMPT)
    mem_before = s.before.strip()

    # get cpu usage: %
    s.sendline(cmd['cpu-usage'])
    s.expect(PROMPT)
    cpu_usage = s.before.strip()

    print('----', mem_before)
    print('-----', cpu_usage)

    print('Running wrk...')
    res = pexpect.run(wrk_cmd, timeout=-1)
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
