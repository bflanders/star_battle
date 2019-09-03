# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from collections import defaultdict, deque
from functools import reduce
from itertools import combinations
from math import factorial as f

# Params ..........
board = '0000111000'
board+= '0000100000'
board+= '0200004444'
board+= '2200334455'
board+= '6223355555'
board+= '6223355959'
board+= '6633355999'
board+= '6677885599'
board+= '7777885599'
board+= '7777885599'
positions = defaultdict(set)
for i,v in enumerate(board):
    positions[int(v)].add(i)
positions = dict(positions)   

def print_board(board, stars, dash={}):
    print('-'*38)
    for i in range(100):
        sep = '*  ' if i in stars else '   ' 
        print(board[i], end=sep)
        if (i+1)%10==0: 
            print('\n')
    print('-'*38)
    print()
print_board(board, set())    

def adjacent(a,b):
    if a//10==b//10: # same row
        return abs(a-b)==1
    elif a%10==b%10: # same col
        return abs(a-b)==10
    else:
        return (abs(a//10-b//10)<2) and (abs(a%10-b%10)<2)
    
def check(stars, smin=0, smax=2):
    if len(stars)==0: return True
    len_s = len(stars)
    combos = f(len_s)/(f(len_s-2)*2)
    valid_combos = len([pair for pair in combinations(stars,2) if not adjacent(*pair)])
    if not (combos==valid_combos):
        return False
    for i in range(10):
        # Column check
        col_count = sum([1 if p%10==i else 0 for p in stars])
        if not (smin <= col_count <= smax):
            return False
        # Row check
        row_count = sum([1 if p//10==i else 0 for p in stars])
        if not (smin <= row_count <= smax):
            return False
        group_count = len(positions[i]&stars)
        if not (smin <= group_count <= smax):
            return False
    return True
    
pairs = {}
for i in range(10):
     pairs[i] = [set(pair) for pair in combinations(positions[i],2) if not adjacent(*pair)] 
     
# Main loop
print(f'Finding solution out of {reduce(lambda a,b: a*b, [len(v) for v in pairs.values()], 1):,d}')    

def next_branches(stars, a, b):
    # stars = set of numbers up to num
    branches = deque()
    for pair in pairs[a]:
        if check(stars|pair):
            branches.append((stars|pair, b))
    return branches
    
nums = [num[0] for num in sorted([(k,len(v)) for k,v in pairs.items()], key=lambda it: it[1])]
nums.append(None)
order = dict([(nums[i], nums[i+1]) for i in range(10)])
branches=next_branches(set(),nums[0], nums[1])
steps = 0
while branches:
    stars, a = branches.pop()
    steps+=1
    if a==None:
        if check(stars, smin=2, smax=2):
            print(f'Solution in {steps:,d} steps:')
            print_board(board, stars)
            break
    else:
        branches.extend(next_branches(stars, a, order[a]))
    if steps%1000==0:
        print(f'{steps:,d}')
