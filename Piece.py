import Util

class Piece(object):
   """Base Piece Class""" 
   def __init__(self,piece="",color="",position=""):
      self.position = ""
      self.color = ""
      self.piece = ""
      self.placed = False
      self.moved = False
      self.lastMove = ()
      self.moveResultReason = "Success"
      if Util.isCoordValid(position):
         self.position = position
         self.placed = True
      if color in [Util.colors.WHITE, Util.colors.BLACK]:
         self.color = color
      if piece in Util.pieces:
         self.piece = piece
            
   def getPieceLetter(self):
      """Returns the letter used to represent this chess piece"""
      if self.piece != "":
         return Util.pieces[self.piece]
      else:
         return " "
            
   def __str__(self):
      """Return the name of this chess piece"""
      returnValue = self.piece
      if returnValue == "":
         return "None"
      else:
         return returnValue
           
   def move(self,coord):
      """Attempt to move this piece, it will fail if the movement places it outside the
         board or if it does not have an initial position"""
      self.moveResultReason = "Success"
      if self.placed:
         if Util.isCoordValid(coord):
            self.lastMove = (self.position, self.moved)
            self.position = coord
            self.moved = True
            return True
         self.moveResultReason = "Destination is not a valid chess square."
         return False
      self.moveResultReason = "Piece has not been placed on the board."
      return False
      
   def undoLastMove(self):
      """Undo the last move performed by this piece"""
      if len(self.lastMove) == 2:
         self.position = self.lastMove[0]
         self.moved = self.lastMove[1]
         self.lastMove = ()
      
         
   def getPath(self, coord, vBoard):
      """This function returns a list of contiguous valid moves between this piece 
         and the coordinate given, exclusive of the destination, inclusive of this piece.
         Please note that if the piece is right next to the target eg Pawn, or jumps to it's 
         target eg Knight, the path will contain only location of the piece"""
      self.getValidMoves(vBoard)
      pathToCoord = [self.position]
      if "paths" in dir(self):
         for path in self.paths:
            if coord in path:
               pathToCoord += path[:path.index(coord)]
      return pathToCoord
         
   def _getMoveValidityAndTermination(self, vBoard, coord):
      """Returns whether or not the move is valid, and if we should stop looking"""
      stopLooking = True
      valid = True
      if not Util.isCoordValid(coord):
         return False, stopLooking
      piece = vBoard.getPiece(coord)
      #If there is no piece here than it is a valid move and we can keep looking
      #If the color is not ours then it is a capture move, but still valid, but we cannot go past
      #If the color is ours then we need to stop
      if piece == None:
         stopLooking = False
      elif piece.color != self.color:
         pass
      else:
         valid = False
      return valid, stopLooking
         
         
class Knight(Piece):
   """A Knight"""
   
   def __init__(self, color, position):
      super(Knight,self).__init__("Knight", color, position)
      
      
   def getValidMoves(self, vBoard):
      """Get the valid moves for a Knight"""
      currentPosition = self.position
      if vBoard.getPiece(currentPosition) == self:
         fileNum = ord(currentPosition[0])
         rankNum = int(currentPosition[1])
         #I probably should break this list comprension up because this is just long, we will see
         physicalMoves = [chr(file) + str(rank) for file in range(fileNum - 2, fileNum + 3) for rank in range(rankNum - 2, rankNum + 3) if (abs(rank-rankNum) == 2 and abs(file-fileNum) == 1) or (abs(rank-rankNum) == 1 and abs(file-fileNum) == 2)]
         validMoves = []
         for move in physicalMoves:
            valid, stop = super(Knight,self)._getMoveValidityAndTermination(vBoard, move)
            if (valid):
               validMoves.append(move)
         return validMoves


class Rook(Piece):
   """A Rook"""

   def __init__(self, color, position):
      super(Rook,self).__init__("Rook", color, position)

   def getValidMoves(self, vBoard):
      """Get the valid moves for a Rook"""
      currentPosition = self.position
      if vBoard.getPiece(currentPosition) == self:
         self.paths = [ [], [], [], [] ]
         continueUp = True
         continueDown = True
         continueLeft = True
         continueRight = True
         keepChecking = True
         fileNum = ord(currentPosition[0])
         rankNum = int(currentPosition[1])
         loopCounter = 1
         validMoves = []
         while keepChecking:
            if continueUp:
               move = chr(fileNum) + str(rankNum+loopCounter)
               valid, stop = super(Rook,self)._getMoveValidityAndTermination(vBoard, move)
               if valid:
                  self.paths[0].append(move)
                  validMoves.append(move)
               continueUp = not stop
            if continueDown:
               move = chr(fileNum) + str(rankNum-loopCounter)
               valid, stop = super(Rook,self)._getMoveValidityAndTermination(vBoard, move)
               if valid:
                  self.paths[1].append(move)
                  validMoves.append(move)
               continueDown = not stop
            if continueLeft:
               move = chr(fileNum-loopCounter) + str(rankNum)
               valid, stop = super(Rook,self)._getMoveValidityAndTermination(vBoard, move)
               if valid:
                  self.paths[2].append(move)
                  validMoves.append(move)
               continueLeft = not stop
            if continueRight:
               move = chr(fileNum+loopCounter) + str(rankNum)
               valid, stop = super(Rook,self)._getMoveValidityAndTermination(vBoard, move)
               if valid:
                  self.paths[3].append(move)
                  validMoves.append(move)
               continueRight = not stop
            loopCounter += 1
            keepChecking = continueUp or continueDown or continueLeft or continueRight
         return validMoves


class Bishop(Piece):
   """A Bishop"""

   def __init__(self, color, position):
      super(Bishop,self).__init__("Bishop", color, position)
      
   
   def getValidMoves(self, vBoard):
      """Get the valid moves for a Bishop"""
      currentPosition = self.position
      if vBoard.getPiece(currentPosition) == self:
         self.paths = [ [], [], [], [] ]
         continueUpperLeft = True
         continueUpperRight = True
         continueLowerLeft = True
         continueLowerRight = True
         keepChecking = True
         fileNum = ord(currentPosition[0])
         rankNum = int(currentPosition[1])
         loopCounter = 1
         validMoves = []
         while keepChecking:
            if continueUpperLeft:
               move = chr(fileNum-loopCounter) + str(rankNum+loopCounter)
               valid, stop = super(Bishop,self)._getMoveValidityAndTermination(vBoard, move)
               if valid:
                  self.paths[0].append(move)
                  validMoves.append(move)
               continueUpperLeft = not stop
            if continueUpperRight:
               move = chr(fileNum+loopCounter) + str(rankNum+loopCounter)
               valid, stop = super(Bishop,self)._getMoveValidityAndTermination(vBoard, move)
               if valid:
                  self.paths[1].append(move)
                  validMoves.append(move)
               continueUpperRight = not stop
            if continueLowerLeft:
               move = chr(fileNum-loopCounter) + str(rankNum-loopCounter)
               valid, stop = super(Bishop,self)._getMoveValidityAndTermination(vBoard, move)
               if valid:
                  self.paths[2].append(move)
                  validMoves.append(move)
               continueLowerLeft = not stop
            if continueLowerRight:
               move = chr(fileNum+loopCounter) + str(rankNum-loopCounter)
               valid, stop = super(Bishop,self)._getMoveValidityAndTermination(vBoard, move)
               if valid:
                  self.paths[3].append(move)
                  validMoves.append(move)
               continueLowerRight = not stop
            loopCounter += 1
            keepChecking = continueUpperLeft or continueUpperRight or continueLowerLeft or continueLowerRight
         return validMoves


class Queen(Piece):
   """A Queen"""
   def __init__(self, color, position):
      super(Queen,self).__init__("Queen", color, position)
      
   
   def getValidMoves(self, vBoard):
      """Get the valid moves for a Queen"""
      currentPosition = self.position
      if vBoard.getPiece(currentPosition) == self:
         self.paths = [ [], [], [], [], [], [], [], [] ]
         continueUpperLeft = True
         continueUpperRight = True
         continueLowerLeft = True
         continueLowerRight = True
         continueUp = True
         continueDown = True
         continueLeft = True
         continueRight = True
         keepChecking = True
         fileNum = ord(currentPosition[0])
         rankNum = int(currentPosition[1])
         loopCounter = 1
         validMoves = []
         while keepChecking:
            if continueUpperLeft:
               move = chr(fileNum-loopCounter) + str(rankNum+loopCounter)
               valid, stop = super(Queen,self)._getMoveValidityAndTermination(vBoard, move)
               if valid:
                  self.paths[0].append(move)
                  validMoves.append(move)
               continueUpperLeft = not stop
            if continueUpperRight:
               move = chr(fileNum+loopCounter) + str(rankNum+loopCounter)
               valid, stop = super(Queen,self)._getMoveValidityAndTermination(vBoard, move)
               if valid:
                  self.paths[1].append(move)
                  validMoves.append(move)
               continueUpperRight = not stop
            if continueLowerLeft:
               move = chr(fileNum-loopCounter) + str(rankNum-loopCounter)
               valid, stop = super(Queen,self)._getMoveValidityAndTermination(vBoard, move)
               if valid:
                  self.paths[2].append(move)
                  validMoves.append(move)
               continueLowerLeft = not stop
            if continueLowerRight:
               move = chr(fileNum+loopCounter) + str(rankNum-loopCounter)
               valid, stop = super(Queen,self)._getMoveValidityAndTermination(vBoard, move)
               if valid:
                  self.paths[3].append(move)
                  validMoves.append(move)
               continueLowerRight = not stop
            if continueUp:
               move = chr(fileNum) + str(rankNum+loopCounter)
               valid, stop = super(Queen,self)._getMoveValidityAndTermination(vBoard, move)
               if valid:
                  self.paths[4].append(move)
                  validMoves.append(move)
               continueUp = not stop
            if continueDown:
               move = chr(fileNum) + str(rankNum-loopCounter)
               valid, stop = super(Queen,self)._getMoveValidityAndTermination(vBoard, move)
               if valid:
                  self.paths[5].append(move)
                  validMoves.append(move)
               continueDown = not stop
            if continueLeft:
               move = chr(fileNum-loopCounter) + str(rankNum)
               valid, stop = super(Queen,self)._getMoveValidityAndTermination(vBoard, move)
               if valid:
                  self.paths[6].append(move)
                  validMoves.append(move)
               continueLeft = not stop
            if continueRight:
               move = chr(fileNum+loopCounter) + str(rankNum)
               valid, stop = super(Queen,self)._getMoveValidityAndTermination(vBoard, move)
               if valid:
                  self.paths[7].append(move)
                  validMoves.append(move)
               continueRight = not stop
            loopCounter += 1
            keepChecking = continueUpperLeft or continueUpperRight or continueLowerLeft or continueLowerRight or continueUp or continueDown or continueLeft or continueRight
         return validMoves


class King(Piece):
   """The King"""
   def __init__(self, color, position):
      super(King,self).__init__("King", color, position)
      
      
   def getValidMoves(self, vBoard):
      """Get the valid moves for the King"""
      currentPosition = self.position
      if vBoard.getPiece(currentPosition) == self:
         fileNum = ord(currentPosition[0])
         rankNum = int(currentPosition[1])
         physicalMoves = [chr(file) + str(rank) for file in range(fileNum - 1, fileNum + 2) for rank in range(rankNum - 1, rankNum + 2) if not file == rank]
         validMoves = []
         for move in physicalMoves:
            valid, stop = super(King,self)._getMoveValidityAndTermination(vBoard, move)
            if (valid):
               validMoves.append(move)
         return validMoves
         
   def getCastleCoords(self):
      pass

class Pawn(Piece):
   """A Pawn"""
   def __init__(self, color, position):
      super(Pawn,self).__init__("Pawn", color, position)
      self.enPassantCapturable = False
      
   def move(self,coord):
      """Attempt to move this piece, it will fail if the movement places it outside the
         board or if it does not have an initial position"""
      self.moveResultReason = "Success"
      if self.placed:
         if Util.isCoordValid(coord):
            self.lastState = (self.position, self.moved, self.enPassantCapturable)
            if self.color.pawnRank in self.position and self.color.pawnChargeRank in coord:
               self.enPassantCapturable = True
            else:
               self.enPassantCapturable = False
            self.position = coord
            self.moved = True
            return True
         self.moveResultReason = "Destination is not a valid chess square."
         return False
      self.moveResultReason = "Piece has not been placed on the board."
      return False
      
   def undoLastMove(self):
      """Undo the last move performed by this piece"""
      if len(self.lastState) == 3:
         self.position = self.lastState[0]
         self.moved = self.lastState[1]
         self.enPassantCapturable = self.lastState[2]
         self.lastState = ()
         
   def getCaptureCoords(self):
      fileNum = ord(self.position[0])
      rankNum = int(self.position[1])
      return [coord for coord in [chr(fileNum-1) + str(rankNum + self.color.pawnRankModifier), chr(fileNum +1) + str(rankNum + self.color.pawnRankModifier)] if Util.isCoordValid(coord)]

   def getValidMoves(self, vBoard):
      """Get the valid moves for a Pawn"""
      currentPosition = self.position
      if vBoard.getPiece(currentPosition) == self:
         fileNum = ord(currentPosition[0])
         rankNum = int(currentPosition[1])
         captures = [ chr(fileNum-1) + str(rankNum + self.color.pawnRankModifier), chr(fileNum +1) + str(rankNum + self.color.pawnRankModifier)]
         regular = [ chr(fileNum) + str(rankNum + self.color.pawnRankModifier) ]
         if (not self.moved):
            regular.append(chr(fileNum) + str(rankNum + (self.color.pawnRankModifier * 2)))
         validMoves = []
         for move in captures:
            if Util.isCoordValid(move):
               piece = vBoard.getPiece(move)
               if piece != None and piece.color != self.color:
                  validMoves.append(move)
         for move in regular:
            if Util.isCoordValid(move):
               piece = vBoard.getPiece(move)
               if piece == None:
                  validMoves.append(move)
               else:
                  #If there is a piece in our regular move path do not continue to the 
                  #(possbily) next move
                  break
         return validMoves
