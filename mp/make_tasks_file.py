#!/usr/bin/python
import dill as pickle
from mp import *
import sys

def f():
    return [2 for i in range(1000)]
 
if __name__ == "__main__":
    futures = [Future(f, [], {})]
    with open('%s_tasks.pkl' % sys.argv[1], 'w') as taskfile:
        pickle.dump(futures, taskfile)
    
