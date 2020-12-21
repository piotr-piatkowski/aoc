#!/usr/bin/python3.8

import re
import sys
from collections import defaultdict

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = 'input.txt'


ings = set()
als = set()
deps = {}
# Need for p1: "How many times do any of those ingredients appear?"
ing_counts = defaultdict(int)

with open(path, 'r') as f:
    for line in f:
        line = line.strip()
        if m := re.match(r'(.*) \(contains (.*)\)', line):
            ii = m.group(1).split()
            aa = m.group(2).split(', ')
            for i in ii:
                ings.add(i)
                ing_counts[i] += 1
            for a in aa:
                als.add(a)
                if a in deps:
                    deps[a] &= set(ii)
                else:
                    deps[a] = set(ii)
        else:
            raise Exception(line)

#print(ings)
#print(als)
#print(deps)

# Part 1, count unused

unused = set(ings)
for k, v in deps.items():
    unused -= v

c = 0
for u in unused:
    c += ing_counts[u]
print(c)

# Part 2, resolve full mapping

known = {}

while True:
    found = False
    #print(f'-- {deps}')
    for a, i in deps.items():
        assert len(i) > 0
        if len(i) == 1:
            ing = i.pop()
            known[a] = ing
            for vv in deps.values():
                if ing in vv:
                    vv.remove(ing)
            found = True
            del(deps[a])
            break
    if not found:
        break

assert len(deps) == 0

#print(known)

# Take ingredients, but sort by allergen names
i2a = {i: a for a, i in known.items()}
print(','.join(sorted(known.values(), key=lambda i: i2a[i])))

