#!/usr/bin/env python3
import unittest, pgn

class pgnTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.parser = pgn.PgnParser()

    def setUp(self):
        self.parser.reset()

    def tagParseTest(self, tagStrings, tagClasses):

        for tagString in tagStrings:
            self.assertTrue(self.parser.parseString(tagString))
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

    def test_ImportFormatTagParse_BackslashAndQuotesInString(self):
        tagString = '[site "The Network\\\\The \\"White\\" House"]'
        goldenTag = pgn.Tag('site', 'The Network\The "White" House')

        self.tagParseTest((tagString,), (goldenTag,))


    def test_ImportFormatMoveParse_TwoMovesNoMoveNumber(self):
        moveString = "e4 e6\n"

        self.assertTrue(self.parser.parseString(moveString))
        self.assertEqual("e4", self.parser.moves[0].san)
        self.assertEqual("e6", self.parser.moves[1].san)

    def test_ImportFormatMoveParse_TwoMovesTwoMoveNumbers_NoDots(self):
        moveString = "1 e4  e6  Nf3 2 Kb5\n"

        self.assertTrue(self.parser.parseString(moveString))
        self.assertEqual("e4", self.parser.moves[0].san)
        self.assertEqual("e6", self.parser.moves[1].san)
        self.assertEqual("Nf3", self.parser.moves[2].san)
        self.assertEqual("Kb5", self.parser.moves[3].san)

    def test_ImportFormatMoveParse_TwoMovesTwoMoveNumbers_WithDots(self):
        moveString = "e4 1... e6  2 . Nf3  Kb5\n"

        self.assertTrue(self.parser.parseString(moveString))
        self.assertEqual("e4", self.parser.moves[0].san)
        self.assertEqual("e6", self.parser.moves[1].san)
        self.assertEqual("Nf3", self.parser.moves[2].san)
        self.assertEqual("Kb5", self.parser.moves[3].san)

    def test_ImportFormatMoveParse_MovesWithSuffixAnnotations(self):
        moveString = "e4? 1... e6  2. Nf3!!  Kb5\n"

        self.assertTrue(self.parser.parseString(moveString))
        self.assertEqual("e4", self.parser.moves[0].san)
        self.assertEqual("e6", self.parser.moves[1].san)
        self.assertEqual("Nf3", self.parser.moves[2].san)
        self.assertEqual("Kb5", self.parser.moves[3].san)
        self.assertEqual(2, self.parser.moves[0].nag)
        self.assertEqual(3, self.parser.moves[2].nag)

    def test_ImportFormatMoveParse_MovesWithNag(self):
        moveString = "e4 1... e6 $200  2. Nf3 $34  Kb5\n"

        self.assertTrue(self.parser.parseString(moveString))
        self.assertEqual("e4", self.parser.moves[0].san)
        self.assertEqual("e6", self.parser.moves[1].san)
        self.assertEqual("Nf3", self.parser.moves[2].san)
        self.assertEqual("Kb5", self.parser.moves[3].san)
        self.assertEqual(200, self.parser.moves[1].nag)
        self.assertEqual(34, self.parser.moves[2].nag)

    def test_ImportFormatMoveParse_MovesWithGameTerminationTie(self):
        moveString = "e4 1... e6 2. Nf3 Kb5 1/2-1/2\n"

        self.assertTrue(self.parser.parseString(moveString))
        self.assertEqual("e4", self.parser.moves[0].san)
        self.assertEqual("e6", self.parser.moves[1].san)
        self.assertEqual("Nf3", self.parser.moves[2].san)
        self.assertEqual("Kb5", self.parser.moves[3].san)
        self.assertEqual("1/2-1/2", self.parser.gameTerm)






if __name__ == "__main__":
    unittest.main()
