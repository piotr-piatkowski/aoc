#!/usr/bin/python3.8

import re
import sys
from collections import defaultdict
from copy import deepcopy

rules = []

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = 'input.txt'

f = open(path, "r")
lines = [line.rstrip() for line in f]

nums = [int(n) for n in lines[0].split(',')]
print(nums)

pos = {}

for i, n in enumerate(nums[:-1]):
    pos[n] = i

last = nums[-1]
for n in range(len(nums), 30000000):
    #print(f"last={last}, pos={pos}")
    if last in pos:
        m = n - 1 - pos[last]
    else:
        m = 0
    pos[last] = n - 1
    last = m
    if n + 1 == 2020:
        print(n + 1, m)
    if n % 1000000 == 0:
        print(f"...{n}...")
print(n + 1, m)

