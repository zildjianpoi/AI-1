# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 13:37:42 2018

@author: Zhejia Yang

whats math used for??
why time so long??
"""
import math, random, time, heapq

class PriorityQueue():
   """Implementation of a priority queue 
   to store nodes during search."""
   # TODO 1 : finish this class
   
   # HINT look up/use the module heapq.

   def __init__(self):
      self.queue = []
      self.current = 0    

   def next(self):
      if self.current >=len(self.queue):
         self.current
         raise StopIteration
   
      out = self.queue[self.current]
      self.current += 1
   
      return out

   def pop(self):
      # Your code goes here
      if not len(self.queue) == 0:              ##checks if heap is empty
          return heapq.heappop(self.queue)      ##pops maintaining heap
      else:
          print("Empty queue")              ##if it is empty prints for debugging
          exit                              ##stops program cause something is wrong
      #return (0, '')
   
       
   def remove(self, nodeId):
     # Your code goes here
     """r = [c for c in self.queue if c[1][-1] == nodeId]      #put all nodes that end in nodeId in list
     for n in r:            #loop through all nodes with nodeId
         #print(n[1][-1])
         self.queue.remove(n)       #remove all nodes with nodeId
     #if not len(r)==0:                  #If something was removed
         #heapq.heapify(self.queue)      #re-heapify list
     #return self.queue.remove(nodeId)"""
     return (0, '')             #return random thing"""

   def __iter__(self):
      return self

   def __str__(self):
      return 'PQ:[%s]'%(', '.join([str(i) for i in self.queue]))

   def append(self, node):
      # Your code goes here
      #print ('Not implemented yet') 
      heapq.heappush(self.queue, node)      #push node onto heap 
       
   def __contains__(self, key):
      self.current = 0
      return key in [n for v,n in self.queue]

   def __eq__(self, other):
      return self == other

   def size(self):
      return len(self.queue)
   
   def clear(self):
      self.queue = []
       
   def top(self):
      return self.queue[0]

   __next__ = next


def check_pq():
   ''' check_pq is checking if your PriorityQueue
   is completed or not'''
   pq = PriorityQueue()
   temp_list = []

   for i in range(10):
      a = random.randint(0,10000)
      pq.append((a,'a'))
      temp_list.append(a)

   temp_list = sorted(temp_list)   
   
   for i in temp_list:
      j = pq.pop()
      if not i == j[0]:
         return False

   return True

def generate_adjacents(current, word_list):
   ''' word_list is a set which has all words.
   By comparing current and words in the word_list,
   generate adjacents set and return it'''
   adj_set = set()
   # TODO 2: adjacents
   # Your code goes here
   alphabet = "abcdefghijklmnopqrstuvwxyz"          #letters of aplphabet
   l1 = current[2]                          #extract word from node
   for al in alphabet:                          #loop through all letters of alphabet
       for index in range(len(l1)):             #loop through all letters of word
           nword = l1[:index] + al + l1[index+1:]   #replace one letter of word
           if nword in word_list and not nword == l1:    #check if word is in word list and is not already in adjacencies or is the original word
               adj_set.add(nword)       #add the word to adj
   return adj_set           #return all adj set

def dist_heuristic(v, goal):
   ''' v is the current node. Calculate the heuristic function
   and then return a numeric value'''
   # TODO 3: heuristic
   # Your code goes here
#   cur_time = time.time()
   diff = 0                     #number of differences from goal
   for l in range(len(goal)):   #loop through all letters of word and goal
       #print(l)
       if not v[l] == goal[l]:  #if letters are not equal
           diff += 1            #add one difference
#   print(str(time.time()-cur_time))
   return diff                  #return total num of differences

def a_star(word_list, start, goal, heuristic=dist_heuristic):
   '''A* algorithm use the sum of cumulative path cost and the heuristic value for each loop
   Update the cost and path if you find the lower-cost path in your process.
   You may start from your BFS algorithm and expand to keep up the total cost while moving node to node.
   '''
   frontier = PriorityQueue()
   if start == goal: return []
   # TODO 4: A* Search
   # Your code goes here
   ex = dict()
   ex[start] = 0
   frontier.append((heuristic(start, goal), [start], start))       #add start node(cost, path) to frontier
   while len(frontier.queue) > 0:           #while frontier is not empty
       curr = frontier.pop()            #pop lowest val from heap
       #frontier.remove(curr[1][-1])     #remove all other higher(heuristic+pathcost) instances ending in popped value from frontier
       #curr = frontier.pop()
       #ex[curr[2]] = len(curr[1])
       if curr[2] == goal:          #if the end of path is goal
           return curr[1]           #return path
       for w in generate_adjacents(curr, word_list)-set(curr[1]):    #else get all adj
       #    if not w in curr[1]:                         #if adj not already in path
           if (len(curr[1]) + 1) <= ex.get(w, len(curr[1])+1): 
               ex[w] = len(curr[1])+1
               z = [*curr[1]]
               z.append(w)          
               frontier.append((heuristic(curr[2], goal)+len(curr[1]), z, w)) #add adj node to heap
   return None          #if never found in while loop, no path exists, return none

def main():
   word_list = set()
   file = open("words_6_longer.txt", "r")
   for word in file.readlines():
      word_list.add(word.rstrip('\n'))
   file.close()
   initial = input("Type the starting word: ")
   goal = input("Type the goal word: ")
   cur_time = time.time()
   path_and_steps = (a_star(word_list, initial, goal))
   if path_and_steps != None:
      print (path_and_steps)
      print ("steps: ", len(path_and_steps))
      print ("Duration: ", time.time() - cur_time)
   else:
      print ("There's no path")
 
if __name__ == '__main__':
   main()

'''Sample output 1
Type the starting word: listen
Type the goal word: beaker
['listen', 'lister', 'bister', 'bitter', 'better', 'beater', 'beaker']
steps:  7
Duration: 0.000997304916381836

Sample output 2
Type the starting word: vaguer
Type the goal word: drifts
['vaguer', 'vagues', 'values', 'valves', 'calves', 'cauves', 'cruves', 'cruses', 'crusts', 'crufts', 'crafts', 'drafts', 'drifts']
steps:  13
Duration: 0.0408782958984375

Sample output 3
Type the starting word: klatch
Type the goal word: giggle
['klatch', 'clatch', 'clutch', 'clunch', 'glunch', 'gaunch', 'launch', 'launce', 'paunce', 'pawnce', 'pawnee', 'pawned', 'panned', 'panged', 'banged', 'bunged', 'bungee', 'bungle', 'bingle', 'gingle', 'giggle']
steps:  21
Duration:  0.0867915153503418
'''
