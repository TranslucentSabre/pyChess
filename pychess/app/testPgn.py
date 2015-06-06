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


    def test_ImportFormatMoveParse_MovesWithGameTerminationOngoing(self):
        moveString = "1 e4 e6 2. Nf3 2 Kb5 *\n"

        self.assertTrue(self.parser.parseString(moveString))
        self.assertEqual("e4", self.parser.moves[0].san)
        self.assertEqual("e6", self.parser.moves[1].san)
        self.assertEqual("Nf3", self.parser.moves[2].san)
        self.assertEqual("Kb5", self.parser.moves[3].san)
        self.assertEqual("*", self.parser.gameTerm)


    def test_ImportFormatMoveParse_MovesWithGameTerminationOngoingAfterNag(self):
        moveString = "1 e4 e6 2. Nf3 2 Kb5 $156 *\n"

        self.assertTrue(self.parser.parseString(moveString))
        self.assertEqual("e4", self.parser.moves[0].san)
        self.assertEqual("e6", self.parser.moves[1].san)
        self.assertEqual("Nf3", self.parser.moves[2].san)
        self.assertEqual("Kb5", self.parser.moves[3].san)
        self.assertEqual(156, self.parser.moves[3].nag)
        self.assertEqual("*", self.parser.gameTerm)

    def test_ImportFormatMoveParse_MovesWithGameTerminationWhiteWins(self):
        moveString = "e4 1... e6 2. Nf3 Kb5 1-0\n"

        self.assertTrue(self.parser.parseString(moveString))
        self.assertEqual("e4", self.parser.moves[0].san)
        self.assertEqual("e6", self.parser.moves[1].san)
        self.assertEqual("Nf3", self.parser.moves[2].san)
        self.assertEqual("Kb5", self.parser.moves[3].san)
        self.assertEqual("1-0", self.parser.gameTerm)

    def test_ImportFormatMoveParse_MovesWithGameTerminationWhiteWinsAfterSuffix(self):
        moveString = "e4 1... e6 2. Nf3 Kb5? 1-0\n"

        self.assertTrue(self.parser.parseString(moveString))
        self.assertEqual("e4", self.parser.moves[0].san)
        self.assertEqual("e6", self.parser.moves[1].san)
        self.assertEqual("Nf3", self.parser.moves[2].san)
        self.assertEqual("Kb5", self.parser.moves[3].san)
        self.assertEqual(2, self.parser.moves[3].nag)
        self.assertEqual("1-0", self.parser.gameTerm)


    def test_ImportFormatMoveParse_MovesWithGameTerminationBlackWins(self):
        moveString = "e4 1... e6 2. Nf3 Kb5 0-1\n"

        self.assertTrue(self.parser.parseString(moveString))
        self.assertEqual("e4", self.parser.moves[0].san)
        self.assertEqual("e6", self.parser.moves[1].san)
        self.assertEqual("Nf3", self.parser.moves[2].san)
        self.assertEqual("Kb5", self.parser.moves[3].san)
        self.assertEqual("0-1", self.parser.gameTerm)

    def test_ImportFormatMoveParse_MovesWithGameTerminationBlackWinsAfterNag(self):
        moveString = "e4 1... e6 2. Nf3 Kb5$87 0-1\n"

        self.assertTrue(self.parser.parseString(moveString))
        self.assertEqual("e4", self.parser.moves[0].san)
        self.assertEqual("e6", self.parser.moves[1].san)
        self.assertEqual("Nf3", self.parser.moves[2].san)
        self.assertEqual("Kb5", self.parser.moves[3].san)
        self.assertEqual(87, self.parser.moves[3].nag)
        self.assertEqual("0-1", self.parser.gameTerm)
        
    def test_ImportFormatGameParse(self):
        lines = ['[Event "F/S Return Match"]']
        lines.append('[Site "Belgrade, Serbia JUG"]')
        lines.append('[Date "1992.11.04"]')
        lines.append('[Round "29"]')
        lines.append('[White "Fischer, Robert J."]')
        lines.append('[Black "Spassky, Boris V."]')
        lines.append('[Result "1/2-1/2"]')
        lines.append('')
        lines.append('1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3')
        lines.append('O-O 9. h3 Nb8 10. d4 Nbd7 11. c4 c6 12. cxb5 axb5 13. Nc3 Bb7 14. Bg5 b4 15.')
        lines.append('Nb1 h6 16. Bh4 c5 17. dxe5 Nxe4 18. Bxe7 Qxe7 19. exd6 Qf6 20. Nbd2 Nxd6 21.')
        lines.append('Nc4 Nxc4 22. Bxc4 Nb6 23. Ne5 Rae8 24. Bxf7+ Rxf7 25. Nxf7 Rxe1+ 26. Qxe1 Kxf7')
        lines.append('27. Qe3 Qg5 28. Qxg5 hxg5 29. b3 Ke6 30. a3 Kd6 31. axb4 cxb4 32. Ra5 Nd5 33.')
        lines.append('f3 Bc8 34. Kf2 Bf5 35. Ra7 g6 36. Ra6+ Kc5 37. Ke1 Nf4 38. g3 Nxh3 39. Kd2 Kb5')
        lines.append('40. Rd6 Kc5 41. Ra6 Nf2 42. g4 Bd3 43. Re6 1/2-1/2')

        for line in lines:
            self.assertTrue(self.parser.parseString(line))
        
        self.assertEqual(self.parser.tags["Event"], pgn.Tag("Event", "F/S Return Match"))
        self.assertEqual(self.parser.tags["Date"], pgn.Tag("Date", "1992.11.04"))
        self.assertEqual(self.parser.tags["Result"], pgn.Tag("Result", "1/2-1/2"))
        self.assertEqual("e4", self.parser.moves[0].san)
        self.assertEqual("e5", self.parser.moves[1].san)
        self.assertEqual("O-O", self.parser.moves[8].san)
        self.assertEqual("cxb5", self.parser.moves[22].san)
        self.assertEqual("Bxf7+", self.parser.moves[46].san)
        self.assertEqual("1/2-1/2", self.parser.gameTerm)
        

if __name__ == "__main__":
    unittest.main()
