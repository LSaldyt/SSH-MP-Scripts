#!/usr/bin/python
from mp import *

import dill as pickle

import subprocess
import time
import sys
import os


def get_cores(server):
    return subprocess.call(['ssh', server, 'NPROC="$(nproc)"; exit "$NPROC"'])

def build_serverlist(servernames):
    serverlist = []
    total_cores = 0

    for name in servernames:
         cores = get_cores(name)
         total_cores += cores
         serverlist.append((name, cores))

    return serverlist, total_cores

def build_servernames(file):
    with open(file, 'r') as servers:
        return servers.read().splitlines()

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
	     for i in range(wanted_parts) ]

def send_tasks(server, futures_chunk): 
    print('Sending tasks to %s' % server)
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
        results = pickle.load(resultfile)
    os.remove('%s_results.pkl' % server)
    return results

def cleanup(server):
    cleanup_command = 'rm %s_results.pkl; rm %s_tasks.pkl;' % (server, server)
    subprocess.call(['ssh', server, cleanup_command])


def _f(x, y=0):
    return [x * 42 for i in range(1000)]

futures = [Future(_f, [10], {'y' : 0}) for i in range(4)]

def parallelize_futures(serverfile, futures):
    servernames             = build_servernames(serverfile)
    serverlist, total_cores = build_serverlist(servernames)

    split_futures            = split_list(futures, wanted_parts=total_cores)

    print('Beginning tasks..') 
   
    for server, cores in serverlist:
       futures_chunk = split_futures[:cores]
       split_futures = split_futures[cores:]
       send_tasks(server, futures_chunk)
       send_task_runner(server)
       send_mp_module(server)
       call_task_runner(server)
       
    print('Retrieving task results..')
 
    totalresults = []

    for server, cores in serverlist:
        results = get_task_result(server)
        cleanup(server)
        totalresults.append(results)
    
    return totalresults
 
if __name__ == "__main__":
    results = parallelize_futures(sys.argv[1], futures)
    print(len(results))

