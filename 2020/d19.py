#!/usr/bin/python3.8

import re
import sys

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

def expand(r, rules):
    orgid = r
    r = rules[r]
    if m := re.match(r'"(.)"', r):
        return m.group(1)
    else:
        orgr = r
        r = re.sub(r'(\d+)', lambda m: expand(m.group(1), rules), r)
        r = '(' + r.replace(' ', '') + ')'
        #print(f"expanded {orgid} ({orgr}) to {r}")
        return r

rule0p1 = re.compile('^' + expand('0', rules ) + '$')

# This was to be changed for part2:
# 8: 42 | 42 8
# 11: 42 31 | 42 11 31
# So I do little cheating, manually expanding recursion in those rules,
# only to level 10 - which was enough
r8 = []
r11 = []
t8 = '42'
t11 = '42 31'
for _ in range(10):
    r8.append(t8)
    r11.append(t11)
    t8 = f'42 {t8}'
    t11 = f'42 {t11} 31'

rules['8'] = '|'.join(r8)
rules['11'] = '|'.join(r11)

rule0p2 = re.compile('^' + expand('0', rules ) + '$')

c1, c2 = 0, 0
for d in data:
    if rule0p1.match(d):
        c1 += 1
    if rule0p2.match(d):
        c2 += 1
print(c1)
print(c2)
