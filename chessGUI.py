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
            result['url'] = '/game/move/'+game.getTurnString("pending")
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
            result['url'] = '/game/move/'+game.getTurnString("pending")
            return result
         else:
            game.cancelTurn()
            result['result'] = 'Failure'
            result['error'] = game.lastError
            return result, 400
            
api.add_resource(Move, "/game/move")

class MoveInstance(Resource):
   def get(self, instance):
      result = {}
      if instance in ["first", "last"]: 
         if instance == "first":
            result['result'] = "Success"
            result['value'] = game.getTurnString("first")
            return result
         elif instance == "last":
            result['result'] = "Success"
            result['value'] = game.getTurnString("last")
            return result
      else:
         if game.gotoTurnString(instance):
            result['result'] = "Success"
            result['board'] = game.getCurrentBoardDictionary()
            result['whiteCaptured'] = game.getCurrentCapturedStrings(Util.colors.WHITE)
            result['whiteStatus'] = game.getCurrentCheckMateStatus(Util.colors.WHITE)
            result['blackCaptured'] = game.getCurrentCapturedStrings(Util.colors.BLACK)
            result['blackStatus'] = game.getCurrentCheckMateStatus(Util.colors.BLACK)
            return result
         else:
            result['result'] = "Failure"
            result['error'] = "No such move to get."
            return result, 400

   def _checkForPendingTurn(self, instance):
      return instance == game.getTurnString("pending")

   def put(self, instance):
      result = {}
      if self._checkForPendingTurn(instance):
         if game.commitTurn():
            result['result'] = "Success"
            return result
         else:
            result['result'] = "Failure"
            result['error'] = "No new move available to commit."
            return result, 400
      else:
         result['result'] = "Failure"
         result['error'] = "Move "+instance+" is not eligible for commit." 
         return result, 400


   def delete(self, instance):
      result = {}
      if self._checkForPendingTurn(instance):
         if game.cancelTurn():
            result['result'] = "Success"
            return result
         else:
            result['result'] = "Failure"
            result['error'] = "No new move available to cancel."
            return result, 400
      else:
         result['result'] = "Failure"
         result['error'] = "Move "+instance+" is not eligible for deletion." 
         return result, 400

api.add_resource(MoveInstance, "/game/move/<instance>")


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
