import random

class randomizer(object):
   """Class used to randomly generate sets of chess pieces"""

   def __init__(self):
      self.pieceValues = { "P" : 1,
                           "N" : 3,
                           "B" : 3,
                           "R" : 5,
                           "Q" : 9 }
      self.generatedPieces = {}
      self.generatedPiecesReverse = {}

   def generatePieceSet(self):
      pieces = []
      while len(pieces) < 15:
         pieces.append(random.choice(list(self.pieceValues.keys())))
      pieceSet = "".join(sorted(pieces))
      pieceSetValue = self.getSetValue(pieceSet)
      self.generatedPieces[pieceSet] = pieceSetValue
      valueSets = self.generatedPiecesReverse.get(pieceSetValue, [])
      valueSets.append(pieceSet)
      self.generatedPiecesReverse[pieceSetValue] = valueSets
      return pieceSet

   def generatePieceSets(self, number=10):
      while number > 0:
         getter.generatePieceSet()
         number = number - 1


   def getSetValue(self, pieceSet):
      return sum([self.pieceValues.get(piece, 0) for piece in pieceSet])

if __name__ == "__main__":
   getter = randomizer()
   print(getter.generatePieceSet())
   print(getter.generatePieceSet())
   print(getter.generatePieceSet())
   print(getter.generatedPieces)
   print(getter.getSetValue("ABCDEFGHIJKLMNPQRSTUVWXYZ"))
   getter.generatePieceSets()
   print(getter.generatedPieces)
   print(getter.generatedPiecesReverse)

