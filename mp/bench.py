#!/usr/bin/python
from mp        import Future
from cross_ssh import parallelize_futures
import time

def f(x):
    time.sleep(x)

def eval(f):
    return f.function(*f.args, **f.kwargs)

if __name__ == "__main__":
    print('Beginning benchmark')
    futures = [Future(f, [20], {}) for i in range(4)]
    begin   = time.time()
    results = []
    for f in futures:
        result = eval(f)
        results.append(result)
    end     = time.time()
    print(end - begin)
    begin   = time.time()
    results = parallelize_futures('servers', futures)
    end     = time.time()
    print(end - begin)
