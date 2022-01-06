# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 13:14:59 2018

@author: Zhejia Yang
"""

#Word ladder
class node:
    def __init__(self, v):
        self.value = v
        self.parent = None
    def setParent(self, p): #p must be a node
        self.parent = p
#import networkx as nx
#import pickle
def oneDiff(word1, word2):
    diff = 0
    for i in range(len(word1)):
        if not word1[i] == word2[i]:
            diff += 1
    #print(diff)
    return diff == 1

def BFS(G, s, en):     # s = graph node
    q = [node(s)]             #queue
    e = set()           #explored
    end = None          #Last node/solution node
    while(q):
        s = q.pop(0)    #FIFO
        if s.value not in e: 
            e.add(s.value)
        if s.value == en:
            end = s
            break
        for c in G[s.value]:                  #goes through possible moves
            if c not in e:
                cc = node(c)
                cc.setParent(s)               #set the parent of the new node
                q.append(cc)
    if end == None:
        print("No solution")
        return
    l = []
    while not end == None:
        l.append(end.value)
        end = end.parent           
    print("-" *5)
    pathlen = len(l)
    l.reverse()
    print(l)
    print("Shortest path: " + str(pathlen))
    return pathlen

"""def DFSr(G, e, s, g, l): #Graph, explored(set), start string, goal, list
    #print("---" + s)
    if s == g:
        l.append(s)
        return l
    elif s in e:
        return []
    e.add(s)
    n = l[:]
    n.append(s)
    ll = []
    for a in G[s]:
        ll += DFSr(G, e, a, g, n)
        #print(ll)
        if ll:
            return ll
    return ll"""



    

#import pickle

file = [line.strip() for line in open("words.txt", "r").readlines()]
#print(file)
G = {}
for f in file:
    G[f] = []
#print(G.has_node("cooler"))

for l1 in file:
    for l2 in file:
        if oneDiff(l1,l2) and not l2 in G[l1]:
            G[l1].append(l2)
            G[l2].append(l1)
#with open("words_dict.pickle", "rb") as infile:
        #word_dict = pickle.load(infile)
#print(word_dict)
#print(G)
#print([a for a in G.neighbors("cooled")])
#for n in G.__iter__():
    #print(n, end = " ")
#print([a for a in G.neighbors("cooper")])
i = "aaa"
while i:
    i = input("Start word: ").strip()
    #print("'" + i + "'")
    #print(bool(i))
    if not i: #or not G.get(i, -1) == -1:
        print("exit")
        break
    j = input("End word: ").strip()
    BFS(G, i, j)

