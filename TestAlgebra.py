#!/usr/bin/python
import unittest
from Algebra import *

class AlgebraTest(unittest.TestCase):

   @classmethod
   def setUpClass(cls):
      cls.parser = AlgebraicParser()
      
   def stringAndClassCrossConversion(self,moveString,moveClass):
      self.parser.setAlgebraicMove(moveClass)
      self.assertEqual(moveString, self.parser.getAlgebraicMoveString())
      
      self.parser.setAlgebraicMove(moveString)
      self.assertEqual(moveClass, self.parser.getAlgebraicMoveClass())

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
        
   def test_PawnBasic(self):
      moveString = "e3"
      moveClass = AlgebraicMove( destination="e3",
                                 piece="Pawn",
                                 disambiguation="", 
                                 capture=False, 
                                 promotion="", 
                                 check=False, 
                                 mate=False)
                                 
      self.stringAndClassCrossConversion(moveString,moveClass)
      
   def test_PawnCapture(self):
      moveString = "dxe3"
      moveClass = AlgebraicMove( destination="e3",
                                 piece="Pawn",
                                 disambiguation="d", 
                                 capture=True, 
                                 promotion="", 
                                 check=False, 
                                 mate=False)
                                 
      self.stringAndClassCrossConversion(moveString,moveClass)
      
   def test_PawnCapturePromotion(self):
      moveString = "cxb8=Q"
      moveClass = AlgebraicMove( destination="b8",
                                 piece="Pawn",
                                 disambiguation="c", 
                                 capture=True, 
                                 promotion="Queen", 
                                 check=False, 
                                 mate=False)
                                 
      self.stringAndClassCrossConversion(moveString,moveClass)
      
   def test_PawnCaptureMate(self):
      moveString = "dxe3#"
      moveClass = AlgebraicMove( destination="e3",
                                 piece="Pawn",
                                 disambiguation="d", 
                                 capture=True, 
                                 promotion="", 
                                 check=True, 
                                 mate=True)
                                 
      self.stringAndClassCrossConversion(moveString,moveClass)
      
   def test_PawnCheck(self):
      moveString = "f6+"
      moveClass = AlgebraicMove( destination="f6",
                                 piece="Pawn",
                                 disambiguation="", 
                                 capture=False, 
                                 promotion="", 
                                 check=True, 
                                 mate=False)
                                 
      self.stringAndClassCrossConversion(moveString,moveClass)
      
   def test_RookBasic(self):
      moveString = "Ra4"
      moveClass = AlgebraicMove( destination="a4",
                                 piece="Rook",
                                 disambiguation="", 
                                 capture=False, 
                                 promotion="", 
                                 check=False, 
                                 mate=False)
                                 
      self.stringAndClassCrossConversion(moveString,moveClass)
      
   def test_RookCapture(self):
      moveString = "Rxe3"
      moveClass = AlgebraicMove( destination="e3",
                                 piece="Rook",
                                 disambiguation="", 
                                 capture=True, 
                                 promotion="", 
                                 check=False, 
                                 mate=False)
                                 
      self.stringAndClassCrossConversion(moveString,moveClass)
      
   def test_RookCaptureDisambiguation(self):
      moveString = "R2xb8"
      moveClass = AlgebraicMove( destination="b8",
                                 piece="Rook",
                                 disambiguation="2", 
                                 capture=True, 
                                 promotion="", 
                                 check=False, 
                                 mate=False)
                                 
      self.stringAndClassCrossConversion(moveString,moveClass)
      
   def test_RookMate(self):
      moveString = "Re3#"
      moveClass = AlgebraicMove( destination="e3",
                                 piece="Rook",
                                 disambiguation="", 
                                 capture=False, 
                                 promotion="", 
                                 check=True, 
                                 mate=True)
                                 
      self.stringAndClassCrossConversion(moveString,moveClass)
      
   def test_RookCaptureCheck(self):
      moveString = "Rxf6+"
      moveClass = AlgebraicMove( destination="f6",
                                 piece="Rook",
                                 disambiguation="", 
                                 capture=True, 
                                 promotion="", 
                                 check=True, 
                                 mate=False)
                                 
      self.stringAndClassCrossConversion(moveString,moveClass)
         
   def test_KnightBasic(self):
      moveString = "Nc6"
      moveClass = AlgebraicMove( destination="c6",
                                 piece="Knight",
                                 disambiguation="", 
                                 capture=False, 
                                 promotion="", 
                                 check=False, 
                                 mate=False)
                                 
      self.stringAndClassCrossConversion(moveString,moveClass)
      
   def test_KnightCapture(self):
      moveString = "Nxe3"
      moveClass = AlgebraicMove( destination="e3",
                                 piece="Knight",
                                 disambiguation="", 
                                 capture=True, 
                                 promotion="", 
                                 check=False, 
                                 mate=False)
                                 
      self.stringAndClassCrossConversion(moveString,moveClass)
      
   def test_KnightCaptureDisambiguation(self):
      moveString = "Naxb8"
      moveClass = AlgebraicMove( destination="b8",
                                 piece="Knight",
                                 disambiguation="a", 
                                 capture=True, 
                                 promotion="", 
                                 check=False, 
                                 mate=False)
                                 
      self.stringAndClassCrossConversion(moveString,moveClass)
      
   def test_KnightMate(self):
      moveString = "Ne3#"
      moveClass = AlgebraicMove( destination="e3",
                                 piece="Knight",
                                 disambiguation="", 
                                 capture=False, 
                                 promotion="", 
                                 check=True, 
                                 mate=True)
                                 
      self.stringAndClassCrossConversion(moveString,moveClass)
      
   def test_KnightCaptureCheck(self):
      moveString = "Nxf6+"
      moveClass = AlgebraicMove( destination="f6",
                                 piece="Knight",
                                 disambiguation="", 
                                 capture=True, 
                                 promotion="", 
                                 check=True, 
                                 mate=False)
                                 
      self.stringAndClassCrossConversion(moveString,moveClass)
      
if __name__ == "__main__":
    unittest.main()

