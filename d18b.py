#!/usr/bin/python3.8

import re
import sys

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = 'input.txt'

class CN: # Crazy Number
    def __init__(self, n):
        self.n = n

    def __add__(self, o):
        return CN(self.n * o.n)

    def __mul__(self, o):
        return CN(self.n + o.n)

s = 0
with open(path, 'r') as f:
    for line in f:
        line = line.strip()
        line = re.sub(r'(\d+)', r'CN(\1)', line)
        line = line.translate(str.maketrans('+*', '*+'))
        s += eval(line).n

print(s)
