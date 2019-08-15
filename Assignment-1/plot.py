#!/bin/python3

import sys
import datetime

import matplotlib
import subprocess
import matplotlib.pyplot as plt

percentageSupports = [1, 5, 10, 25, 50, 90]

filename = str(sys.argv[1])

time = {'apriori': [], 'fptree': []}

for x in percentageSupports:
	start = datetime.datetime.now()
	subprocess.call(['./2016CS50400.sh', filename, str(x), '-apriori', 'out1'])

	end = datetime.datetime.now()
	time['apriori'].append((end-start).total_seconds())
	
	start = datetime.datetime.now()
	subprocess.call(['./2016CS50400.sh', filename, str(x), '-fptree', 'out1'])
	
	end = datetime.datetime.now()
	time['fptree'].append((end-start).total_seconds())

plt.xlabel("X-axis: Percent support threshold")
plt.ylabel("Y-axis: Algorithm execution time")
plt.title("Plot")
plt.savefig("compare-plots.png")

for key in time:
	plt.plot(percentageSupports, time[key], label='Algo: {}'.format(key))

plt.legend()
plt.show()
