# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 14:12:44 2018

@author: Zhejia Yang
"""

class node:
    def __init__(self, v):
        self.value = v
        self.parent = None
    def setParent(self, p): #p must be a node
        self.parent = p


def swap(s, a, b): #state, index, index
    if a >= len(s) or b >= len(s):
        print("Index out of bounds " + str(a) + ", " + str(b))
        return
    if not a<b:
        temp = a
        a = b
        b = temp
    #print(str(a) + ", " + str(b))
    #print("length " + str(len(s)) + " index " + str(b+1))
    return s[:a] + s[b] + s[a+1:b] + s[a] + s[b+1:]

def goaltest(s):
    return s.value == "_12345678"

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

def f(st):
    line1 = []
    line2 = []
    line3 = []
    col = 0
    index = -1
    while st:
        s = st.pop()
        col += 1
        if col%17 == 1:             #python on my computer only can print 17 of these in one line and then it overflows
            line1.append("")
            line2.append("")
            line3.append("")
            index += 1
        #print(s)
        if len(s) == 9:
            line1[index] += s[0:3] + " "
            line2[index] += s[3:6] + " "
            line3[index] += s[6:] + " "
        else:
            print("Error: length does not match")
    for i in range(index + 1):
        print(line1[i] + "\n" + line2[i] + "\n" + line3[i] + "\n" + "-" * 68) 
#print(frontier("123450678"))
#a = [1,2,3] + [4,5,6]
#print(a)
"""012345678
120345678
142305678"""

def BFS(s):
    #print("Enter")
    ns = node(s)
    q = [ns]            #queue
    e = set()           #explored
    end = None          #Last node/solution node
    #solved = False
    while(q):
        s = q.pop(0)    #FIFO
        if s not in e:  #Checks if already explored, if not, add to explored
            e.add(s.value)
        #print("-----" + s.value)
        if goaltest(s):
            #f(s.value)
            end = s
            #solved = True
            break
        st = s.value
        for c in generate_children(st):                  #goes through possible moves
            curr = node(swap(st, st.find("_"), c))
            if curr.value not in e:
                curr.setParent(s)               #set the parent of the new node
                q.append(curr)
    print("Explored States: " + str(len(e)))             
    if end == None:
        print("No solution")
        return
    stack = []
    while not end == None:
        stack.append(end.value)
        end = end.parent            #trace the path to the solution: Including original state!! unlike pt2 
    print("-" *5)
    pathlen = len(stack)
    f(stack)
    print("Shortest path: " + str(pathlen))
        
def DFS(s):
    #print("Enter")
    ns = node(s)
    q = [ns]        #This q = a STACK (only difference with BFS)
    e = set()       #Explored
    end = None
    #solved = False
    while(q):
        n = q.pop()     #FILO
        if n not in e:
            e.add(n.value)
        #print("-----" + n.value)
        if goaltest(n):
            #f(n.value)
            end = n
            #solved = True
            break
        st = n.value
        for c in generate_children(st):
            curr = node(swap(st, st.find("_"), c))
            if (curr.value not in e):
                #a = curr.value
                #e.add(n)
                curr.setParent(n)
                q.append(curr)
    #print("Explored States: " + str(len(e)))
    if end == None:
        print("No solution")
        return
    stack = []
    while not end == None:
        stack.append(end.value)
        end = end.parent
    print("-" *5)
    pathlen = len(stack)
    f(stack)
    print("First path found: " + str(pathlen))

def dls(s, limit, l, e):   #string limit list
    if limit == 0 or e.get(s,0) >= limit:
        return []
    if s == "_12345678":
        l.append(s)
        return l
    e[s] = limit
    m = []
    for c in generate_children(s):
        newString = swap(s, c, s.find("_"))
        m = m + dls(newString, limit-1, l[:]+[newString],e)
        if m:
            return m
    return m
        
    
    
sss = input("Starting state?").strip()       
#print("BFS: ")
#BFS(sss)
#print("-" * 68)
print("DLS: ")
ii = int(input("limit: "))
sol = []
#ii = 2
print("-" * 68)
e = {}
#while not sol:
sol = dls(sss, ii, [], e)
#    ii = ii+1
print("steps: " + str(len(sol)))
if len(sol) == 0:
    print("No solution with given limit")
f(sol)