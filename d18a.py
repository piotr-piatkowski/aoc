#!/usr/bin/python3.8

import re
import sys
from collections import defaultdict
from copy import deepcopy

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = 'input.txt'

def ev(l):
    n = []
    op = None
    while len(l) > 0:
        if l[0] == ')':
            return n.pop(), l[1:]
        elif l[0] == '(':
            r, l = ev(l[1:])
            n.append(r)
        elif m := re.match(r'(\d+)(.*)', l):
            n.append(int(m.group(1)))
            l = m.group(2)
        elif l[0] in '+-*/':
            op = l[0]
            l = l[1:]
        else:
            raise Exception(f"l={l}")
        if op and len(n) > 1:
            n1, n2 = n
            n = [eval(f"{n1}{op}{n2}")]
            op = None
    return n.pop(), l

s = 0
with open(path, 'r') as f:
    for line in f:
        line = line.strip()
        line = line.replace(' ', '')
        s += ev(line)[0]

print(s)
