from Piece import *
from Board import *
from Algebra import *
from ChessFile import *
import Coord


class MoveType(object):
   NORMAL = 1
   CAPTURE = 2
   EN_PASSANT = 4
   CASTLE = 8
   PROMOTION = 16

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
      
   def move(self, startCoord, endCoord, promotion=""):
      """Attempt to make a move and return whether the move was possible or not, if this returns false
         the reason for the failure will be in my moveResultReason member"""
      debugPrint("Two coordinate move attempted.")
      self.lastMoveString = ""
      if self.mateCheck():
         debugPrint("Checkmate detected, game over.")
         return False
      self.updateMoveValues = True
      moveValid = self._movePiece(startCoord, endCoord, promotion)
      if moveValid:
         #print(self.algebraicMoveClass)
         debugPrint("Checking for check and checkmate.")
         self._postMoveChecks()
         self.algebraicMoveClass.valid = True
         self.parser.setAlgebraicMove(self.algebraicMoveClass)
         self.lastMoveString = self.parser.getAlgebraicMoveString()
         debugPrint("Algebraic move string:", self.lastMoveString)
      return moveValid
      
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
            moveValid = self._movePiece(potentialPieces[0].position, algebraicMove.destination, algebraicMove.promotion)
            if moveValid:
               self._postMoveChecks()
               self.algebraicMoveClass.valid = True
               self.parser.setAlgebraicMove(self.algebraicMoveClass)
               self.lastMoveString = self.parser.getAlgebraicMoveString()
            
         return moveValid
      else:
         self.moveResultReason = "Invalid algebraic notation given."
         return False
   
   def getPiecesThatCanMoveToLocation(self, pieceType, location, disambiguation):
      """Return a list of my pieces that can move to given location, filtered by disambiguation"""
      def canPieceMoveToLocation(piece):
         moves = self.getValidMovesForPiece(piece)
         result = True
         if (location not in moves):
            result = False
         if disambiguation != "" and disambiguation not in piece.position:
            result = False
         return result
      return list(filter(canPieceMoveToLocation, self.pieceMap[pieceType]))
      
   def getValidMovesForPieceAtCoord(self, coord):
      """Return a map of available moves for the piece at the coordinate, move mapped to move type"""
      validMap = {}
      vBoard = VerifyBoard(self.getAllPieces)
      piece = vBoard.getPiece(coord)
      if piece:
         validMap = self.getValidMovesForPiece(piece)
      return validMap
      
   def getValidMovesForPiece(self, piece):
      """Return a map of available moves for the piece, move mapped to move type"""
      validMap = {}
      vBoard = VerifyBoard(self.getAllPieces() + self.otherPlayer.getAllPieces())
      if piece and piece.color == self.color:
         validList = piece.getValidMoves(vBoard)
         for move in validList:
            validMap[move] = set()
            if self.enemyPieceIsAtLocation(move, vBoard):
               validMap[move].add(MoveType.CAPTURE)
            else:
               validMap[move].add(MoveType.NORMAL)
         #En Passant and promotion checking for Pawns
         if type(piece) == Pawn:
            capturables = piece.getCaptureCoords()
            for move in capturables:
               if move not in validMap and self.canPawnCaptureEnPassantAtCoord(piece, move):
                  validMap[move].add(MoveType.EN_PASSANT)
            for move in validMap:
               if self.promotionRank in move:
                  validMap[move].add(MoveType.PROMOTION)
         #TODO Now check for Castle Moves
         elif type(piece) == King:
            pass
      return validMap
      
   def canPawnCaptureEnPassantAtCoord(self, pawn, coord):
      if type(pawn) == Pawn:
         possibleEnemyPosition = coord[0] + pawn.position[1]
         vBoard = VerifyBoard(self.getAllPieces() + self.otherPlayer.getAllPieces())
         enemyPiece = vBoard.getPiece(possibleEnemyPosition)
         if type(enemyPiece) == Pawn:
            if enemyPiece.enPassantCapturable:
               return True
            else:
               return False
         else:
            return False
      return False
      
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
      
   def _movePiece(self, startCoord, endCoord, promotionPieceStr=""):
      """This checks a number of things, it makes sure that we do have a piece at the start location, it makes sure that the requested 
         end location is in the physical move set of the peice, it captures an opponent piece at the end location if necessary, and it 
         makes sure that the requested move does not expose or leave our king in check. If any of these problem areas arise, it leaves both 
         players in their initial state."""
      if isDebugEnabled():
         print("Debuging information is enabled")
      if self.updateMoveValues:
         self.algebraicMoveClass = AlgebraicMove()
         self.algebraicMoveClass.valid = False
         moveClass = self.algebraicMoveClass
 
      currPieces = filter(self._generateLocator(startCoord), self.getAllPieces())
      self.moveResultReason = "Success"
      previousCheckStatus = self.checked
      for piece in currPieces:
         #This is a little weird at first glance
         #It is possible that filter could return more than one piece
         #so what we do is we move the first one found
         self.generateMovePiece(piece)
         validMoves = self.getValidMovesForPiece(piece)
         #print(validMoves)
         if endCoord in validMoves:
            self.generateDisambiguation(piece, endCoord)
            self.generateDestination(endCoord)
            capturePiece = None
            promotionPiece = None
            if MoveType.CAPTURE in validMoves[endCoord]:
               self.generateCapture(piece, True)
               capturePiece = self.capture(endCoord)
            elif MoveType.EN_PASSANT in validMoves[endCoord]:
               #We know that this is a pawn now
               self.generateCapture(piece, True)
               capturePiece = self.capture(endCoord[0]+piece.position[1])
            piece.move(endCoord)
            if MoveType.PROMOTION in validMoves[endCoord]:
               if promotionPieceStr not in invPieces or promotionPieceStr == pieces["Pawn"]:
                  piece.undoLastMove()
                  self.moveResultReason = "No valid piece given to promote to."
                  return False
               promotionTypeString = invPieces[promotionPieceStr]
               promotionPiece = globals()[promotionTypeString](self.color, endCoord)
               pieceList = self.pieceMap[piece.piece]
               pieceList.remove(piece)
               promotionPieceList = self.pieceMap[promotionPiece.piece]
               promotionPieceList.append(promotionPiece)
            self.moveResultReason = piece.moveResultReason
            self.lastMove = (piece, capturePiece, promotionPiece)
            if self.verifyCheck():
               self.undoLastMove()
               if previousCheckStatus:
                  self.moveResultReason = "That move does not resolve the check!"
               else:
                  self.moveResultReason = "That move results in check!"
               return False
            #print(moveClass)
            return True
         else:
            self.moveResultReason = "The end square is not in the valid move range of this piece."
            pass
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
      self.generateCheckMate(self.otherPlayer.checked, self.otherPlayer.mated)
      
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

   def generateMovePiece(self, piece):
      """If required, generate the piece string for the piece to be moved"""
      if self.updateMoveValues:
         self.algebraicMoveClass.piece = piece.piece

   def generateDestination(self, coord):
      """If required, generate the destination coordinate for the move"""
      if self.updateMoveValues:
         self.algebraicMoveClass.destination = coord

   def generateCapture(self, piece, captureHappened):
      """If required, generate the capture status for the move"""
      if self.updateMoveValues:
         self.algebraicMoveClass.capture = captureHappened
         if captureHappened and type(piece) == Pawn:
            #Pawns need to specify their file as disambiguation when capturing
            self.algebraicMoveClass.disambiguation = piece.position[0]

   def generateCheckMate(self, checkStatus, mateStatus):
      """If required, generate the check and mate status for the move"""
      if self.updateMoveValues:
         self.algebraicMoveClass.check = checkStatus
         self.algebraicMoveClass.mate = mateStatus
      
   
   def undoLastMove(self):
      """Undo the previous move"""
      if len(self.lastMove) == 3:
         self.lastMove[0].undoLastMove()
         if self.lastMove[1] != None:
            self.otherPlayer.returnPiece(self.captured.pop(self.captured.index(self.lastMove[1])))
         if self.lastMove[2] != None:
            #We are undoing a promotion special things need to happened
            pieceList = self.pieceMap[self.lastMove[0].piece]
            pieceList.append(self.lastMove[0])
            promotionPieceList = self.pieceMap[self.lastMove[2].piece]
            promotionPieceList.remove(self.lastMove[2])
         self.lastMove = ()
         #It is almost guaranteed that we could undo back into a check position. Because of that, run
         #the verify to update our state properly
         self.verifyCheck()
         return True
      return False
      
   def capture(self, coord):
      """Capture the piece from the other player at the given coordinate"""
      vBoard = VerifyBoard(self.getAllPieces()+self.otherPlayer.getAllPieces())
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
         moves = self.getValidMovesForPiece(piece)
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
            kingCanMove = False
            kingMovements = self.getValidMovesForPiece(self.king)
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
               vBoard = VerifyBoard(self.getAllPieces() + self.otherPlayer.getAllPieces())
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

