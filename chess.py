#!/usr/bin/python
from colorama import init
from Board import *
from Player import *
from ChessFile import *
import Coord
import cmd

"""This tries to make raw_input look like input for python 2.7
    it does obscure the 2.7 version of input, but I am not using it anyway"""
try:
    input = raw_input
except NameError:
    pass

class Chess(cmd.Cmd):
   files = ChessFiles()
   intro = "Welcome to pyChess. Type help or ? to list commands.\nWritten by Tim Myers -- Version 0.7\n"
   prompt = "pyChess# "
   whitePlayer = WhitePlayer()
   blackPlayer = BlackPlayer()
   whitePlayer.setOpponent(blackPlayer)
   blackPlayer.setOpponent(whitePlayer)
   gameBoard = GameBoard(whitePlayer, blackPlayer)
   
   def emptyline(self):
       return
   
   def do_show(self,arg):
      """Display the current board"""
      print(self.gameBoard)
      
   def do_first(self,arg):
      """Go to the first move in the game"""
      self.gameBoard.firstTurn()
      
   def do_last(self,arg):
      """Go to the last move in the game"""
      self.gameBoard.lastTurn()
      
   def do_next(self,arg):
      """Go to the next move in the game"""
      self.gameBoard.nextTurn()
      
   def do_previous(self,arg):
      """Go to the previous move in the game"""
      self.gameBoard.previousTurn()
      
   def do_restart(self,arg):
      """Restart our current game"""
      self.files.resetWriteString()
      self.whitePlayer = WhitePlayer()
      self.blackPlayer = BlackPlayer()
      self.whitePlayer.otherPlayer = self.blackPlayer
      self.blackPlayer.otherPlayer = self.whitePlayer
      self.gameBoard = GameBoard(self.whitePlayer, self.blackPlayer)
      
   def do_move(self,arg):
      """Move a piece, this function takes two chess coordinates, the first being the starting square of the piece to move and the second being the ending square of the move.\n
         Ex. move b2 b4\n"""
      moves = arg.split()
      if len(moves) != 2:
         print("Two coordinates are required.")
         return
      for move in moves:
         if not Coord.isCoordValid(move):
            print("Both arguments must be valid chess coordinates.")
            return
      currentPlayer = self._getNextPlayer()
      if currentPlayer.move(moves[0], moves[1]):
         self.gameBoard.setTurn(self.whitePlayer, self.blackPlayer)
         print(self.gameBoard.getPendingMoveString())
         if self._booleanPrompt("Are you sure this is the move you would like to make?"):
            self.gameBoard.commitTurn()
            self.files.appendMoveForWrite(currentPlayer.lastMoveString)
         else:
            self.gameBoard.cancelCommit()
            currentPlayer.undoLastMove()
      else:
         print("Move Failed:\n"+currentPlayer.moveResultReason)
         
   def do_algebra(self,arg):
      """Move a piece, this function takes one move in algebraic notation.\n
         Ex. algebra Nf3\n"""
      move = arg.split()
      if len(move) > 1:
         print("Only one argument is valid.")
         return
      currentPlayer = self._getNextPlayer()
      if currentPlayer.algebraicMove(move[0]):
         self.gameBoard.setTurn(self.whitePlayer, self.blackPlayer)
         print(self.gameBoard.getPendingMoveString())
         if self._booleanPrompt("Are you sure this is the move you would like to make?"):
            self.gameBoard.commitTurn()
            self.files.appendMoveForWrite(currentPlayer.lastMoveString)
         else:
            self.gameBoard.cancelCommit()
            currentPlayer.undoLastMove()
      else:
         print("Move Failed:\n"+currentPlayer.moveResultReason)
      
   def do_import(self,arg):
      """Read all moves from a file and apply them to the current game, if no argument is given use the default import file configured,
if one is given use the argument as a filename to read a savegame from."""
      numOfArgs = len(arg.split())
      if numOfArgs > 1:
         print("Too many arguments recieved")
         return
      elif numOfArgs == 1:
         importFileName = arg
      else:
         importFileName = self._getConfigOption(ValidConfig.ImportFile)
      self.files.changeInputFile(importFileName)
      if self.files.inFileStatus != "Ready":
         print("Cannot read from that file. Please try again.")
         return
      elif self._booleanPrompt("If any moves are invalid, this game will be reset. Continue?"):
         for move in self.files.readMoves():
            currentPlayer = self._getNextPlayer()
            if currentPlayer.algebraicMove(move):
               self.gameBoard.setTurn(self.whitePlayer, self.blackPlayer)
               self.gameBoard.commitTurn()
               self.files.appendMoveForWrite(currentPlayer.lastMoveString)
            else:
               print("Move:",move,"\nMove Failed:\n"+currentPlayer.moveResultReason)
               self.do_restart() 

   def do_export(self,arg):
      """Write the current game out to a file. This will erase the old export file. If no argument is given use the default export file configured,
if one is given use the argument as a filename to write the savegame to."""
      numOfArgs = len(arg.split())
      if numOfArgs > 1:
         print("Too many arguments recieved")
         return
      elif numOfArgs == 1:
         exportFileName = arg
      else:
         exportFileName = self._getConfigOption(ValidConfig.ExportFile)
      self.files.changeOutputFile(exportFileName)
      if self.files.outFileStatus != "Ready":
         print("Cannot write to that file. Please try again.")
      elif self._booleanPrompt("This will erase the contents of the the export file before writing. Continue?"):
         self.files.writeGame()
         
   def do_config(self,arg):
      """Set or read configuration options. The first argument must be one of the following settings:
      import    (read/set default import file)
      export    (read/set default export file)
      name      (read/set the players real name)
      location  (read/set the physical location of the player)
   If the second argument is given then the argument will be saved as the setting, if it is omitted then
   the current value of the setting is printed to the screen.""" 
      configMap = {"import":ValidConfig.ImportFile, "export":ValidConfig.ExportFile, \
                   "name":ValidConfig.PlayerName, "location":ValidConfig.Location}
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
               self._setConfigOption(configMap[args[0]],args[1])
         else:
            print("Invalid setting provided")

   def do_quit(self,arg):
      """Stop playing chess"""
      return True
   
   def help_help(self):
       print("Display the help for one of the available commands.")

   def _getConfigOption(self, option):
      retVal = ""
      if option in ValidConfig.validConfigItems:
         retVal = self.files.getConfigItem(option)
      return retVal

   def _setConfigOption(self, option, value):
      if option in ValidConfig.validConfigItems:
         self.files.setConfigItem(option, value)
         self.files.writeConfig()
      
   def _booleanPrompt(self, prompt):
      confirmation = input(prompt+" [y/n]:")
      if confirmation in ["y" , "Y" , "Yes" , "yes" , "YES"]:
         return True
      else:
         return False


   def _getNextPlayer(self):
      nextMove = self.gameBoard.getTurnString("pending")
      currentPlayer = None
      if "..." in nextMove:
         currentPlayer = self.blackPlayer
      else:
         currentPlayer = self.whitePlayer
      return currentPlayer
     

if __name__ == "__main__":
    init()
    Chess().cmdloop()
