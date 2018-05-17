#!/usr/bin/env python3
import unittest
from pychess.app.randomizer import *


class RandomizerTest(unittest.TestCase):

   @classmethod
   def setUpClass(cls):
      cls.randomizer = Randomizer()

   def setUp(self):
      self.randomizer.clearGeneratedSets()

   def test_generateSingleSet(self):
      genSet = self.randomizer.generatePieceSet()
      self.assertEqual(1, len(self.randomizer.generatedPieces))
      self.assertEqual(15, len(genSet))

      for piece in genSet:
         self.assertEqual(True, piece in self.randomizer.pieceValues)

   def test_generateMultipleSets_Default(self):
      self.randomizer.generatePieceSets()
      self.assertEqual(10, len(self.randomizer.generatedPieces))

   def test_generateMultipleSets_Specified(self):
      specifiedSets = 7
      self.randomizer.generatePieceSets(specifiedSets)
      self.assertEqual(specifiedSets, len(self.randomizer.generatedPieces))

   def test_setValues(self):
      specifiedSets = { "BBBBBBBBBBBBBBB" : 45,
                        "NNNNNNNNNNNNNNN" : 45,
                        "PPPPPPPPPPPPPPP" : 15,
                        "QQQQQQQQQQQQQQQ" : 135,
                        "RRRRRRRRRRRRRRR" : 75,
                        "BBBNNNNNNPQQQRR" : 65,
                        "BNPQR"           : 21,
                        "ABCDEFGHIJKLMNOPQRSTUVWXYZ" : 21}
      for pieceSet in specifiedSets:
         self.assertEqual(specifiedSets[pieceSet], self.randomizer.getSetValue(pieceSet))
   
if __name__ == "__main__":
    unittest.main()
