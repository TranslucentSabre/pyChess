#!/usr/bin/env python
from colorama import init
from ChessGame import *
import cmd

"""This tries to make raw_input look like input for python 2.7
    it does obscure the 2.7 version of input, but I am not using it anyway"""
try:
    input = raw_input
except NameError:
    pass

class Chess(cmd.Cmd):
   intro = "Welcome to pyChess. Type help or ? to list commands.\nWritten by Tim Myers -- Version 1.0.0\n"
   prompt = "pyChess# "
   game = ChessGame()
   
   def emptyline(self):
       return
   
   def do_show(self,arg):
      """Display the current board"""
      print(self.game.showCurrentBoard())
      
   def do_first(self,arg):
      """Go to the first move in the game"""
      self.game.firstMove()
      
   def do_last(self,arg):
      """Go to the last move in the game"""
      self.game.lastMove()
      
   def do_next(self,arg):
      """Go to the next move in the game"""
      self.game.nextMove()
      
   def do_previous(self,arg):
      """Go to the previous move in the game"""
      self.game.previousMove()
      
   def do_restart(self,arg):
      """Restart our current game"""
      self.game.restartGame()
      
   def do_move(self,arg):
      """Move a piece, this function takes two chess coordinates and an optional Piece to use for promotion if necessary, the first being the starting square of the piece to move and the second being the ending square of the move.\n
         In order to perform a castle move, move the king to the final position required for the castle.
         Ex. move b2 b4\n
             move e7 f8 Q\n
             move e8 c8"""
      moves = arg.split()
      if len(moves) < 2:
         print("Two coordinates are required.")
         return
      if len(moves) > 3:
         print("Only two coordinates and one promotion piece are accepted")
         return
      if len(moves) == 2:
          """Add the nonexistent promotion piece to the array"""
          moves.append(None)
      if self.game.twoCoordMove(moves[0], moves[1], moves[2]):
         print(self.game.showPendingBoard())
         if self._booleanPrompt("Are you sure this is the move you would like to make?"):
             self.game.commitTurn()
         else:
             self.game.cancelTurn()
      else:
         print(self.game.lastError)
         self.game.cancelTurn()
         
   def do_algebra(self,arg):
      """Move a piece, this function takes one move in algebraic notation.\n
         Ex. algebra Nf3\n
             algebra O-O\n"""
      move = arg.split()
      if len(move) > 1:
         print("Only one argument is valid.")
         return
      if self.game.algebraicMove(move[0]):
         print(self.game.showPendingBoard())
         if self._booleanPrompt("Are you sure this is the move you would like to make?"):
            self.game.commitTurn()
         else:
            self.game.cancelTurn()
      else:
         print(self.game.lastError)
         self.game.cancelTurn()
      
   def do_load(self,arg):
      """Read all moves from a file and apply them to the current game, if no argument is given use the default import file configured,
if one is given use the argument as a filename to read a savegame from."""
      if self._booleanPrompt("If any moves are invalid, this game will be reset. Continue?"):
         if not self.game.loadSaveFile(arg):
            print(self.game.lastError)

   def do_save(self,arg):
      """Write the current game out to a file. This will erase the old savegame file. If no argument is given use the default export file configured,
if one is given use the argument as a filename to write the savegame to."""
      if self._booleanPrompt("This will erase the contents of the the export file before writing. Continue?"):
         if not self.game.writeSaveFile():
            print(self.game.lastError)
         
   def do_config(self,arg):
      """Set or read configuration options. The first argument must be one of the following settings:
      import    (read/set default import file)
      export    (read/set default export file)
      name      (read/set the players real name)
      location  (read/set the physical location of the player)
      strict    (read/set strict algebraic parsing mode, if True only exactly formed algebraic notation is accepted)
   If the second argument is given then the argument will be saved as the setting, if it is omitted then
   the current value of the setting is printed to the screen.""" 
      #Only split once, this allows the user to supply items with spaces in them
      args = arg.split(None,1)
      numOfArgs = len(args)
      if numOfArgs == 0:
         print("You must specify a configuration item to set or read.")
      elif numOfArgs > 2:
         print("Too many aguments provided.")
      else:
         if numOfArgs == 1:
            value = self.game.getConfigItem(args[0])
            if value != None:
               print(value)
            else:
               print(self.game.lastError)
         else:
            if not self.game.setConfigItem(args[0], args[1]):
               print(self.game.lastError)
            
   def do_test(self,arg):
      """Run the unit tests that have been developed for pyChess"""
      if(arg == "-v" or arg == "--verbose"):
         verbose = True
      else:
         verbose = False
      self.game.runTests(verbose)

   def do_quit(self,arg):
      """Stop playing chess"""
      return True
      
   do_exit = do_quit
   
   def help_help(self):
       print("Display the help for one of the available commands.")

   def _booleanPrompt(self, prompt):
      confirmation = input(prompt+" [y/n]:")
      if confirmation in ["y" , "Y" , "Yes" , "yes" , "YES"]:
         return True
      else:
         return False

if __name__ == "__main__":
    init()
    Chess().cmdloop()
