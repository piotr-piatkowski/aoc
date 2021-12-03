#!/usr/bin/python3.8

import re
import sys
from collections import defaultdict
from copy import deepcopy

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = 'input.txt'

rules = {}
data = []
mode = 'r'
with open(path, 'r') as f:
    for line in f:
        line = line.strip()
        if line == '':
            mode = 'd'
        elif mode == 'r':
            m = re.match(r'(\d+): (.*)', line)
            assert(m)
            rules[m.group(1)] = m.group(2)
        else:
            data.append(line)


def match(rid, rules, text, pos=0, lvl=0):
    if lvl > 20:
        return []
    r = rules[rid]
    prefix = ' ' * lvl * 2
    #print(f"{prefix}matching rid={rid}, r={r}, text={text}, pos={pos}, lvl={lvl}")
    if pos >= len(text):
        #print(f"{prefix}pos after end")
        return []
    if m := re.match(r'"(.)"', r):
        if text[pos] == m.group(1):
            #print(f"{prefix}text match")
            return [pos + 1]
        else:
            #print(f"{prefix}text no match")
            return []
    else:
        sols = []
        for alt in r.split('|'):
            rs = [rr.strip() for rr in alt.split(' ') if rr.strip() != '']
            ok = True
            ppos = pos
            pos_to_check = [pos]
            for ri in rs:
                new_pos_to_check = set()
                for p in pos_to_check:
                    ppos = match(ri, rules, text, p, lvl+1)
                    for pp in ppos:
                        new_pos_to_check.add(pp)
                if new_pos_to_check:
                    pos_to_check = new_pos_to_check
                else:
                    ok = False
                    break
            if ok:
                sols += list(new_pos_to_check)
        #print(f"{prefix}sols={sols}")
        return sols

# Part 1
c = 0
for d in data:
    pos = match('0', rules, d)
    if any(p == len(d) for p in pos):
        c+= 1
print(c)

# Part 2
rules['8'] = '42 | 42 8'
rules['11'] = '42 31 | 42 11 31'

c = 0
for d in data:
    pos = match('0', rules, d)
    if any(p == len(d) for p in pos):
        c+= 1
print(c)
