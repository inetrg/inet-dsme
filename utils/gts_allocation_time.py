#!/usr/bin/env python

import argparse
import numpy
import matplotlib.pyplot as plt
import re
import math
from collections import deque

def printMatrix(a):
   rows = a.shape[0]
   cols = a.shape[1]
   for i in range(0,rows):
      for j in range(0,cols):
         print("%2.0f" %a[i,j]),
      print
   print


parser = argparse.ArgumentParser(description="Extracts the number of allocated and deallocated slots per second.")
parser.add_argument("-l", "--log", type=str, required=True, help="the log file to parse")
parser.add_argument("-o", "--output", type=str, default="gts_allocation.csv", help="the output file")
parser.add_argument("-s", "--step", type=str, default="1", help="unit of time")
parser.add_argument("-v", "--visual", help="plot the data", action='store_true')
parser.add_argument("-f", "--filter", type=str, default="[0-9]*", help="unit of time")
args = parser.parse_args()

length = 500 / int(args.step)

allocationVector = numpy.zeros((length,3))
totalAlloc = 0
totalDealloc = 0

for i in range(0,length):
    allocationVector[i][0] = i * int(args.step)

pattern = re.compile("^\[\w*\]\s*([0-9.]*)\s*" + args.filter + ": ((de)?)alloc ([0-9]+)(.)([0-9]+) ([0-9]+),([0-9]+),([0-9]+)")
for line in open(args.log):
    m = pattern.match(line)
    if m:
        #print m.group(0)
        direction = ''
        if m.group(5) == '>':
            source = int(m.group(4)) - 1
            destination = int(m.group(6)) - 1
            time = float(m.group(1))
            pos = math.floor(math.floor(time) / int(args.step))
            if m.group(2) == 'de':
                totalDealloc += 1
                allocationVector[pos][1] += 1
            else:
                totalAlloc += 1
                allocationVector[pos][2] += 1


print "Data collection finished"

print "Dealloc %i  Alloc %i"%(totalDealloc,totalAlloc)
numpy.savetxt(args.output, allocationVector, delimiter=";")

if args.visual:
    times = allocationVector[:,0]
    allocations = allocationVector[:,2]
    deallocations = numpy.negative(allocationVector[:,1])

    fig = plt.figure(figsize=(20,10))

    width = int(args.step)
    plt.bar(times, allocations, width, color="blue")
    plt.bar(times, deallocations, width, color="red")

    plt.tight_layout()
    plt.show()

