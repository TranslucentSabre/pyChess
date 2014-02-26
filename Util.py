
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

   class CommonColorEnums(object):
      kingsideRookFile = "h"
      kingsideKingFile = "g"
      queensideRookFile = "a"
      queensideKingFile = "c"
      
      def __str__(self):
         return self.name

   class WHITE(CommonColorEnums):
      name  = "white"
      pawnRank = "2"
      majorRank = "1"
      promotionRank = "8"
      pawnChargeRank = "4"
      pawnRankModifier = 1
      
   class BLACK(CommonColorEnums):
      name = "black"
      pawnRank = "7"
      majorRank = "8"
      promotionRank = "1"
      pawnChargeRank = "5"
      pawnRankModifier = -1


