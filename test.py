#!/usr/bin/python
from colorama import init
from Board import *
from Player import *

def moveAndPrint(board, white, black, start, end, cancel = False):
   print("")
   nextMove = board.getTurnString("pending")
   currentPlayer = None
   if "..." in nextMove:
      currentPlayer = black
   else:
      currentPlayer = white
   if currentPlayer.move(start, end):
      board.setTurn(white, black)
      if not cancel:
         board.commitTurn()
         print(board)
      else:
         print(board.getPendingMoveString())
         board.cancelCommit()
         currentPlayer.undoLastMove()
         print(board)

   else:
      print(currentPlayer.moveResultReason)
      
def algebraicMoveAndPrint(board, white, black, move, cancel = False):
   print("")
   nextMove = board.getTurnString("pending")
   currentPlayer = None
   if "..." in nextMove:
      currentPlayer = black
   else:
      currentPlayer = white
   if currentPlayer.algebraicMove(move):
      board.setTurn(white, black)
      if not cancel:
         board.commitTurn()
         print(board)
      else:
         print(board.getPendingMoveString())
         board.cancelCommit()
         currentPlayer.undoLastMove()
         print(board)

   else:
      print(currentPlayer.moveResultReason)

init()

white = WhitePlayer()
black = BlackPlayer()

white.otherPlayer = black
black.otherPlayer = white

b = GameBoard(white, black)
print(b)

moveAndPrint(b,white,black,"g1","f3")
moveAndPrint(b,white,black,"d7","d5")
moveAndPrint(b,white,black,"b1","c3")

moveAndPrint(b,white,black,"c8","g4",True)
moveAndPrint(b,white,black,"c8","e6")

moveAndPrint(b,white,black,"c3","d5")

moveAndPrint(b,white,black,"e6","d5",True)
moveAndPrint(b,white,black,"d8","d5")

moveAndPrint(b,white,black,"e2","e4")
moveAndPrint(b,white,black,"d5","e4")
algebraicMoveAndPrint(b, white, black , "c4")



white1 = WhitePlayer()
black1 = BlackPlayer()

white1.otherPlayer = black1
black1.otherPlayer = white1

del white1.pawns[:]
del white1.knights[:]
del white1.bishops[:]
del white1.queens[:]
white1.rooks[0].position = "g7"
white1.rooks[0].moved = True
white1.rooks[1].position = "b5"
white1.rooks[1].moved = True

del black1.pawns[:]
del black1.knights[:]
del black1.bishops[:]
del black1.queens[:]
del black1.rooks[:]

b1 = GameBoard(white1, black1)
print(b1)

moveAndPrint(b1,white1,black1,"b5","b8")
#moveAndPrint(b1,white1,black1,"b5","b7")
#moveAndPrint(b1,white1,black1,"e8","f7")
#moveAndPrint(b1,white1,black1,"e8","d8")
#moveAndPrint(b1,white1,black1,"b7","b8")
moveAndPrint(b1,white1,black1,"e8","f7")





white2 = WhitePlayer()
black2 = BlackPlayer()

white2.otherPlayer = black2
black2.otherPlayer = white2


del white2.knights[:]
del white2.bishops[:]
del white2.queens[:]

del black2.knights[:]
del black2.bishops[:]
del black2.queens[:]


b2 = GameBoard(white2, black2)
print(b2)
algebraicMoveAndPrint(b2,white2,black2,"g4")
algebraicMoveAndPrint(b2,white2,black2,"g5")
algebraicMoveAndPrint(b2,white2,black2,"0-0")
algebraicMoveAndPrint(b2,white2,black2,"0-0-0", True)

"""
print("")
b.previousTurn()
print(b)

print("")
b.firstTurn()
print(b)

print("")
b.nextTurn()
print(b)

print("")
b.nextTurn()
print(b)

print("")
b.lastTurn()
print(b)
"""
