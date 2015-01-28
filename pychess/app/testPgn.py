#!/usr/bin/env python
import unittest, pgn

class pgnTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.parser = pgn.PgnParser()

    def tagParseTest(self, tagString, tagClass):

        self.parser.parseTags(tagString)
        self.assertEqual(self.parser.tags[tagClass.name], tagClass)

    def test_ImportFormatTagParseV1(self):
        tagString = '[ site  "The Internet" ]'
        goldenTag = pgn.Tag("site", "The Internet")

        self.tagParseTest(tagString, goldenTag)

    def test_ImportFormatTagParseV2(self):
        tagString = '[site "The  Internet"]'
        goldenTag = pgn.Tag("site", "The  Internet")

        self.tagParseTest(tagString, goldenTag)

    def test_ImportFormatTagParseV3(self):
        tagString = '    [site"The   Internet"]      '
        goldenTag = pgn.Tag("site", "The   Internet")

        self.tagParseTest(tagString, goldenTag)

    def test_ImportFormatTagParseV4(self):
        tagString = '  [ site"My House"   ]    [Date      "2015.01.28"] '
        goldenTag1 = pgn.Tag("site", "My House")
        goldenTag2 = pgn.Tag("Date", "2015.01.28")

        self.parser.parseTags(tagString)
        self.assertEqual(self.parser.tags[goldenTag1.name], goldenTag1)
        self.assertEqual(self.parser.tags[goldenTag2.name], goldenTag2)




if __name__ == "__main__":
    unittest.main()
