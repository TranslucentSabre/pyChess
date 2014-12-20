
def isCoordValid(coordinate):
   """Returns a boolean indicating whether the given coordinate is a valid chess coordinate"""
   return coordinate in allCoords
files = "abcdefgh"
ranks = "87654321"
allCoords = [file+rank for rank in ranks for file in files]


pieces = { "Pawn" : "P", "Rook" : "R", "Knight" : "N", "Bishop" : "B", "Queen" : "Q", "King" : "K"}
invPieces = {"P" : "Pawn", "R" : "Rook", "N" : "Knight", "B" : "Bishop", "Q" : "Queen", "K" : "King"}

class Castle(object):
   KINGSIDE = "kingside"
   QUEENSIDE = "queenside"
   NONE = "none"

class MoveType(object):
   NORMAL = "normal"
   CAPTURE = "capture"
   EN_PASSANT = "enPassant"
   KINGSIDECASTLE = Castle.KINGSIDE
   QUEENSIDECASTLE = Castle.QUEENSIDE
   PROMOTION = "promotion"


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
      name  = "white"
      pawnRank = "2"
      majorRank = "1"
      promotionRank = "8"
      pawnChargeRank = "4"
      pawnRankModifier = 1

   class BLACK(CommonColor):
      name = "black"
      pawnRank = "7"
      majorRank = "8"
      promotionRank = "1"
      pawnChargeRank = "5"
      pawnRankModifier = -1

   class NONE(CommonColor):
      name = "none"
      pawnRank = "0"
      majorRank = "0"
      promotionRank = "0"
      pawnChargeRank = "0"
      pawnRankModifier = 0
      
