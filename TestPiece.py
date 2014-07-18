#!/usr/bin/python
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

   def test_PieceMovement(self):
      black = Util.colors.BLACK
      piece = Piece("Bishop", black, "")
      success = piece.move("b5")
      self.assertFalse(success)
      self.assertFalse(piece.moved)
      self.assertEqual(piece.moveResultReason, "Piece has not been placed on the board.")

      piece = Piece("Bishop", black , "b5")
      success = piece.move("c10")
      self.assertFalse(success)
      self.assertFalse(piece.moved)
      self.assertEqual(piece.moveResultReason, "Destination is not a valid chess square.")

      success = piece.move("c5")
      self.assertTrue(success)
      self.assertTrue(piece.moved)
      self.assertEqual(piece.position, "c5")
      self.assertEqual(piece.moveResultReason, "Success")


   def test_PieceUndoMovement(self):
      white = Util.colors.WHITE
      previousLocation = "b5"
      piece = Piece("Rook", white, previousLocation)
      movements = [("c2", False), ("g4", True), ("a8", True)]
      for move, movedPreviously in movements:
         piece.move(move)
         self.assertTrue(piece.moved)
         self.assertEqual(piece.position, move)
         self.assertEqual(piece.lastMove, (previousLocation, movedPreviously))
         piece.undoLastMove()
         self.assertEqual(piece.moved, movedPreviously)
         self.assertEqual(piece.position, previousLocation)
         piece.move(move)
         self.assertTrue(piece.moved)
         self.assertEqual(piece.position, move)
         self.assertEqual(piece.lastMove, (previousLocation, movedPreviously))
         previousLocation = move

class VerifySpecificPiece(unittest.TestCase):
   white = Util.colors.WHITE
   black = Util.colors.BLACK
   def VerifyMovement(self, pieceString, moveDict, otherPieces=[], pieceColor=Util.colors.BLACK):
      for origin in moveDict:
         piece = globals()[pieceString](pieceColor, origin);
         computedDestinations = piece.getValidMoves(VerifyBoard(otherPieces+[piece]))
         computedDestinations.sort()
         moveDict[origin].sort()
         self.assertEqual(computedDestinations, moveDict[origin])

   def CreatePieces(self, pieceDict, pieceColor):
      pieceList = []
      for coord in pieceDict:
         pieceList.append(globals()[pieceDict[coord]](pieceColor, coord))
      return pieceList

class VerifyKnight(VerifySpecificPiece):

   def test_PieceReadsAsKnight(self):
      knight = Knight(self.white, "c3")

      self.assertEqual(knight.getPieceLetter(), "N")
      self.assertEqual(str(knight), "Knight")
      
   def test_KnightGetMovesOnEmptyBoard(self):
      moveDict = { "a1" : ["b3", "c2"],
                   "c3" : ["b1", "d1", "a2", "a4", "b5", "d5", "e2", "e4"],
                   "e8" : ["c7", "d6", "f6", "g7"],
                   "a3" : ["b5", "c4", "c2", "b1"],
                   "g5" : ["h3", "f3", "e4", "e6", "f7", "h7"] }

      self.VerifyMovement("Knight", moveDict)

   def test_KnightGetMovesWithEnemyPieces(self):
      pieceDict = { "b3" : "Pawn",
                    "b1" : "Pawn",
                    "c7" : "Bishop" }
      moveDict = { "a1" : ["b3", "c2"],
                   "c3" : ["b1", "d1", "a2", "a4", "b5", "d5", "e2", "e4"],
                   "e8" : ["c7", "d6", "f6", "g7"],
                   "a3" : ["b5", "c4", "c2", "b1"],
                   "g5" : ["h3", "f3", "e4", "e6", "f7", "h7"] }
      pieceList = self.CreatePieces(pieceDict,self.white)
      self.VerifyMovement("Knight", moveDict, pieceList, self.black)

   def test_KnightGetMovesWithAlliedPieces(self):
      pieceDict = { "b3" : "Pawn",
                    "b1" : "Pawn",
                    "c7" : "Bishop" }
      moveDict = { "a1" : ["c2"],
                   "c3" : ["d1", "a2", "a4", "b5", "d5", "e2", "e4"],
                   "e8" : ["d6", "f6", "g7"],
                   "a3" : ["b5", "c4", "c2",],
                   "g5" : ["h3", "f3", "e4", "e6", "f7", "h7"] }
      pieceList = self.CreatePieces(pieceDict,self.white)
      self.VerifyMovement("Knight", moveDict, pieceList, self.white)

if __name__ == "__main__":
    unittest.main()

