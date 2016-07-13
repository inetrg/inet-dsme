#!/usr/bin/env python

import argparse
import numpy
import re
from collections import deque

from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

def printMatrix(a):
   rows = a.shape[0]
   cols = a.shape[1]
   for i in range(0,rows):
      for j in range(0,cols):
         print("%2.0f" %a[i,j]),
      print
   print


parser = argparse.ArgumentParser(description="Creates an animation from a log file to visualise the GTS allocation process.")
parser.add_argument("-l", "--log", type=str, required=True, help="the log file to parse")
parser.add_argument("-o", "--output", type=str, default="gts_allocation.mp4", help="the output file")
args = parser.parse_args()

numNodes = 62

currentAllocationMatrix = numpy.zeros((numNodes, numNodes))
positionVector = numpy.zeros((numNodes,2))
totalAlloc = 0
totalDealloc = 0

allocationMatrixHistory = []

distance = 100

totalCircles = 0
totalNodesOnInnerCircles = 0
nodesOnThisCircle = 1

myCircle = 0
nodesOnInnerCircles = 0

for line in open(args.log):
    m = re.search("^\[\w*\]\s*0\s*([0-9]*): POSITION: x=([0-9.]+), y=([0-9.]+)", line)
    if m:
        #print m.group(0)
        index = int(m.group(1))-1
        positionVector[index][0] = float(m.group(2))
        positionVector[index][1] = float(m.group(3))

#for i in range(0, numNodes):
#    if i - totalNodesOnInnerCircles >= nodesOnThisCircle:
#        totalCircles += 1
#        totalNodesOnInnerCircles += nodesOnThisCircle
#        nodesOnThisCircle = int(2 * numpy.pi * totalCircles)
#    
#    radius = distance * totalCircles
#    angularStep = 2 * numpy.pi / nodesOnThisCircle
#    angle = angularStep * (i - totalNodesOnInnerCircles)
#    positionVector[i][0] = radius * numpy.sin(angle)
#    positionVector[i][1] = radius * numpy.cos(angle)

#printMatrix(positionVector)

currentMatrixToAdd = currentAllocationMatrix.copy()
allocationMatrixHistory.append((0, currentMatrixToAdd))

for line in open(args.log):
    m = re.search("^\[\w*\]\s*([0-9.]*)\s*[0-9]*: ((de)?)alloc ([0-9]+)(.)([0-9]+) ([0-9]+),([0-9]+),([0-9]+)", line)
    if m:
        #print m.group(0)
        direction = ''
        if m.group(5) == '>':
            source = int(m.group(4)) - 1
            destination = int(m.group(6)) - 1
            time = float(m.group(1))
            if m.group(2) == 'de':
                totalDealloc += 1
                currentAllocationMatrix[source][destination] -= 1
            else:
                totalAlloc += 1
                currentAllocationMatrix[source][destination] += 1
            currentMatrixToAdd = currentAllocationMatrix.copy()
            allocationMatrixHistory.append((time, currentMatrixToAdd))

fig = plt.figure(figsize=(10,10))
ax = plt.axes(xlim=(-100, 900), ylim=(-100, 900))
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
last_time_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)

for i in range(0, numNodes):
    x = positionVector[i][0]
    y = positionVector[i][1]
    circle = Circle((x, y), 10)
    ax.add_artist(circle)

cmap = ListedColormap(['b', 'r', 'b'])
norm = BoundaryNorm([0, 1, 1.5, 2], cmap.N)

line = LineCollection([], cmap=cmap, norm=norm,lw=2)
ax.add_collection(line)

keys = len(allocationMatrixHistory)

def init():
    line.set_segments([])
    time_text.set_text('')
    last_time_text.set_text('')
    return line, time_text, last_time_text

previous_key = 0
def animate(i):
    global previous_key
    lastKey = 0
    next_time, unused = allocationMatrixHistory[lastKey + 1]
    while lastKey + 2 < keys and i > int(next_time):
        lastKey += 1
        next_time, unused = allocationMatrixHistory[lastKey + 1]

    time, allocationMatrix = allocationMatrixHistory[lastKey]
 
    time_text.set_text("time=" + "%4d" % i + "s")
    last_time_text.set_text(time)
    segments = []
    widths = []
    colors = []
    for s in range(0,numNodes):
        for d in range(0,numNodes):
            if allocationMatrix[s][d] > 0:
                xs = positionVector[s][0];
                ys = positionVector[s][1];
                xd = positionVector[d][0];
                yd = positionVector[d][1];
                segments.append([(xs, ys), (xd, yd)])
                widths.append(allocationMatrix[s][d])
                if lastKey > 0:
                    unused_time, lastMatrix = allocationMatrixHistory[previous_key]
                    if int(allocationMatrix[s][d]) == int(lastMatrix[s][d]):
                        colors.append("#0000FF")
                    elif int(allocationMatrix[s][d]) < int(lastMatrix[s][d]):
                        colors.append("#00FF00")
                    else:
                        colors.append("#FF0000")
                else:
                    colors.append("#0000FF")
    if colors:    
        line.set_edgecolors(colors)
        line.set_facecolors(colors)
    if widths:
        line.set_linewidths(widths)
    line.set_segments(segments)
    previous_key = lastKey
    return line, time_text, last_time_text

final_time, unused =  allocationMatrixHistory[keys - 1]
anim = animation.FuncAnimation(fig, animate, init_func=init, frames=int(final_time) + 10, interval=1, blit=True)

anim.save(args.output, writer='avconv', fps=2, extra_args=['-vcodec', 'libx264'])

plt.show()

print "Dealloc %i  Alloc %i\n"%(totalDealloc,totalAlloc)

