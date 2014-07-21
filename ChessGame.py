#!/usr/bin/env python
from Board import *
from Player import *
from ChessFile import *
from TestPyChess import *
import Piece
import Util


class ChessGame():
   files = ChessFiles()
   whitePlayer = WhitePlayer()
   blackPlayer = BlackPlayer()
   whitePlayer.setOpponent(blackPlayer)
   blackPlayer.setOpponent(whitePlayer)
   gameBoard = GameBoard(whitePlayer, blackPlayer)
   lastError = ""
   
   def getLastError(self):
      return self.lastError

   def showCurrentBoard(self):
      return str(self.gameBoard)

   def showPendingBoard(self):
      return self.gameBoard.getPendingMoveString()
      
   def firstMove(self):
      self.gameBoard.firstTurn()
      
   def lastMove(self):
      self.gameBoard.lastTurn()
      
   def nextMove(self):
      self.gameBoard.nextTurn()
      
   def previousMove(self):
      self.gameBoard.previousTurn()
      
   def restartGame(self):
      self.files.resetWriteString()
      self.whitePlayer = WhitePlayer()
      self.blackPlayer = BlackPlayer()
      self.whitePlayer.otherPlayer = self.blackPlayer
      self.blackPlayer.otherPlayer = self.whitePlayer
      self.gameBoard = GameBoard(self.whitePlayer, self.blackPlayer)

   def commitTurn(self):
      currentPlayer = self._getNextPlayer()
      self.gameBoard.commitTurn()
      self.files.appendMoveForWrite(currentPlayer.lastMoveString)

   def cancelTurn(self):
      currentPlayer = self._getNextPlayer()
      self.gameBoard.cancelCommit()
      currentPlayer.undoLastMove()
      
   def twoCoordMove(self,firstCoord,secondCoord,promotionAbbreviation=None):
      """Move a piece, this function takes two chess coordinates and an optional Piece to use for promotion if necessary, the first being the starting square of the piece to move and the second being the ending square of the move.\n
         In order to perform a castle move, move the king to the final position required for the castle."""
      moves = [firstCoord, secondCoord]
      if promotionAbbreviation != None and promotionAbbreviation not in Util.invPieces:
         self.lastError = "A valid piece abbreviation must be given for promotions."
         return False
      promotionAbbreviation = Util.invPieces[promotionAbbreviation]

      for move in moves:
         if not Util.isCoordValid(move):
            self.lastError = "Two valid chess coordinates must be given."
            return False

      currentPlayer = self._getNextPlayer()
      if currentPlayer.move(moves[0], moves[1], promotionAbbreviation):
         self.gameBoard.setTurn(self.whitePlayer, self.blackPlayer)
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
            return True
      self.lastError = "Move Failed:\n"+currentPlayer.moveResultReason
      return False
      
   def loadSaveFile(self,fileName=None):
      """Read all moves from a file and apply them to the current game, if no argument is given use the default import file configured,
if one is given use the argument as a filename to read a savegame from."""
      if fileName != None:
         importFileName = fileName
      else:
         importFileName = self._getConfigOption(ValidConfig.ImportFile)
      self.files.changeInputFile(importFileName)
      if self.files.inFileStatus != "Ready":
         self.lastError = "Cannot read from that file. Please try again."
         return False
      for move in self.files.readMoves():
         if not self.algebraicMove(move):
            self.do_restart() 
            return False
      return True

   def writeSaveFile(self,fileName=None):
      """Write the current game out to a file. This will erase the old savegame file. If no argument is given use the default export file configured,
    if one is given use the argument as a filename to write the savegame to."""
      if fileName != None:
         exportFileName = fileName
      else:
         exportFileName = self._getConfigOption(ValidConfig.ExportFile)
      self.files.changeOutputFile(exportFileName)
      if self.files.outFileStatus != "Ready":
         self.lastError = "Cannot write to that file. Please try again."
         return False
      self.files.writeGame()
      return True
         
   def do_config(self,arg):
      """Set or read configuration options. The first argument must be one of the following settings:
      import    (read/set default import file)
      export    (read/set default export file)
      name      (read/set the players real name)
      location  (read/set the physical location of the player)
      strict    (read/set strict algebraic parsing mode, if True only exactly formed algebraic notation is accepted)
   If the second argument is given then the argument will be saved as the setting, if it is omitted then
   the current value of the setting is printed to the screen.""" 
      configMap = {"import":ValidConfig.ImportFile, "export":ValidConfig.ExportFile, \
                   "name":ValidConfig.PlayerName, "location":ValidConfig.Location, \
                   "debug":ValidConfig.Debug, "strict":ValidConfig.StrictParse}
      #Only split once, this allows the user to supply items with spaces in them
      args = arg.split(None,1)
      numOfArgs = len(args)
      if numOfArgs == 0:
         print("You must specify a configuration item to set or read.")
      elif numOfArgs > 2:
         print("Too many aguments provided.")
      else:
         if args[0] in configMap:
            if numOfArgs == 1:
               config = self._getConfigOption(configMap[args[0]])
               if config == "":
                  print("Option is not set, please set it.")
               else:
                  print(config)
            else:
               args[1] = args[1].strip("\"")
               if not self._setConfigOption(configMap[args[0]],args[1]):
                  print("Set Failed. Valid options are:", configMap[args[0]]["values"])
         else:
            print("Invalid setting provided")
            
   def do_test(self,arg):
      """Run the unit tests that have been developed for pyChess"""
      if(arg == "-v" or arg == "--verbose"):
         unittest.main(verbosity=3, exit=False)
      else:
         unittest.main(exit=False)

   def _getConfigOption(self, option):
      retVal = ""
      if option["name"] in ValidConfig.validConfigItems:
         retVal = self.files.getConfigItem(option["name"])
      return retVal

   def _setConfigOption(self, option, value):
      if option["name"] in ValidConfig.validConfigItems:
         if "values" in option and value not in option["values"]:
            return False
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
     

