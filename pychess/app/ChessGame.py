#!/usr/bin/env python3
from pychess.app.Board import *
from pychess.app.Player import *
from pychess.app.ChessFile import *
from pychess.test.TestPyChess import *
from pychess.app import Piece, Util
from pychess.app.fen import FEN
import os

VERSION = "1.6.0"

class ChessGame(object):
   files = ChessFiles()
   fen = FEN()
   lastError = ""

   def __init__(self):
      self.resetAllGames()

   def getLastError(self):
      return self.lastError

   def showCurrentBoard(self):
      return str(self.gameBoard)

   def getCurrentBoardDictionary(self):
       return self.gameBoard.getBoardDictionary()

   def getCurrentCapturedStrings(self,color):
       return self.gameBoard.getColorCapturedStrings(color)

   def getCurrentCheckMateStatus(self,color):
       return self.gameBoard.getColorCheckMateStatus(color)

   def showPendingBoard(self):
      return self.gameBoard.getPendingMoveString()

   def firstMove(self):
      return self.gameBoard.firstTurn()

   def lastMove(self):
      return self.gameBoard.lastTurn()

   def nextMove(self):
      return self.gameBoard.nextTurn()

   def previousMove(self):
      return self.gameBoard.previousTurn()

   def gotoTurnString(self,turnString):
      return self.gameBoard.gotoTurnString(turnString)

   def restartGame(self):
      self.files.resetCurrentGame()
      self.resetGameRepresentation()

   def resetAllGames(self):
      self.files.resetPgnFile()
      self.resetGameRepresentation()

   def resetGameRepresentation(self):
      self.files.resetCurrentGameMoves()
      self.fen.reset()

      self.setupRandomGame()

      fenString = FEN.STANDARD_OPENING
      #Returned tags are tuples of (name, value)
      fenTag = self.getTag("FEN")[1]
      if self.getTag("SetUp")[1] == "1" and fenTag != "":
         #We should use the given FEN for initial setup
         fenString = fenTag
      if not self.fen.parse(fenString):
         self.fen.reset()
         self.fen.parse(FEN.STANDARD_OPENING)

      self.whitePlayer = WhitePlayer(self.fen)
      self.blackPlayer = BlackPlayer(self.fen)
      self.whitePlayer.setOpponent(self.blackPlayer)
      self.blackPlayer.setOpponent(self.whitePlayer)
      self.gameBoard = GameBoard(self.whitePlayer, self.blackPlayer, self.fen)
      self.moveList = []
      
   def commitTurn(self):
      currentPlayer = self._getNextPlayer()
      if self.gameBoard.commitTurn():
         self.files.appendMoveForWrite(currentPlayer.lastMoveString)
         return True
      return False

   def cancelTurn(self):
      currentPlayer = self._getNextPlayer()
      if self.gameBoard.cancelCommit():
         self.moveList = self.moveList[:-1]
         currentPlayer.undoLastMove()
         return True
      return False

   def getTurnString(self, turn="current"):
      return self.gameBoard.getTurnString(turn)

   def getTurnStringArray(self):
      turnNum = self.gameBoard.initialSetup
      turnArray = [ { self.gameBoard.getTurnString(turnNum) : "Initial" } ]
      for move in self.moveList:
         turnNum += 1
         turnArray.append({self.gameBoard.getTurnString(turnNum) : move })
      return turnArray

   def twoCoordMove(self,firstCoord,secondCoord,promotionAbbreviation=None):
      """Move a piece, this function takes two chess coordinates and an optional Piece to use for promotion if necessary, the first being the starting square of the piece to move and the second being the ending square of the move.\n
         In order to perform a castle move, move the king to the final position required for the castle."""
      moves = [firstCoord, secondCoord]
      if promotionAbbreviation != None:
         if promotionAbbreviation not in Util.invPieces:
            self.lastError = "A valid piece abbreviation must be given for promotions."
            return False
         else:
            promotionAbbreviation = Util.invPieces[promotionAbbreviation]
      else:
         promotionAbbreviation = ""

      for move in moves:
         if not Util.isCoordValid(move):
            self.lastError = "Two valid chess coordinates must be given."
            return False

      currentPlayer = self._getNextPlayer()
      if currentPlayer.move(moves[0], moves[1], promotionAbbreviation):
         self.gameBoard.setTurn(self.whitePlayer, self.blackPlayer)
         self.moveList.append(currentPlayer.lastMoveString)
         return True
      else:
         self.lastError = "Move Failed:\n"+currentPlayer.moveResultReason
         return False

   def algebraicMove(self,move):
      """Move a piece, this function takes one move in algebraic notation."""
      currentPlayer = self._getNextPlayer()
      if currentPlayer.algebraicMove(move):
         if booleanConfigItemIsTrue(self._getConfigOption(ValidConfig.StrictParse)) and not currentPlayer.generatedAlgebraicMoveIsEqualToGiven():
            currentPlayer.undoLastMove()
            currentPlayer.moveResultReason = "Strict Parsing mode enabled. Input Algebraic move ("+move[0]+") is not the strict move ("+currentPlayer.lastMoveString+")"
         else:
            self.gameBoard.setTurn(self.whitePlayer, self.blackPlayer)
            self.moveList.append(currentPlayer.lastMoveString)
            return True
      self.lastError = "Move Failed:\n"+currentPlayer.moveResultReason
      return False
      
   def readMovesFromCurrentGame(self):
      """Apply all moves from the current game in the file."""
      allMoves = self.files.readMoves()
      self.resetGameRepresentation()
      for move in allMoves:
         if self.algebraicMove(move):
            self.commitTurn()
         else:
            self.resetGameRepresentation()
            return False
      return True

   def getAllValidMoves(self):
      """Returns the valid moves for all pieces on the board at the latest game state"""
      allMoves = {}
      for player in [self.whitePlayer, self.blackPlayer]:
         for piece in player.getAllPieces():
            allMoves[piece.position] = self.getValidMovesForPieceAtPosition(piece.position)
      return allMoves

   def getValidMovesForPieceAtPosition(self, coord):
      """Returns the valid moves for the piece at the coordinate, or None if there is no piece there"""
      moves = None
      for player in [self.whitePlayer, self.blackPlayer]:
         piece = player.getMyPieceAtLocation(coord)
         if piece:
            return [ piece.piece, player.getValidMovesForPiece(piece) ]
         else:
            continue

   def loadSaveFile(self,fileName=""):
      """Read all games from a file and store the game information, if no argument is given use the default import file configured,
if one is given use the argument as a filename to read a savegame from."""
      if fileName != "":
         importFileName = fileName
      else:
         importFileName = self._getConfigOption(ValidConfig.ImportFile)
      self.files.changeInputFile(importFileName)
      if self.files.inFileStatus != "Ready":
         self.lastError = "Cannot read from that file. Please try again."
         return False
      if self.files.readPgn():
         return True
      else:
         self.lastError = self.files.getPgnErrorString()
         return False

   def writeSaveFile(self,fileName=""):
      """Write the current pgn information out to a file. This will erase the old savegame file. If no argument is given use the default export file configured,
    if one is given use the argument as a filename to write the savegame to."""
      if fileName != "":
         exportFileName = fileName
      else:
         exportFileName = self._getConfigOption(ValidConfig.ExportFile)
      self.files.changeOutputFile(exportFileName)
      if self.files.outFileStatus != "Ready":
         self.lastError = "Cannot write to that file. Please try again."
         return False
      self.files.writeGame()
      return True
      
   def getGameHeaders(self):
      return self.files.getGameHeaders()
      
   def selectGame(self, game):
      return self.files.selectGame(game)
      
   def getCurrentGameIndex(self):
      return self.files.getCurrentGameIndex()
      
   def setTag(self, tagName, tagValue):
      self.files.setTag(tagName, tagValue)
      # Special case, reset if FEN applicability could have changed
      if tagName == "SetUp" or tagName == "FEN":
         self.resetGameRepresentation()

   def deleteTag(self, tagName):
      self.files.deleteTag(tagName)
      # Special case, reset if FEN applicability could have changed
      if tagName == "SetUp" or tagName == "FEN":
         self.resetGameRepresentation()
      
   def getTag(self, tagName):
      return self.files.getTag(tagName)
      
   def getTags(self):
      return self.files.getTags()

   def getAllConfigItems(self):
      config = {}
      for configItem in ValidConfig.configMap:
         config[configItem] = self._getConfigOption(ValidConfig.configMap[configItem])
      return config
      
   def startNewGame(self):
      self.files.startNewGame()
      self.restartGame()

   def setupRandomGame(self):
      # Generate random fen and set the appropriate tags, if we are configured to do so
      if self.getConfigItem("random") == "True":
         try:
            threshold = self.getConfigItem("threshold")
            if threshold == None:
               threshold = 5
            threshold = int(threshold)
         except ValueError:
            threshold = 5

         existingFen = self.getTag("FEN")[0]
         #Only reset with random FEN if we don't already have a FEN
         if existingFen != "":
            fen = FEN.generateRandomFEN(threshold)
            #Write these tags directly to the files object to avoid representation reset in our setTag function
            self.files.setTag("FEN", fen)
            self.files.setTag("SetUp", "1")


   def getConfigItem(self,configItem):
      """Read configuration options. The argument must be one of the following settings:
      import    (read/set default import file)
      export    (read/set default export file)
      name      (read/set the players real name)
      location  (read/set the physical location of the player)
      strict    (read/set strict algebraic parsing mode, if True only exactly formed algebraic notation is accepted)
   The current value of the setting is printed to the screen."""
      if configItem in ValidConfig.configMap:
         config = self._getConfigOption(ValidConfig.configMap[configItem])
         if config == "":
            self.lastError = "Option is not set, please set it."
            return None
         else:
            return config
      else:
         self.lastError = "Invalid setting provided"
         return None

   def setConfigItem(self,configItem,configValue):
      """Set configuration options. The first argument must be one of the following settings:
      import    (read/set default import file)
      export    (read/set default export file)
      name      (read/set the players real name)
      location  (read/set the physical location of the player)
      strict    (read/set strict algebraic parsing mode, if True only exactly formed algebraic notation is accepted)
   The second argument will be saved as the setting."""
      if configItem in ValidConfig.configMap:
         if not self._setConfigOption(ValidConfig.configMap[configItem],configValue):
            self.lastError = "Set Failed. Valid options are:" + str(ValidConfig.configMap[configItem]["values"])
            return False
      else:
         self.lastError = "Invalid setting provided"
         return False
      return True

   def runTests(self,verbose=False):
      """Run the unit tests that have been developed for pyChess"""
      if(verbose):
         unittest.main(verbosity=3, exit=False)
      else:
         unittest.main(exit=False)

   def enableDebug(self, debugEnabled):
      self.whitePlayer.enableDebug(debugEnabled)
      self.blackPlayer.enableDebug(debugEnabled)

   def setDebugFileName(self, debugFileName):
      self.whitePlayer.setDebugFileName(debugFileName)
      self.blackPlayer.setDebugFileName(debugFileName)

   def _getConfigOption(self, option):
      retVal = ""
      if option["name"] in ValidConfig.validConfigItems:
         retVal = self.files.getConfigItem(option["name"])
      return retVal

   def _setConfigOption(self, option, value):
      if option["name"] in ValidConfig.validConfigItems:
         if "values" in option and value not in option["values"]:
            return False
         #Make immediate changes
         #Do these first, if these fail, do not write to file
         if option["name"] == ValidConfig.Debug["name"]:
            self.enableDebug(booleanConfigItemIsTrue(value))
         elif option["name"] == ValidConfig.DebugFile["name"]:
            if value == ValidConfig.DebugFile["default"]:
               filename = value
            else:
               fileDir = os.path.abspath(self._getConfigOption(ValidConfig.FileDir))
               filename = os.path.join(fileDir, value)
            self.setDebugFileName(filename)
         #Write config option to file
         self.files.setConfigItem(option["name"], value)
         self.files.writeConfig()
         return True
      return False

   def _getNextPlayer(self):
      nextMove = self.gameBoard.getTurnString("pending")
      currentPlayer = None
      if "..." in nextMove:
         currentPlayer = self.blackPlayer
      else:
         currentPlayer = self.whitePlayer
      return currentPlayer
