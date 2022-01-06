#Name: Zhejia Yang         #Date: 11/12/18

hex = [[0,1,2,6,7,8], [2,3,4,8,9,10], [5,6,7,12,13,14], [7,8,9,14,15,16], [9,10,11,16,17,18], [13,14,15,19,20,21], [15,16,17,21,22,23]]
con = dict()
for l in hex:
   for c in l:
      n = l.copy()
      n.remove(c)
      n = set(n)
      con.setdefault(c, set())
      con[c] = con[c]|n
   
#print(con)
def backTracker(adj):
   r = set([1,2,3,4,5,6])
   return recur({}, r, adj)
   
def recur(curr, r, adj):      #curr = dict with ranges (rgb) (gets copied each time)
   #print(len(curr), len(adj))
   if len(curr) == len(adj):
      return curr
   var = selectVar(curr, r, adj)
   #print(var)
   for child in r:
      #print(len([x for x in adj[var] if x in curr and curr[x] == child]))
      #print(var)
      if len([x for x in adj[var] if x in curr and curr[x] == child]) == 0:
         curr[var] = child
         #print(curr)
         #print(var)
         rr = recur(curr, r, adj)
         if rr == None:
            del curr[var]
            continue
         return rr
   return None
def selectVar(curr, r, adj):         #least poss first
   max = 0
   v = None
   for a in range(24):
      if a not in curr and len(adj[a]) > max:
         max = len(adj[a])
         v = a
   return v
   
d = backTracker(con) 
s = ''
for k in range(len(d)):
   s += str(d[k])
print(' ', s[:5], ' \n', s[5:12], '\n', s[12:19], '\n', '', s[19:]) 