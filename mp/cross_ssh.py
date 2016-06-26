#!/usr/bin/python
from mp import *

import dill as pickle

import subprocess
import time
import sys
import os


def get_cores(server):
    return subprocess.call(['ssh', server, 'NPROC="$(nproc)"; exit "$NPROC"'])

def build_server_dict(servernames):
    server_dict = {}
    total_cores = 0

    for name in servernames:
         cores = get_cores(name)
         total_cores += cores
         server_dict[name] = cores

    return server_dict, total_cores

def build_servernames(file):
    with open(file, 'r') as servers:
        return servers.read().splitlines()

def _f(x, y=0):
    return [x * 42 for i in range(1000)]

futures = [Future(_f, [10], {'y' : 0})]

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
	     for i in range(wanted_parts) ]

def send_tasks(server, server_cores, split_futures): 
    print('Sending tasks to %s' % server)

    futures_chunk = split_futures[:server_cores]
    split_futures = split_futures[server_cores:]

    with open('%s_tasks.pkl' % server, 'wb') as taskfile:
        pickle.dump(futures_chunk, taskfile)
    # Copy tasks file to server
    subprocess.call(['scp', '%s_tasks.pkl' % server,  '%s:' % server])
    os.remove('%s_tasks.pkl' % server)

def send_task_runner(server):
    subprocess.call(['scp', 'run_tasks_file.py', '%s:' % server])

def send_mp_module(server):
    subprocess.call(['scp', 'mp.py', '%s:' % server])

def call_task_runner(server):
    subprocess.call(['ssh', server, 'python3 run_tasks_file.py %s' % server])

def get_task_result(server):
    checkfile = '[ -f %s_results.pkl ] && exit 0 || exit 1' % server
    while(subprocess.call(['ssh', server, checkfile]) == 1):
        time.sleep(1)
        print('Waiting for server')
    subprocess.call(['scp', '-r', '%s:%s_results.pkl' % (server, server), '.'])
    with open('%s_results.pkl' % server, 'rb') as resultfile:
        return pickle.load(resultfile)

def cleanup(server):
    cleanup_command = 'rm %s_results.pkl; rm %s_tasks.pkl;'
    subprocess.call(['ssh', server, cleanup_command])

if __name__ == "__main__":
    servernames              = build_servernames(sys.argv[1])
    server_dict, total_cores = build_server_dict(servernames)

    split_futures            = split_list(futures, wanted_parts=total_cores)
    
    for server in server_dict:
       send_tasks(server, server_dict[server], split_futures)
       send_task_runner(server)
       send_mp_module(server)
       call_task_runner(server)
       
    for server in server_dict:
        results = get_task_result(server)
        cleanup(server)
        print(results)

   

