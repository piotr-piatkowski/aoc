#!/usr/bin/python3.8

import sys

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = 'input.txt'

with open(path, 'r') as f:
    lines = list(f)

pub1 = int(lines[0])
pub2 = int(lines[1])

s1, s2  = 7, pub1
v1, v2 = 1, 1
while v1 != pub2:
    v1 = (v1 * s1) % 20201227
    v2 = (v2 * s2) % 20201227

print(v2)


