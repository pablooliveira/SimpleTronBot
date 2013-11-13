#!/usr/bin/env python
#
# SimpleTronBot
# (C) 2010-2013 Pablo Oliveira
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import tron
import sys
import random
import time

SEPARATED = False
START_TIME = None
infinity = 2**31

class Elapsed(Exception):
  pass

def check_elapsed_time():
  """ raises Elapsed exception, when our alloted time is
      almost finished.
  """
  t = time.time()
  if (t-START_TIME) > 0.98:
    raise Elapsed()

def dist(ori,des):
  """ returns the manhattan distance between two points """
  a,b = ori
  c,d = des
  return (abs(a-c)+abs(b-d))

def are_connected(board,st,en):
  """ returns true if 'st' and 'en' are not separated by a wall,
      implemented with A*
  """
  closedset = set()
  openset = [st]
  g_score = {st : 0 }
  h_score = {st : dist(st,en)}
  f_score = {st : h_score[st]}

  def lowestf(x,y):
    if f_score[x] > f_score[y]:
      return -1
    elif f_score[x] == f_score[y]:
      return 0
    else: return 1

  def neighbor_nodes(board,x):
    for i in board.adjacent(x):
      if board[i] != tron.WALL:
        yield i

  while len(openset) > 0:
    openset.sort(lowestf)
    x = openset.pop()
    if x == en:
      return True
    closedset.add(x)
    for y in neighbor_nodes(board, x):
      if y in closedset: continue
      tentative_g_score = g_score[x] + 1
      if y not in openset:
        openset.append(y)
        tentative_is_better = True
      elif tentative_g_score < g_score[y]:
        tentative_is_better = True
      else:
        tentative_is_better = False

      if tentative_is_better == True:
        g_score[y] = tentative_g_score
        h_score[y] = dist(y, en)
        f_score[y] = g_score[y] + h_score[y]

  return False

def fill_from(board, me, maxi=200):
  """ a naive flood_fill algorithm, returns the reachable floor tiles
      from the 'me' position. We never look at more than 'maxi' tiles.
  """
  old = set()
  new = set()
  new.add(me)
  while len(new)>0 and len(old) < maxi:
    t = new.pop()
    old.add(t)
    for a in board.adjacent(t):
      if (not board.passable(a)) or (a in old):
        continue
      else:
        new.add(a)
  return old

def evaluate(board,player):
  """ Our minimax evaluation function """
  me_valid = len(board.moves(1))
  them_valid = len(board.moves(-1))
  players_adjacent = board.them() in board.adjacent(board.me())

  if (them_valid==0 or me_valid==0): # end game position
    if me_valid > 0:
      if players_adjacent:
        result = -11
      else:
        result = 100
    elif them_valid > 0:
      if players_adjacent:
        result = -11
      else:
        result = -100
    else:
      result = -11
  else: # not end game position
    if not are_connected(board,board.me(),board.them()):
      # when me and them are separated, favour positions where
      # I have more free space.
      mine = fill_from(board, board.me())
      theirs = fill_from(board, board.them())
      m = len(mine)
      t = len(theirs)
      result = 12+float(abs(m-t))/float(max(m,t))*86
      if t > m:
        result = -result
      # the result should be between -12..-99 when the opponent has more space
      # and between 12..99 when we have more space !
    else:
      result = 0

  return result*player

def order_by_closeness(board,to,moves):
  y,x = board.me()
  oy,ox = to
  dy = y-oy
  dx = x-ox

  def order(a,b):
   if dy > 0:
     if a == tron.SOUTH : return 1
     if b == tron.SOUTH : return -1
     if a == tron.NORTH : return -1
     if b == tron.NORTH : return 1
   if dy < 0:
     if a == tron.SOUTH : return -1
     if b == tron.SOUTH : return 1
     if a == tron.NORTH : return 1
     if b == tron.NORTH : return -1
   if dx > 0:
     if a == tron.EAST : return 1
     if b == tron.EAST : return -1
     if a == tron.WEST : return -1
     if b == tron.WEST : return 1
   if dx < 0:
     if a == tron.EAST : return 1
     if b == tron.EAST : return -1
     if a == tron.WEST : return -1
     if b == tron.WEST : return 1
   return 0

  moves.sort(order)

def alphabeta(node, depth, alpha, beta, player, best_first_move=None):
  # get the reasonable moves.
  moves = list(node.moves(player))

  # if there are no possible moves, evaluate the board.
  if (depth == 0) or (len(moves) == 0):
    alpha = evaluate(node,player)
    return alpha, None

  # order the moves by closeness to the enemy
  order_by_closeness(node, (node.height/2,node.width/2), moves)
  order_by_closeness(node, node.them(), moves)

  # if a best_first_move is provided put it first in the list
  # in hope of getting more alpha-beta cuts
  if best_first_move != None:
    moves.remove(best_first_move)
    moves = [best_first_move] + moves

  # prepare a default best_move
  best_move = moves[0] if len(moves) > 0 else None

  #print depth, [tron.NAMES[m] for m in moves]

  # explore each move
  for move in moves:

    check_elapsed_time()

    node.move_forth(move,player)
    val = -alphabeta(node, depth-1, -beta, -alpha, -player)[0]
    node.move_back(move,player)

    #print " "*(10-depth)+"(%d) %d %s"%(player,val,tron.NAMES[move])

    if val > alpha:
      # found a new best move
      best_move = move
      alpha = val
      if alpha >= beta:
        # alpha-beta cut
        return alpha, best_move

  # Consider suicide as an honorable alternative...
  val = -11*player
  if val > alpha:
    for d in tron.DIRECTIONS:
      if node[node.rel(d,node.origin(player))] == tron.ME \
          or node[node.rel(d,node.origin(player))] == tron.THEM :
          return val, d

  return alpha, best_move

def fill(board):
  pass

def which_move(board):
  global START_TIME
  START_TIME = time.time()
  move = None
  depth = 1
  try:
    if SEPARATED == False: # We are not separated from the opponent, minimax mode:
      while(True):
        # iterative deepening, until time is almost elapsed.
        alpha, move = alphabeta(board,depth,-infinity,+infinity,1,
                                  best_first_move=move)
        depth=depth+1
    else: # We go into fill mode
      move = fill(board)
  except Elapsed:
    if move != None:
      return move
    else:
      return tron.NORTH

def main():
  for board in tron.Board.generate():
    tron.move(which_move(board))

# Try to get some extra cycles
try:
   import psyco
   psyco.full()
except ImportError:
   pass

main()
