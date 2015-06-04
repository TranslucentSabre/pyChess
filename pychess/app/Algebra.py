#!/usr/bin/env python3
import re
import pychess.app.Piece
from pychess.app import Util


class AlgebraicMove(object):

   def __init__(self, destination="a1", piece="Pawn", disambiguation="", capture=False, promotion="", check=False, mate=False, castle=False, kingside=False):
      self.destination = destination
      self.piece = piece
      self.disambiguation = disambiguation
      self.capture = capture
      self.promotion = promotion
      self.check = check
      self.mate = mate

      self.castle = castle
      self.kingside = kingside

   def __str__(self):
      retString = ""
      for item in dir(self):
         if not item.startswith("_"):
            value = getattr(self, item)
            retString += item + ": "+ str(value) + "; "
      return retString

   def __eq__(self, other):
      if type(other) != AlgebraicMove:
         return NotImplemented
      if self.destination == other.destination and \
         self.piece == other.piece and \
         self.disambiguation == other.disambiguation and \
         self.capture == other.capture and \
         self.promotion == other.promotion and \
         self.check == other.check and \
         self.mate == other.mate and \
         self.castle == other.castle and \
         self.kingside == other.kingside:
         return True
      else:
         return False

class AlgebraicParser(object):
   pieces = r"[RNBQK]"
   promotionPieces = r"[RNBQ]"
   ranks = r"[1-8]"
   files = r"[a-h]"
   rePieceString = r"("+pieces+")?"
   reDisambiguationString = r"(?:("+files+")?("+ranks+")?)"
   reCaptureString = r"(x)?"
   reDestinationString = r"("+files+ranks+")"
   rePromotionString = r"(?:=("+promotionPieces+"))?"
   reCheckMateString = r"(\+|#)?"
   rePGNCastleString = "O-(O-)?O"
   reCastleString = "0-(0-)?0"
   reString = r"\A"+rePieceString + reDisambiguationString + reCaptureString \
            + reDestinationString + rePromotionString + reCheckMateString + r"\Z"

   def __init__(self):
      self.castle = re.compile(self.reCastleString)
      self.pgnCastle = re.compile(self.rePGNCastleString)
      self.move = re.compile(self.reString)
      self.moveString = ""
      self.moveClass = None
      self.valid = False

   def setAlgebraicMove(self, move):
      if type(move) == str:
         self.setAlgebraicMoveUsingString(move)
      elif type(move) == AlgebraicMove:
         self.setAlgebraicMoveUsingClass(move)
      else:
         return

   def getAlgebraicMoveString(self):
      return self.moveString

   def getAlgebraicMoveClass(self):
      return self.moveClass

   def setAlgebraicMoveUsingString(self, move):
      """Generate our internal AlgebraicMove class and use that to reset the string"""
      self.moveString = move
      castleMatch = self.castle.match(move)
      if not castleMatch:
        castleMatch = self.pgnCastle.match(move)
      regularMatch = self.move.match(move)
      if castleMatch:
         kingsideCastle = self.isKingsideCastleFromMatch(castleMatch.group(1))
         move = AlgebraicMove(castle=True, kingside=kingsideCastle)
         self.valid = self.setAlgebraicMoveUsingClass(move)
      elif regularMatch:
         subs = regularMatch.groups()
         piece = self.getPieceStringFromMatch(subs[0])
         disambiguation = self.getDisambiguationFromMatches(subs[1], subs[2])
         capture = self.isCaptureFromMatch(subs[3])
         promotion = self.getPieceStringFromMatch(subs[5], True)
         check = self.isCheckFromMatch(subs[6])
         mate = self.isMateFromMatch(subs[6])
         move = AlgebraicMove(subs[4], piece, disambiguation, capture, promotion, check, mate, False, False)
         self.valid = self.setAlgebraicMoveUsingClass(move)
      else:
         self.setAlgebraicMoveUsingClass(AlgebraicMove())
         self.valid = False
      return self.valid

   def isKingsideCastleFromMatch(self, matchValue):
      if matchValue != None:
         return False
      else:
         return True

   def getPieceStringFromMatch(self, matchValue, pawnPossible=False):
      piece = ""
      if matchValue != None:
         piece = Util.invPieces[matchValue]
      else:
         if not pawnPossible:
            piece = "Pawn"
      return piece

   def getDisambiguationFromMatches(self, fileValue, rankValue):
      disambiguation = ""
      if fileValue != None:
         disambiguation += fileValue
      if rankValue != None:
         disambiguation += rankValue
      return disambiguation

   def isCaptureFromMatch(self, matchValue):
      capture = False
      if matchValue != None:
         capture = True
      return capture

   def isCheckFromMatch(self, matchValue):
      check = False
      #If we are mated then we are also checked
      if matchValue != None and matchValue == "+" or matchValue == "#":
         check = True
      return check

   def isMateFromMatch(self, matchValue):
      mate = False
      if matchValue != None and matchValue == "#":
         mate = True
      return mate

   def setAlgebraicMoveUsingClass(self, move):
      """Set the passed in move class and generate our move string based upon it"""
      self.moveClass = move

      if self.moveClass.castle == True:
         self.valid = True
         self.moveString = self.getCastleStringFromClass(self.moveClass.kingside)

      else:
         self.valid = True
         self.moveString = ""
         self.moveString += self.getPieceStringFromClassAndValidate(self.moveClass.piece)
         self.moveString += self.getDisambiguationStringFromClassAndValidate(self.moveClass.disambiguation)
         self.moveString += self.getCaptureStringFromClass(self.moveClass.capture)
         self.moveString += self.getDestinationStringFromClassAndValidate(self.moveClass.destination)
         self.moveString += self.getPromotionStringFromClassAndValidate(self.moveClass.promotion, self.moveClass.piece)
         self.moveString += self.getCheckMateStringFromClassAndValidate(self.moveClass.check, self.moveClass.mate)

      return self.valid

   def getCastleStringFromClass(self, classValue):
      castleStr = "O-"
      if classValue == False:
         castleStr += "O-"
      castleStr += "O"
      return castleStr

   def getPieceStringFromClassAndValidate(self, classValue):
      pieceStr = ""
      if classValue != "Pawn":
         if classValue in Util.pieces:
            pieceStr = Util.pieces[classValue]
         else:
            self.valid = False
            pieceStr = classValue
      return pieceStr

   def getDisambiguationStringFromClassAndValidate(self, classValue):
      disambigLen = len(classValue)
      if disambigLen > 2:
         self.valid = False
      elif disambigLen == 2 and not Util.isCoordValid(classValue):
         self.valid = False
      elif disambigLen == 1 and not (classValue in Util.ranks or classValue in Util.files):
         self.valid = False
      return classValue

   def getCaptureStringFromClass(self, classValue):
      captureStr = ""
      if classValue:
         captureStr += "x"
      return captureStr

   def getDestinationStringFromClassAndValidate(self, classValue):
      destLen = len(classValue)
      if destLen > 2 or destLen == 0:
         self.valid = False
      elif destLen == 2 and not Util.isCoordValid(classValue):
         self.valid = False
      return classValue

   def getPromotionStringFromClassAndValidate(self, classPromoteValue, classPieceValue):
      promotionStr = ""
      if classPieceValue != "Pawn" and classPromoteValue != "":
         self.valid = False
      if classPromoteValue != "":
         if classPromoteValue in Util.pieces:
            promotionStr += "="+Util.pieces[classPromoteValue]
         else:
            self.valid = False
            promotionStr += "="+classPromoteValue
      return promotionStr

   def getCheckMateStringFromClassAndValidate(self, classCheckValue, classMateValue):
      checkOrMate = ""
      #If we are mated then we are also checked, so make sure that both flags are true before signalling mate
      if classMateValue:
         if classCheckValue:
            checkOrMate += "#"
         else:
            self.valid = False
      elif classCheckValue:
         checkOrMate += "+"
      return checkOrMate





if __name__ == "__main__":
   print("Algebraic Notation Module")

   parser = AlgebraicParser()
   print(parser.move.pattern)
   print(parser.castle.pattern)
   print(parser.pgnCastle.pattern)

   def setAndDisplay(move):
      parser.setAlgebraicMove(move)
      print(parser.getAlgebraicMoveString())
      print(parser.getAlgebraicMoveClass())
      print("VALIDITY: "+ str(parser.valid))
      print("")

   def areMovesTheSame(move1, move2):
      print(move1)
      print(move2)
      print(str(move1 == move2))

   setAndDisplay("Pe4")
   setAndDisplay("Be4")
   setAndDisplay("Nxe4#")
   setAndDisplay("bxa8=Q+#")
   setAndDisplay("B5c1")
   setAndDisplay("O-O")
   setAndDisplay("O-O-O")
   setAndDisplay("0-0")
   setAndDisplay("0-0-0")


   #def destination,
   #piece="Pawn",
   #disambiguation="",
   #capture=False,
   #promotion="",
   #check=False,
   #mate=False,
   #castle=False,
   #kingside=False):
   setAndDisplay(AlgebraicMove("h8", "Pawn", "g", True, "Rook", False, False))
   setAndDisplay(AlgebraicMove("e2", "King", "", False, "", False, False))
   setAndDisplay(AlgebraicMove("a6", "Queen", "", True, "", True, True))
   setAndDisplay(AlgebraicMove(castle=True, kingside=False))

   areMovesTheSame(AlgebraicMove("a1", "Bishop", "", False, "", False, False, False, False), \
                   AlgebraicMove("a1", "Bishop", "", False, "", False, False, False, False))
   areMovesTheSame(AlgebraicMove("f3", "Rook", "e", False, "", True, False, True, False), \
                   AlgebraicMove("f3", "Rook", "e", False, "", True, False, False, False))
   areMovesTheSame("Ref3+", \
                   AlgebraicMove("f3", "Rook", "e", False, "", True, False, True, False))
