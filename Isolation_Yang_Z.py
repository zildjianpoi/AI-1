import copy
import time
import io
from random import randint

# Name: Zhejia Yang    Date: 12/7/18

class OpenMoveEvalFn():
   """Evaluation function that outputs a 
    score equal to how many moves are open
    for AI player on the board minus
    the moves open for opponent player."""
   def score(self, game, maximizing_player_turn=True):
        # TODO: finish this function!
      ab = len(game.get_legal_moves_of_queen()) - len(game.get_opponent_moves())
      if maximizing_player_turn: #game.__active_player__ == game.__player_2__:
         return ab
      else:
         return -ab
        
      #return 0      
        

class CustomEvalFn():
   """Custom evaluation function that acts
    however you think it should. This is not
    required but highly encouraged if you
    want to build the best AI possible."""
   def score(self, game, maximizing_player_turn=True):
        # TODO: finish this function!
      return len(game.get_legal_moves_of_queen()) - 2*len(game.get_opponent_moves())
             
 

class Board:
   BLANK = 0
   NOT_MOVED = (-1, -1)
   __active_queen__= None
   __active_players_queen__= None                       
   __inactive_players_queen__= None
   
   def __init__(self, player_1, player_2, width=5, height=5):
      self.width=width
      self.height=height
      
      self.queen_1 = "queen1"
      self.queen_2 = "queen2"
      
      self.__board_state__ = [ [Board.BLANK for i in range(0, width)] for j in range(0, height)]
      self.__last_queen_move__ = {self.queen_1:Board.NOT_MOVED, self.queen_2:Board.NOT_MOVED}
      self.__queen_symbols__ = {Board.BLANK: Board.BLANK, self.queen_1:1, self.queen_2:2}     
      
      self.move_count = 0
      
      self.__queen_1__ = self.queen_1
      self.__queen_2__ = self.queen_2
      
      self.__player_1__ = player_1
      self.__player_2__ = player_2
      
      self.__active_player__ = player_1
      self.__inactive_player__ = player_2 
      
      self.__active_players_queen__= 1                    
      self.__inactive_players_queen__= 2 
       
   def get_queen_name(self, queen_num):
      if queen_num == 1:
         return self.queen_1
      elif queen_num == 2:
         return self.queen_2
      else:
         return None
   
   def get_state(self):
      return copy.deepcopy(self.__board_state__)
       
   def __apply_move__(self, move):
      row,col = move
      self.__last_queen_move__[self.__active_queen__] = move     
      self.__board_state__[row][col] = self.__queen_symbols__[self.__active_queen__]   
      
      #swap the players
      
      tmp = self.__active_player__
      self.__active_player__ = self.__inactive_player__
      self.__inactive_player__ = tmp
      
      #swaping the queens
      
      tmp = self.__active_players_queen__
      self.__active_players_queen__ = self.__inactive_players_queen__
      self.__inactive_players_queen__ = tmp
      
      self.move_count = self.move_count + 1

   def __apply_move_write__(self, move, __active_queen__):
      row,col = move
      self.__last_queen_move__[__active_queen__] = move     
      self.__board_state__[row][col] = self.__queen_symbols__[__active_queen__]   
      
      #swap the players
      
      tmp = self.__active_player__
      self.__active_player__ = self.__inactive_player__
      self.__inactive_player__ = tmp
      self.move_count = self.move_count + 1
       
   def copy(self):
      b = Board(self.__player_1__, self.__player_2__, width=self.width, height=self.height)
      for key, value in self.__last_queen_move__.items():
         b.__last_queen_move__[key] = value
      for key, value in self.__queen_symbols__.items():
         b.__queen_symbols__[key] = value
      b.move_count = self.move_count
      b.__active_player__ = self.__active_player__
      b.__inactive_player__ = self.__inactive_player__
      b.__active_queen__ = self.__active_queen__
      b.__active_players_queen__ = self.__active_players_queen__
      b.__inactive_players_queen__ = self.__inactive_players_queen__
      b.__board_state__ = self.get_state()
      return b
   
   def set_active_queen(self, queen):                       
      if(queen==1):
         self.__active_queen__=self.queen_1
      elif(queen==2):
         self.__active_queen__=self.queen_2

   def forecast_move(self, move, queen):    
      new_board = self.copy()
      new_board.set_active_queen(queen)
      new_board.__apply_move__(move)
      return new_board

   def get_active_player(self):
      return self.__active_player__

   def get_inactive_player(self):
      return self.__inactive_player__
   
   def get_active_players_queen(self):
      return self.__active_players_queen__
   
   def get_inactive_players_queen(self):
      return self.__inactive_players_queen__
      
   def get_active_queen(self):
      return self.__active_queen__

   def get_opponent_moves(self):                  
      #chnaged so that you get access to even the inactive players queens.
      return {self.__inactive_players_queen__:self.__get_moves__(self.__last_queen_move__[self.get_queen_name(self.__inactive_players_queen__)])}

   def get_legal_moves(self):
      #We have changed this. Now we have to place 4 queens on board in first 4 moves.
      
      move_by_q = self.__last_queen_move__[self.get_queen_name(self.__active_players_queen__)]
      return {self.__active_players_queen__:self.__get_moves__(move_by_q)}

   def get_legal_moves_of_queen(self):
      return self.__get_moves__(self.__last_queen_move__[self.get_queen_name(self.__active_players_queen__)])

   def __get_moves__(self, move):
      if move == self.NOT_MOVED:
         return self.get_first_moves()
      if self.move_count < 2:
         return self.get_first_moves()
   
      r, c = move
   
      directions = [ (-1, -1), (-1, 0), (-1, 1),
                     (0, -1),          (0,  1),
                     (1, -1), (1,  0), (1,  1)]
   
      fringe = [((r+dr,c+dc), (dr,dc)) for dr, dc in directions if self.move_is_legal(r+dr, c+dc)]
   
      valid_moves = []
   
      while fringe:
         move, delta = fringe.pop()
         
         r, c = move
         dr, dc = delta
      
         if self.move_is_legal(r,c):
            new_move = ((r+dr, c+dc), (dr,dc))
            fringe.append(new_move)
            valid_moves.append(move)
   
      return valid_moves

   def get_first_moves(self):
      return [ (i,j) for i in range(0,self.height) for j in range(0,self.width) if self.__board_state__[i][j] == Board.BLANK]

   def move_is_legal(self, row, col):
      return 0 <= row < self.height and \
            0 <= col < self.width  and \
             self.__board_state__[row][col] == Board.BLANK

   def get_player_locations(self, queen):                            
      return [ (i,j) for j in range(0, self.width) for i in range(0,self.height) if self.__board_state__[i][j] == self.__queen_symbols__[queen]]

   def print_board(self):
      p1_r, p1_c = self.__last_queen_move__[self.__queen_1__]
      p2_r, p2_c = self.__last_queen_move__[self.__queen_2__]
      b = self.__board_state__
      
      out = ''
   
      for i in range(0, len(b)):
         for j in range(0, len(b[i])):
            if not b[i][j]:
               out += '  '
            
            elif i == p1_r and j == p1_c:
               out += '11'
            elif i == p2_r and j == p2_c:
               out += '22'
            else:
               out += '--'
         
            out += ' | '
         out += '\n\r'
   
      return out

   def play_isolation(self, time_limit = 5000):
      #changed the time_limit
      
      move_history = []
      queen_history =[]
      mi=1
   
      while True:
         game_copy = self.copy()            
         move_start = time.time()
         time_left = time_limit - (time.time() - move_start)            
         curr_move = Board.NOT_MOVED
         #try:
         legal_player_moves=self.get_legal_moves()
         curr_move, queen = self.__active_player__.move(game_copy,legal_player_moves , time_left)  
         if queen == None:                
            return self.__inactive_player__, move_history,queen_history, "illegal move"                
         self.set_active_queen(queen)

         if curr_move is None:
            curr_move = Board.NOT_MOVED
             
         if self.__active_player__ == self.__player_1__:
            move_history.append([curr_move])
            queen_history.append([self.__active_queen__])
         else:
            move_history[-1].append(curr_move)
            queen_history[-1].append(self.__active_queen__)
             
         if time_left <= 0:                
            return  self.__inactive_player__, move_history,queen_history, "timeout"
         
         legal_moves_of_queen =  self.get_legal_moves_of_queen()
         
         if self.__active_players_queen__ == queen and curr_move not in legal_moves_of_queen:
            return self.__inactive_player__, move_history,queen_history, "illegal move"
         
         if curr_move not in legal_moves_of_queen and curr_move not in legal_moves_of_queen:                
            return self.__inactive_player__, move_history,queen_history, "illegal move"
         
         self.__apply_move__(curr_move)


def game_as_text(winner, move_history, queen_history, termination="", board=Board(1,2)):
   print(winner)
   ans = io.StringIO()
   k=0
  
   for i, move1 in enumerate(move_history):
      p1_move = move1[0]
      ans.write(queen_history[k][0]+"  player1 "+"%d." % i + " (%d,%d)\r\n" % p1_move)
      if p1_move != Board.NOT_MOVED:
         board.__apply_move_write__(p1_move, queen_history[k][0])
      ans.write(board.print_board())
   
      if len(move1) > 1:
         p2_move = move1[1]
         ans.write(queen_history[k][1]+" player2 "+"%d. ..." % i + " (%d,%d)\r\n" % p2_move)
         if p2_move != Board.NOT_MOVED:
            board.__apply_move_write__(p2_move , queen_history[k][1])
         ans.write(board.print_board())
      k=k+1
   ans.write(termination + "\r\n")
   ans.write("Winner: " + winner.__name__ + "\r\n")

   return ans.getvalue()

class RandomPlayer():
    """Player that chooses a move randomly."""    
    __name__ = ""
    def move(self, game, legal_moves, time_left):
        if not legal_moves: return (-1,-1)        
        num = game.__active_players_queen__
        if not len(legal_moves[num]):
            num = game.__active_players_queen__
            if not len(legal_moves[num]):
                return (-1,-1),num
        
        moves=legal_moves[num][randint(0,len(legal_moves[num])-1)]
        return moves,num   
   
   
   
class CustomPlayer():
    # TODO: finish this class!
   """Player that chooses a move using 
    your evaluation function and 
    a depth-limited minimax algorithm 
    with alpha-beta pruning.
    You must finish and test this player
    to make sure it properly uses minimax
    and alpha-beta to return a good move
    in less than 5 seconds."""
    
   __name__ = ""
   def __init__(self,  search_depth=2, eval_fn=OpenMoveEvalFn()):
   #def __init__(self, search_depth=2, eval_fn=CustomEvalFn()):
   #def __init__(self, search_depth = 4, eval_fn=CustomEvalFn()):
        # if you find yourself with a superior eval function, update the
        # default value of `eval_fn` to `CustomEvalFn()`
      self.eval_fn = eval_fn
      self.search_depth = search_depth
   
   def utility(self, game):
      """TODO: Update this function to calculate the utility of a game state"""
      return OpenMoveEvalFn().score(game)
   
   def minimax(self, game, time_left, depth=5, maximizing_player=True):
        # TODO: finish this function!
      #best_val = 0
      #best_move = None
      #best_queen = None
      #print(game)
      #print(game.print_board())
      #print('---')
      #print(depth)
      if depth == 0:
         #print('done')
         #print (self.utility(game))
         return [self.utility(game)]
      if game.get_active_player() == game.__player_2__:
         #print('in')
         v = (float('-inf'), None, None)
         for c in game.get_legal_moves_of_queen():
            #print('---', c)
            #print("---1",game.forecast_move(c, game.get_active_players_queen()))
            recur = (self.minimax(game.forecast_move(c, game.get_active_players_queen()), time_left, depth - 1)[0], c, game.get_active_players_queen())
            #print(v)
            v = max(v, recur)
            #print('max', v)
      else:
         #print('in2')
         v = (float('inf'), None, None)
         for c in game.get_legal_moves_of_queen():
            #print('---2', game.forecast_move(c, game.get_active_players_queen()))
            recur = (self.minimax(game.forecast_move(c, game.get_active_players_queen()), time_left, depth - 1)[0], c, game.get_active_players_queen())
            v = min(v, recur)
            #print('min', v)
      #print(v)
      return v

      
   def alphabeta(self, game, time_left, depth=float("inf"), alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        # TODO: finish this function!
         return 0, None, None     
   
   def move(self, game, legal_moves, time_left):
         utility,best_move,best_queen= self.minimax(game,time_left, depth=self.search_depth)   
         #change minimax to alphabeta after completing alphabeta part of assignment 
         #best_move, best_queen, utility = self.alphabeta(game, time_left, depth=self.search_depth)
         #best_move = None
         #best_queen = None
         return best_move, best_queen
         
if __name__ == '__main__':

   print("Starting game:")
   k = 0
   r = 0
   for i in range(100):
      player_1 = RandomPlayer()
      player_2 = CustomPlayer()
      player_1.__name__ = "Ronith"
      player_2.__name__ = "Kaien"
      
      board = Board(player_1, player_2)
      #print(board.print_board())
      #print('aaa')
      winner, move_history,queen_history, termination = board.play_isolation()
      print(winner.__name__)
      if winner.__name__ == "Kaien":
         k += 1
      else:
         r += 1
   #print (game_as_text(winner, move_history,queen_history, termination))
   print('k: ', k, ' ', 'r: ', r, ' %k = ', k/(r+k)*100)
