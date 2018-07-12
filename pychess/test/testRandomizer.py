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
         self.assertTrue(piece in self.randomizer.pieceValues)

   def test_generateMultipleSets_Default(self):
      self.randomizer.generatePieceSets()
      self.assertEqual(10, len(self.randomizer.generatedPieces))

   def test_generateMultipleSets_Specified(self):
      for generatedSets in range(0,101,5):
         with self.subTest(generatedSets=generatedSets):
            self.randomizer.generatePieceSets(generatedSets)
            self.assertEqual(generatedSets, len(self.randomizer.generatedPieces))
            self.randomizer.clearGeneratedSets()

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

   def test_getRandomSet_Empty(self):
      self.assertIsNone(self.randomizer.getRandomPieceSet())

   def test_getRandomSet_NonEmpty(self):
      self.randomizer.generatePieceSets()
      iterations = 10
      while iterations > 0:
         pieceSet = self.randomizer.getRandomPieceSet()
         self.assertIsNotNone(pieceSet)
         self.assertIn(pieceSet, self.randomizer.generatedPieces)
         iterations = iterations - 1 

   def test_getSetsWithinThreshold_Empty(self):
      self.assertEqual([], self.randomizer.getPieceSetsWithinThreshold("QQQQQQQQQQQQQQQ"))

   def test_getSetsWithinThreshold(self):
      self.randomizer.generatePieceSets()
      #Get one set of the ones generated
      pieceSet = list(self.randomizer.generatedPieces.keys())[0]
      for threshold in range(0,21,5):
         with self.subTest(threshold=threshold):
            self.assertEqual([], self.randomizer.getPieceSetsWithinThreshold("QQQQQQQQQQQQQQQ", threshold))
            pieceSets = self.randomizer.getPieceSetsWithinThreshold(pieceSet, threshold)
            self.assertTrue(len(pieceSets) >= 1)
            setValue = self.randomizer.getSetValue(pieceSet)
            for testedSet in pieceSets:
               self.assertTrue(abs(setValue-self.randomizer.getSetValue(testedSet)) <= threshold)
   
   def test_getSetWithinThreshold_Empty(self):
      self.assertEqual(None, self.randomizer.getPieceSetWithinThreshold("QQQQQQQQQQQQQQQ"))

   def test_getSetWithinThreshold(self):
      self.randomizer.generatePieceSets()
      #Get one set of the ones generated
      pieceSet = list(self.randomizer.generatedPieces.keys())[0]
      for threshold in range(0,21,5):
         with self.subTest(threshold=threshold):
            self.assertEqual(None, self.randomizer.getPieceSetWithinThreshold("QQQQQQQQQQQQQQQ", threshold))
            otherSet = self.randomizer.getPieceSetWithinThreshold(pieceSet, threshold)
            setValue = self.randomizer.getSetValue(pieceSet)
            otherValue = self.randomizer.getSetValue(otherSet)
            self.assertTrue(abs(setValue-otherValue) <= threshold)
   
if __name__ == "__main__":
    unittest.main()
