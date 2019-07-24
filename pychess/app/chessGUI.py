#!/usr/bin/env python3
from flask import Flask, jsonify, make_response, render_template
from flask_restful import Api, Resource, reqparse
from pychess.app.ChessGame import *

game = ChessGame()
app = Flask(__name__)
api = Api(app)

@app.route("/")
def hello():
   return render_template("chess.html")

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
         Move.parser.add_argument("firstCoord", type=str)
         Move.parser.add_argument("secondCoord", type=str)
         Move.parser.add_argument("promotion", type=str)
         Move.parser.add_argument("algebra", type=str)
         Move.setupDone = True

   def get(self):
      self.setup()
      result = {}
      result['result'] = 'Success'
      result['firstTurn'] = game.getTurnString("first")
      result['lastTurn'] = game.getTurnString("last")
      result['turns'] = game.getTurnStringArray()
      return result

   def post(self):
      self.setup()
      result = {}
      args = Move.parser.parse_args()
      if args["method"] == "algebra":
         moveString = args["algebra"]
         if moveString == None:
            result['result'] = 'Failure'
            result['error'] = 'Missing algebraic move'
            return result
         if game.algebraicMove(moveString):
            result['result'] = 'Success'
            result['url'] = '/game/move/'+game.getTurnString("pending")
            return result
         else:
            game.cancelTurn()
            result['result'] = 'Failure'
            result['error'] = game.lastError
            return result
      else:
         firstCoord = args['firstCoord']
         if firstCoord == None:
            result['result'] = 'Failure'
            result['error'] = 'Missing first coordinate'
            return result
         secondCoord = args['secondCoord']
         if secondCoord == None:
            result['result'] = 'Failure'
            result['error'] = 'Missing second coordinate'
            return result
         promotion = args['promotion']
         if promotion == None:
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
            return result

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
            return result

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
            return result
      else:
         result['result'] = "Failure"
         result['error'] = "Move "+instance+" is not eligible for commit."
         return result


   def delete(self, instance):
      result = {}
      if self._checkForPendingTurn(instance):
         if game.cancelTurn():
            result['result'] = "Success"
            return result
         else:
            result['result'] = "Failure"
            result['error'] = "No new move available to cancel."
            return result
      else:
         result['result'] = "Failure"
         result['error'] = "Move "+instance+" is not eligible for deletion."
         return result

api.add_resource(MoveInstance, "/game/move/<instance>")

class Moves(Resource):
   def get(self):
      result = {}
      result['result'] = "Success"
      result['moves'] = game.getAllValidMoves()
      return result

api.add_resource(Moves, "/game/moves")


class MovesCoordinate(Resource):
   def get(self, coordinate):
      result = {}
      moves = game.getValidMovesForPieceAtPosition(coordinate)
      if(moves):
         result['result'] = "Success"
         result['moves'] = moves
      else:
         result['result'] = "Failure"
         result['error'] = "No piece at that coordinate to get moves from"
      return result


api.add_resource(MovesCoordinate, "/game/moves/<coordinate>")

class Tag(Resource):
   setupDone = False
   def setup(self):
      if not Tag.setupDone:
         Tag.parser = reqparse.RequestParser()
         Tag.parser.add_argument("tagName", type=str, required=True)
         Tag.parser.add_argument("tagValue", type=str, required=True)
         Tag.setupDone = True
         
   def get(self):
      result = {}
      tags = []
      for tag in game.getTags():
         tags.append({tag[0]: tag[1]})
      result['tags'] = tags
      result['result'] = "Success"
      return result
      
   def post(self):
      self.setup()
      result = {}
      args = Tag.parser.parse_args()
      game.setTag(args["tagName"], args["tagValue"])
      result["url"] = "/game/tag/"+args["tagName"]
      result['result'] = 'Success'
      return result
   
api.add_resource(Tag, "/game/tag")

class TagName(Resource):
   def get(self,tagName):
      result = {}
      result['tag'] = { tagName : game.getTag(tagName)[1] }
      result['result'] = "Success"
      return result

   def delete(self,tagName):
      result = {}
      game.deleteTag(tagName)
      result['result'] = "Success"
      return result
   
api.add_resource(TagName, "/game/tag/<tagName>")

class Games(Resource):
   def post(self):
      result = {}
      game.startNewGame()
      result['url'] = "/games/"+str(game.getCurrentGameIndex()+1);
      result['result'] = "Success"
      return result

   def get(self):
      result = {}
      headers = game.getGameHeaders()
      result['games'] = []
      for info in headers:
         gameInfo = {}
         gameInfo['url'] = '/games/'+str(int(info.index) + 1)
         gameInfo['Date'] = info.date.value
         gameInfo['White'] = info.white.value
         gameInfo['Black'] = info.black.value
         result['games'].append(gameInfo)
      result["currentGameIndex"] = int(game.getCurrentGameIndex())+1
      result['result'] = "Success"
      return result
      
   
   def delete(self):
      result = {}
      game.resetAllGames()
      result['result'] = "Success"
      return result

api.add_resource(Games, "/games")

class GamesIndex(Resource):
   currentString = "currentGameIndex"

   def put(self,gameIndex):
      result = {}
      if gameIndex != self.currentString:
         if game.selectGame(int(gameIndex)-1):
            if not game.readMovesFromCurrentGame():
               result['result'] = "Failure"
               result['error'] = "Error encountered while loading moves from game"
               return result
            result['result'] = "Success"
            return result
         else:
            result['result'] = "Failure"
            result['error'] = "That game does not exist."
            return result
      else:
         result['result'] = "Failure"
         result['error'] = "Operation not permitted on that URL"
         return result
         
   def get(self, gameIndex):
      result = {}
      if gameIndex == self.currentString:
         result[self.currentString] = int(game.getCurrentGameIndex())+1
         result['result'] = "Success"
         return result
      else:
         result['result'] = "Failure"
         result['error'] = "Operation not permitted on that URL"
         return result
         
api.add_resource(GamesIndex, "/games/<gameIndex>")
      
class Load(Resource):
   setupDone = False
   def setup(self):
      if not Load.setupDone:
         Load.parser = reqparse.RequestParser()
         Load.parser.add_argument("fileName", type=str)
         Load.setupDone = True

   def put(self):
      self.setup()
      result = {}
      args = Load.parser.parse_args()
      fileName = args['fileName']
      if fileName == None:
         loadSuccess = game.loadSaveFile()
      else:
         loadSuccess = game.loadSaveFile(fileName)

      if loadSuccess:
         result['result'] = "Success"
         return result
      else:
         result['result'] = "Failure"
         result['error'] = game.lastError
         return result

api.add_resource(Load, "/load")

class Save(Resource):
   setupDone = False
   def setup(self):
      if not Save.setupDone:
         Save.parser = reqparse.RequestParser()
         Save.parser.add_argument("fileName", type=str)
         Save.setupDone = True

   def put(self):
      self.setup()
      result = {}
      args = Save.parser.parse_args()
      fileName = args['fileName']
      if fileName == None:
         saveSuccess = game.writeSaveFile()
      else:
         saveSuccess = game.writeSaveFile(fileName)

      if saveSuccess:
         result['result'] = "Success"
         return result
      else:
         result['result'] = "Failure"
         result['error'] = game.lastError
         return result

api.add_resource(Save, "/save")

"""Set or read configuration options. The first argument must be one of the following settings:
import    (read/set default import file)
export    (read/set default export file)
name      (read/set the players real name)
location  (read/set the physical location of the player)
strict    (read/set strict algebraic parsing mode, if True only exactly formed algebraic notation is accepted)
files     (read/set path to the location of save games and configuration
random    (read/set whether we have random peices when starting a new game
threshold (read/set allowed piece value variance between players in random mode"""

class Config(Resource):
   def get(self):
      result = {}
      result['result'] = "Success"
      result['config'] = game.getAllConfigItems()
      return result

api.add_resource(Config, "/config")

class ConfigItem(Resource):
   setupDone = False
   def setup(self):
      if not ConfigItem.setupDone:
         ConfigItem.parser = reqparse.RequestParser()
         ConfigItem.parser.add_argument("value", required=True, type=str)
         ConfigItem.setupDone = True

   def get(self, item):
      result = {}
      configValue = game.getConfigItem(item)
      if configValue != None:
         result['result'] = "Success"
         result['value'] = configValue
         return result
      else:
         result['result'] = "Failure"
         result['error'] = game.lastError
         return result


   def put(self, item):
      result = {}
      self.setup()
      args = ConfigItem.parser.parse_args()
      value = args["value"]
      if not game.setConfigItem(item, value):
         result['result'] = "Failure"
         result['error'] = game.lastError
         return result
      else:
         result['result'] = "Success"
         return result

api.add_resource(ConfigItem, "/config/<item>")

if __name__ == "__main__":
    app.run(debug=True)
