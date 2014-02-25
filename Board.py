from colorama import Style, Fore, Back
import Util
from Piece import *
from math import ceil


class Board(object):
   """Basic parent board object"""
   rankLen = 8
   lastRank = 7
   firstRank = 0

class DisplayBoard(Board):
   """A board that holds all of the information necessary to display the state of the game."""

   def __init__(self, pieces = []):
      """Setup the colors for the board, as well as the pieces if they are given"""
      self.board = {}
      self.captures = [[],[]]
      self.whiteCheckMateStatus = (False,False)
      self.blackCheckMateStatus = (False,False)
      color = Util.colors.WHITE
      numberOfCoordinates = len(Util.allCoords)
      for index in range(numberOfCoordinates):
         coordKey = Util.allCoords[index]
         self.board[coordKey] = [color,Piece()]
         #If we reach the end of the rank we do not flip the color
         if index % self.rankLen != self.lastRank:
            if color == Util.colors.WHITE:
               color = Util.colors.BLACK
            else:
               color = Util.colors.WHITE
      self.placePieces(pieces)
   
   def __str__(self):
      """Returns the nice printable form of the board"""
      rep = ""
      rank = -1 
      numberOfCoordinates = len(Util.allCoords)
      if self.blackCheckMateStatus[0]:
         if self.blackCheckMateStatus[1]:
            rep += "Black is CHECKMATED! Game Over.\n"
         else:
            rep += "Black is CHECKED!\n"
      if self.whiteCheckMateStatus[0]:
         if self.whiteCheckMateStatus[1]:
            rep += "White is CHECKMATED! Game Over.\n"
         else:
            rep += "White is CHECKED!\n"
      rep += "Captured by Black:\n"
      rep += Fore.RED + " "
      captureCounter = 1
      if len(self.captures[1]) != 0:
         for piece in self.captures[1]:
            rep += piece.getPieceLetter()
            if captureCounter % 8 == 0:
               rep += "\n"
      else:
         rep += "None"
      rep += Style.RESET_ALL + "\n"
      for index in range(numberOfCoordinates):
         #If we are about the print the first file, print the rank designator
         if index % self.rankLen == self.firstRank:
            rank += 1
            rep += Util.ranks[rank]
         coordKey = Util.allCoords[index]
         #Because we are printing to CLI use red for black and yellow for white
         backColor = self.board[coordKey][0]
         if backColor  == Util.colors.WHITE:
            backColor = Back.YELLOW
         else:
            backColor = Back.RED
         #Now we get the current piece and retrieve it's color and piece letter
         currentPiece = self.board[coordKey][1]
         foreColor = currentPiece.color
         if foreColor == Util.colors.WHITE:
            foreColor = Fore.WHITE
         else:
            foreColor = Fore.BLACK
         pieceChar = currentPiece.getPieceLetter()
         #Print out all of the information for this square and piece
         rep += (backColor + foreColor + pieceChar)
         #Add a newline after the last file
         if index % self.rankLen == self.lastRank:
            rep += Style.RESET_ALL + "\n"
      #Print out all of the file designators at the bottom
      rep += " "+Util.files+"\n"
      rep += "Captured by White:\n"
      rep += Fore.RED + " "
      captureCounter = 1
      if len(self.captures[0]) != 0:
         for piece in self.captures[0]:
            rep += piece.getPieceLetter()
            if captureCounter % 8 == 0:
               rep += "\n"
      else:
         rep += "None"
      rep += Style.RESET_ALL + "\n"
      return rep
      
   def setCaptured(self, color, pieces):
      """Take the list of currently captures pieces from the player 
         and save them off for display"""      
      if color == Util.colors.WHITE:
         self.captures[0] = pieces[:]
      else:
         self.captures[1] = pieces[:]
         

   def placePieces(self,piecesLst):
      """Add the pieces passed in onto the board"""
      for piece in piecesLst:
         self.board[piece.position][1] = piece
         
   def getPiece(self, coordinate):
      """Return the piece found at the coordinate or None
         if the coordinate is not valid"""
      if Util.isCoordValid(coordinate):
         return self.board[coordinate][1]
         
   def setCheckMateStatus(self, player):
      """Take the current check and checkmake status from the player 
         and save them off for display"""
      status = (player.checked, player.mated)
      if player.color == Util.colors.WHITE:
         self.whiteCheckMateStatus = status
      else:
         self.blackCheckMateStatus = status

class VerifyBoard(Board):
   """A minimal board that is more suitable for tactical use by the players."""
   
   def __init__(self, pieces = []):
      """Create our board and fill it with pieces if they are given"""
      self.board = {}
      self.placePieces(pieces)
      
   def placePieces(self, piecesLst):
      """Add the pieces passed in onto the board"""
      for piece in piecesLst:
         self.board[piece.position] = piece

   def getPiece(self, coordinate):
      """Return the piece found at the coordinate or None
         if there is no piece at that location or the
         coordinate is not valid"""
      if coordinate in self.board:
         return self.board[coordinate]

class GameBoard(object):
   """The board that holds all of the turns in the game"""
   
   def __init__(self, whitePlayer, blackPlayer):
      """Sets up the game, with the initial positions being the positions as given by the players at this time."""
      self.boards = []
      self.boards.append(DisplayBoard(whitePlayer.getAllPieces() + blackPlayer.getAllPieces()))
      self.boards.append(DisplayBoard())
      self.currentTurn = 0
      self.initialSetup = 0
      self.pendingTurn = 1
      self.commitReady = False
      
   def __str__(self):
      """Returns a nice string representation of the current turn"""
      return "Turn: " + self.getTurnString() + "\n" + str(self.boards[self.currentTurn])
      
   def getTurnString(self,turn="current"):
      """Returns a string informing of the current round and player"""
      turnString = "Invalid"
      if turn in ("current","initial","pending"):
         if turn == "current":
            turn = self.currentTurn
         elif turn == "first":
            turn = self.initialSetup
         else:
            turn = self.pendingTurn

         if turn == self.initialSetup:
            turnString = "0"
         else:
            numericTurn = int(ceil(turn/float(2)))
            WHITE = 1
            if turn & 1 == WHITE:
               turnString = str(numericTurn)+"."
            else:
               turnString = str(numericTurn)+"..."
      return turnString
      
   def firstTurn(self):
      """Move our current turn to the initial setup of the board"""
      self.currentTurn = self.initialSetup
      
   def lastTurn(self):
      """Move our current turn to the last commit turn of the board"""
      self.currentTurn = self.pendingTurn - 1
      
   def nextTurn(self):
      """Increment our current turn"""
      if self.currentTurn < self.pendingTurn - 1:
         self.currentTurn += 1
         
   def previousTurn(self):
      """Decrement our current turn"""
      if self.currentTurn > self.initialSetup:
         self.currentTurn -= 1
   
   def setTurn(self, whitePlayer, blackPlayer):
      """Takes both players and stores all the necessary information to 
         commit and print the state of the game, call commitTurn to save this turn
         or cancelCommit to cancel it."""
      if self.commitReady == False:
         self.boards[self.pendingTurn].placePieces(whitePlayer.getAllPieces()+blackPlayer.getAllPieces())
         self.boards[self.pendingTurn].setCaptured(whitePlayer.color, whitePlayer.captured)
         self.boards[self.pendingTurn].setCaptured(blackPlayer.color, blackPlayer.captured)
         self.boards[self.pendingTurn].setCheckMateStatus(whitePlayer)
         self.boards[self.pendingTurn].setCheckMateStatus(blackPlayer)
         self.commitReady = True
         return True
      else:
         return False
   
   def commitTurn(self):
      """Commits the turn given by setTurn, this adds a turn and moves our current turn
         to the newly added turn."""
      if self.commitReady == True:
         self.currentTurn = self.pendingTurn
         self.pendingTurn += 1
         self.boards.append(DisplayBoard())
         self.commitReady = False
         return True
      else:
         return False
         
   def cancelCommit(self):
      """This cancels a turn given by setTurn"""
      if self.commitReady == True:
         self.boards[self.pendingTurn] = DisplayBoard()
         self.commitReady = False
         return True
      else:
         return False
         
   def getPendingMoveString(self):
      """This returns a nice printable string of the state of the game considering the
         pending move given by setTurn."""
      return "Pending Move\n" + "Turn: " + self.getTurnString("pending") + "\n" + str(self.boards[self.pendingTurn])
      
   def getCurrentBoard(self):
      """Returns the display board for our current turn."""
      return self.boards[self.currentTurn]
