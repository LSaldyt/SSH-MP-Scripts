#!/usr/bin/python
from mp import *
import dill as pickle
import sys

if __name__ == "__main__":
    server = sys.argv[1]
    with open('%s_tasks.pkl' % server, 'rb') as taskfile:
        futures = pickle.load(taskfile)
    results = run_tasks(futures)
    with open('%s_results.pkl' % server, 'wb') as resultfile:
        pickle.dump(results, resultfile)
    
