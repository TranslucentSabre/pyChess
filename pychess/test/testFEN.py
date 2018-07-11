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

   
if __name__ == "__main__":
    unittest.main()
