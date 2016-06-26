#!/usr/bin/python
from mp import *

import dill as pickle

import subprocess
import sys
import os

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as sshservers:
        servernames = sshservers.read().splitlines()

    server_dict = {}
    total_cores = 0

    for name in servernames:
         # Get number of processors on each server machine
         cores = subprocess.call(['ssh', name, 'NPROC="$(nproc)"; exit "$NPROC"'])
         print("%s has %s cores" % (name, cores))
         total_cores += cores
         server_dict[name] = cores

    def _f(x, y=0):
        return [x * 42 for i in range(1000)]

    futures = [Future(_f, [10], {'y' : 0})]

    print('Total Cores: %s' % total_cores)

    def split_list(alist, wanted_parts=1):
        length = len(alist)
        return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
                 for i in range(wanted_parts) ]

    split_futures = split_list(futures, wanted_parts=total_cores)
    print(split_futures)
    
    for server in server_dict:
        print('Sending tasks to %s' % server)
        server_cores = server_dict[server]
        futures_chunk=split_futures[:server_cores]
        split_futures=split_futures[server_cores:]
        print('Tasks for %s : %s' % (server, futures_chunk))
        with open('%s_tasks.pkl' % server, 'wb') as taskfile:
            pickle.dump(futures_chunk, taskfile)
        subprocess.call(['scp', '%s_tasks.pkl' % server,  '%s:' % server])
        os.remove('%s_tasks.pkl' % server)

#    subprocess.call(['ssh', name, 'python sleep.py 1'])
 #   subprocess.call(['scp', '%s:out' % name, '%s.out' % name ])
   

