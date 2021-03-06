import random

class Randomizer(object):
   """Class used to randomly generate sets of chess pieces"""

   def __init__(self):
      self.pieceValues = { "P" : 1,
                           "N" : 3,
                           "B" : 3,
                           "R" : 5,
                           "Q" : 9 }
      self.generatedPieces = {}

   def generatePieceSet(self):
      pieces = []
      while len(pieces) < 15:
         pieces.append(random.choice(list(self.pieceValues.keys())))
      pieceSet = "".join(pieces)
      pieceSetValue = self.getSetValue(pieceSet)
      self.generatedPieces[pieceSet] = pieceSetValue
      return pieceSet

   def generatePieceSets(self, number=10):
      startingSize = len(self.generatedPieces)
      while len(self.generatedPieces) - startingSize < number :
         self.generatePieceSet()

   def clearGeneratedSets(self):
      self.generatedPieces = {}

   def getSetValue(self, pieceSet):
      return self.generatedPieces.get(pieceSet, sum([self.pieceValues.get(piece, 0) for piece in pieceSet]))

   def getPieceSets(self):
      for pieces in self.generatedPieces.keys():
         yield pieces

   def getRandomPieceSet(self):
      try:
         return random.choice(list(self.generatedPieces.keys()))
      except IndexError:
         return None

   def getPieceSetsWithinThreshold(self, otherPieceSet, threshold=5):
      otherValue = self.getSetValue(otherPieceSet)
      possibleMatches = []
      for pieceSet, value in self.generatedPieces.items():
         if value - threshold <= otherValue and otherValue <= value + threshold:
            possibleMatches.append(pieceSet)
      return possibleMatches

   def getPieceSetWithinThreshold(self, otherPieceSet, threshold=5):
      possibleMatches = self.getPieceSetsWithinThreshold(otherPieceSet, threshold)
      try:
         return random.choice(possibleMatches)
      except IndexError:
         return None


