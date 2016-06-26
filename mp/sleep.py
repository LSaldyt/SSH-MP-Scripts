import time
import sys

if __name__ == "__main__":
    time.sleep(float(sys.argv[1]))
    with open('out', 'w') as output:
        output.write('Finished successfully')
