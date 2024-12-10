import os
import sys
import re
import argparse
import inspect
import itertools

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

C_ALL_DIRS = [complex(dx, dy) for dx, dy in ALL_DIRS]
C_HV_DIRS = [complex(dx, dy) for dx, dy in HV_DIRS]

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
