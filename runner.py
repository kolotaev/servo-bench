import sys
from contextlib import contextmanager

import pexpect


PROMPT = 'vagrant@lamp:~\$'
WRK_CMD = 'wrk -t12 -c400 -d300s http://lamp:8080/db'

# fout = open('runner_log.txt', 'a')
fout = sys.stdout


@contextmanager
def vagrant():
    try:
        pexpect.run('vagrant up', timeout=300)
        child = pexpect.spawnu('vagrant ssh')
        child.expect(PROMPT)

        # child.logfile_read = fout
        child.setecho(False)

        yield child
    finally:
        pexpect.run('vagrant halt')


def run(s):
    s.sendline('ls -la')
    s.expect(PROMPT)

    s.sendline('free -m')
    s.expect(PROMPT)
    print(s.before)

    s.sendline('/bin/bash', ["grep 'cpu ' /proc/stat | awk '{print ($2+$4)*100/($2+$4+$5)}'"])
    s.expect(PROMPT)
    print(s.before)

    s.sendline('df')
    s.expect(PROMPT)
    print(s.before)

    s.sendline('exit')
    index = s.expect([pexpect.EOF, "(?i)there are stopped jobs"])
    if index == 1:
        s.sendline("exit")
        s.expect(pexpect.EOF)


if __name__ == '__main__':
    with vagrant() as ssh:
        run(ssh)
