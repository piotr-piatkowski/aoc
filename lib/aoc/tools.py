import os
import sys
import re
import argparse
import inspect
import itertools
import time

from collections import defaultdict, Counter
from copy import deepcopy
from icecream import ic

def read_ints(args):
    return read_split(args, int)

def read_floats(args):
    return read_split(args, float)

def read_words(args):
    return read_split(args, str)

def read_smart(args):
    def smart_conv(x):
        for conv in (int, float):
            try:
                return conv(x)
            except:
                pass
        return x
    return read_split(args, smart_conv)

def read_split(args, conv):
    with open(args.path, "r") as f:
        l = []
        for line in f:
            l.append([conv(x) for x in line.split()])
    return l

def read_lines(args):
    with open(args.path, "r") as f:
        l = []
        for line in f:
            l.append(line.strip())
    return l

def transpose(l):
    return list(map(list, zip(*l)))

def read_columns(args, conv):
    return transpose(read_split(args, conv))

def read_all(args):
    with open(args.path, "r") as f:
        return f.read().strip()

ALL_DIRS = {(dx, dy) 
            for dx in (-1, 0, 1) 
            for dy in (-1, 0, 1) 
            if (dx, dy) != (0, 0)}
HV_DIRS = {(-1, 0), (1, 0), (0, -1), (0, 1)}

DIR_L = complex(-1, 0)
DIR_R = complex(1, 0)
DIR_U = complex(0, -1)
DIR_D = complex(0, 1)

DMAP = {
    "<": DIR_L,
    ">": DIR_R,
    "^": DIR_U,
    "v": DIR_D,
}

def turn_left(d):
    return d * complex(0, -1)

def turn_right(d):
    return d * complex(0, 1)

C_ALL_DIRS = [complex(dx, dy) for dx, dy in ALL_DIRS]
C_HV_DIRS = [complex(dx, dy) for dx, dy in HV_DIRS]
C_CORNER_DIRS = list(set(C_ALL_DIRS) - set(C_HV_DIRS))

C_CORNER_DIRS_ROUND = [
    complex(-1, -1),
    complex(1, -1),
    complex(1, 1),
    complex(-1, 1),
]

# For debug prints, PH=point human, DH=direction human,
# PDH=point direction human
def PH(p):
    return f"({int(p.real)}, {int(p.imag)})"

def DH(d):
    if d == DIR_U:
        return '^'
    elif d == DIR_D:
        return 'v'
    elif d == DIR_L:
        return '<'
    elif d == DIR_R:
        return '>'
    else:
        return '?'

def PDH(p):
    return f"({PH(p[0])}, {DH(p[1])})"


debug = False

def dbg(s):
    if debug:
        print(s)

def main(run):
    script_dir = os.path.dirname(inspect.stack()[1].filename)
    os.chdir(script_dir)

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
            help='Enable debug')
    parser.add_argument('path', nargs='?', default=f'input.txt',
            help='Path to the input file')

    args = parser.parse_args()
    global debug
    debug = args.debug
    run(args)

class Timer:
    start_ts: float = 0
    lap_start_ts: float = 0

    def start(self):
        self.start_ts = time.time()
        self.lap_start_ts = self.start_ts

    def lap(self, name: str):
        now = time.time()
        lap = now - self.lap_start_ts
        self.lap_start_ts = now
        print(f"{name}: {lap:.6f}")

    def stop(self):
        now = time.time()
        total = now - self.start_ts
        print(f"Total: {total:.6f}")
