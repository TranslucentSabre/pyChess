#!/usr/bin/env python
from flask import Flask, jsonify, make_response
from flask.ext.restful import Api, Resource, reqparse
from ChessGame import *

game = ChessGame()
app = Flask(__name__)
api = Api(app)

@app.route("/")
def hello():
   return "Hello World!"

class Game(Resource):
   def delete(self):
      game.restartGame()
      result = {}
      result['result'] = 'Success'
      return result, 204

api.add_resource(Game, "/game")

class Move(Resource):
   setupDone = False
   def setup(self):
      if not Move.setupDone:
         Move.parser = reqparse.RequestParser()
         Move.parser.add_argument("method", required=True, choices=("coordinate","algebra"))
         Move.parser.add_argument("firstCoord")
         Move.parser.add_argument("secondCoord")
         Move.parser.add_argument("promotion")
         Move.parser.add_argument("algebra", type=str)
         Move.setupDone = True

   def get(self):
      self.setup()
      result = {}
      result['result'] = 'Success'
      result['firstTurn'] = game.getTurnString("first")
      result['lastTurn'] = game.getTurnString("last")
      result['currentTurn'] = game.getTurnString()
      result['turns'] = game.getTurnStringToMoveDictionary()
      return result

   def post(self):
      self.setup()
      result = {}
      args = Move.parser.parse_args()
      if args["method"] == "algebra":
         try:
            moveString = args["algebra"]
         except KeyError:
            result['result'] = 'Failure'
            result['error'] = 'Missing algebraic move'
            return result, 400
         if game.algebraicMove(moveString):
            result['result'] = 'Success'
            return result
         else:
            game.cancelTurn()
            result['result'] = 'Failure'
            result['error'] = game.lastError
            return result, 400
      else:
         try:
            firstCoord = args['firstCoord']
         except KeyError:
            result['result'] = 'Failure'
            result['error'] = 'Missing first coordinate'
            return result, 400
         try:
            secondCoord = args['secondCoord']
         except KeyError:
            result['result'] = 'Failure'
            result['error'] = 'Missing second coordinate'
            return result, 400
         try:
            promotion = args['promotion']
         except KeyError:
            moveResult = game.twoCoordMove(firstCoord, secondCoord)
         else:
            moveResult = game.twoCoordMove(firstCoord, secondCoord, promotion)
         if moveResult:
            result['result'] = 'Success'
            return result
         else:
            game.cancelTurn()
            result['result'] = 'Failure'
            result['error'] = game.lastError
            return result, 400
            
api.add_resource(Move, "/game/move")


@app.route("/show/board")
def showBoard():
   """Display the current board"""
   return jsonify(board=game.getCurrentBoardDictionary(),
                  whiteCaptured=game.getCurrentCapturedStrings(Util.colors.WHITE),
                  whiteStatus=game.getCurrentCheckMateStatus(Util.colors.WHITE),
                  blackCaptured=game.getCurrentCapturedStrings(Util.colors.BLACK),
                  blackStatus=game.getCurrentCheckMateStatus(Util.colors.BLACK))
   
@app.route("/show/board/pending")
def showPendingBoard():
   """Display the pending board"""
   return game.showPendingBoard()
   
@app.route("/turn/first")
def firstMove():
   """Go to the first move in the game"""
   game.firstMove()
   return jsonify(result="Success")

@app.route("/turn/last")
def lastMove():
   """Go to the last move in the game"""
   game.lastMove()
   return jsonify(result="Success")
   
@app.route("/turn/next")
def nextMove():
   """Go to the next move in the game"""
   game.nextMove()
   return jsonify(result="Success")
   
@app.route("/turn/previous")
def previousMove():
   """Go to the previous move in the game"""
   game.previousMove()
   return jsonify(result="Success")

@app.route("/turn/string/<turnString>")
def gotoTurn(turnString):
    game.gotoTurnString(turnString)
    return jsonify(result="Success")
   
@app.route("/commit")
def commitMove():
    game.commitTurn()
    return jsonify(result="Success")

@app.route("/cancel")
def cancelMove():
    game.cancelTurn()
    return jsonify(result="Success")

@app.route("/load")
@app.route("/load/<fileName>")
def load(fileName=""):
   """Read all moves from a file and apply them to the current game, if no argument is given use the default import file configured,
if one is given use the argument as a filename to read a savegame from."""
   if not game.loadSaveFile(fileName):
      return jsonify(result="Error: "+game.lastError)
   else:
      return jsonify(result="Success")

@app.route("/save")
@app.route("/save/<fileName>")
def save(fileName=""):
   """Write the current game out to a file. This will erase the old savegame file. If no argument is given use the default export file configured,
if one is given use the argument as a filename to write the savegame to."""
   if not game.writeSaveFile(fileName):
      return jsonify(result="Error: "+game.lastError)
   else:
      return jsonify(result="Success")
      
"""Set or read configuration options. The first argument must be one of the following settings:
import    (read/set default import file)
export    (read/set default export file)
name      (read/set the players real name)
location  (read/set the physical location of the player)
strict    (read/set strict algebraic parsing mode, if True only exactly formed algebraic notation is accepted)"""
@app.route("/config/<item>")
def getConfig(item):
   configValue = game.getConfigItem(item)
   if configValue != None:
      return jsonify(value=configValue)
   else:
      return jsonify(result="Error: "+game.lastError)

@app.route("/config/<item>/<value>")
def setConfig(item, value):
   if not game.setConfigItem(item, value):
      return jsonify(result="Error: "+game.lastError)
   else:
      return jsonify(result="Success")


if __name__ == "__main__":
    app.run(debug=True)
