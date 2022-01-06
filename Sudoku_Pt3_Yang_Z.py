
#Name: Zhejia Yang         #Date: 11/26/18
import time

def createSqu(size):
   x = int(size**0.5)   #rows (up and down)
   y = int(size/x)      #cols (left and right)
   sq = [set(range(x*i, x*(i+1), 1)) for i in range(y)]       #row
   sqy = [set(range(y*i, y*(i+1), 1)) for i in range(x)]       #col
   #print("xy:", x, y)
   #print(sq, "\n", sqy)
   con = dict()
   con[0] = dict()
   con[1] = dict()
   for Set in sq:
      for c in Set:
         n = Set.copy()
         n.remove(c)
         #print(n)
         #print(Set)
         #con[0].setdefault(c, set())
         con[0][c] = con[0].get(c, set())|n
   for Set in sqy:
      for c in Set:
         n = Set.copy()
         n.remove(c)
         #print(n)
         #print(Set)
         #con[0].setdefault(c, set())
         con[1][c] = con[1].get(c, set())|n
   #print (con)
   return con

def eachCon(size):
   con = createSqu(size)
   const = {}
   for i in range(size):
      js = set([(i,xx) for xx in range(size)])    #rows
      Is = set([(xx,i) for xx in range(size)])    #cols
      #print("ijs: ", js, Is)
      for j in range(size):
         const[(i,j)] = const.setdefault((i,j), set())|(js - {(i,j)})
         const[(j,i)] = const.setdefault((j,i), set())|(Is - {(j,i)})
         for k in con[0][i]:
            for m in con[1][j]:
               const[(i,j)].add((k,m))
               #const[(j,i)].add((m,k))
   return const



def pSudoku(curr):
      #print(curr)
      print()
      if curr == None:
         print("Unsolvable")
         return
      for i in range(size):
         l = ''
         for j in range(size):
            l += str(curr.get((i,j), "."))
            if j%col == col-1:
               l += ' ' 
         print(l)
         if i%row == row-1:
            print()
      #print('\n')
def countOcc(r, curr, adj):
   dr = {c: {cc:0 for cc in ss} for c in range(size)}
   dc = {c: {cc:0 for cc in ss} for c in range(size)}
   update = False
   #ds = {c: {cc:0 for cc in ss} for c in size}
   for j in r:
      for v in r[j]:
         dr[j[0]][v]+=1
         dc[j[1]][v]+=1
   for i in range(size):      
      minr = min([(dr[i][k], k) for k in dr[i]])
      minc = min([(dc[i][k], k) for k in dc[i]])
      if 1 == minr[0] or 1 == minc[0]:
         for y in range(size):
            if 1 == minr[0] and minr[1] in r.get((i,y), set()):
               curr[(i,y)] = minr[1]
               updateRange((i,y), minr[1], adj, r)
               q[minr[1]] += 1
            if 1 == minc[0] and minc[1] in r.get((y, i), set()):
               curr[(y,i)] = minc[1]
               updateRange((y,i), minc[1], adj, r)
               q[minc[1]] += 1
         update = True
   return update
      
def updateRange(var, v, adj, r): #updates r; returns changes
   #print((var,v))
   changes = set()            #set of pos (aka vars) that have their ranges changed
   for i in adj[var]:
      if i in r and v in r[i]:      #r[i] = a set
         changes.add(i)
         r[i].remove(v)
   #print(r)
   #print(var in r)
   if var in r:
      del r[var]
   return changes      
  
#print(con)
def backTracker(s, size, adj, r, row, col, q):     #s = start state
   curr = dict()
   #fs = 0                     #already filled space count
   #print(q)
   for i in range(size):
      #curr.setdefault(i, {})
      for j in range(i*size,i*size + size, 1):
         ch = s[j: j+1]
         if not ch == ".":
            mult = (i,j -(i*size))
            curr[mult] = ch
            #print(mult, ch, size)
            updateRange(mult, ch, adj, r)
            #print(r)
            q[ch] += 1
            #fs += 1
   #pSudoku(curr) ###
   update = True
   while(update and r):
      #pSudoku(curr)
      up = False
      #print(r)
      m = min([(len(v), k) for (k,v) in r.items() if k not in curr])
      if m[0] == 1:
         curr[m[1]] = r[m[1]].pop()
         #print((m[1], curr[m[1]]))
         updateRange(m[1], curr[m[1]], adj, r)
         q[curr[m[1]]] += 1
         up = True
      update = countOcc(r, curr, adj) 
      update = (up or update)
   #pSudoku(curr) 
   #print("done")
   aa = recur(curr, r, adj, size, q) 
   #pSudoku(aa)   ###
   print(aa) 
   return q 
   
def orderVar(rl, q):
   return sorted(rl, key=lambda c: q[c], reverse = True)
   
   #return [i[1] for i in sorted([(q[v], v) for v in rl], reverse = False)]
   
def recur(curr, r, adj, size, q):      #curr = dict with ranges (rgb) (gets copied each time)
   if len(curr) == size**2:
      return curr
   var = selectVar(curr, r, adj) 
   ss = orderVar(r[var], q)
   for child in ss:
      curr[var] = str(child)
      #if (index == 3):
         #pSudoku(curr)
      q[child] += 1
      #pSudoku(curr)
      #print(var,child, r)
      changes = updateRange(var, child, adj, r)
      rr = recur(curr, r, adj, size, q)
      if rr == None:
         del curr[var]
         q[child] = q[child] - 1
         for c in changes:       #Reverse Changes to Range
            r[c].add(child)
         continue
      return rr
   r[var] = set(ss)
   return None
   
def selectVar(curr, r, adj):         #least poss first
   return min(r, key=lambda c: len(r[c]))

def checkSum(q):
   ascii = 0
   for v in q:
      ascii += asci[v]*q[v]
   print("CheckSum: ", ascii)

#"ALL FILE INPUTS" 
HEX = "123456789ABCDEF0" 
hh = list(HEX)
asci = {hh[i]:int(i+1) for i in range(len(hh))} 
asci['0'] = 0
print(asci)
#size = int(input("Size: "))
size = 0
puzzles = open('NbyN_sample.txt', 'r')
#print(r)

#s = input("Sudoku: ")
t = time.clock()

index = 1


for line in puzzles:
   print(index)
   size = int(len(line.strip())**0.5)
   row = int(size**0.5)
   col = size//row
   adj = eachCon(size)
   ss = set(HEX[:size])
   r = {i:ss.copy() for i in adj}
   q = {x:0 for x in r[(0,0)]}
   aa = backTracker(line.strip(), size, adj, r, row, col, q)
   checkSum(aa)
   #print('line ', i, ': ', aa, ', ', )
   r = {i:ss.copy() for i in adj}
   index+=1
"""
backTracker(s, size, adj, r, row, col, q)
"""
print(time.clock()-t)
#print(sorted(list(eachCon(12)[(0,0)])))
#print()