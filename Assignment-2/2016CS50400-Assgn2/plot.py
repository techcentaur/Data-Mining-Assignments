#!/bin/python3

import sys
import time
import subprocess
import matplotlib.pyplot as plt

import gspan
import gaston
import pafi


time_consumed = {
    'gSpan': [],
    'PAFI': [],
    'GASTON': []
}
supports = [95, 50, 25, 10, 5]


for support in supports:
    print('[*] Support level:', support, flush=True)
    
    print('[*] Running algorithm: gSpan', flush=True)
    gspan.change_format(sys.argv[1])
    start = time.time()
    subprocess.run(['./gSpan-1/gSpan-64', '-f', 'gspan_' + sys.argv[1].split('/')[-1], '-s',  str(support / 100)])
    time_consumed['gSpan'].append(time.time() - start)
    print(time_consumed, flush=True)

    print('[*] Running algorithm: GASTON', flush=True)
    gaston.change_format(sys.argv[1])
    start = time.time()
    subprocess.run(['./gaston-1.1/gaston', str(support), 'gaston_' + sys.argv[1].split('/')[-1]])
    print(' '.join(['./gaston-1.1/gaston', str(support), 'gaston_' + sys.argv[1].split('/')[-1]]))
    time_consumed['GASTON'].append(time.time() - start)
    print(time_consumed, flush=True)
    
    
    print('[*] Running algorithm: PAFI', flush=True)
    pafi.change_format(sys.argv[1])
    start = time.time()
    subprocess.run(['./pafi-1.0.1/Linux/fsg', '-s', str(float(support)), 'pafi_' + sys.argv[1].split('/')[-1]])
    time_consumed['PAFI'].append(time.time() - start)
    print(time_consumed, flush=True)


plt.xlabel('Percentage support threshold')
plt.ylabel('Execution time')
plt.title('Plot')

for key, value in time_consumed.items():
    plt.plot(supports, value, label=key)

plt.legend()
plt.savefig(sys.argv[2])
