from Piece import *
from Board import *
from Algebra import *
from Debug import *
import Util


class MoveType(object):
   NORMAL = "normal"
   CAPTURE = "capture"
   EN_PASSANT = "enPassant"
   CASTLE = "castle"
   PROMOTION = "promotion"

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
      
      self.debug = Debug()
      
      self.pawns = [Pawn(self.color,file+self.color.pawnRank) for file in Util.files]
      self.rooks = [Rook(self.color,file+self.color.majorRank) for file in rookFiles]
      self.knights = [Knight(self.color,file+self.color.majorRank) for file in knightFiles]
      self.bishops = [Bishop(self.color,file+self.color.majorRank) for file in bishopFiles]
      self.queens = [Queen(self.color,"d"+self.color.majorRank)]
      self.king = King(self.color,"e"+self.color.majorRank)
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
      self.debug.startSection("move")
      self.debug.dprint("Two coordinate move attempted.")
      self.lastMoveString = ""
      if self.mateCheck():
         self.debug.dprint("Checkmate detected, game over.")
         return False
      self.updateMoveValues = True
      moveValid = self._movePiece(startCoord, endCoord, promotion)
      if moveValid:
         self.debug.dprint("Checking for check and checkmate.")
         self._postMoveChecks()
         self.algebraicMoveClass.valid = True
         self.parser.setAlgebraicMove(self.algebraicMoveClass)
         self.debug.dprint("Output Algebraic move class:\n", self.algebraicMoveClass)
         self.lastMoveString = self.parser.getAlgebraicMoveString()
         self.debug.dprint("Algebraic move string:", self.lastMoveString)
      self.debug.endSection()
      return moveValid
      
   def algebraicMove(self, move):
      """Take in a string in algebraic notation and attempt that move"""
      self.debug.startSection("algebraicMove")
      self.debug.dprint("Algebraic move attempted.")
      self.lastMoveString = ""
      if self.mateCheck():
         self.debug.dprint("Checkmate detected, game over.")
         return False
      moveValid = False
      self.parser.setAlgebraicMove(move)
      self.debug.dprint("Incoming Algebraic move string: ", move)
      if self.parser.valid == True:
         algebraicMove = self.parser.getAlgebraicMoveClass()
         #Save off this move class, we can use it as a comparison after the move
         self.parsedAlgebraicMoveClass = algebraicMove
         self.debug.dprint("Parsed Algebraic move class:\n", self.parsedAlgebraicMoveClass)
         potentialPieces = self.getPiecesThatCanMoveToLocation(algebraicMove.piece, algebraicMove.destination, algebraicMove.disambiguation)
         self.debug.dprint("Pieces that can move: ", potentialPieces)
         if len(potentialPieces) == 0:
            self.moveResultReason = "No pieces of that type may move to the selected location"
         elif len(potentialPieces) > 1:
            self.moveResultReason = "More than one piece may move based upon your selection"
         else:
            self.updateMoveValues = True
            moveValid = self._movePiece(potentialPieces[0].position, algebraicMove.destination, algebraicMove.promotion)
            if moveValid:
               self.debug.dprint("Checking for check and checkmate.")
               self._postMoveChecks()
               self.algebraicMoveClass.valid = True
               self.parser.setAlgebraicMove(self.algebraicMoveClass)
               self.debug.dprint("Output Algebraic move class:\n", self.algebraicMoveClass)
               self.lastMoveString = self.parser.getAlgebraicMoveString()
               self.debug.dprint("Algebraic move string:", self.lastMoveString)
         self.debug.endSection()   
         return moveValid
      else:
         self.debug.dprint("Invalid Algebraic move string.")
         self.moveResultReason = "Invalid algebraic notation given."
         self.debug.endSection()
         return False
   
   def getPiecesThatCanMoveToLocation(self, pieceType, location, disambiguation):
      """Return a list of my pieces that can move to given location, filtered by disambiguation"""
      self.debug.startSection("getPiecesThatCanMoveToLocation")
      self.debug.dprint("Finding piece to move.")
      def canPieceMoveToLocation(piece):
         moves = self.getValidMovesForPiece(piece)
         self.debug.dprint("Piece and it's moves:", piece.position, moves)
         result = True
         if (location not in moves):
            self.debug.dprint("Piece disqualified due to lack of ability to move.")
            result = False
         if disambiguation != "" and disambiguation not in piece.position:
            self.debug.dprint("Piece disqualified due to disambiguation.")
            result = False
         return result
      pieceList = list(filter(canPieceMoveToLocation, self.pieceMap[pieceType]))
      self.debug.endSection()
      return pieceList
      
   def getValidMovesForPieceAtCoord(self, coord):
      """Return a map of available moves for the piece at the coordinate, move mapped to move type"""
      self.debug.startSection("getValidMovesForPieceAtCoord")
      validMap = {}
      vBoard = VerifyBoard(self.getAllPieces)
      piece = vBoard.getPiece(coord)
      if piece:
         self.debug.dprint("Found piece for getting valid moves.")
         validMap = self.getValidMovesForPiece(piece)
      self.debug.endSection()
      return validMap
      
   def getValidMovesForPiece(self, piece):
      """Return a map of available moves for the piece, move mapped to move type"""
      self.debug.startSection("getValidMovesForPiece")
      self.debug.dprint("Get valid moves for: ", piece.position)
      validMap = {}
      vBoard = VerifyBoard(self.getAllPieces() + self.otherPlayer.getAllPieces())
      if piece and piece.color == self.color:
         validList = piece.getValidMoves(vBoard)
         self.debug.dprint("Valid moves from Piece: ", validList)
         for move in validList:
            validMap[move] = set()
            if self.enemyPieceIsAtLocation(move, vBoard):
               self.debug.dprint("Set move as capture:", move)
               validMap[move].add(MoveType.CAPTURE)
            else:
               validMap[move].add(MoveType.NORMAL)
         #En Passant and promotion checking for Pawns
         if type(piece) == Pawn:
            self.debug.dprint("Pawn Specials.")
            capturables = piece.getCaptureCoords()
            for move in capturables:
               if move not in validMap and self.canPawnCaptureEnPassantAtCoord(piece, move):
                  self.debug.dprint("Set move as En Passant: ", move)
                  validMap[move].add(MoveType.EN_PASSANT)
            for move in validMap:
               if self.color.promotionRank in move:
                  self.debug.dprint("Set move as Promotion: ", move)
                  validMap[move].add(MoveType.PROMOTION)
         #TODO Now check for Castle Moves
         elif type(piece) == King:
            self.debug.dprint("King Specials.")
            pass
      self.debug.endSection()
      return validMap
      
   def canPawnCaptureEnPassantAtCoord(self, pawn, coord):
      """Determine if the destination coordinate is an En Passant capture for the given pawn"""
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
      self.debug.startSection("_movePiece")
      if self.updateMoveValues:
         self.algebraicMoveClass = AlgebraicMove()
         self.algebraicMoveClass.valid = False
         moveClass = self.algebraicMoveClass
 
      currPieces = filter(self._generateLocator(startCoord), self.getAllPieces())
      self.moveResultReason = "Success"
      previousCheckStatus = self.checked
      for piece in currPieces:
         self.debug.dprint("Found piece at location: ", piece)
         #This is a little weird at first glance
         #It is possible that filter could return more than one piece
         #so what we do is we move the first one found
         self.generateMovePiece(piece)
         validMoves = self.getValidMovesForPiece(piece)
         self.debug.dprint("Valid moves for piece: ", validMoves)
         if endCoord in validMoves:
            self.generateDisambiguation(piece, endCoord)
            self.generateDestination(endCoord)
            capturePiece = None
            promotionPiece = None
            if MoveType.CAPTURE in validMoves[endCoord]:
               self.debug.dprint("Capture move.")
               self.generateCapture(piece, True)
               capturePiece = self.capture(endCoord)
               self.debug.dprint("Captured piece: ", capturePiece)
            elif MoveType.EN_PASSANT in validMoves[endCoord]:
               #We know that this is a pawn now
               self.debug.dprint("En Passant Capture move.")
               self.generateCapture(piece, True)
               capturePiece = self.capture(endCoord[0]+piece.position[1])
               self.debug.dprint("En Passant Captured piece: ", capturePiece)
            piece.move(endCoord)
            self.moveResultReason = piece.moveResultReason
            #Go ahead and set the last move, minus any promotion piece, so that we can do an undo if promotion falls through
            self.lastMove = (piece, capturePiece, promotionPiece)
            if MoveType.PROMOTION in validMoves[endCoord]:
               if promotionPieceStr not in Util.pieces or promotionPieceStr == "Pawn" or promotionPieceStr == "King":
                  self.debug.dprint("Invalid promotion move.")
                  self.undoLastMove()
                  self.moveResultReason = "No valid piece given to promote to."
                  self.debug.endSection()
                  return False
               self.debug.dprint("Valid promotion move.")
               self.generatePromotion(promotionPieceStr)
               promotionPiece = globals()[promotionPieceStr](self.color, endCoord)
               self.debug.dprint("Pawn: ", id(piece))
               pieceList = self.pieceMap[piece.piece]
               pieceList.remove(piece)
               self.debug.dprint("Pawn list: ", getIds(pieceList))
               self.debug.dprint("Promotion piece: ", promotionPieceStr, id(promotionPiece))
               promotionPieceList = self.pieceMap[promotionPiece.piece]
               promotionPieceList.append(promotionPiece)
               self.debug.dprint("Promotion piece list: ", getIds(promotionPieceList))
            self.lastMove = (piece, capturePiece, promotionPiece)
            self.debug.dprint("Last Move: ", self.lastMove)
            if self.verifyCheck():
               self.debug.dprint("That move placed us in check.")
               self.undoLastMove()
               if previousCheckStatus:
                  self.moveResultReason = "That move does not resolve the check!"
               else:
                  self.moveResultReason = "That move results in check!"
               self.debug.endSection()
               return False
            self.debug.endSection()
            return True
         else:
            self.moveResultReason = "The end square is not in the valid move range of this piece."
            pass
         self.debug.endSection()
         return False
      self.moveResultReason = "No piece found at that start square."
      self.debug.endSection()
      return False
      
   def _testMove(self, startCoord, endCoord):
      """We are just testing to see if a move is valid, we do not care if it affects the other player,
         and we want it to have no lasting impact on the board"""
      self.debug.startSection("_testMove")
      savedSetting = self.updateMoveValues
      self.updateMoveValues = False
      self.debug.dprint("Disabling algebraic move generation")
      testMoveValid = self._movePiece(startCoord, endCoord)
      if testMoveValid:
         self.debug.dprint("Move succeeded, undoing.")
         self.undoLastMove()
      self.updateMoveValues = savedSetting
      self.debug.dprint("Algebraic move generation restored to: ", self.updateMoveValues)
      self.debug.endSection()
      return testMoveValid
      
   def _postMoveChecks(self):
      """Run and checks after a move is completed successfully"""
      self.debug.startSection("_postMoveChecks")
      self.debug.dprint(self.color, "Player Post move checking, transfer control to other player to check and see if they are checked or mated.")
      self.otherPlayer.verifyCheck()
      self.otherPlayer.verifyMate()
      self.generateCheckMate(self.otherPlayer.checked, self.otherPlayer.mated)
      self.debug.endSection()
      
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
         
   def generatePromotion(self, promotion):
      """If required, generate the promotion piece for the move"""
      if self.updateMoveValues:
         if promotion in Util.pieces:
            self.algebraicMoveClass.promotion = promotion
         elif promotion in Util.invPieces:
            self.algebraicMoveClass.promotion = Util.invPieces[promotion]
         else:
            self.algebraicMoveClass.promotion = ""
      
   
   def undoLastMove(self):
      """Undo the previous move"""
      self.debug.startSection("undoLastMove")
      if len(self.lastMove) == 3:
         self.debug.dprint("Valid last move to undo detected: ", self.lastMove)
         self.lastMove[0].undoLastMove()
         if self.lastMove[1] != None:
            self.otherPlayer.returnPiece(self.captured.pop(self.captured.index(self.lastMove[1])))
         if self.lastMove[2] != None:
            #We are undoing a promotion, special things need to happen
            pieceList = self.pieceMap[self.lastMove[0].piece]
            pieceList.append(self.lastMove[0])
            promotionPieceList = self.pieceMap[self.lastMove[2].piece]
            promotionPieceList.remove(self.lastMove[2])
         self.lastMove = ()
         #It is almost guaranteed that we could undo back into a check position. Because of that, run
         #the verify to update our state properly
         self.verifyCheck()
         self.debug.dprint("Verifying/setting check status after undo: ", self.checked)
         self.debug.endSection()
         return True
      self.debug.endSection()
      return False
      
   def capture(self, coord):
      """Capture the piece from the other player at the given coordinate"""
      self.debug.startSection("capture")
      vBoard = VerifyBoard(self.getAllPieces()+self.otherPlayer.getAllPieces())
      capturePiece = vBoard.getPiece(coord)
      self.debug.dprint("Piece to capture: ", id(capturePiece))
      self.debug.dprint(self.color, "Player transferring control to other to get captured piece")
      self.otherPlayer.giveCapturedPiece(capturePiece)
      self.captured.append(capturePiece)
      self.debug.dprint("New capture list: ", getIds(self.captured))
      self.debug.endSection()
      return capturePiece
      
   def giveCapturedPiece(self, piece):
      """Remove the selected piece from our list and return it"""
      self.debug.startSection("capture")
      #I cannot simply use the all pieces API because that returns a new list
      # and I need to get these pieces where they live
      pieceList = self.pieceMap[piece.piece]
      self.debug.dprint("Piece list prior to giving: ", piece, getIds(pieceList))
      self.debug.dprint("Piece removed: ", id(piece))
      capturedPiece = pieceList.pop(pieceList.index(piece))
      self.debug.dprint("New piece list: ", getIds(pieceList))
      self.debug.endSection()
      return capturedPiece
      
   def returnPiece(self, piece):
      """Add the given piece to our lists"""
      #I cannot simply use the all pieces API because that returns a new list
      #and I need to get these pieces where they live"""
      self.pieceMap[piece.piece].append(piece)
      
   def getPiecesThatThreatenLocation(self, location):
      """Return a list of my pieces that can capture the piece at the given location"""
      def canPieceAttackLocation(piece):
         moves = self.getValidMovesForPiece(piece)
         if location in moves and MoveType.CAPTURE in moves[location]:
            return True
      return list(filter(canPieceAttackLocation, self.getAllPieces()))
   
   def verifyCheck(self):
      """Check to see if I am checked, and update my flag as appropriate"""
      self.debug.startSection("verifyCheck")
      self.debug.dprint(self.color, "Player transferring control to other player to get pieces that can attack our King at: ", self.king.position)
      if len(self.otherPlayer.getPiecesThatThreatenLocation(self.king.position)) != 0:
         self.checked = True
      else:
         self.checked = False
      self.debug.dprint("Our checked status: ", self.checked)
      self.debug.endSection()
      return self.checked
      
   def verifyMate(self):
      """Check to see if I am mated, and update my flag as appropriate""" 
      self.debug.startSection("verifyMate")
      if self.checked:
         #Get the attacking pieces to start off with"""
         self.debug.dprint(self.color, "Player transferring control to other player to get pieces that can attack our King at: ", self.king.position)
         attackingPieces = self.otherPlayer.getPiecesThatThreatenLocation(self.king.position)
         numberOfAttackers = len(attackingPieces)
         self.debug.dprint("Number of pieces attacking our King: ", numberOfAttackers)
         if numberOfAttackers == 0:
            self.checked = False
            self.mated = False
         else:
            #Assume mated unless proven otherwise"""
            self.mated = True
            #Always check to see if we can just move the king away"""
            kingCanMove = False
            self.debug.dprint("Getting all valid moves for the king and trying them.")
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
               self.debug.dprint("The king is stuck, try moving all other pieces into the path of the one attacker.")
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
         self.debug.dprint("Not checked.")
         self.mated = False
      self.debug.dprint("Our mated status: ", self.mated)
      self.debug.endSection()
      return self.mated


class WhitePlayer(Player):
   """The Player of the White Pieces"""
   def __init__(self):
      self.color = Util.colors.WHITE
      super(WhitePlayer,self).__init__()
      
class BlackPlayer(Player):
   """The Player of the Black Pieces"""
   def __init__(self):
      self.color = Util.colors.BLACK
      super(BlackPlayer,self).__init__()
      
def getIds(lst):
   return [id(val) for val in lst]

