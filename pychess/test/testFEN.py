#!/usr/bin/env python3
import unittest
from pychess.app.fen import FEN


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
      self.assertEqual([], self.fen.getBlackPieces())

   def test_getWhitePieces_NoParse(self):
      self.assertEqual([], self.fen.getWhitePieces())

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
   
if __name__ == "__main__":
    unittest.main()
