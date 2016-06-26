from multiprocessing import cpu_count, Pool
from contextlib      import contextmanager
from collections     import namedtuple
import sys
import time

@contextmanager
def redirected(filename):
    with open(filename, 'w') as output:
        sys.stdout = output
        print('Redirected File: ')
        yield
        sys.stdout = sys.__stdout__

Future = namedtuple('Future', ['function', 'args', 'kwargs'])

def launch(pool, fs):
    results = []
    for f in fs:
        with redirected("%s.out" % f.function.__name__):
            results.append(pool.apply_async(f.function, f.args, f.kwargs))
    return results
            

def _f(x, y=0):
    return [x * 42 for i in range(1000)]

if __name__ == "__main__":
    print("Creating pool with %s CPUs" % cpu_count())
    pool = Pool(processes=cpu_count())
    results = launch(pool, [Future(_f, [10], {'y':0})])
    for result in results:
        result.get()
    

