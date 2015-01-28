#!/usr/bin/env python
import unittest, pgn

class pgnTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.parser = pgn.PgnParser()

    def tagParseTest(self, tagString, *tagClasses):

        self.assertTrue(self.parser.parseTags(tagString))
        for tagClass in tagClasses:
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

        self.tagParseTest(tagString, goldenTag1, goldenTag2)

    def test_ImportFormatTagParseV5(self):
        tagString = '[event "The best \\"Game\\" In the place"]'
        goldenTag = pgn.Tag('event', 'The best "Game" In the place')

        self.tagParseTest(tagString, goldenTag)




if __name__ == "__main__":
    unittest.main()
