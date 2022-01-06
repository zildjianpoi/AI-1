# Name: Zhejia Yang       Date: 10/26/18
import heapq, random, pickle, math, time
from math import pi, acos , sin , cos

#class PriorityQueue():
"""Implementation of a priority queue 
to store nodes during search."""
# TODO: finish this class


'''Making class Graph(), Node(), and Edge() are optional'''
'''You can make any helper methods'''
         ##0         1           2                    3                    
###dlist [{coords}, {city code}, {(edges,stepcost)}, {empty heuristic}]
def make_graph(nodes_file, node_city_file, edge_file):
   dlist = [{} for i in range(4)]
   with open(nodes_file, "r") as nodes:
      for line in nodes:
         temp = line.strip().split()
         #print(temp)
         dlist[0][temp[0]] = (float(temp[1]), float(temp[2]))
   nodes.close()
   with open(node_city_file, "r") as city:
      for c in city:
         cc = c.strip().split()
         #print(cc)
         #print(" ".join(cc[1:]))
         dlist[1][cc[0]] = " ".join(cc[1:])          ##Number NOT int but STRING
         dlist[1][" ".join(cc[1:])] = cc[0]          ##City to number(as string)
   city.close()
   with open(edge_file, "r") as edges:
      for e in edges:
         #print("---" + e)
         ee = e.strip().split()
         #print(ee)
         dlist[2].setdefault(ee[0], {})            #Changed to Dictionaryyyy!!!
         dlist[2].setdefault(ee[1], {})
         pathcost = calc_edge_cost(ee[1], ee[0], dlist[0])
         dlist[2][ee[0]][ee[1]] = pathcost
         dlist[2][ee[1]][ee[0]] = pathcost
         #dlist[4][(ee[0], ee[1])]
         #dlist[4][(ee[0], ee[1])]
   #dlist[2][None] = (None,0)
   edges.close()
   #print(dlist[2]["0600316"])
   #print(dlist[1]["Los Angeles"])
   return dlist

def calc_edge_cost(start, end, graph):
   # TODO: calculate the edge cost from start city to end city
   #       by using the great circle distance formula.
   #       Refer the distanceDemo.py
   return calcd(graph[start][0], graph[start][1], graph[end][0], graph[end][1])
   
def calcd(y1,x1, y2,x2):
   #
   # y1 = lat1, x1 = long1
   # y2 = lat2, x2 = long2
   # all assumed to be in decimal degrees

   # if (and only if) the input is strings
   # use the following conversions

   """y1  = float(y1)
   x1  = float(x1)
   y2  = float(y2)
   x2  = float(x2)"""
   #
   R   = 3958.76 # miles = 6371 km
   #
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0
   #print((x1, y1, x2, y2))
   #
   # approximate great circle distance with law of cosines
   #
   return acos( min(1, sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1)) ) * R
   #
def path(curr, ex, cost, graph, s):
   #p = []
   if curr == s:
      #print(curr)
      print(cost)
      return []
   pp = path(ex[curr],ex,cost+graph[2][curr][ex[curr]], graph, s)
   pp.append(curr)
   #print(pp) 
   return pp

def breadth_first_search(start, goal, graph):
   # TODO: finish this method
   #       print the number of explored nodes somewhere
   n = 0
   if start == goal:
      return []
   ex = dict()
   s = graph[1][start]
   g = graph[1][goal]
   q = [s]
   i = 0
   while len(q) > i:
      curr = q[i]
      n += 1
      if i == 100:
         q[:100] = []
         i = 0
      i += 1
      if curr == g:
         ex[s] = None
         print("Nodes: " + str(n))
         #print(curr)
         return path(curr, ex, 0, graph, s)
      for child in graph[2][curr]:
         #print("Hewo??")
         c = child
         if c in ex:
            continue
         ex[c] = curr
         q.append(c)
               
   return []

def dist_heuristic(v, goal, graph):
   # TODO: calculate the heuristic value from node v to the goal
   return calc_edge_cost(v, goal, graph[0])
   #return 0
      
def a_star(start, goal, graph, heuristic=dist_heuristic):
   # TODO: Implement A* search algorithm
   #       print the number of explored nodes somewhere
   n = 1
   if start == goal:
      return []
   #cur_time = time.time()
   frontier = []
   s = graph[1][start]
   g = graph[1][goal]
   if s == g: return []
   ###
   #ex = set()
   ex = dict()
   h = heuristic(s, g, graph)
   frontier.append((h, s, [s], 0))
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
       n += 1
       #f = frontier.pop(0)
       #curr = f[1]
       h = frontier[i][0]
       p = frontier[i][2]
       #print(curr)
       #print(frontier[i])
       pathcost = frontier[i][3]
       i += 1
       if curr in ex and ex[curr] < pathcost:                  #could add to frontier super late because of prev high heuristic but have shorter path
           continue
       ex[curr] = pathcost
       #ex.add(curr)
       for c in graph[2][curr]:
           #print("Child: " + c)
           cost = graph[2][curr][c]
           if c == g:
               print("Nodes: " + str(n))
               print("pathcost: " + str(pathcost+cost))
               return p + [c]
           if c in ex and ex[c] < pathcost + cost:
               #print("continue")
               continue
           frontier.append((heuristic(c, g, graph)+ pathcost + cost, c, p + [c], pathcost+cost))
   return None
   #return []

def bidirectional_BFS(start, goal, graph):
   # TODO: Implement bi-directional BFS
   #       print the number of explored nodes somewhere
   n = 0
   if start == goal:
      return []
   ex = set()
   ex2 = dict()
   s = graph[1][start]
   g = graph[1][goal]
   q = [[s]]
   q2 = [[g]]
   i = 0
   ii = 0
   while len(q) > i:
      curr = q[i][-1]
      path1 = q[i]
      n += 1
      if i == 100:
         q[:100] = []
         i = 0
      i += 1
      if curr in ex2:
         #while q2[ii][-1] != curr:
            #ii += 1
         ex2[curr].reverse()
         #print(path2)
         path1 = path1 + ex2[curr][1:]
         #ex[s] = None
         print("Nodes: " + str(n))
         #print(curr)
         return path1
      for c in graph[2][curr]:
         #print("Hewo??")
         #c = child
         if c in ex:
            continue
         ex.add(c)
         q.append(path1+[c])
         
         
      curr = q2[ii][-1]
      path2 = q2[ii]
      n += 1
      if ii == 100:
         q2[:100] = []
         ii = 0
      ii += 1
      """if curr in ex2:
         while q2[ii][-1] != curr:
            ii += 1
         path2 = q2[ii].reverse()
         path1 = path1 + path2[1:]
         #ex[s] = None
         print(n)
         #print(curr)
         return path1"""
      for c in graph[2][curr]:
         #print("Hewo??")
         #c = child
         if c in ex2:
            continue
         ex2[c] = path2+[c]
         q2.append(ex2[c])
               
   return []
   
def bidirectional_a_star(start, goal, graph, tri, heuristic=dist_heuristic):
   # TODO: Implement bi-directional A*
   #       print the number of explored nodes somewhere
   n = 0
   if start == goal:
      return []
   ex = dict()             #cost
   ex2 = dict()            #(cost, path)
   s = graph[1][start]
   g = graph[1][goal]
   h = heuristic(s, g, graph)
   h2 = h
   q = [(h, [s], s, 0)]
   q2 = [(h2, [g], g, 0)]
   i = 0
   ii = 0 
   while len(q) > i:
      if q[i][0] > h:
         q[:i] = []
         q = sorted(q)
         i = 0
      curr = q[i][2]
      path1 = q[i][1]
      h = q[i][0]
      pathcost = q[i][-1]
      n += 1
      i += 1
      if curr in ex and ex[curr] < pathcost:
         continue
      ex[curr] = pathcost
      for c in graph[2][curr]:
         #print("Hewo??")
         #c = child
         cost = graph[2][curr][c]
         if c in ex and ex[c] < pathcost + cost:
               continue
         if curr in ex2:
            ex2[curr][-1].reverse()
            path1 = path1 + ex2[curr][-1]
            print("Nodes: " + str(n))
            #print(pathCost(path1, graph))
            if tri:
               return(path1, n)
            return path1
         q.append((heuristic(c, g, graph) + pathcost + cost, path1+[c], c, pathcost+cost))
         
         
      if q2[ii][0] > h2:
         q2[:ii] = []
         q2 = sorted(q2)
         ii = 0
      curr = q2[ii][2]
      path2 = q2[ii][1]
      h2 = q2[ii][0]
      pathcost = q2[ii][-1]
      n += 1
      ii += 1
      if curr in ex2 and ex2[curr][0] < pathcost:
         continue
      ex2[curr] = (pathcost, path2)
      for c in graph[2][curr]:
         #print("Hewo??")
         #c = child
         cost = graph[2][curr][c]
         if c in ex2 and ex2[c][0] < pathcost + cost:
               continue
         """if curr in ex2:
            ex2[curr][-1].reverse()
            path1 = path1 + ex2[curr][-1]
            print(n)
            return path1"""
         q2.append((heuristic(c, s, graph) + pathcost + cost, path2+[c], c, pathcost+cost))
               
   return []


def tridirectional_search(goals, graph, heuristic=0):          #wth is heuristic = 0???
   # TODO: Do this! Good luck!
   side01 = dist_heuristic(goals[0],goals[1],graph)
   side02 = dist_heuristic(goals[0],goals[2],graph)
   side12 = dist_heuristic(goals[2],goals[1],graph)
   m = max(side01, side02, side12)
   #print(goals)
   goals = [graph[1][c] for c in goals]
   #print(goals)
   if side01 == m:
      s = goals[0]
      e = goals[1]
      middle = goals[2]
   elif side02 == m:
      middle = goals[1]
      s = goals[0]
      e = goals[2]
   else:
      middle = goals[0]
      s = goals[1]
      e = goals[2]
   #print((s, middle, e))
   pathpt1 = bidirectional_a_star(s, middle, graph, True)
   pathpt2 = bidirectional_a_star(middle, e, graph, True)
   print("Nodes Tri-Dir: " + str(pathpt1[1] + pathpt2[1]))
   
   return pathpt1[0][:-2] + pathpt2[0]
   
def cities(ll, graph):
   city = []
   for c in ll:
      if c in graph[1]:
         city.append(graph[1][c])
   return city

def pathCost(ll, graph):
   pc = 0
   city = []
   for i in range(len(ll)-1):
      pc += calc_edge_cost(ll[i], ll[i+1], graph[0])
      if ll[i] in graph[1]:
         city.append(graph[1][ll[i]])
   if ll[-1] in graph[1]:
      city.append(graph[1][ll[-1]])
   print("Pathcost: ", pc)
   print("City Path", city)

def main():
   start = input("Start city: ")
   goal = input("Goal city: ")

   '''depends on your data setup, you can change this part'''
   graph = make_graph("rrNodes.txt", "rrNodeCity.txt", "rrEdges.txt")

   print ("\nBFS Summary")
   cur_time = time.time()
   bfs_path = breadth_first_search(start, goal, graph)
   next_time = time.time()
   print ("BFS path: ", bfs_path)
   print ("City Path: ", cities(bfs_path, graph))
   print ("BFS Duration: ", (next_time - cur_time))
   #print ("# of cities: " + str(len(bfs_path)))

   print ("\nA* Search Summary")
   cur_time = time.time()
   a_star_path = a_star(start, goal, graph)
   next_time = time.time()
   print ("A* path: ", a_star_path)
   print ("City Path: ", cities(a_star_path, graph))
   print ("A* Duration: ", (next_time - cur_time))
   #print ("# of cities: " + str(len(a_star_path)))

   print ("\nBi-directional BFS Summary")
   cur_time = time.time()
   bi_path = bidirectional_BFS(start, goal, graph)
   next_time = time.time()
   pathCost(bi_path, graph)
   print ("Bi-directional BFS path: ", bi_path)
   print ("Bi-directional BFS Duration: ", (next_time - cur_time))

   print ("\nBi-directional A* Summary")
   cur_time = time.time()
   bi_a_path = bidirectional_a_star(start, goal, graph, False)
   next_time = time.time()
   pathCost(bi_a_path, graph)
   print ("Bi-directional A* path: ", bi_a_path)
   print ("Bi-directional A* Duration: ", (next_time - cur_time))
   
   # TODO: check your tridirectional search algorithm here
   print ("\nTri-directional search Summary")
   goals = [graph[1][input("goal " + str(i) + ": ").strip()] for i in range(3)]
   #print(goals)
   cur_time = time.time()
   tri_path = tridirectional_search(goals, graph)
   next_time = time.time()
   pathCost(tri_path, graph)
   print ("Tri-directional search path: ", tri_path)
   print ("Tri-directional search Duration: ", (next_time - cur_time))
   
   
if __name__ == '__main__':
   main()

"""Sample Run
Start city: Los Angeles
Goal city: Chicago

BFS Summary
cost:  2093.868463307088
node path:  ['0600316', '0600089', '0600426', '0600087', '0600531', '0600760', '0600411', '0600027', '0600590', '0600023', '0600899', '0600900', '0600901', '0600902', '0600035', '0600321', '0600769', '0600436', '0600032', '0600414', '0600867', '0600866', '0600031', '0600033', '0600795', '0600602', '0600603', '0600036', '0600604', '0600871', '0600870', '0600872', '0600495', '0000144', '0400113', '0400114', '0400009', '0400010', '0400116', '0400117', '0400148', '0400074', '0400146', '0400147', '0400064', '0400005', '0400006', '0400063', '0400100', '0400075', '0400071', '0400070', '0400002', '0400050', '0000312', '3500036', '3500062', '3500063', '3500068', '3500069', '3500101', '3500111', '3500061', '3500109', '3500084', '3500089', '3500102', '3500065', '3500066', '3500032', '3500027', '3500119', '3500071', '3500070', '3500090', '3500107', '3500072', '3500013', '3500047', '3500039', '3500141', '3500025', '3500099', '0000257', '4801203', '4800003', '4801200', '4800002', '0000248', '4000264', '4000138', '4000231', '0000246', '2000206', '2000503', '2000360', '2000427', '2000500', '2000452', '2000207', '2000419', '2000501', '2000502', '2000073', '2000074', '2000075', '2000473', '2000519', '2000505', '2000291', '2000289', '2000290', '2000288', '2000292', '2000298', '2000087', '2000093', '2000094', '2000095', '2000096', '2000135', '2000280', '2000133', '2000342', '2000439', '2000358', '2000134', '2000121', '2000442', '2000441', '2000124', '2000125', '2000271', '2000127', '2000272', '2000237', '2000273', '2000353', '2000220', '0000541', '2900116', '2900283', '2900235', '2900198', '2900286', '2900241', '2900103', '2900482', '2900102', '2900545', '2900556', '2900111', '2900120', '2900122', '2900494', '2900355', '2900121', '2900162', '2900165', '2900566', '2900468', '2900164', '0000395', '1900057', '1900382', '1900070', '0000393', '1701225', '1700286', '1701010', '1701170', '1700285', '1701321', '1701322', '1700287', '1700296', '1701472', '1700303', '1700328', '1700926', '1700582', '1700310', '1700311', '1700312', '1700583', '1700313', '1701182', '1701345', '1700327', '1700432', '1701622', '1700449', '1700419', '1700465', '1700418', '1701034', '1701194', '1700417', '1700629', '1701394', '1700653', '1700631', '1700415', '1701267', '1701265', '1701291']
number of explored:  13268
BFS path:  ['Los Angeles', 'Chicago']
BFS Duration:  0.03057575225830078

A* Search Summary
cost:  2002.0784404122933
node path:  ['0600316', '0600427', '0600322', '0600751', '0600084', '0600685', '0600085', '0600080', '0600079', '0600686', '0600766', '0600402', '0600799', '0600408', '0600460', '0600588', '0600384', '0600688', '0600463', '0600435', '0600107', '0600775', '0600769', '0600436', '0600032', '0600414', '0600867', '0600866', '0600031', '0600033', '0600795', '0600602', '0600603', '0600036', '0600604', '0600871', '0600870', '0600872', '0600495', '0000144', '0400113', '0400114', '0400009', '0400010', '0400116', '0400117', '0400148', '0400074', '0400146', '0400147', '0400064', '0400005', '0400006', '0400063', '0400100', '0400075', '0400071', '0400070', '0400002', '0400050', '0000312', '3500036', '3500062', '3500063', '3500068', '3500069', '3500101', '3500111', '3500061', '3500109', '3500084', '3500089', '3500102', '3500065', '3500066', '3500032', '3500027', '3500119', '3500071', '3500070', '3500090', '3500107', '3500072', '3500013', '3500047', '3500039', '3500141', '3500025', '3500099', '0000257', '4801203', '4800003', '4801200', '4800002', '0000248', '4000264', '4000138', '4000231', '0000246', '2000206', '2000503', '2000360', '2000427', '2000500', '2000452', '2000207', '2000419', '2000501', '2000502', '2000073', '2000074', '2000075', '2000473', '2000519', '2000506', '2000294', '2000295', '2000296', '2000514', '2000523', '2000077', '2000292', '2000504', '2000293', '2000092', '2000311', '2000472', '2000470', '2000094', '2000095', '2000404', '2000097', '2000277', '2000102', '2000414', '2000103', '2000104', '2000106', '2000356', '2000114', '2000372', '2000117', '2000465', '2000466', '2000467', '2000270', '2000258', '2000257', '2000256', '2000260', '0000232', '2900371', '2900374', '2900378', '2900238', '2900184', '2900358', '2900343', '2900206', '2900095', '2900598', '2900476', '2900101', '2900212', '2900100', '2900106', '2900281', '2900210', '2900290', '2900291', '2900292', '2900207', '2900558', '2900416', '2900493', '2900253', '2900121', '2900162', '2900165', '2900566', '2900468', '2900164', '0000395', '1900057', '1900382', '1900070', '0000393', '1701225', '1700286', '1701010', '1701170', '1700285', '1701321', '1701325', '1701326', '1701323', '1700750', '1701328', '1701327', '1700292', '1700281', '1700280', '1701120', '1700301', '1700922', '1701121', '1700487', '1700480', '1700479', '1700478', '1700477', '1700430', '1700431', '1701157', '1700449', '1700419', '1700465', '1700418', '1701034', '1701194', '1700417', '1700629', '1701394', '1700653', '1700631', '1700415', '1701267', '1701265', '1701291']
number of explored:  1272
A* path:  ['Los Angeles', 'Chicago']
A* Duration:  0.036072492599487305

Bi-directional BFS Summary
cost:  2093.868463307088
node path:  ['0600316', '0600089', '0600426', '0600087', '0600531', '0600760', '0600411', '0600027', '0600590', '0600023', '0600899', '0600900', '0600901', '0600902', '0600035', '0600321', '0600769', '0600436', '0600032', '0600414', '0600867', '0600866', '0600031', '0600033', '0600795', '0600602', '0600603', '0600036', '0600604', '0600871', '0600870', '0600872', '0600495', '0000144', '0400113', '0400114', '0400009', '0400010', '0400116', '0400117', '0400148', '0400074', '0400146', '0400147', '0400064', '0400005', '0400006', '0400063', '0400100', '0400075', '0400071', '0400070', '0400002', '0400050', '0000312', '3500036', '3500062', '3500063', '3500068', '3500069', '3500101', '3500111', '3500061', '3500109', '3500084', '3500089', '3500102', '3500065', '3500066', '3500032', '3500027', '3500119', '3500071', '3500070', '3500090', '3500107', '3500072', '3500013', '3500047', '3500039', '3500141', '3500025', '3500099', '0000257', '4801203', '4800003', '4801200', '4800002', '0000248', '4000264', '4000138', '4000231', '0000246', '2000206', '2000503', '2000360', '2000427', '2000500', '2000452', '2000207', '2000419', '2000501', '2000502', '2000073', '2000074', '2000075', '2000473', '2000519', '2000505', '2000291', '2000289', '2000290', '2000288', '2000292', '2000298', '2000087', '2000093', '2000094', '2000095', '2000096', '2000135', '2000280', '2000133', '2000342', '2000439', '2000358', '2000134', '2000121', '2000442', '2000441', '2000124', '2000125', '2000271', '2000127', '2000272', '2000237', '2000273', '2000353', '2000220', '0000541', '2900116', '2900283', '2900235', '2900198', '2900286', '2900241', '2900103', '2900482', '2900102', '2900545', '2900556', '2900111', '2900120', '2900122', '2900494', '2900355', '2900121', '2900162', '2900165', '2900566', '2900468', '2900164', '0000395', '1900057', '1900382', '1900070', '0000393', '1701225', '1700286', '1701010', '1701170', '1700285', '1701321', '1701322', '1700287', '1700296', '1701472', '1700303', '1700328', '1700926', '1700582', '1700310', '1700311', '1700312', '1700583', '1700313', '1701182', '1701345', '1700327', '1700432', '1701622', '1700449', '1700419', '1700465', '1700418', '1701034', '1701194', '1700417', '1700629', '1701394', '1700653', '1700631', '1700415', '1701267', '1701265', '1701291']
number of explored:  ### Not Shown ###
Bi-directional BFS path:  ['Los Angeles', 'Chicago']
Bi-directional BFS Duration:  0.0

Bi-directional A* Summary
cost:  2002.0784404122933
node path:  ['0600316', '0600427', '0600322', '0600751', '0600084', '0600685', '0600085', '0600080', '0600079', '0600686', '0600766', '0600402', '0600799', '0600408', '0600460', '0600588', '0600384', '0600688', '0600463', '0600435', '0600107', '0600775', '0600769', '0600436', '0600032', '0600414', '0600867', '0600866', '0600031', '0600033', '0600795', '0600602', '0600603', '0600036', '0600604', '0600871', '0600870', '0600872', '0600495', '0000144', '0400113', '0400114', '0400009', '0400010', '0400116', '0400117', '0400148', '0400074', '0400146', '0400147', '0400064', '0400005', '0400006', '0400063', '0400100', '0400075', '0400071', '0400070', '0400002', '0400050', '0000312', '3500036', '3500062', '3500063', '3500068', '3500069', '3500101', '3500111', '3500061', '3500109', '3500084', '3500089', '3500102', '3500065', '3500066', '3500032', '3500027', '3500119', '3500071', '3500070', '3500090', '3500107', '3500072', '3500013', '3500047', '3500039', '3500141', '3500025', '3500099', '0000257', '4801203', '4800003', '4801200', '4800002', '0000248', '4000264', '4000138', '4000231', '0000246', '2000206', '2000503', '2000360', '2000427', '2000500', '2000452', '2000207', '2000419', '2000501', '2000502', '2000073', '2000074', '2000075', '2000473', '2000519', '2000506', '2000294', '2000295', '2000296', '2000514', '2000523', '2000077', '2000292', '2000504', '2000293', '2000092', '2000311', '2000472', '2000470', '2000094', '2000095', '2000404', '2000097', '2000277', '2000102', '2000414', '2000103', '2000104', '2000106', '2000356', '2000114', '2000372', '2000117', '2000465', '2000466', '2000467', '2000270', '2000258', '2000257', '2000256', '2000260', '0000232', '2900371', '2900374', '2900378', '2900238', '2900184', '2900358', '2900343', '2900206', '2900095', '2900598', '2900476', '2900101', '2900212', '2900100', '2900106', '2900281', '2900210', '2900290', '2900291', '2900292', '2900207', '2900558', '2900416', '2900493', '2900253', '2900121', '2900162', '2900165', '2900566', '2900468', '2900164', '0000395', '1900057', '1900382', '1900070', '0000393', '1701225', '1700286', '1701010', '1701170', '1700285', '1701321', '1701325', '1701326', '1701323', '1700750', '1701328', '1701327', '1700292', '1700281', '1700280', '1701120', '1700301', '1700922', '1701121', '1700487', '1700480', '1700479', '1700478', '1700477', '1700430', '1700431', '1701157', '1700449', '1700419', '1700465', '1700418', '1701034', '1701194', '1700417', '1700629', '1701394', '1700653', '1700631', '1700415', '1701267', '1701265', '1701291']
number of explored:  ### Not Shown ###
Bi-directional A* path:  ['Los Angeles', 'Tucson', 'Fort Worth', 'Chicago']
Bi-directional A* Duration:  0.0
"""


#Why both costs and Nodes explored different???