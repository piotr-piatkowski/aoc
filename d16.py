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

valid_by_key = defaultdict(lambda: defaultdict(int))
valid_any = defaultdict(int)

tickets = []
my_ticket = None

mode = 'rules'

with open(path, 'r') as f:
    for line in f:
        line = line.strip()
        if line == 'your ticket:':
            mode = 'your'
        elif line == 'nearby tickets:':
            mode = 'nearby'
        elif line == '':
            pass
        elif mode == 'rules':
            m = re.match(r'(.*): (\d+)-(\d+) or (\d+)-(\d+)', line)
            assert m, line
            name = m.group(1)
            r1 = range(int(m.group(2)), int(m.group(3)) + 1)
            r2 = range(int(m.group(4)), int(m.group(5)) + 1)
            for v in [*r1, *r2]:
                valid_by_key[name][v] = 1
                valid_any[v] = 1
        elif mode == 'your':
            my_ticket = [int(v) for v in line.split(',')]
        elif mode == 'nearby':
            ticket = [int(v) for v in line.split(',')]
            if all(v in valid_any for v in ticket):
                tickets.append(ticket)
        else:
            raise Exception(f"Invalid line: {line}")

ticket_size = len(my_ticket)
possible_columns = {k: set(range(ticket_size)) for k in valid_by_key.keys()}

# Remove columns which don't fit in any ticket
for t in tickets:
    for column, val in enumerate(t):
        for key, valid_values in valid_by_key.items():
            if val not in valid_values:
                possible_columns[key].remove(column)

# Now build map from column to key, by finding keys with only one possible
# column, and then removing this column from all other keys
column_to_key = {}
while possible_columns:
    for key, columns in possible_columns.items():
        if len(columns) == 1:
            col = columns.pop()
            column_to_key[col] = key
            del(possible_columns[key])
            for s in possible_columns.values():
                s.remove(col)
            break
    #print(possible_columns)

#print(column_to_key)

n = 1
for i, v in enumerate(my_ticket):
    if column_to_key[i].startswith('departure'):
        n *= v
print(n)


