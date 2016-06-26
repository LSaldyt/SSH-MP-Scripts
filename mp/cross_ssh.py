#!/usr/bin/python
import subprocess
import sys

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as sshservers:
        servernames = sshservers.read().splitlines()

    for name in servernames:
         print(name)
         subprocess.call(['scp', 'sleep.py',  '%s:' % name])
         subprocess.call(['ssh', name, 'python sleep.py 1'])
         subprocess.call(['scp', '%s:out' % name, '%s.out' % name ])

