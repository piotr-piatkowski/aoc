#!/usr/bin/python3.8

import re
import sys
from collections import defaultdict
from copy import deepcopy

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = 'input.txt'

def ev(l, part):
    while '(' in l:
        l = re.sub(r'\(([^()]+)\)', lambda m: ev(m.group(1), part), l)
    if part == 1:
        while '+' in l or '*' in l:
            l = re.sub(r'(\d+[+*]\d+)', lambda m: str(eval(m.group(1))), l, count=1)
    else:
        while '+' in l:
            l = re.sub(r'(\d+\+\d+)',
                    lambda m: str(eval(m.group(1))), l)
        while '*' in l:
            l = re.sub(r'(\d+\*\d+)',
                    lambda m: str(eval(m.group(1))), l)
    assert re.match(r'\d+', l)
    return l

s1 = 0
s2 = 0
with open(path, 'r') as f:
    for line in f:
        line = line.strip()
        line = line.replace(' ', '')
        s1 += int(ev(line, part=1))
        s2 += int(ev(line, part=2))

print(s1)
print(s2)
