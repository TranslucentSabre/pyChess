#!/usr/bin/python3
import unittest
from Algebra import *

class AlgebraTest(unittest.TestCase):

   @classmethod
   def setUpClass(cls):
      cls.parser = AlgebraicParser()
      
   def stringAndClassCrossConversion(self,moveString,moveClass):
      self.parser.setAlgebraicMove(moveString)
      self.assertEqual(moveClass, self.parser.getAlgebraicMoveClass())

      self.parser.setAlgebraicMove(moveClass)
      self.assertEqual(moveString, self.parser.getAlgebraicMoveString())

   def test_QueenSideCastle(self):
      castleString = "0-0-0"
      castleClass = AlgebraicMove(castle=True)

      self.parser.setAlgebraicMove(castleString)
      self.assertEqual(castleClass, self.parser.getAlgebraicMoveClass())

      castleString = "O-O-O"

      self.stringAndClassCrossConversion(castleString,castleClass)
      
   def test_KingsideSideCastle(self):
      castleString = "0-0"
      castleClass = AlgebraicMove(castle=True, kingside=True)

      self.parser.setAlgebraicMove(castleString)
      self.assertEqual(castleClass, self.parser.getAlgebraicMoveClass())

      castleString = "O-O"

      self.stringAndClassCrossConversion(castleString,castleClass)
        
   def test_BasicPawn(self):
      moveString = "e3"
      moveClass = AlgebraicMove( destination="e3",
                                 piece="Pawn",
                                 disambiguation="", 
                                 capture=False, 
                                 promotion="", 
                                 check=False, 
                                 mate=False)
                                 
      self.stringAndClassCrossConversion(moveString,moveClass)
      
if __name__ == "__main__":
    unittest.main()

