#Name: Zhejia Yang      Date: 11/9/18

#import copy    #??

def backTracker(adj):
   range = {}
   for key in adj:
      range[key] = ['R', 'G', 'B']
   return recur({}, range, adj)
   
def recur(curr, range, adj):      #curr = dict with ranges (rgb) (gets copied each time)
   #print(len(curr), len(adj))
   if len(curr) == len(adj):
      return curr
   var = selectVar(curr, range, adj)
   #print(var)
   for child in range[var]:
      #print(len([x for x in adj[var] if x in curr and curr[x] == child]))
      if len([x for x in adj[var] if x in curr and curr[x] == child]) == 0:
         curr[var] = child
         #print(curr)
         #print(var)
         r = recur(curr, range, adj)
         if r == None:
            del curr[var]
            continue
         return r
   return None
def selectVar(curr, range, adj):         #least poss first
   min = len(range)
   v = None
   for a in range:
      if a not in curr and len(range[a]) < min:
         min = len(range[a])
         v = a
   return v
   
adj = {"WA": ["NT", "SA"], "NT": ["SA", "WA", "Q"], "SA": ["WA", "NT", "Q", "NSW", "V"], "Q": ["NT", "SA", "NSW"], "NSW": ["Q", "SA", "V"], "V":["SA","NSW"], "T":[]}
print(backTracker(adj))



