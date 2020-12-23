#!/usr/bin/python3.8

import sys
import re
from collections import defaultdict
from copy import deepcopy

class Node:
    def __init__(self, n):
        self.next = self
        self.n = n

    def __repr__(self):
        return f"Node(n={self.n}, next={self.next.n})"

    def get_next(self, n=1):
        node = self
        for i in range(n):
            node = node.next
        return node

def ll_to_list(ll):
    node = ll
    l = []
    while True:
        l.append(node.n)
        node = node.next
        if node == ll:
            break
    return l

def print_list(ll):
    print(ll_to_list(ll))

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = 'input.txt'

with open(path, 'r') as f:
    for line in f:
        cups = [int(n) for n in line.strip()]

def play(cups, iterations):

    # We assume cups contain all numbers from 1 to len(cups)
    num2node = [None]*(len(cups)+1)

    # Build a linked list, while also keeping references to each node
    # in the num2node array - thus we can find any number's node in O(1)
    nfirst = Node(cups[0])
    num2node[nfirst.n] = nfirst
    last = nfirst
    for c in cups[1:]:
        n = Node(c)
        n.next = nfirst
        last.next = n
        last = n
        num2node[c] = n

    # ...and start actual game
    cur = nfirst
    for i in range(iterations):
        #if iterations < 1000 or (i + 1) % 100000 == 0:
        #    print(f"move {i+1}")
        #print_list(cur)

        seln = [cur.get_next(i).n for i in range(1, 4)]

        target = cur.n - 1
        while target == 0 or target in seln:
            target -= 1
            if target <= 0:
                target = len(cups)

        target_node = num2node[target]
        #print(f"target={target}, target_node={target_node}")

        first_sel = cur.next
        last_sel = first_sel.next.next

        cur.next = last_sel.next
        last_sel.next = target_node.next
        target_node.next = first_sel

        #print_list(cur)
        cur = cur.next

    return num2node[1]

# Part 1 - just cups, 100 iterations

first = play(cups, 100)
print(''.join(map(str, ll_to_list(first)[1:])))

# Part 2 - fill up to 1 million, 10M iterations

cups = cups + list(range(len(cups)+1, 1_000_001))
first = play(cups, 10_000_000)
print(first.next.n * first.next.next.n)

