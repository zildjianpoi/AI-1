import re, random, copy, time
#"wbbw"
#Zhejia Yang
blank, black, white, edge = ".", "X", "O", "#"
#START = "###########........##........##........##...OX...##...XO...##........##........##........###########"
"""...........................OX......XO..........................."""
S = input("Starting Board? ").strip()
START = '#'*11
for i in range(8):
    START = START + S[i*8:(i+1) * 8] + '##'
START = START + '#'*9

def pBoard(board):
   for i in range(10):
      print(board[i*10:i*10+10])
      
def update(index, ch, board, slist, olist):
   #print(index)
   for i in index:
      board = board[:i] + ch + board[i+1:]
      slist.add(i)
      olist.discard(i)
   return board      
      
class Player:

   """def __init__(self, ch, board):
      self.ch = ch
      if ch == "X":
         self.opp = "O"
      else:
         self.opp = "X"
      self.pos = {a.start() for a in re.finditer(ch, board)}"""
   
   def setOtherPlayer(self, h):
      self.other = h
      
   def setChar(self, ch, board):
      self.ch = ch
      if ch == "X":
         self.opp = "O"
      else:
         self.opp = "X"
      self.pos = {a.start() for a in re.finditer(ch, board)}
      
   def possMoves(self, board):
      m = dict()
      for i in self.pos:
         adj = {x for x in {-11, -10, -9, -1, 1, 9, 10, 11} if board[x+i] == self.opp}
         for a in adj:
            ii = i
            line = set()
            while board[a+ii] == self.opp:
               line.add(ii+a)
               ii += a
            if board[ii+a] == ".":
               line.add(ii+a)
               m[ii+a] = m.get(ii+a, set())|line
      return m
      
   def play():
      print("Uninplemented")
      
class Human(Player):

   def play(self, board, m):
      print(m)
      op = 0         #player option #/index of place in 
      print('across, down')
      #moves = self.possMoves(board)
      if not m:        #if no more moves, return
         return board
      #m = moves
      moves = list(m.keys())
      for i in moves:       #avalible indexes
         print ([op], ' (', i%10, ', ', i//10, ') ')
         op += 1
      index = int(input("Which move? "))
      #print(moves[])
      board = update(m[moves[index]], self.ch, board, self.pos, self.other.pos)
      print()
      pBoard(board)
      return board
      
class Random(Player):

   def play(self, board, m):
      op = 0         #player option #/index of place in 
      print('across, down')
      #moves = self.possMoves(board)
      if not m:        #if no more moves, return
         return board
      #m = moves
      moves = list(m.keys())
      index = random.randint(0, len(moves)-1)
      print("Possible moves:(down across) ", moves)
      print(moves[index])
      board = update(m[moves[index]], self.ch, board, self.pos, self.other.pos)
      print()
      pBoard(board)
      return board
      
class Minimax(Player):
   
   global DEPTH
   DEPTH = 5
   
   def play(self, board, m):
      if not m:        #if no more moves, return
         return board
      board = self.minimax(m, board)  #=moves[index] = 65 or 34 etc
      pBoard(board)
      return board
   def minimax(self, m, board):
      #print("begin")
      choice = self.Max(m, board, DEPTH)[1]
      board = update(m[choice], self.ch, board, self.pos, self.other.pos)
      print("Possible moves:(down across) ", m.keys())
      print(choice)
      return board
   def Max(self, m, board, level):
      if level == 0 or (not m and not self.possMoves(board)):
         return self.eval(board, level)
      if len(m) <= 3 and level < DEPTH - 1:
         level = level + 1
      v = float("-inf")
      if not m:
         cc = copy.deepcopy(self)
         return cc.Min(cc.other.possMoves(board),board,level-1)
      for i in m:
         cc = copy.deepcopy(self)
         poss = update(m[i], cc.ch, board, cc.pos, cc.other.pos)
         minval = cc.Min(cc.other.possMoves(poss),poss,level-1)
         if minval > v:
            v = minval
            #print("value: ", v)
            if level == DEPTH:
               position = i
      if level == DEPTH and m:
         return(v, position)
      return v
         
   def Min(self, m, board, level):
      if level == 0 or (not m and not self.possMoves(board)):
         return self.eval(board, level)
      if len(m) <= 3:
         level = level + 1
      v = float("inf")
      if not m:
         cc = copy.deepcopy(self)
         return cc.Max(cc.possMoves(board),board,level-1)
      for i in m:
         cc = copy.deepcopy(self)
         poss = update(m[i], cc.other.ch, board, cc.other.pos, cc.pos)
         v = min(v, cc.Max(cc.possMoves(poss),poss,level-1))
      #print("value: ", v)
      return v

         
   def eval(self, board, level):
      
      myCoins = len(self.pos)
      oppCoins = len(self.other.pos)
      if myCoins + oppCoins <= 10:
         return random.random()*37
      diffCoins = 10*(myCoins - oppCoins)/(myCoins + oppCoins)    ###
      if not level == 0:
         return diffCoins/10*37
      myMoves = len(self.possMoves(board))
      oppMoves = len(self.other.possMoves(board))
      diffMoves = 0
      if not myMoves + oppMoves == 0:
         diffMoves = 12*(myMoves - oppMoves)/(myMoves + oppMoves)    ###
      corners = {11, 18, 81, 88}
      myC = 0
      oppC = 0
      for i in corners:
         if board[i] == self.ch:
            myC += 1
         if board[i] == self.opp:
            oppC += 1
      diffC = 0
      if not myC + oppC == 0:
         diffC = 15*(myC - oppC)/(myC + oppC)                        ###
      #edges = {13,14,15,16, 31,41,51,61, 38,48,58,68, 83,84,85,86}
      diffAc = 0
      if not (myC == 0 and oppC == 0):
         cornerAdj = {11:{12, 21, 22}, 18:{17, 27, 28}, 81:{71, 72, 82}, 88:{78, 77, 87}}
         myAc = 0
         oppAc = 0
         for i in cornerAdj:
            if board[i] == self.ch:
               for j in cornerAdj[i]:
                  if board[j] == self.opp:
                     oppAc += 1
            elif board[i] == self.opp:
               for j in cornerAdj[i]:
                  if board[j] == self.ch:
                     myAc += 1
            else:
               for j in cornerAdj[i]:
                  if board[j] == self.ch:
                     myAc += 1
                  if board[j] == self.opp:
                     oppAc += 1
         if not myAc + oppAc == 0:
            diffC = -10*(myAc - oppAc)/(myAc + oppAc) 
      #unstable = not next to a wall and next to opp peice
      #stable = next to walls and not next to opp
      return diffCoins + diffMoves + diffC + diffAc
      
class Alphabeta(Minimax):
   DEPTH = 7
   def play(self, board, m):
      if not m:        #if no more moves, return
         return board
      board = self.alphabeta(m, board)  #=moves[index] = 65 or 34 etc
      pBoard(board)
      return board
   def alphabeta(self, m, board):
      choice = self.Max(m, board, DEPTH)[1]
      board = update(m[choice], self.ch, board, self.pos, self.other.pos)
      print("Possible moves:(down across) ", m.keys())
      print(choice)
      return board 
   def Max(self, m, board, level, a = float("-inf"), b = float('inf')):
      if level == 0 or (not m and not self.possMoves(board)):
         return self.eval(board, level)
      if len(m) <= 3 and level < DEPTH-1:
         level = level + 1
      if not m:
         cc = copy.deepcopy(self)
         return cc.Min(cc.other.possMoves(board),board,level-1, a, b)
      for i in m:
         cc = copy.deepcopy(self)
         poss = update(m[i], cc.ch, board, cc.pos, cc.other.pos)
         minval = cc.Min(cc.other.possMoves(poss),poss,level-1, a, b)
         if minval > a:
            a = minval
            if level == DEPTH:
               position = i
         if a > b:
            return a
            #a = max(a, v)
            
      if level == DEPTH and m:
         return(a, position)
      return a
         
   def Min(self, m, board, level, a, b):
      if level == 0 or (not m and not self.possMoves(board)):
         return self.eval(board, level)
      v = float("inf")
      if len(m) <= 3:
         level = level + 1
      if not m:
         cc = copy.deepcopy(self)
         return cc.Max(cc.possMoves(board),board,level-1, a, b)
      for i in m:
         cc = copy.deepcopy(self)
         poss = update(m[i], cc.other.ch, board, cc.other.pos, cc.pos)
         v = min(v, cc.Max(cc.possMoves(poss),poss,level-1, a, b))
         if v < a:
            return v
         b = min(b, v)
      return v

      
   
         

def countWinner(p1, p2, board):
   l1 = len(p1.pos)
   l2 = len(p2.pos)
   print("P1: ", l1, " vs P2: ", l2)
   #print(p1.pos, " ", p2.pos)
   if l1 == l2:
      print("Tie")
   elif l1>l2:
      print("Player 1 Wins")
   else:
      print("Player 2 Wins")  
         
pBoard(START)
print()
switch = {1:Random(), 2:Human(), 3:Minimax(), 4:Alphabeta()}
aa = int(input("Player One is: Random-1, Human-2, Minimax-3, Alphabeta-4 ").strip())
bb = int(input("Player Two? (same choices) ").strip())
player1 = switch[aa]
player2 = switch[bb]
player1.setChar("X", START)
player2.setChar("O", START)
player1.setOtherPlayer(player2)
player2.setOtherPlayer(player1)
board = START
starttime = time.time()
while True:
   p1 = player1.possMoves(board)

   p2 = player2.possMoves(board)
   if not(p1 or p2):
      countWinner(player1, player2, board)
      break
   print("Player 1's turn")
   board = player1.play(board, p1)
   print('Player 2\'s turn')
   p2 = player2.possMoves(board)
   board = player2.play(board, p2)
   
print(time.time()-starttime)

