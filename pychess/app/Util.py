from math import ceil

def getTurnStringFromOnesBasedIndex(onesBasedIndex):
    turnString = ""
    numericTurn = int(ceil(onesBasedIndex/float(2)))
    WHITE = 1
    if onesBasedIndex & 1 == WHITE:
        turnString = str(numericTurn)+"."
    else:
        turnString = str(numericTurn)+"..."
    return turnString

def getNextTurnString(turnString):
    if turnString == "0":
        return "1."
    parts = turnString.split(".")
    if len(parts) == 2:
        return parts[0]+"..."
    elif len(parts) == 4:
        return str(int(parts[0])+1)+"."
    else:
        return False

def isCoordValid(coordinate):
   """Returns a boolean indicating whether the given coordinate is a valid chess coordinate"""
   return coordinate in allCoords
files = "abcdefgh"
ranks = "87654321"
allCoords = [file+rank for rank in ranks for file in files]


pieces = { "Pawn" : "P", "Rook" : "R", "Knight" : "N", "Bishop" : "B", "Queen" : "Q", "King" : "K"}
invPieces = {"P" : "Pawn", "R" : "Rook", "N" : "Knight", "B" : "Bishop", "Q" : "Queen", "K" : "King"}

class Castle(object):
   KINGSIDE = "Kingside Castle"
   QUEENSIDE = "Queenside Castle"
   NONE = "None"

class MoveType(object):
   NORMAL = "Normal"
   CAPTURE = "Capture"
   EN_PASSANT = "En Passant"
   KINGSIDECASTLE = Castle.KINGSIDE
   QUEENSIDECASTLE = Castle.QUEENSIDE
   PROMOTION = "Promotion"


class colors(object):
   """Central holding place for my colors"""

   class CommonColor():
      kingsideRookFile = "h"
      kingsideRookMoveFile = "f"
      kingsideKingFile = "g"
      queensideRookFile = "a"
      queensideRookMoveFile = "d"
      queensideKingFile = "c"


   class WHITE(CommonColor):
      name  = "White"
      pawnRank = "2"
      majorRank = "1"
      promotionRank = "8"
      pawnRankModifier = 1

   class BLACK(CommonColor):
      name = "Black"
      pawnRank = "7"
      majorRank = "8"
      promotionRank = "1"
      pawnRankModifier = -1

   class NONE(CommonColor):
      name = "None"
      pawnRank = "0"
      majorRank = "0"
      promotionRank = "0"
      pawnRankModifier = 0
      
