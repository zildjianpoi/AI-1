import heapq
import random, time, math

# Extension #1
def inversion_count(new_state, size):
   ''' Depends on the size(width, N) of the puzzle, 
   we can decide if the puzzle is solvable or not by counting inversions.
   If N is odd, then puzzle instance is solvable if number of inversions is even in the input state.
   If N is even, puzzle instance is solvable if
      the blank is on an even row counting from the bottom (second-last, fourth-last, etc.) and number of inversions is odd.
      the blank is on an odd row counting from the bottom (last, third-last, fifth-last, etc.) and number of inversions is even.
   ''' 
   # Your code goes here
   return True

def getInitialState(sample):
   sample_list = list(sample)
   random.shuffle(sample_list)
   new_state = ''.join(sample_list)
   if(inversion_count(new_state, 4)): return new_state
   else: return None
   
def swap(s, i, j):
   # Your code goes here
   if i>=len(s) or j>=len(s) or j<0 or i<0:
       print("Index out of Bounds")
       exit
   if i>j:
       a = j
       b = i
   else:
       a = i
       b = j
   #print(str(len(s)) + " " + str(a) + " " + str(b))
   return s[:a] + s[b] + s[a+1:b] + s[a] + s[b+1:]
         
def generateChild(s, size):
   # Your code goes here
   i = s.find("_")
   #print(s)
   c = []
   for a in (-size, -1, 1, size):
       ss = size**2
       if i+a >= 0 and i+a < ss:
           #print("Gen child: " + str(i+a))
           if not(((a == -1) and (i%size == 0)) or ((a == 1) and (i%size == size-1))):
               c.append(swap(s, i, i + a))
   return c

def display_path(path_list, size):
   for n in range(size):
      for i in range(len(path_list)):
         print (path_list[i][n*size:(n+1)*size], end = " "*size)
      print ()
   print ("\nThe shortest path length is :", len(path_list))
   return ""

def dist_heuristic(start, table, size):
   # Your code goes here
   swaps = 0            #swap number away from goal
   #print(start)
   for c in start:
       if c=="_":
         continue
       i = start.index(c)
       col = i%size
       row = i//size
       ig = table[c]
       #ig = "_123456789ABCDEF".index(c)
       colg = ig%size
       rowg = ig//size
       swaps = swaps + abs(col - colg) + abs(row - rowg)       
   return swaps  

"""def path(curr, ex):
    p = []
    p.append(curr)
    while curr:
        p.append(ex[curr])
        curr = ex[curr]
    return p"""

def a_star(start, goal="_123456789ABCDEF", heuristic=dist_heuristic):
    node = 1
    #cur_time = time.time()
    frontier = []
    if start == goal: return []
    size = 4
    ###
    table = {x:i for i,x in enumerate(goal)}
    ###
    #ex = set()
    ex = dict()
    h = heuristic(start, table, size)
    frontier.append((h, start, [start]))
    i = 0 #index
    # Your code goes here
    #print ("Duration: ", (time.time() - cur_time))
    while len(frontier)>0:
        if frontier[i][0] > h:
            frontier[:i] = []
            frontier = sorted(frontier)
            #print("save time??")
            i = 0
        curr = frontier[i][1]
        #f = frontier.pop(0)
        #curr = f[1]
        h = frontier[i][0]
        p = frontier[i][2]
        i += 1
        #print(curr)
        plen = len(p)
        if curr in ex and ex[curr] < plen:                  #could add to frontier super late because of prev high heuristic but have shorter path
            continue
        ex[curr] = plen
        #ex.add(curr)
        for c in generateChild(curr, size):
            #print("Child: " + c)
            if c == goal:
                print(node)
                return p + [c]
            if c in ex and ex[c] < plen + 1:
                #print("continue")
                continue
            frontier.append((heuristic(c, table, size)+ len(p) + 1, c, p + [c]))
            node += 1
    return None

def main():
   # check PriorityQueue
   #if check_pq(): print ("PriorityQueue is good to go.")
   #else: print ("PriorityQueue is not ready.")

   # A star
   ''' This part is for extension
   initial_state = getInitialState("_123456789ABCDEF")
   while initial_state == None:
      initial_state = getInitialState("_123456789ABCDEF")
   '''
   initial_state = input("Type initial state: ")
   cur_time = time.time()
   path = (a_star(initial_state))
   if path != None: display_path(path, 4)
   else: print ("No Path Found.")
   print ("Duration: ", (time.time() - cur_time))

if __name__ == '__main__':
   main()

''' Sample output 1
PriorityQueue is good to go.

Initial State: 152349678_ABCDEF
1523    1523    1_23    _123    
4967    4_67    4567    4567    
8_AB    89AB    89AB    89AB    
CDEF    CDEF    CDEF    CDEF    

The shortest path length is : 4
Duration:  0.0

Sample output 2
PriorityQueue is good to go.

Initial State: 2_63514B897ACDEF
2_63    _263    5263    5263    5263    5263    5263    5263    5263    52_3    5_23    _523    1523    1523    1_23    _123    
514B    514B    _14B    1_4B    14_B    147B    147B    147_    14_7    1467    1467    1467    _467    4_67    4567    4567    
897A    897A    897A    897A    897A    89_A    89A_    89AB    89AB    89AB    89AB    89AB    89AB    89AB    89AB    89AB    
CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    

The shortest path length is : 16
Duration:  0.005984306335449219

Sample output 3
PriorityQueue is good to go.

Initial state: 8936C_24A71FDB5E
8936    8936    8936    893_    89_3    8943    8943    8_43    84_3    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    _423    4_23    4123    4123    4123    4123    _123    
C_24    C2_4    C24_    C246    C246    C2_6    C_26    C926    C926    C9_6    C916    C916    C916    C916    C916    C916    C916    C916    C916    _916    9_16    91_6    916_    9167    9167    9167    9167    9167    9167    _167    8167    8167    8_67    8567    8567    _567    4567    
A71F    A71F    A71F    A71F    A71F    A71F    A71F    A71F    A71F    A71F    A7_F    A_7F    AB7F    AB7F    AB7F    AB7_    AB_7    A_B7    _AB7    CAB7    CAB7    CAB7    CAB7    CAB_    CA_B    C_AB    C5AB    C5AB    _5AB    95AB    95AB    95AB    95AB    9_AB    _9AB    89AB    89AB    
DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    D_5E    D5_E    D5E_    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D_EF    _DEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    

The shortest path length is : 37
Duration:  0.34381628036499023
'''