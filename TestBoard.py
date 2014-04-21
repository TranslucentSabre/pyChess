#!/usr/bin/python3
import unittest
from Board import *

class VerifyBoardTest(unittest.TestCase):

   def setUp(self):
      self.vBoard = VerifyBoard()
      
   def checkAllSquares(self, pieceList):
      pieceMap = {}
      for piece in pieceList:
         pieceMap[piece.position] = piece
         
      for coord in Util.allCoords:
         piece = self.vBoard.getPiece(coord)
         checkPiece = None
         if coord in pieceMap:
            checkPiece = pieceMap[coord]
         self.assertEqual(checkPiece, piece)
     
   def test_EmptyVerifyBoard(self):
      self.checkAllSquares([])
      
   def test_AddPieceOutsideOfBoard(self):
      pieces = [Pawn(Util.colors.WHITE,"k9")]
      self.vBoard.placePieces(pieces)
      self.checkAllSquares([])
      
   def test_AddPiecesWhenConstructing(self):
      white = Util.colors.WHITE
      black = Util.colors.BLACK
      pieces = [  Pawn(white, "b2"),
                  Knight(white, "b1"),
                  King(white, "e1"),
                  King(black, "e8"),
                  Knight(black, "g8"),
                  Pawn(black, "g7")]
      self.vBoard = VerifyBoard(pieces)
      self.checkAllSquares(pieces)
      
   def test_AddPiecesAfterConstruction(self):
      white = Util.colors.WHITE
      black = Util.colors.BLACK
      pieces = [  Pawn(white, "b2"),
                  Knight(white, "b1"),
                  King(white, "e1"),
                  King(black, "e8"),
                  Knight(black, "g8"),
                  Pawn(black, "g7")]
      self.vBoard.placePieces(pieces)
      self.checkAllSquares(pieces)
      
   def test_AppendAdditionalPieces(self):
      white = Util.colors.WHITE
      black = Util.colors.BLACK
      pieces = [  Pawn(white, "b2"),
                  Knight(white, "b1"),
                  King(white, "e1"),
                  King(black, "e8"),
                  Knight(black, "g8"),
                  Pawn(black, "g7")]
      self.vBoard.placePieces(pieces)
      pieces2 = [ Bishop(white, "c1"),
                  Queen(white, "d1"),
                  Queen(black, "d8"),
                  Bishop(black, "f8")]
      self.vBoard.placePieces(pieces2)
      self.checkAllSquares(pieces+pieces2)
      
   def test_OverwritePieceWhileAppending(self):
      white = Util.colors.WHITE
      black = Util.colors.BLACK
      pieces = [  Pawn(white, "b2"),
                  Knight(white, "b1"),
                  King(white, "e1"),
                  King(black, "e8"),
                  Knight(black, "g8"),
                  Pawn(black, "g7")]
      self.vBoard.placePieces(pieces)
      pieces2 = [ Bishop(white, "c1"),
                  Queen(white, "d1"),
                  Queen(black, "d8"),
                  Bishop(black, "f8"),
                  Pawn(white, "g7")]
      self.vBoard.placePieces(pieces2)
      self.checkAllSquares(pieces[:-1]+pieces2)
   
if __name__ == "__main__":
    unittest.main()

