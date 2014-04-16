#!/usr/bin/python3
import unittest
from Algebra import *

class AlgebraTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.parser = AlgebraicParser()

    def test_CastleString(self):
        castleString = "0-0-0"
        castleClass = AlgebraicMove(castle=True)

        self.parser.setAlgebraicMove(castleString)

        self.assertEqual(castleClass, self.parser.getAlgebraicMoveClass())


if __name__ == "__main__":
    unittest.main()

