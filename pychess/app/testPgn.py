#!/usr/bin/env python
import unittest, pgn

class pgnTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.parser = pgn.PgnParser()

    def test_ImportFormatTagParseV1(self):
        tagString = '[ site  "The Internet" ]'
        goldenTag = pgn.Tag("site", "The Internet", "string")

        tagClass = self.parser.parseTag(tagString)
        self.assertEqual(goldenTag, tagClass)


if __name__ == "__main__":
    unittest.main()
