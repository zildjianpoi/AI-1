#Name: Zhejia Yang         #Date: 11/12/18

import time

def createSqu():
   sq = [[0,1,2], [3,4,5], [6,7,8]]       #both row vs and column
   con = dict()
   for l in sq:
      for c in l:
         n = l.copy()
         n.remove(c)
         n = set(n)
         con.setdefault(c, set())
         con[c] = con[c]|n
   #print (con)
   return con

def checkCon(var, v, adj, curr):
   #pSudoku(curr)
   #print(adj)
   #print(var)
   #print('')
   v = str(v)
   for i in curr[var[0]]:           #Row check
      #print(curr[var[0]][i], v)
      if curr[var[0]][i] == v:
         return False
   for i in range(9):               #Column check
      #pSudoku(curr)
      #print(curr[i][var[1]], v)
      if curr[i][var[1]] == v:
         return False
   for k in adj[var[0]]:
      for j in adj[var[1]]:
         #print(curr[k][j],v)
         if curr[k][j] == v: 
            return False 
   return True

def pSudoku(curr):
      #print(curr)
      for i in range(len(curr)):
         l = ''
         for j in range(len(curr[i])):
            l += str(curr[i][j])
         print(l)
      print('\n')
  
#print(con)
def backTracker(adj, s):
   r = set([1,2,3,4,5,6,7,8,9])
   curr = dict()
   for i in range(9):
      curr.setdefault(i, {})
      for j in range(9):
         curr[i].setdefault(j, s[i*9+j:i*9+j+1])
   #pSudoku(curr)
   #print(conNum(curr, (0,0), adj))
   return recur(curr, r, adj)
   
def recur(curr, r, adj):      #curr = dict with ranges (rgb) (gets copied each time)
   #pSudoku(curr)
   if not [x for x in curr if '.' in curr[x].values()]:
      return curr
   var = selectVar(curr, r, adj)
   #print(var)
   for child in r:
      if checkCon(var, child, adj, curr):
         #   print(var, child)
         #pSudoku(curr)
         curr[var[0]][var[1]] = str(child)
         #pSudoku(curr)
         #print(curr)
         #print(var)
         rr = recur(curr, r, adj)
         if rr == None:
            curr[var[0]][var[1]] = '.'
            continue
         return rr
   return None
   
def selectVar(curr, r, adj):         #least poss first
   max = 0
   v = None
   for k in curr:
      for a in curr[k]:
         #print(k,a)
         if (curr[k][a] == '.'): 
            cc = conNum(curr, (k,a), adj)
            #print(cc)
            if cc > max:
               max = cc
               v = (k,a)
   return v

def conNum(curr, val, adj):
   i = 0
   i += len([k for k in curr[val[0]] if not curr[val[0]][k] == '.']) #and not k == val[1]]) (Dont ever test smthg that already exists anyways)
   #print(i)
   i += len([k for k in range(9) if not curr[k][val[1]] == '.']) #and not k == val[0]])
   #print(i)
   #print(val)
   #print(adj[val[0]], adj[val[1]])
   for k in adj[val[0]]:
      for j in adj[val[1]]:
         #print('---',k, j)
         if not curr[k][j] == '.':
            i += 1
   return i
      
   
#s = ''
#for k in range(len(d)):
   #s += str(d[k])

s = input("Sudoku: ")
t = time.clock()
adj = createSqu()
aa = backTracker(adj, s)
pSudoku(aa)
print(time.clock()-t)
#print(checkCon((7,6), 3, adj, aa))
#print(checkCon((8,7), 2, adj, {0: {0: 4, 1: 4, 2: '3', 3: 4, 4: '2', 5: 1, 6: '6', 7: 5, 8: 5}, 1: {0: '9', 1: 2, 2: 4, 3: '3', 4: 4, 5: '5', 6: 7, 7: 2, 8: '1'}, 2: {0: 2, 1: 2, 2: '1', 3: '8', 4: 7, 5: '6', 6: '4', 7: 2, 8: 2}, 3: {0: 3, 1: 3, 2: '8', 3: '1', 4: 3, 5: '2', 6: '9', 7: 3, 8: 3}, 4: {0: '7', 1: 1, 2: 4, 3: 4, 4: 3, 5: 4, 6: 1, 7: 1, 8: '8'}, 5: {0: 1, 1: 1, 2: '6', 3: '7', 4: 3, 5: '8', 6: '2', 7: 1, 8: 3}, 6: {0: 1, 1: 1, 2: '2', 3: '6', 4: 4, 5: '9', 6: '5', 7: 1, 8: 4}, 7: {0: '8', 1: 1, 2: 4, 3: '2', 4: 4, 5: '3', 6: 1, 7: 1, 8: '9'}, 8: {0: 4, 1: 4, 2: '5', 3: 4, 4: '1', 5: 4, 6: '3', 7: '.', 8: 2}}
#))
#pSudoku({0: {0: 4, 1: 4, 2: '3', 3: 4, 4: '2', 5: 1, 6: '6', 7: 5, 8: 5}, 1: {0: '9', 1: 2, 2: 4, 3: '3', 4: 4, 5: '5', 6: 7, 7: 2, 8: '1'}, 2: {0: 2, 1: 2, 2: '1', 3: '8', 4: 7, 5: '6', 6: '4', 7: 2, 8: 2}, 3: {0: 3, 1: 3, 2: '8', 3: '1', 4: 3, 5: '2', 6: '9', 7: 3, 8: 3}, 4: {0: '7', 1: 1, 2: 4, 3: 4, 4: 3, 5: 4, 6: 1, 7: 1, 8: '8'}, 5: {0: 1, 1: 1, 2: '6', 3: '7', 4: 3, 5: '8', 6: '2', 7: 1, 8: 3}, 6: {0: 1, 1: 1, 2: '2', 3: '6', 4: 4, 5: '9', 6: '5', 7: 1, 8: 4}, 7: {0: '8', 1: 1, 2: 4, 3: '2', 4: 4, 5: '3', 6: 1, 7: 1, 8: '9'}, 8: {0: 4, 1: 4, 2: '5', 3: 4, 4: '1', 5: 4, 6: '3', 7: '.', 8: 2}}
#)


"""
Test Cases:

..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..


"""



