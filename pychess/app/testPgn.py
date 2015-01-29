#!/usr/bin/env python
import unittest, pgn

class pgnTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.parser = pgn.PgnParser()

    def setUp(self):
        self.parser.reset()

    def tagParseTest(self, tagStrings, tagClasses):

        for tagString in tagStrings:
            self.assertTrue(self.parser.parseTags(tagString))
        for tagClass in tagClasses:
            self.assertEqual(self.parser.tags[tagClass.name], tagClass)

    def test_ImportFormatTagParse_Freeform(self):
        tagString = '[ site  "The Internet" ]'
        goldenTag = pgn.Tag("site", "The Internet")

        self.tagParseTest((tagString,), (goldenTag,))

    def test_ImportFormatTagParse_Export(self):
        tagString = '[site "The  Internet"]'
        goldenTag = pgn.Tag("site", "The  Internet")

        self.tagParseTest((tagString,), (goldenTag,))

    def test_ImportFormatTagParse_NoSpaces(self):
        tagString = '    [site"The   Internet"]      '
        goldenTag = pgn.Tag("site", "The   Internet")

        self.tagParseTest((tagString,), (goldenTag,))

    def test_ImportFormatTagParse_TwoTagsOneLine(self):
        tagString = '  [ site"My House"   ]    [Date      "2015.01.28"] '
        goldenTag1 = pgn.Tag("site", "My House")
        goldenTag2 = pgn.Tag("Date", "2015.01.28")

        self.tagParseTest((tagString,), (goldenTag1, goldenTag2))

    def test_ImportFormatTagParse_QuotesInString(self):
        tagString = '[event "The best \\"Game\\" In the place"]'
        goldenTag = pgn.Tag('event', 'The best "Game" In the place')

        self.tagParseTest((tagString,), (goldenTag,))

    def test_ImportFormatTagParse_TagOverMultipleStrings(self):
        tagString1 = '[ site  '
        tagString2 = '  "The Internet"]'
        goldenTag = pgn.Tag("site", "The Internet")

        self.tagParseTest((tagString1, tagString2), (goldenTag,))

    def test_ImportFormatTagParse_TagInOneStringMultipleLines(self):
        tagString = '[   \ndate  "2014.12.31" ]'
        goldenTag = pgn.Tag("date", "2014.12.31")

        self.tagParseTest((tagString,), (goldenTag,))





if __name__ == "__main__":
    unittest.main()
