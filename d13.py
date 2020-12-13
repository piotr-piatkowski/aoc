#!/usr/bin/python3.8

import sys

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = 'input.txt'

f = open(path, "r")
lines = [line.rstrip() for line in f]

start_t = int(lines[0])
buses = [(i, int(b)) for i, b in enumerate(lines[1].split(',')) if b != 'x']

print(start_t, buses)

# Part 1, brute force
t = start_t
found = False
while not found:
    for _, b in buses:
        if t % b == 0:
            print("Part 1:", (t - start_t) * b)
            found = True
            break
    t += 1

# Part 2, a bit smarter - we use step as product of first maxf buses,
# so we never loose the match for already matched buses.
t = 0
step = 1
maxf = 0
while True:
    f = 0
    for i, b in buses:
        exp = (b - i) % b
        #print(f"t={t} maxf={maxf} b={b}, i={i}, mod={t % b}, exp={exp}")
        if t % b != exp:
            break
        f += 1
    if f == len(buses):
        print("Part 2:", t)
        break
    elif f > maxf:
        step *= buses[f-1][1];
        #print(f"==== setting step to {step}")
        maxf = f
    t += step
