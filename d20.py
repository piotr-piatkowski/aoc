#!/usr/bin/python3.8

import re
import sys
import math
from collections import defaultdict
import itertools

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = 'input.txt'

tiles = defaultdict(list)
ctile = None
with open(path, 'r') as f:
    for line in f:
        line = line.strip()
        if m := re.match(r'Tile (\d+):', line):
            ctile = int(m.group(1))
        elif line == '':
            ctile = None
        elif ctile is not None:
            tiles[ctile].append(line)
        else:
            raise Exception(f"line: {line}")

def transform(t, tr):
    flip = bool(tr & 0x04)
    rot = tr % 4
    l = len(t)
    for tt in t:
        assert len(tt) == l
    if flip:
        t = list(reversed(t))
    for _ in range(rot):
        newt = []
        for y in range(l):
            row = []
            for x in range(l):
                row.append(t[x][-1-y])
            newt.append(''.join(row))
        t = newt
    return t

def strip_border(t):
    return [tt[1:-1] for tt in t[1:-1]]

def prt(t):
    for row in t:
        print(row)
    print()

def get_border(tile, which, reverse=False):
    if which == 'L':
        b = ''.join(r[0] for r in tile)
    elif which == 'R':
        b = ''.join(r[-1] for r in tile)
    elif which == 'T':
        b = tile[0]
    elif which == 'B':
        b = tile[-1]
    else:
        raise Exception(f"which: {which}")
    if reverse:
        b = b[::-1]
    return b

borders = {k: defaultdict(set) for k in "TRBL"} # Top, Right, Bottom, Left
for tid, tile in tiles.items():
    for tr in range(8):
        t2 = transform(tile, tr)
        for b in "TRBL":
            borders[b][get_border(t2, b)].add((tid, tr))

# puzzle size
psize = int(math.sqrt(len(tiles)))
assert psize * psize == len(tiles)

def solve(tlist):
    if len(tlist) == len(tiles):
        return tlist
    #print(f"tlist={tlist}")
    inext = len(tlist)
    x = inext % psize
    y = inext // psize
    m = None # possible tiles for (x,y)
    #print(f"x={x}, y={y}")
    if x > 0:
        tid, tr, tile = tlist[-1]
        lborder = get_border(tile, 'R')
        m = borders['L'][lborder]
        #print(f"Matches for x (lborder={lborder}): {m}")
    if y > 0:
        tid, tr, tile = tlist[-psize]
        tborder = get_border(tile, 'B')
        my = borders['T'][tborder]
        if m:
            m = m & my
        else:
            m = my
        #print(f"Matches for y (tborder={tborder}): {m}")
    tids_used = set(t[0] for t in tlist)
    for tid, tr in m:
        if tid not in tids_used:
            tile = transform(tiles[tid], tr)
            if sol := solve(tlist + [(tid, tr, tile)]):
                #print(f"Found: {sol}")
                return sol
    return None

sol = None
for tid in tiles.keys():
    if sol:
        break
    for tr in range(8):
        tile = transform(tiles[tid], tr)
        found = [(tid, tr, tile)]
        if sol := solve(found):
            #print(f"SOL: {sol}")
            print(
                sol[0][0] *
                sol[psize-1][0] *
                sol[-psize][0] *
                sol[-1][0]
            )
            break

assert(sol is not None)

# So now to the part 2... Build the bitmap of the puzzle

# Tile size
tsize = len(next(iter(tiles.values())))

puzzle = []
for y in range(psize):
    row = [[] for _ in range(tsize-2)]
    for x in range(psize):
        tid, tr, tile = sol[y*psize+x]
        tile = strip_border(tile)
        for i, trow in enumerate(tile):
            row[i].append(trow)
    for r in row:
        puzzle.append(''.join(r))

#prt(puzzle)

# Here be drag^H^H^H^Hsea monsters

spsize = len(puzzle[0])

sm = [
    '..................#.',
    '#....##....##....###',
    '.#..#..#..#..#..#...'
]
sm_w = len(sm[0])
sm_h = len(sm)
smre = list(map(re.compile, sm))

def find_sm(t):
    c = 0
    newt = [list(r) for r in t]
    for x in range(spsize-sm_w):
        for y in range(spsize-sm_h):
            found = True
            for i, regex in enumerate(smre):
                #print(f"Checking {t[y+i][x:]} at {regex}")
                if not regex.match(t[y+i][x:]):
                    found = False
                    break
            if found:
                c += 1
                #print(f"Found at x={x}, y={y}")
                for sx in range(sm_w):
                    for sy in range(sm_h):
                        if sm[sy][sx] == '#':
                            newt[y+sy][x+sx] = 'O'

    if c > 0:
        newt = [''.join(r) for r in newt]
        prt(newt)
        print(''.join(newt).count('#'))

    return c

for tr in range(8):
    #print(f"Checking with tr={tr}")
    t = transform(puzzle, tr)
    if find_sm(t):
        break;

