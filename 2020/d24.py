#!/usr/bin/python3.8

import re
import sys
from collections import defaultdict

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = 'input.txt'

# / \     / \     / \     / \     /
#/   \   /   \   /   \   /   \   /
#     \ /     \ /     \ /     \ /
#      |       |       |       |
# -2,1 | -1,1  |  0,1  |  1,1  | 2,1
#      |       |       |       |
#     / \     / \     / \     / \
#\   /   \   nw ne   /   \   /   \
# \ /     \ /     \ /     \ /     \
#  |       |       |       |       |
#  | -1,0  w  0,0  e  1,0  |  2,0  |
#  |       |       |       |       |
# / \     / \     / \     / \     /
#/   \   /   sw se   \   /   \   /
#     \ /     \ /     \ /     \ /
#      |       |       |       |
#-1,-1 | 0,-1  | 1,-1  | 2,-1  |
#      |       |       |       |
#     / \     / \     / \     / \

DIR_MAP = {
    'ne': ( 0,  1),
    'nw': (-1,  1),
    'se': ( 1, -1),
    'sw': ( 0, -1),
    'e':  ( 1,  0),
    'w':  (-1,  0),
}

def flip(blacks, path):
    x = 0
    y = 0
    while len(path):
        for d, (dx, dy) in DIR_MAP.items():
            if path.startswith(d):
                x += dx
                y += dy
                path = path[len(d):]
    blacks ^= {(x,y)}

def conway_step(blacks):
    neighbour_count = defaultdict(int)
    for x, y in blacks:
        for dx, dy in DIR_MAP.values():
            neighbour_count[(x+dx, y+dy)] += 1

    new_blacks = set()
    for k, count in neighbour_count.items():
        if count == 1 and k in blacks:
            new_blacks.add(k)
        if count == 2:
            new_blacks.add(k)

    return new_blacks

blacks = set()

with open(path, 'r') as f:
    for line in f:
        line = line.strip()
        flip(blacks, line)

# Part 1 - already done during data loading

print(len(blacks))

# Part2 - conway

for i in range(100):
    blacks = conway_step(blacks)

print(len(blacks))
