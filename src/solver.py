from collections import defaultdict, deque
from copy import deepcopy
from functools import reduce
from itertools import combinations
from math import factorial as f
from random import shuffle, randint

# Params ..........
board = '0011222222'
board+= '0011202425'
board+= '0001103425'
board+= '0000003445'
board+= '0600003445'
board+= '6606033445'
board+= '7666666945'
board+= '7776669955'
board+= '7886669999'
board+= '8888666999'
positions = defaultdict(set)
for i,v in enumerate(board):
    positions[int(v)].add(i)
positions = dict(positions)   

def print_board(board, stars, dash={}):
    print('-'*28)
    for i in range(100):
        sep = '* ' if i in stars else '- ' if i in dash else '  ' 
        print(board[i], end=sep)
        if (i+1)%10==0: print()
    print('-'*28)
    print()
print_board(board, set())    
def adjacent(a,b):
    if a//10==b//10: # same row
        return abs(a-b)==1
    elif a%10==b%10: # same col
        return abs(a-b)==10
    else:
        return (abs(a//10-b//10)<2) and (abs(a%10-b%10)<2)

def valid(s):
    len_s = len(s)
    combos = f(len_s)/(f(len_s-2)*2)
    return combos==len([pair for pair in combinations(s,2) if not adjacent(*pair)])
    
def check(stars):
    if len(stars)==0: return True
    has_2 = 1
    for i in range(10):
        # Column check
        has_2 *= int(sum([1 if p%10==i else 0 for p in stars])==2)
        # Row check
        has_2 *= int(sum([1 if p//10==i else 0 for p in stars])==2)
        # check groups
        has_2 *= len(positions[i]&stars)==2
        # Early out
        if not has_2: break
    return bool(has_2)
    
pairs = {}
for i in range(10):
     pairs[i] = [set(pair) for pair in combinations(positions[i],2) if not adjacent(*pair)] 
     
# Main loop
print(f'Finding solution out of {reduce(lambda a,b: a*b, [len(v) for v in pairs.values()], 1):,d}')    

def next_branches(branch, a, b):
    # branch = set of numbers up to num
    branches = deque()
    for pair in pairs[a]:
        if valid(branch|pair):
            branches.append((branch|pair, b))
    return branches
    
nums = [num[0] for num in sorted([(k,len(v)) for k,v in pairs.items()], key=lambda it: it[1])]
nums.append(None)
order = dict([(nums[i], nums[i+1]) for i in range(10)])
branches=next_branches(set(),nums[0], nums[1])
steps = 0
while branches:
    branch, a = branches.pop()
    steps+=1
    if a==None:
        if check(branch):
            print(f'Solution in {steps}:')
            print_board(board, branch)
            break
    else:
        branches.extend(next_branches(branch, a, order[a]))
        
