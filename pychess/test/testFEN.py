#!/usr/bin/env python3
import unittest
from pychess.app.Util import colors
from pychess.app.fen import FEN,Pieces
from pychess.app import Piece


class FENTest(unittest.TestCase):

   @classmethod
   def setUpClass(cls):
      cls.fen = FEN()

   def setUp(self):
      self.fen.reset()

   def test_isParseValid_NoParse(self):
      self.assertFalse(self.fen.getParseValid())

   def test_parseErrors_NoParse(self):
      self.assertEqual("No parse attempted", self.fen.getParseErrors())

   def test_getBlackPieces_NoParse(self):
      self.assertEqual([], self.fen.getBlackPieces().pawns)
      self.assertEqual([], self.fen.getBlackPieces().rooks)
      self.assertEqual([], self.fen.getBlackPieces().knights)
      self.assertEqual([], self.fen.getBlackPieces().bishops)
      self.assertEqual([], self.fen.getBlackPieces().queens)
      self.assertEqual(None, self.fen.getBlackPieces().king)

   def test_getWhitePieces_NoParse(self):
      self.assertEqual([], self.fen.getWhitePieces().pawns)
      self.assertEqual([], self.fen.getWhitePieces().rooks)
      self.assertEqual([], self.fen.getWhitePieces().knights)
      self.assertEqual([], self.fen.getWhitePieces().bishops)
      self.assertEqual([], self.fen.getWhitePieces().queens)
      self.assertEqual(None, self.fen.getWhitePieces().king)

   def test_getNextPlayer_NoParse(self):
      self.assertEqual("", self.fen.getNextPlayer())
   
   def test_getHalfmoveClock_NoParse(self):
      self.assertEqual("", self.fen.getHalfmoveClock())
   
   def test_getFullmoveClock_NoParse(self):
      self.assertEqual("", self.fen.getFullmoveClock())
   
   def test_getFENString_NoParse(self):
      self.assertEqual("", self.fen.getFENString())

   def test_parse_standard(self):
      self.assertTrue(self.fen.parse())
      self.assertEqual("", self.fen.getParseErrors())

   def test_parse_bad_positions(self):
      testFen = "rnbqkbnr/pppppppp/8/9/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
      error = "Rank 5 should be 8 files, there are 9, or it has invalid pieces.\n"
      self.assertFalse(self.fen.parse(testFen))
      self.assertEqual(error, self.fen.getParseErrors())

   def test_parse_bad_next_player(self):
      testFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR h KQkq - 0 1"
      error = "Next player token must be either b or w.\n"
      self.assertFalse(self.fen.parse(testFen))
      self.assertEqual(error, self.fen.getParseErrors())

   def test_parse_bad_castle_dash(self):
      testFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQ-kq - 0 1"
      error = "Invalid character '-' in castle specification.\n"
      self.assertFalse(self.fen.parse(testFen))
      self.assertEqual(error, self.fen.getParseErrors())
   
   def test_parse_bad_castle_other(self):
      testFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b mike - 0 1"
      error = """Invalid character 'm' in castle specification.
Invalid character 'i' in castle specification.
Invalid character 'e' in castle specification.
"""
      self.assertFalse(self.fen.parse(testFen))
      self.assertEqual(error, self.fen.getParseErrors())
   
   def test_parse_good_enPassant(self):
      testFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq e2 0 1"
      error = ""
      self.assertTrue(self.fen.parse(testFen))
      self.assertEqual(error, self.fen.getParseErrors())

   def test_parse_bad_enPassant(self):
      testFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq 14 0 1"
      error = "En Passant value of '14' is not valid.\n"
      self.assertFalse(self.fen.parse(testFen))
      self.assertEqual(error, self.fen.getParseErrors())
   
   def test_parse_bad_halfmove(self):
      testFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - a 1"
      error = "Halfmove clock is not an integer.\n"
      self.assertFalse(self.fen.parse(testFen))
      self.assertEqual(error, self.fen.getParseErrors())
   
   def test_parse_bad_fullmove(self):
      testFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 b"
      error = "Fullmove clock is not an integer.\n"
      self.assertFalse(self.fen.parse(testFen))
      self.assertEqual(error, self.fen.getParseErrors())
   
   def test_parse_bad_sky_is_falling(self):
      testFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNKBNR k KhQkq er h b"
      error = """Rank 1 should be 8 files, there are 6, or it has invalid pieces.
Next player token must be either b or w.
Invalid character 'h' in castle specification.
En Passant value of 'er' is not valid.
Halfmove clock is not an integer.
Fullmove clock is not an integer.
"""
      self.assertFalse(self.fen.parse(testFen))
      self.assertEqual(error, self.fen.getParseErrors())

   def test_add_king(self):
      testKing = Piece.King(colors.WHITE,"e1")
      pieces = Pieces()
      pieces.createKing(colors.WHITE,"e1","","")
      self.assertEqual(testKing,pieces.pieces[colors.WHITE].king)
   
   
if __name__ == "__main__":
    unittest.main()
