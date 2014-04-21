#!/usr/bin/python3
import unittest
from Board import *
from Piece import *

class VerifyBasePiece(unittest.TestCase):

   def test_PieceLetter(self):
      for pieceName in Util.pieces:
         piece = Piece(pieceName, Util.colors.WHITE, "a1")
         self.assertEqual(piece.getPieceLetter(), Util.pieces[pieceName])
      piece = Piece("Mike", Util.colors.WHITE, "a1")
      self.assertEqual(piece.getPieceLetter(), " ")
      piece = Piece("", Util.colors.WHITE, "a1")
      self.assertEqual(piece.getPieceLetter(), " ")
      
   def test_PieceNameString(self):
      for pieceName in Util.pieces:
         piece = Piece(pieceName, Util.colors.WHITE, "a1")
         self.assertEqual(str(piece), pieceName)
      piece = Piece("Mike", Util.colors.WHITE, "a1")
      self.assertEqual(str(piece), "None")
      piece = Piece("", Util.colors.WHITE, "a1")
      self.assertEqual(str(piece), "None")
      
   def test_PieceStartingCoordinate(self):
      black = Util.colors.BLACK
      invalidCoords = ["tom", "bob", "j2", "a9", "14", "bf"]
      for coord in Util.allCoords:
         piece = Piece("Pawn", black, coord)
         self.assertTrue(piece.placed)
         self.assertEqual(piece.position, coord)
      for coord in invalidCoords:
         piece = Piece("Pawn", black, coord)
         self.assertFalse(piece.placed)
         self.assertEqual(piece.position, "")

if __name__ == "__main__":
    unittest.main()

