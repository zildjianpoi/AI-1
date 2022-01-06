##Strategy - Zhejia Yang
import re, random, copy 

EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PLAYERS = {BLACK: 'Black', WHITE: 'White'}


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

   
   def setOtherPlayer(self, h):
      self.other = h
      
   def setChar(self, ch, board):
      self.ch = ch
      if ch == BLACK:
         self.opp = WHITE
      else:
         self.opp = BLACK
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

class Alphabeta(Player):
   def play(self, board, m):
      if not m:        #if no more moves, return
         return board
      board = self.alphabeta(m, board)  #=moves[index] = 65 or 34 etc
      pBoard(board)
      return board
   def alphabeta(self, m, board, DEPTH):
      choice = self.Max(m, board, DEPTH)[1]
      board = update(m[choice], self.ch, board, self.pos, self.other.pos)
      print("Possible moves:(down across) ", m.keys())
      print(choice)
      return board 
   def Max(self, m, board, level, DEPTH, a = float("-inf"), b = float('inf')):
      if level == 0 or (not m and not self.possMoves(board)):
         return self.eval(board, level)
      if len(m) <= 3 and level < DEPTH-1:
         level = level + 1
      for i in m:
         cc = copy.deepcopy(self)
         poss = update(m[i], cc.ch, board, cc.pos, cc.other.pos)
         minval = cc.Min(cc.other.possMoves(board),poss,level-1, DEPTH, a, b)
         if minval > a:
            a = minval
            if a > b:
               return a
            #a = max(a, v)
            if level == DEPTH:
               position = i
      if level == DEPTH:
         return(a, position)
      return a
         
   def Min(self, m, board, level, DEPTH, a, b):
      if level == 0 or (not m and not self.possMoves(board)):
         return self.eval(board, level)
      v = float("inf")
      if len(m) <= 3:
         level = level + 1
      for i in m:
         cc = copy.deepcopy(self)
         poss = update(m[i], cc.other.ch, board, cc.other.pos, cc.pos)
         v = min(v, cc.Max(cc.possMoves(board),poss,level-1, DEPTH, a, b))
      if v < a:
         return v
      b = min(b, v)
      return v
   
   def eval(self, board, level):
      
      myCoins = len(self.pos)
      oppCoins = len(self.other.pos)
      diffCoins = 10*(myCoins - oppCoins)/(myCoins + oppCoins)    ###
      if not level == 0:
         return diffCoins/10*37
      myMoves = len(self.possMoves(board))
      oppMoves = len(self.other.possMoves(board))
      diffMoves = 0
      if not myMoves + oppMoves == 0:
         diffMoves = 15*(myMoves - oppMoves)/(myMoves + oppMoves)    ###
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
         diffC = 17*(myC - oppC)/(myC + oppC)                        ###
      edges = {13,14,15,16, 31,41,51,61, 38,48,58,68, 83,84,85,86}
      mye = 0
      oppe = 0
      for i in edges:
         if board[i] == self.ch:
            mye+=1
         if board[i] == self.opp:
            oppe += 1
      diffe = 0
      if not mye+oppe == 0:
         diffe = (mye-oppe)/(mye+oppe)*5
      diffAc = 0
      #if not (myC == 0 and oppC == 0):
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
         diffC = -13*(myAc - oppAc)/(myAc + oppAc) 
   #unstable = not next to a wall and next to opp peice
   #stable = next to walls and not next to opp
      return diffCoins + diffMoves + diffC + diffAc + diffe

   



class Strategy():
   def best_strategy(self, board, player, best_move, still_running):
      depth = 3
      while(True):
         best_move.value = self.move(board, player, depth)
         depth += 1
         
   def move(self, board, player, depth):
      p1 = Alphabeta()
      p2 = Random()
      if player == BLACK:
         p1.setChar(BLACK, board)
         p2.setChar(WHITE, board)
      else:
         p1.setChar(BLACK, board)
         p2.setChar(WHITE, board)
      p1.setOtherPlayer(p2)
      p2.setOtherPlayer(p1)
      return p1.Max(p1.possMoves(board), board, depth, depth)[1]


     