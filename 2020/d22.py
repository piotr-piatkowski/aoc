#!/usr/bin/python3.8

import sys
import re
from collections import defaultdict
from copy import deepcopy

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = 'input.txt'

players = [[], []]
curp = None

with open(path, 'r') as f:
    for line in f:
        line = line.strip()
        if m := re.match(r'Player (\d+):', line):
            curp = int(m.group(1)) - 1
        elif line == '':
            curp = None
        elif curp is not None:
            players[curp].append(int(line))
        else:
            raise Exception(line)

def play(players, part=1):

    history = set()
    while True:
        for i, cards in enumerate(players):
            if len(cards) == 0:
                return int(not(i))

        if part == 2:
            key = (tuple(players[0]), tuple(players[1]))
            if key in history:
                return 0
            history.add(key)

        c = [p.pop(0) for p in players]

        if part == 2 and all(len(players[i]) >= c[i] for i in range(2)):
            winner = play(tuple(players[i][:c[i]] for i in range(2)), part)
        else:
            winner = 0 if c[0] > c[1] else 1

        players[winner].append(c[winner])
        players[winner].append(c[not(winner)])


org_players = players
for part in (1, 2):
    players = deepcopy(org_players)
    winner = play(players, part)
    win_cards = players[winner]
    res = 0
    for i, c in enumerate(reversed(win_cards)):
        res += (i + 1) * c
    print(res)

