#name: Zhejia Yang   date: 11/28/18

import random
from itertools import product

N = int(input("size? "))

def makeAdj(N):
   adj = dict()
   for i in range(N):
      sr = {(i, s) for s in range(N)}
      sc = {(s, i) for s in range(N)}
      for j in range(N):
         #adj[(i,j)] = {'a', 'b'}
         #print(adj.get((i,j), set()))
         adj[(i,j)] = adj.get((i,j), set())|(sr-{(i,j)})
         adj[(j,i)] = adj.get((j,i), set())|(sc - {(j,i)})
         adj[(i,j)] = adj.get((i,j), set())|{(i+a,j+a) for a in range(-1*N, N, 1) if not (i+a >= N or i+a < 0 or j+a >= N or j+a < 0 or a==0)}
         adj[(i,j)] = adj.get((i,j), set())|{(i+a,j-a) for a in range(-1*N, N, 1) if not (i+a >= N or i+a < 0 or j-a >= N or j-a < 0 or a==0)}
   return adj 

def upCon(xy, con, adj, prev):
   for c in adj[xy]:
      if not c == xy:
         con[c] += 1
   if prev:
      for c in adj[prev]:
         if not c == prev:
            con[c] -= 1 

def createStart(N, con, adj):
   curr = dict()
   tee = (0,random.randint(0,N-1))
   curr[tee] = True
   upCon(tee, con, adj, None)
   for r in range(1,N,1):
      val = min(range(N), key=lambda d: con[(r,d)])
      curr[(r,val)] = True
      upCon((r,val), con, adj, None)
   return curr    
"""
function MIN-CONFLICTS(csp,max steps) returns a solution or failure inputs: 
   csp, a constraint satisfaction problem 
   max steps, the number of steps allowed before giving up
   current <- an initial complete assignment for csp 
   for i = 1 to max steps do
      if current is a solution for csp then return current 
      var <- a randomly chosen, conflicted variable from VARIABLES[csp] 
      value <- the value v for var that minimizes CONFLICTS(var,v,current,csp) 
      set var = value in current 
   return failure
   
   min(X, key=lambda c: len(X[c]))

"""
def check(curr, con):
   s = set()
   for vv in curr.keys():
      #print(vv, con[vv], curr[vv])
      if curr[vv] == True and con[vv] > 0:
         s.add(vv)
   return s

def minConflicts(N):
   adj = makeAdj(N)
   con = {(i,j):0 for i in range(N) for j in range(N)}
   curr = createStart(N, con, adj)
   #print(adj)
   #print(curr)
   #print(con)
   cf = check(curr, con)      #conflicts set
   ex = set()
   while cf:
      #print(cf)
      #print(curr)
      #print(curr)
      var = cf.pop()
      ex.add(str(curr))
      list = [x for x in con.keys() if not(x in curr.keys() and curr[x]==True)]
      #print(list)
      val = min(list, key=lambda d: con[d]) 
      curr[val] = True
      curr[var] = False
      while str(curr) in ex:
         curr[val] = False
         list.remove(val)
         val = min(list, key=lambda d: con[d]) 
         curr[val] = True
      upCon(val, con, adj, var)
      cf = check(curr, con)
      #if con[val] > 0:
         #cf.add(val)
   #print(curr)
   if len([i for i in curr.values() if i == True]) < N:
      return None
   return curr

def pBoard(curr):
   for xx in range(N):
      line = ''
      for yy in range(N):
         if (xx,yy) not in curr.keys() or curr[(xx,yy)] == False:
            line = line + '.'
         else:
            line = line + 'Q'
      print(line)
pBoard(minConflicts(N))
