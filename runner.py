import sys
from contextlib import contextmanager

import pexpect
from pexpect import EOF


COMMAND_PROMPT = 'vagrant@lamp:~\$'

# fout = open('mylog.txt', 'a')
fout = sys.stdout


@contextmanager
def vagrant():
    try:
        pexpect.run('vagrant up')
        child = pexpect.spawnu('vagrant ssh')
        child.expect(COMMAND_PROMPT)

        # child.logfile_read = fout
        child.setecho(False)

        yield child
    finally:
        pexpect.run('vagrant halt')


def action(child):
    child.sendline('ls -la')
    child.expect(COMMAND_PROMPT)

    child.sendline('free -m')
    child.expect(COMMAND_PROMPT)
    print(child.before)

    child.sendline('df')
    child.expect(COMMAND_PROMPT)
    print(child.before)

    child.sendline('exit')
    index = child.expect([pexpect.EOF, "(?i)there are stopped jobs"])
    if index == 1:
        child.sendline("exit")
        child.expect(EOF)


if __name__ == '__main__':
    with vagrant() as ssh:
        action(ssh)
