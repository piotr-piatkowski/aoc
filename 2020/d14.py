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

def expand(addr):
    if 'X' in addr:
        return expand(addr.replace('X', '0', 1)) + expand(addr.replace('X', '1', 1))
    else:
        return [addr]

def put1(mem, addr, val, mask):
    val = list(format(val, '036b'))
    for i, m in enumerate(mask):
        if m != 'X':
            val[i] = m
    val = int(''.join(val), 2)
    mem[addr] = val

def put2(mem, addr, val, mask):
    addr = list(format(addr, '036b'))
    for i, m in enumerate(mask):
        if m == '1':
            addr[i] = '1'
        elif m == 'X':
            addr[i] = 'X'
    addr = ''.join(addr)
    for addr in expand(addr):
        addr = int(addr, 2)
        mem[addr] = val

mem1 = defaultdict(int)
mem2 = defaultdict(int)

for l in lines:
    if r := re.match(r'mask = ([01X]+)', l):
        mask = r.group(1)
    elif r := re.match(r'mem\[(\d+)\] = (\d+)', l):
        addr = int(r.group(1))
        value = int(r.group(2))
        put1(mem1, addr, value, mask)
        put2(mem2, addr, value, mask)
    else:
        raise Exception(l)

print(sum(mem1.values()))
print(sum(mem2.values()))
