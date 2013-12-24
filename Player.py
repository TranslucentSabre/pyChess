from Piece import *
from Board import *
from Algebra import *
import Coord



class Player(object):
   """Base player class"""
   
   def __init__(self):
      """Create all our pieces in their initial locations"""
      
      self.checked = False
      self.mated = False
      
      self.lastMove = ()
      self.captured = []

      self.moveResultResaon = "Success"
      self.lastMoveString = ""

      rookFiles = "ah"
      knightFiles = "bg"
      bishopFiles = "cf"
      
      self.parser = AlgebraicParser()
      self.algebraicMoveClass = AlgebraicMove()
      self.parsedAlgebraicMoveClass = AlgebraicMove()
      self.updateMoveValues = False
      
      self.pawns = [Pawn(self.color,file+self.pawnRank) for file in Coord.files]
      self.rooks = [Rook(self.color,file+self.majorRank) for file in rookFiles]
      self.knights = [Knight(self.color,file+self.majorRank) for file in knightFiles]
      self.bishops = [Bishop(self.color,file+self.majorRank) for file in bishopFiles]
      self.queens = [Queen(self.color,"d"+self.majorRank)]
      self.king = King(self.color,"e"+self.majorRank)
      #This is a lookup table that is primarily used for captures and un-captures
      self.pieceMap = { "Pawn" : self.pawns, 
                        "Rook" : self.rooks, 
                        "Knight" : self.knights, 
                        "Bishop" : self.bishops, 
                        "Queen" : self.queens, 
                        "King" : [self.king]}
   
   def setOpponent(self, player):
      self.otherPlayer = player
       
   def getAllPieces(self):
      """Return an array of all of my current pieces"""
      return self.pawns + self.rooks + self.knights + self.bishops + self.queens + [self.king]
      
   def mateCheck(self):
      mated = False
      if self.mated or self.otherPlayer.mated:
         self.moveResultReason = "The game is over."
         mated = True
      return mated
      
   def move(self, startCoord, endCoord):
      """Attempt to make a move and return whether the move was possible or not, if this returns false
         the reason for the failure will be in my moveResultReason member"""
      self.lastMoveString = ""
      if self.mateCheck():
         return False
      moveValid = self._movePiece(startCoord, endCoord)
      if moveValid:
         #print(self.algebraicMoveClass)
         self.parser.setAlgebraicMove(self.algebraicMoveClass)
         self.lastMoveString = self.parser.getAlgebraicMoveString()
         self._postMoveChecks()
      return moveValid
      
   def setPromotionPiece(self, piece):
      pass
      
   def algebraicMove(self, move):
      """Take in a string in algebraic notation and attempt that move"""
      self.lastMoveString = ""
      if self.mateCheck():
         return False
      moveValid = False
      self.parser.setAlgebraicMove(move)
      if self.parser.valid == True:
         algebraicMove = self.parser.getAlgebraicMoveClass()
         #Save off this move class, we will use it as a comparison after the move
         self.parsedAlgebraicMoveClass = algebraicMove
         potentialPieces = self.getPiecesThatCanMoveToLocation(algebraicMove.piece, algebraicMove.destination, algebraicMove.disambiguation)
         if len(potentialPieces) == 0:
            self.moveResultReason = "No pieces of that type may move to the selected location"
         elif len(potentialPieces) > 1:
               self.moveResultReason = "More than one piece may move based upon your selection"
         else:
            self.updateMoveValues = True
            moveValid = self._movePiece(potentialPieces[0].position, algebraicMove.destination)
            if moveValid:
               self.parser.setAlgebraicMove(self.algebraicMoveClass)
               self.lastMoveString = self.parser.getAlgebraicMoveString()
               self._postMoveChecks()
            
         return moveValid
      else:
         self.moveResultReason = "Invalid algebraic notation given."
         return False
   
   def getPiecesThatCanMoveToLocation(self, pieceType, location, disambiguation):
      """Return a list of my pieces that can move to given location, filtered by disambiguation"""
      vBoard = VerifyBoard(self.getAllPieces() + self.otherPlayer.getAllPieces())
      def canPieceMoveToLocation(piece):
         moves = piece.getValidMoves(vBoard)
         result = True
         if location not in moves:
            result = False
         if disambiguation != "" and disambiguation not in piece.position:
            result = False
         return result
      return list(filter(canPieceMoveToLocation, self.pieceMap[pieceType]))
   
   def _generateLocator(self,coord):
      """Returns a function that only accepts pieces that are at the specificed coordinate"""
      return lambda piece: piece.position == coord
      
   def enemyPieceIsAtLocation(self,coord, vBoard):
      """This checks to see if there is an enemy piece at the position given"""
      result = False
      otherPiece = vBoard.getPiece(coord)
      if otherPiece != None and otherPiece.color != self.color:
         result = True
      return result
      
   def _movePiece(self, startCoord, endCoord):
      """This checks a number of things, it makes sure that we do have a piece at the start location, it makes sure that the requested 
         end location is in the physical move set of the peice, it captures an opponent piece at the end location if necessary, and it 
         makes sure that the requested move does not expose or leave our king in check. If any of these problem areas arise, it leaves both 
         players in their initial state."""
      if self.updateMoveValues:
         self.algebraicMoveClass = AlgebraicMove()
         moveClass = self.algebraicMoveClass
      checkBoard = VerifyBoard(self.getAllPieces()+self.otherPlayer.getAllPieces())
      pieces = filter(self._generateLocator(startCoord), self.getAllPieces())
      self.moveResultReason = "Success"
      previousCheckStatus = self.checked
      for piece in pieces:
         #This is a little weird at first glance
         #It is possible that filter could return more than one piece
         #so what we do is we move the first one found
         self.algebraicMoveClass.piece = piece.piece
         validMoves = piece.getValidMoves(checkBoard)
         #print(validMoves)
         if endCoord in validMoves:
            self.generateDisambiguation(piece, endCoord)
            self.algebraicMoveClass.destination = endCoord
            piece.move(endCoord)
            self.moveResultReason = piece.moveResultReason
            capturePiece = None
            if self.enemyPieceIsAtLocation(endCoord, checkBoard):
               self.algebraicMoveClass.capture = True
               capturePiece = self.capture(endCoord, checkBoard)
            self.lastMove = (piece, capturePiece)
            if self.verifyCheck():
               self.undoLastMove()
               if previousCheckStatus:
                  self.moveResultReason = "That move does not resolve the check!"
               else:
                  self.moveResultReason = "That move results in check!"
               return False
            #print(moveClass)
            return True
         self.moveResultReason = "The end square is not in the valid move range of this piece."
         return False
      self.moveResultReason = "No piece found at that start square."
      return False
      
   def _testMove(self, startCoord, endCoord):
      """We are just testing to see if a move is valid, we do not care if it affects the other player,
         and we want it to have no lasting impact on the board"""
      savedSetting = self.updateMoveValues
      self.updateMoveValues = False
      testMoveValid = self._movePiece(startCoord, endCoord)
      if testMoveValid:
         #Undo that move if it happened to be valid
         self.undoLastMove()
      self.updateMoveValues = savedSetting
      return testMoveValid
      
   def _postMoveChecks(self):
      """Run and checks after a move is completed successfully"""
      self.otherPlayer.verifyCheck()
      self.otherPlayer.verifyMate()
      
   def generateDisambiguation(self, piece, destination):
      """If required, based upon instance variable, generate the disambiguation string"""
      if self.updateMoveValues:
         #We need the file if that works, the rank if the file does not, and both if neither is sufficient
         pieces = self.getPiecesThatCanMoveToLocation(piece.piece, destination, "")
         pieces.remove(piece)
         if len(pieces) > 0:
            fileAndRank = piece.position
            otherPositions = []
            for otherPiece in pieces:
               otherPositions.append(otherPiece.position)
            if any(fileAndRank[0] not in position for position in otherPositions):
               self.algebraicMoveClass.disambiguation = fileAndRank[0]
            elif any(fileAndRank[1] not in position for position in otherPositions):
               self.algebraicMoveClass.disambiguation = fileAndRank[1]
            else:
               self.algebraicMoveClass.disambiguation = piece.position
         else:
            #This is the only piece that can move here, no disambiguation needed
            self.algebraicMoveClass.disambiguation = ""
   
   def undoLastMove(self):
      """Undo the previous move"""
      if len(self.lastMove) == 2:
         self.lastMove[0].undoLastMove()
         if self.lastMove[1] != None:
            self.otherPlayer.returnPiece(self.captured.pop(self.captured.index(self.lastMove[1])))
         self.lastMove = ()
         #It is almost guaranteed that we could undo back into a check position. Because of that, run
         #the verify to update our state properly
         self.verifyCheck()
         return True
      return False
      
   def capture(self, coord, vBoard):
      """Capture the piece from the other player at the given coordinate"""
      capturePiece = vBoard.getPiece(coord)
      self.otherPlayer.giveCapturedPiece(capturePiece)
      self.captured.append(capturePiece)
      return capturePiece
      
   def giveCapturedPiece(self, piece):
      """Remove the selected piece from our list and return it"""
      #I cannot simply use the all pieces API because that returns a new list
      # and I need to get these pieces where they live
      pieceList = self.pieceMap[piece.piece]
      capturedPiece = pieceList.pop(pieceList.index(piece))
      return capturedPiece
      
   def returnPiece(self, piece):
      """Add the given piece to our lists"""
      #I cannot simply use the all pieces API because that returns a new list
      #and I need to get these pieces where they live"""
      self.pieceMap[piece.piece].append(piece)
      
   def getPiecesThatThreatenLocation(self, location):
      """Return a list of my pieces that can capture the piece at the given location"""
      vBoard = VerifyBoard(self.getAllPieces() + self.otherPlayer.getAllPieces())
      def canPieceAttackLocation(piece):
         moves = piece.getValidMoves(vBoard)
         if location in moves and self.enemyPieceIsAtLocation(location,vBoard):
            return True
      return list(filter(canPieceAttackLocation, self.getAllPieces()))
   
   def verifyCheck(self):
      """Check to see if I am checked, and update my flag as appropriate"""
      if len(self.otherPlayer.getPiecesThatThreatenLocation(self.king.position)) != 0:
         self.checked = True
      else:
         self.checked = False
      self.algebraicMoveClass.check = self.checked
      return self.checked
      
   def verifyMate(self):
      """Check to see if I am mated, and update my flag as appropriate""" 
      if self.checked:
         #Get the attacking pieces to start off with"""
         attackingPieces = self.otherPlayer.getPiecesThatThreatenLocation(self.king.position)
         numberOfAttackers = len(attackingPieces)
         if numberOfAttackers == 0:
            self.checked = False
            #We must set this here for correctness
            self.algebraicMoveClass.check = self.checked
            self.mated = False
         else:
            #Assume mated unless proven otherwise"""
            self.mated = True
            #Always check to see if we can just move the king away"""
            vBoard = VerifyBoard(self.getAllPieces() + self.otherPlayer.getAllPieces())
            kingCanMove = False
            kingMovements = self.king.getValidMoves(vBoard)
            for move in kingMovements:
                  if self._testMove(self.king.position, move):
                     kingCanMove = True
                     self.mated = False
                     break
                  
            if numberOfAttackers == 1 and not kingCanMove:
               #We only check other pieces to see if they can interfere if there is only one attacker,
               #I believe that there are no cases where two or more attacking pieces can be stopped by
               #anything other than moving the king
               attacker = attackingPieces[0]
               pathToKing = attacker.getPath(self.king.position, vBoard)
               
               #Now get all of my pieces minus the king, we have already taken care of his movements
               myPieces = self.getAllPieces()
               myPieces.pop() #here we use the fact that the king is added last as a quick way of removing him
               for piece in myPieces:
                  for coord in pathToKing:
                     if self._testMove(piece.position, coord):
                        self.mated = False
                        break
      else:
         self.mated = False
      self.algebraicMoveClass.mate = self.mated
      return self.mated


class WhitePlayer(Player):
   """The Player of the White Pieces"""
   def __init__(self):
      self.color = colors.WHITE
      self.pawnRank = "2"
      self.majorRank = "1"
      self.promotionRank = "8"
      super(WhitePlayer,self).__init__()
      
class BlackPlayer(Player):
   """The Player of the Black Pieces"""
   def __init__(self):
      self.color = colors.BLACK
      self.pawnRank = "7"
      self.majorRank = "8"
      self.promotionRank = "1"
      super(BlackPlayer,self).__init__()
