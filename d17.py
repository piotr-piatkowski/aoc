#!/usr/bin/python3.8

import re
import sys
from collections import defaultdict
from copy import deepcopy

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = 'input.txt'

l = set()

z = 0
y = 0
w = 0
with open(path, 'r') as f:
    for line in f:
        line = line.strip()
        for x, ch in enumerate(line):
            if ch == '#':
                l.add((x, y, z, w))
        y += 1

def dims(l):
    mins = None
    maxs = None
    for k in l:
        if mins is None:
            mins = list(k)
            maxs = list(k)
        for i, kv in enumerate(k):
            if kv > maxs[i]:
                maxs[i] = kv
            if kv < mins[i]:
                mins[i] = kv
    return mins, maxs

def num(l, x, y, z, w):
    c = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                for dw in range(-1, 2):
                    if dx != 0 or dy != 0 or dz != 0 or dw != 0:
                        if (x+dx, y+dy, z+dz, w+dw) in l:
                            c += 1
    return c

def pr(l, n):
    mins, maxs = dims(l)
    print(mins, maxs)
    for w in range(mins[3], maxs[3] + 1) if n > 3 else [0]:
        for z in range(mins[2], maxs[2] + 1):
            print(f"------ w={w}, z={z}")
            for y in range(mins[1], maxs[1] + 1):
                for x in range(mins[0], maxs[0] + 1):
                    ch = '#' if (x, y, z, w) in l else '.'
                    print(ch, end='')
                print()


def next_gen(l, n):
    mins, maxs = dims(l)
    l2 = set()
    for x in range(mins[0]-1, maxs[0] + 2):
        for y in range(mins[1]-1, maxs[1] + 2):
            for z in range(mins[2]-1, maxs[2] + 2):
                for w in range(mins[3]-1, maxs[3] + 2) if n > 3 else [0]:
                    ncnt = num(l, x, y, z, w)
                    v = (x, y, z, w) in l
                    #print(f"({x},{y},{z},{w}), ncnt={ncnt}, v={v}")
                    if ncnt == 3 or (v and ncnt == 2):
                        #print(f"Live: ({x}, {y}, {z}, {w})")
                        l2.add((x, y, z, w))
    return l2

# ----- Part 1 -----
#pr(l, 3)
orig_world = deepcopy(l)
for i in range(6):
    l = next_gen(l, 3)
    #print(f"==== GEN {i+1} ====")
    #pr(l, 3)
print(len(l))

# ----- Part 2 -----

l = orig_world
#pr(l, 4)
for i in range(6):
    l = next_gen(l, 4)
    #print(f"==== GEN {i+1} ====")
    #pr(l, 4)
print(len(l))
