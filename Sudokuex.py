from itertools import product

def solve_sudoku(size, grid):
    R, C = size
    N = R * C        #r = row    c = col     n = number
    X = ([("rc", rc) for rc in product(range(N), range(N))] +
         [("rn", rn) for rn in product(range(N), range(1, N + 1))] +
         [("cn", cn) for cn in product(range(N), range(1, N + 1))] +
         [("bn", bn) for bn in product(range(N), range(1, N + 1))])
    Y = dict()
    for r, c, n in product(range(N), range(N), range(1, N + 1)):
        b = (r // R) * R + (c // C) # Box number
        Y[(r, c, n)] = [
            ("rc", (r, c)),
            ("rn", (r, n)),
            ("cn", (c, n)),
            ("bn", (b, n))]
    X, Y = exact_cover(X, Y)
    for i, row in enumerate(grid): #Grid = list of rows of lists col (rows contents) => enumerate(grid) = (row num, row contents)
        #print(row)
        for j, n in enumerate(row): # j= col num; n = num in pos(i,j)
            if n:                   #aka if not n == 0
               #if ii == 3:
                 #print(n)
               select(X, Y, (i, j, n))
    for solution in solve(X, Y, []):
        for (r, c, n) in solution:
            grid[r][c] = n
        yield grid

def exact_cover(X, Y):
    X = {j: set() for j in X}      #all the rc rn cn bn tuples
    for i, row in Y.items():     #i = (r,c,n)    row = list(rc,rn,cn,bn)
        for j in row:
            X[j].add(i)          #X = dict(rc/rn/cn/bn: (r,c,n) (original points)) ex: rc=(0,0): points((0,0,1),(0,0,2)...etc)
    return X, Y

def solve(X, Y, solution):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))     #rc/etc pair with list num of poss points
        for r in list(X[c]):                    #for r in list of poss points
            solution.append(r)                  #append to solution
            cols = select(X, Y, r)              #select the point
            for s in solve(X, Y, solution):     #recur
                yield s
            deselect(X, Y, r, cols)             #if nothing returned/yeilded, wrong path, remove and pop
            solution.pop()

def select(X, Y, r):
    cols = []
    for j in Y[r]:         #for all rc/rn/ect pairs associated with the point r
        for i in X[j]:     #go through all the points associated with these rc/etc pairs
            for k in Y[i]: #for all the rc/etc pairs associated with these other points (assoc. w/ points accoc. w/r by pairs)
                if k != j: #if pair diff from original(the one we want to set)
                    X[k].remove(i)  #remove the point poss (that conflicts with selected one) {aka setting x[tuple] to ONLY selected point}
        cols.append(X.pop(j))    #removes original 4 rc/etc pairs assoc. with r from X; stores values(X[rc]) (aka i) in col
    return cols

def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)

#if __name__ == "__main__":
    #import doctest
    #doctest.testmod()

import time

HEX = "123456789ABCDEF0"
hh = list(HEX)
asci = {hh[i]:int(i+1) for i in range(len(hh))}
print(asci) 
asci[0] = 0
#size = int(input("size: ")) 

ii = 1
t = time.clock()
for line in open('NbyN_sample.txt', 'r'):
   print(ii)
   size = int(len(line)**0.5)
   row = int(size**0.5)
   col = size//row 
   #print(size)
   s = line.strip()
   curr = [['' for j in range(size)] for i in range(size)]
   for i in range(size):
      for j in range(i*size,i*size + size, 1):
         ch = s[j: j+1]
         if ch == ".":
            ch = 0
         else:
            ch = asci[ch]
         mult = j -(i*size)
         curr[i][mult] = ch
   grid = curr
   #print(*grid, sep='\n')
   
   #print(curr)
   for solution in solve_sudoku((row, col), grid):
      print(*solution, sep='\n')
   ii+=1
   
print(time.clock()-t)
