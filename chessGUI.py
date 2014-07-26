#!/usr/bin/env python
from flask import Flask
from ChessGame import *

game = ChessGame()
app = Flask(__name__)

@app.route("/")
def hello():
   return "Hello World!"

@app.route("/show/board")
def showBoard():
   """Display the current board"""
   output = ""
   output += "Board: "+str(game.getCurrentBoardDictionary())
   output += "White Captured: "+str(game.getCurrentCapturedStrings(Util.colors.WHITE))
   output += "White Status: "+str(game.getCurrentCheckMateStatus(Util.colors.WHITE))
   output += "Black Captured: "+str(game.getCurrentCapturedStrings(Util.colors.BLACK))
   output += "Black Status: "+str(game.getCurrentCheckMateStatus(Util.colors.BLACK))
   return output
   
@app.route("/show/board/pending")
def showPendingBoard():
   """Display the pending board"""
   return game.showPendingBoard()
   
@app.route("/turn/first")
def firstMove():
   """Go to the first move in the game"""
   game.firstMove()
   return "Success"
   
@app.route("/turn/last")
def lastMove():
   """Go to the last move in the game"""
   game.lastMove()
   return "Success"
   
@app.route("/turn/next")
def nextMove():
   """Go to the next move in the game"""
   game.nextMove()
   return "Success"
   
@app.route("/turn/previous")
def previousMove():
   """Go to the previous move in the game"""
   game.previousMove()
   return "Success"

@app.route("/turn/string/<turnString>")
def gotoTurn(turnString):
    game.gotoTurnString(turnString)
    return "Success"
   
@app.route("/restart")
def restart():
   """Restart our current game"""
   game.restartGame()
   return "Success"
   
@app.route("/commit")
def commitMove():
    game.commitTurn()
    return "Success"

@app.route("/cancel")
def cancelMove():
    game.cancelTurn()
    return "Success"

@app.route("/move/coord/<first>/<second>")
@app.route("/move/coord/<first>/<second>/<promotion>")
def coordMovePromotion(first,second,promotion=""):
   """Move a piece, this function takes two chess coordinates and a Piece letter to use for promotion, the first being the starting square of the piece to move and the second being the ending square of the move. In order to perform a castle move, move the king to the final position required for the castle."""
   if game.twoCoordMove(first,second,promotion):
      return "Success"
   else:
      game.cancelTurn()
      return game.lastError

@app.route("/move/algebra/<move>")
def algebraMove(move):
   """Move a piece, this function takes one move in algebraic notation."""
   if game.algebraicMove(move):
      return "Success"
   else:
      game.cancelTurn()
      return game.lastError
   
@app.route("/load")
@app.route("/load/<fileName>")
def load(fileName=""):
   """Read all moves from a file and apply them to the current game, if no argument is given use the default import file configured,
if one is given use the argument as a filename to read a savegame from."""
   if not game.loadSaveFile(fileName):
      return game.lastError
   else:
      return "Success"

@app.route("/save")
@app.route("/save/<fileName>")
def save(fileName=""):
   """Write the current game out to a file. This will erase the old savegame file. If no argument is given use the default export file configured,
if one is given use the argument as a filename to write the savegame to."""
   if not game.writeSaveFile(fileName):
      return game.lastError
   else:
      return "Success"
      
"""Set or read configuration options. The first argument must be one of the following settings:
import    (read/set default import file)
export    (read/set default export file)
name      (read/set the players real name)
location  (read/set the physical location of the player)
strict    (read/set strict algebraic parsing mode, if True only exactly formed algebraic notation is accepted)"""
@app.route("/config/<item>")
def getConfig(item):
   value = game.getConfigItem(item)
   if value != None:
      return value
   else:
      return game.lastError

@app.route("/config/<item>/<value>")
def setConfig(item, value):
   if not game.setConfigItem(item, value):
      return game.lastError
   else:
      return "Success"


if __name__ == "__main__":
    app.run(debug=True)
