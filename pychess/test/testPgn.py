#!/usr/bin/env python3
import unittest
from pychess.app import pgn

class pgnTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pgn = pgn.PgnFile()

    def setUp(self):
        self.pgn.reset()

    def tagParseTest(self, tagStrings, tagClasses):

        for tagString in tagStrings:
            success = self.pgn.parseString(tagString)
            self.assertEqual("", self.pgn.getParseErrorString())
            self.assertTrue(success)
        for tagClass in tagClasses:
            self.assertEqual(self.pgn.currentGame.getTag(tagClass.name), tagClass)

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

        success = self.pgn.parseString(moveString)
        self.assertEqual("", self.pgn.getParseErrorString())
        self.assertTrue(success)
        self.assertEqual("e4", self.pgn.currentGame.getMove("1.").san)
        self.assertEqual("e6", self.pgn.currentGame.getMove("1...").san)

    def test_ImportFormatMoveParse_TwoMovesTwoMoveNumbers_NoDots(self):
        moveString = "1 e4  e6  Nf3 2 Kb5\n"

        success = self.pgn.parseString(moveString)
        self.assertEqual("", self.pgn.getParseErrorString())
        self.assertTrue(success)
        self.assertEqual("e4", self.pgn.currentGame.getMove("1.").san)
        self.assertEqual("e6", self.pgn.currentGame.getMove("1...").san)
        self.assertEqual("Nf3", self.pgn.currentGame.getMove("2.").san)
        self.assertEqual("Kb5", self.pgn.currentGame.getMove("2...").san)

    def test_ImportFormatMoveParse_TwoMovesTwoMoveNumbers_WithDots(self):
        moveString = "e4 1... e6  2 . Nf3  Kb5\n"

        success = self.pgn.parseString(moveString)
        self.assertEqual("", self.pgn.getParseErrorString())
        self.assertTrue(success)
        self.assertEqual("e4", self.pgn.currentGame.getMove("1.").san)
        self.assertEqual("e6", self.pgn.currentGame.getMove("1...").san)
        self.assertEqual("Nf3", self.pgn.currentGame.getMove("2.").san)
        self.assertEqual("Kb5", self.pgn.currentGame.getMove("2...").san)

    def test_ImportFormatMoveParse_MovesWithSuffixAnnotations(self):
        moveString = "e4? 1... e6  2. Nf3!!  Kb5\n"

        success = self.pgn.parseString(moveString)
        self.assertEqual("", self.pgn.getParseErrorString())
        self.assertTrue(success)
        self.assertEqual("e4", self.pgn.currentGame.getMove("1.").san)
        self.assertEqual("e6", self.pgn.currentGame.getMove("1...").san)
        self.assertEqual("Nf3", self.pgn.currentGame.getMove("2.").san)
        self.assertEqual("Kb5", self.pgn.currentGame.getMove("2...").san)
        self.assertEqual(2, self.pgn.currentGame.getMove("1.").nag)
        self.assertEqual(3, self.pgn.currentGame.getMove("2.").nag)

    def test_ImportFormatMoveParse_MovesWithNag(self):
        moveString = "e4 1... e6 $200  2. Nf3 $34  Kb5\n"

        success = self.pgn.parseString(moveString)
        self.assertEqual("", self.pgn.getParseErrorString())
        self.assertTrue(success)
        self.assertEqual("e4", self.pgn.currentGame.getMove("1.").san)
        self.assertEqual("e6", self.pgn.currentGame.getMove("1...").san)
        self.assertEqual("Nf3", self.pgn.currentGame.getMove("2.").san)
        self.assertEqual("Kb5", self.pgn.currentGame.getMove("2...").san)
        self.assertEqual(200, self.pgn.currentGame.getMove("1...").nag)
        self.assertEqual(34, self.pgn.currentGame.getMove("2.").nag)

    def test_ImportFormatMoveParse_MovesWithGameTerminationTie(self):
        moveString = "e4 1... e6 2. Nf3 Kb5 1/2-1/2\n"

        success = self.pgn.parseString(moveString)
        self.assertEqual("", self.pgn.getParseErrorString())
        self.assertTrue(success)
        self.assertEqual("e4", self.pgn.games[0].getMove("1.").san)
        self.assertEqual("e6", self.pgn.games[0].getMove("1...").san)
        self.assertEqual("Nf3", self.pgn.games[0].getMove("2.").san)
        self.assertEqual("Kb5", self.pgn.games[0].getMove("2...").san)
        self.assertEqual("1/2-1/2", self.pgn.games[0].gameTerm)


    def test_ImportFormatMoveParse_MovesWithGameTerminationOngoing(self):
        moveString = "1 e4 e6 2. Nf3 2 Kb5 *\n"

        success = self.pgn.parseString(moveString)
        self.assertEqual("", self.pgn.getParseErrorString())
        self.assertTrue(success)
        self.assertEqual("e4", self.pgn.games[0].getMove("1.").san)
        self.assertEqual("e6", self.pgn.games[0].getMove("1...").san)
        self.assertEqual("Nf3", self.pgn.games[0].getMove("2.").san)
        self.assertEqual("Kb5", self.pgn.games[0].getMove("2...").san)
        self.assertEqual("*", self.pgn.games[0].gameTerm)


    def test_ImportFormatMoveParse_MovesWithGameTerminationOngoingAfterNag(self):
        moveString = "1 e4 e6 2. Nf3 2 Kb5 $156 *\n"

        success = self.pgn.parseString(moveString)
        self.assertEqual("", self.pgn.getParseErrorString())
        self.assertTrue(success)
        self.assertEqual("e4", self.pgn.games[0].getMove("1.").san)
        self.assertEqual("e6", self.pgn.games[0].getMove("1...").san)
        self.assertEqual("Nf3", self.pgn.games[0].getMove("2.").san)
        self.assertEqual("Kb5", self.pgn.games[0].getMove("2...").san)
        self.assertEqual(156, self.pgn.games[0].getMove("2...").nag)
        self.assertEqual("*", self.pgn.games[0].gameTerm)

    def test_ImportFormatMoveParse_MovesWithGameTerminationWhiteWins(self):
        moveString = "e4 1... e6 2. Nf3 Kb5 1-0\n"

        success = self.pgn.parseString(moveString)
        self.assertEqual("", self.pgn.getParseErrorString())
        self.assertTrue(success)
        self.assertEqual("e4", self.pgn.games[0].getMove("1.").san)
        self.assertEqual("e6", self.pgn.games[0].getMove("1...").san)
        self.assertEqual("Nf3", self.pgn.games[0].getMove("2.").san)
        self.assertEqual("Kb5", self.pgn.games[0].getMove("2...").san)
        self.assertEqual("1-0", self.pgn.games[0].gameTerm)

    def test_ImportFormatMoveParse_MovesWithGameTerminationWhiteWinsAfterSuffix(self):
        moveString = "e4 1... e6 2. Nf3 Kb5? 1-0\n"

        success = self.pgn.parseString(moveString)
        self.assertEqual("", self.pgn.getParseErrorString())
        self.assertTrue(success)
        self.assertEqual("e4", self.pgn.games[0].getMove("1.").san)
        self.assertEqual("e6", self.pgn.games[0].getMove("1...").san)
        self.assertEqual("Nf3", self.pgn.games[0].getMove("2.").san)
        self.assertEqual("Kb5", self.pgn.games[0].getMove("2...").san)
        self.assertEqual(2, self.pgn.games[0].getMove("2...").nag)
        self.assertEqual("1-0", self.pgn.games[0].gameTerm)


    def test_ImportFormatMoveParse_MovesWithGameTerminationBlackWins(self):
        moveString = "e4 1... e6 2. Nf3 Kb5 0-1\n"

        success = self.pgn.parseString(moveString)
        self.assertEqual("", self.pgn.getParseErrorString())
        self.assertTrue(success)
        self.assertEqual("e4", self.pgn.games[0].getMove("1.").san)
        self.assertEqual("e6", self.pgn.games[0].getMove("1...").san)
        self.assertEqual("Nf3", self.pgn.games[0].getMove("2.").san)
        self.assertEqual("Kb5", self.pgn.games[0].getMove("2...").san)
        self.assertEqual("0-1", self.pgn.games[0].gameTerm)

    def test_ImportFormatMoveParse_MovesWithGameTerminationBlackWinsAfterNag(self):
        moveString = "e4 1... e6 2. Nf3 Kb5$87 0-1\n"

        success = self.pgn.parseString(moveString)
        self.assertEqual("", self.pgn.getParseErrorString())
        self.assertTrue(success)
        self.assertEqual("e4", self.pgn.games[0].getMove("1.").san)
        self.assertEqual("e6", self.pgn.games[0].getMove("1...").san)
        self.assertEqual("Nf3", self.pgn.games[0].getMove("2.").san)
        self.assertEqual("Kb5", self.pgn.games[0].getMove("2...").san)
        self.assertEqual(87, self.pgn.games[0].getMove("2...").nag)
        self.assertEqual("0-1", self.pgn.games[0].gameTerm)
        
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
            success = self.pgn.parseString(line)
            self.assertEqual("", self.pgn.getParseErrorString())
            self.assertTrue(success)
        
        self.assertEqual(self.pgn.games[0].getTag("Event"), pgn.Tag("Event", "F/S Return Match"))
        self.assertEqual(self.pgn.games[0].getTag("Date"), pgn.Tag("Date", "1992.11.04"))
        self.assertEqual(self.pgn.games[0].getTag("Result"), pgn.Tag("Result", "1/2-1/2"))
        self.assertEqual("e4", self.pgn.games[0].getMove("1.").san)
        self.assertEqual("e5", self.pgn.games[0].getMove("1...").san)
        self.assertEqual("O-O", self.pgn.games[0].getMove("5.").san)
        self.assertEqual("cxb5", self.pgn.games[0].getMove("12.").san)
        self.assertEqual("Bxf7+", self.pgn.games[0].getMove("24.").san)
        self.assertEqual("1/2-1/2", self.pgn.games[0].gameTerm)
        
    def test_ImportFormatGameParse_TestExport(self):
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
            success = self.pgn.parseString(line)
            self.assertEqual("", self.pgn.getParseErrorString())
            self.assertTrue(success)
        
        self.assertEqual("\n".join(lines), str(self.pgn))
        
    def test_ImportFormatGameParse_TestExport_ExtraTags(self):
        lines = ['[Event "F/S Return Match"]']
        lines.append('[Site "Belgrade, Serbia JUG"]')
        lines.append('[Date "1992.11.04"]')
        lines.append('[Time "210435Z"]')
        lines.append('[Round "29"]')
        lines.append('[White "Fischer, Robert J."]')
        lines.append('[Black "Spassky, Boris V."]')
        lines.append('[Domain "temyers.dyndns.org"]')
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
            success = self.pgn.parseString(line)
            self.assertEqual("", self.pgn.getParseErrorString())
            self.assertTrue(success)
            
        lines = ['[Event "F/S Return Match"]']
        lines.append('[Site "Belgrade, Serbia JUG"]')
        lines.append('[Date "1992.11.04"]')
        lines.append('[Round "29"]')
        lines.append('[White "Fischer, Robert J."]')
        lines.append('[Black "Spassky, Boris V."]')
        lines.append('[Result "1/2-1/2"]')
        lines.append('[Domain "temyers.dyndns.org"]')
        lines.append('[Time "210435Z"]')
        lines.append('')
        lines.append('1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3')
        lines.append('O-O 9. h3 Nb8 10. d4 Nbd7 11. c4 c6 12. cxb5 axb5 13. Nc3 Bb7 14. Bg5 b4 15.')
        lines.append('Nb1 h6 16. Bh4 c5 17. dxe5 Nxe4 18. Bxe7 Qxe7 19. exd6 Qf6 20. Nbd2 Nxd6 21.')
        lines.append('Nc4 Nxc4 22. Bxc4 Nb6 23. Ne5 Rae8 24. Bxf7+ Rxf7 25. Nxf7 Rxe1+ 26. Qxe1 Kxf7')
        lines.append('27. Qe3 Qg5 28. Qxg5 hxg5 29. b3 Ke6 30. a3 Kd6 31. axb4 cxb4 32. Ra5 Nd5 33.')
        lines.append('f3 Bc8 34. Kf2 Bf5 35. Ra7 g6 36. Ra6+ Kc5 37. Ke1 Nf4 38. g3 Nxh3 39. Kd2 Kb5')
        lines.append('40. Rd6 Kc5 41. Ra6 Nf2 42. g4 Bd3 43. Re6 1/2-1/2')
        
        self.assertEqual("\n".join(lines), str(self.pgn))
        
    def test_ImportFormatGameParse_TestExport_TwoGames(self):
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

        lines.append('')
        lines.append('[Event "10th Nantes Open"]')
        lines.append('[Site "Nantes FRA"]')
        lines.append('[Date "2011.12.28"]')
        lines.append('[Round "-"]')
        lines.append('[White "Le Borgne,P"]')
        lines.append('[Black "Okhotnik,V"]')
        lines.append('[Result "0-1"]')
        lines.append('[BlackTitle "IM"]')
        lines.append('[Opening "Petrov\'s defence"]')
        lines.append('[BlackElo "2427"]')
        lines.append('[ECO "C42"]')
        lines.append('[EventDate "2011.12.27"]')
        lines.append('[WhiteElo "2198"]')
        lines.append('[BlackFideId "14101289"]')
        lines.append('[EventType "swiss"]')
        lines.append('[WhiteFideId "624799"]')
        lines.append('')
        lines.append('1.e4 e5 2.Nf3 Nf6 3.Nxe5 d6 4.Nf3 Nxe4 5.Bd3 Nf6 6.h3 Be7 7.O-O O-O 8.c3')
        lines.append('Re8 9.Re1 Nbd7 10.Bc2 b6 11.d4 Bb7 12.Nbd2 Bf8 13.Nf1 Rxe1 14.Nxe1 g6 15.Ng3')
        lines.append('Qe7 16.Bg5 h6 17.Bd2 Ne4 18.Nxe4 Bxe4 19.Bxe4 Qxe4 20.Qf3 Qxf3 21.Nxf3')
        lines.append('f5 22.Re1 Nf6 23.Bc1 b5 24.Kf1 a5 25.Ng1 a4 26.Ne2 g5 27.Ng3 f4 28.Ne4')
        lines.append('Nd5 29.Ke2 Kf7 30.Kf3 b4 31.Bd2 bxc3 32.bxc3 Rb8 33.c4 Ne7 34.Bc3 d5 35.Nd2')
        lines.append('Bg7 36.Rc1 c6 37.Ke2 c5 38.dxc5 d4 39.Ba1 Nc6 40.Ne4 Be5 41.Kd2 Ke6 42.f3')
        lines.append('Bc7 43.Rh1 Be5 44.h4 gxh4 45.Rxh4 Rb1 46.Rxh6+ Kd7 47.Rh7+ Kd8 48.Bxd4')
        lines.append('Nxd4 49.Nc3 Rb2+ 50.Kd3 Ne6 51.Nxa4 Rxa2   0-1')

        for line in lines:
            success = self.pgn.parseString(line)
            self.assertEqual("", self.pgn.getParseErrorString())
            self.assertTrue(success)
        
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

        lines.append('')
        lines.append('[Event "10th Nantes Open"]')
        lines.append('[Site "Nantes FRA"]')
        lines.append('[Date "2011.12.28"]')
        lines.append('[Round "-"]')
        lines.append('[White "Le Borgne,P"]')
        lines.append('[Black "Okhotnik,V"]')
        lines.append('[Result "0-1"]')
        lines.append('[BlackElo "2427"]')
        lines.append('[BlackFideId "14101289"]')
        lines.append('[BlackTitle "IM"]')
        lines.append('[ECO "C42"]')
        lines.append('[EventDate "2011.12.27"]')
        lines.append('[EventType "swiss"]')
        lines.append('[Opening "Petrov\'s defence"]')
        lines.append('[WhiteElo "2198"]')
        lines.append('[WhiteFideId "624799"]')
        lines.append('')
        lines.append('1. e4 e5 2. Nf3 Nf6 3. Nxe5 d6 4. Nf3 Nxe4 5. Bd3 Nf6 6. h3 Be7 7. O-O O-O 8.')
        lines.append('c3 Re8 9. Re1 Nbd7 10. Bc2 b6 11. d4 Bb7 12. Nbd2 Bf8 13. Nf1 Rxe1 14. Nxe1 g6')
        lines.append('15. Ng3 Qe7 16. Bg5 h6 17. Bd2 Ne4 18. Nxe4 Bxe4 19. Bxe4 Qxe4 20. Qf3 Qxf3 21.')
        lines.append('Nxf3 f5 22. Re1 Nf6 23. Bc1 b5 24. Kf1 a5 25. Ng1 a4 26. Ne2 g5 27. Ng3 f4 28.')
        lines.append('Ne4 Nd5 29. Ke2 Kf7 30. Kf3 b4 31. Bd2 bxc3 32. bxc3 Rb8 33. c4 Ne7 34. Bc3 d5')
        lines.append('35. Nd2 Bg7 36. Rc1 c6 37. Ke2 c5 38. dxc5 d4 39. Ba1 Nc6 40. Ne4 Be5 41. Kd2')
        lines.append('Ke6 42. f3 Bc7 43. Rh1 Be5 44. h4 gxh4 45. Rxh4 Rb1 46. Rxh6+ Kd7 47. Rh7+ Kd8')
        lines.append('48. Bxd4 Nxd4 49. Nc3 Rb2+ 50. Kd3 Ne6 51. Nxa4 Rxa2 0-1')

        self.assertEqual("\n".join(lines), str(self.pgn))

if __name__ == "__main__":
    unittest.main()
