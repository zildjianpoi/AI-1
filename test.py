# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 15:39:54 2018

@author: Chelsea Chen
"""

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
 
import pickle
       
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
    
def DFSr(G, e, s, g, l, limit): #Graph, explored(dict(word, level)), start string, goal, list, limit
    #print("---" + s + "  limit: " + str(limit))
    if s == g:
        l.append(s)
        #l;l';'.print(s)
        return l
    elif limit == 1 or e.get(s, 0) >= limit:     #s in e or 
        #print("---" + s + "  limit: " + str(limit))
        return []
    e[s] = limit
    n = l[:]
    n.append(s)
    ll = []
    for a in G[s]:
        if ll not in l:
            ll += DFSr(G, e, a, g, n, limit-1)
        #print(ll)
        if ll:
            return ll
    return ll

def dls(G, s, g, limit):
    e = dict()
    path = DFSr(G,e,s,g,[],limit)
    print(path)
    print("Pathlength: " + str(len(path)))
    return len(path)
    
file = [line.strip() for line in open("words.txt", "r").readlines()]

i = "aaa"
while i:
    i = input("Start word: ").strip()
    word_dict = {}
    with open("words_dict.pickle", "rb") as infile:
        word_dict = pickle.load(infile)
        
    if not i or len(word_dict[i]) == 0:     # not G.has_node(i):
        print("exit")
        break
    j = input("End word: ").strip()

    #e = set()
    #dls(G,i,j,#)
    #ii = BFS(word_dict, i, j)
    ii = int(input("limit: "))
    if ii:
        length = dls(word_dict, i, j, ii) #ii = limit
    if length == 0:
        print("No solution with this limit")
    """DFS = DFSr(G, e, i, j, [])
    print(DFS)
    print("Pathlength: " + str(len(DFS)))"""

