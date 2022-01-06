# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 20:46:46 2018

@author: Zhejia Yang
"""

#count solvable states


def swap(s, a, b): #state, index, index
    if a >= len(s) or b >= len(s):
        print("Index out of bounds " + str(a) + ", " + str(b))
        return
    if not a<b:
        temp = a
        a = b
        b = temp
    return s[:a] + s[b] + s[a+1:b] + s[a] + s[b+1:]

def generate_children(s):
    i = s.find("_")
    #[int(c) for c in range(len(s)) if int(s[c]) == 0]
   # print(i[0])
   # print("---" + str(i))
    c = []
    for a in [-3,-1,1,3]:
        #print(i[0] + a)
        if i + a >= 0 and i+a <= 8:
            if not(((a == -1) and (i in [3,6])) or ((a == 1) and (i in [2,5]))):
                c.append(i + a)
        #print(i)
    return c

s = set() #solvable states
d = {}
#levels = {}
start = "_12345678"
q = list()
invalid = list()
q.append((start, 1))
while q:
    c = q.pop(0)
    curr = c[0]
    level = c[1]
    if curr not in invalid:
        #print(c)
        if curr not in s:
            s.add(curr)
            d[curr] = [level]
            for c in generate_children(curr):
                if level <= 31:
                    print(level)
                    q.append((swap(curr, curr.find("_"), c), level+1))
        else:
            d[curr].append(level)
            if level == d[curr][0]:
                #print(curr)
                invalid.append(curr)
                for c in generate_children(curr):
                    invalid.append((swap(curr, curr.find("_"), c)))

#print(str(len(s)))
print("181440 - Invalid: " , str(181440 - len(invalid)))
#print(sorted(d.values()))
count = 0
for v in d:
    if len([i for i in d[v] if i == min(d[v])]) == 1:
        #print(v)
        count += 1
print(count)
#f = open("solvable_8_puzzle.txt", "w")
#f.write(str(s))

