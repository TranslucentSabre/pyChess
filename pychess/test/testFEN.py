#!/usr/bin/env python3
import unittest
from pychess.app.Util import colors,Castle
from pychess.app.fen import FEN,Pieces
from pychess.app import Piece


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
      self.assertEqual([], self.fen.getBlackPieces().pawns)
      self.assertEqual([], self.fen.getBlackPieces().rooks)
      self.assertEqual([], self.fen.getBlackPieces().knights)
      self.assertEqual([], self.fen.getBlackPieces().bishops)
      self.assertEqual([], self.fen.getBlackPieces().queens)
      self.assertEqual(None, self.fen.getBlackPieces().king)

   def test_getWhitePieces_NoParse(self):
      self.assertEqual([], self.fen.getWhitePieces().pawns)
      self.assertEqual([], self.fen.getWhitePieces().rooks)
      self.assertEqual([], self.fen.getWhitePieces().knights)
      self.assertEqual([], self.fen.getWhitePieces().bishops)
      self.assertEqual([], self.fen.getWhitePieces().queens)
      self.assertEqual(None, self.fen.getWhitePieces().king)

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

   def test_parse_bad_positions(self):
      testFen = "rnbqkbnr/pppppppp/8/9/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
      error = "Rank 5 should be 8 files, there are 9, or it has invalid pieces.\n"
      self.assertFalse(self.fen.parse(testFen))
      self.assertEqual(error, self.fen.getParseErrors())

   def test_parse_bad_next_player(self):
      testFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR h KQkq - 0 1"
      error = "Next player token must be either b or w.\n"
      self.assertFalse(self.fen.parse(testFen))
      self.assertEqual(error, self.fen.getParseErrors())

   def test_parse_bad_castle_dash(self):
      testFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQ-kq - 0 1"
      error = "Invalid character '-' in castle specification.\n"
      self.assertFalse(self.fen.parse(testFen))
      self.assertEqual(error, self.fen.getParseErrors())
   
   def test_parse_bad_castle_other(self):
      testFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b mike - 0 1"
      error = """Invalid character 'm' in castle specification.
Invalid character 'i' in castle specification.
Invalid character 'e' in castle specification.
"""
      self.assertFalse(self.fen.parse(testFen))
      self.assertEqual(error, self.fen.getParseErrors())
   
   def test_parse_good_enPassant(self):
      testFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq e2 0 1"
      error = ""
      self.assertTrue(self.fen.parse(testFen))
      self.assertEqual(error, self.fen.getParseErrors())

   def test_parse_bad_enPassant(self):
      testFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq 14 0 1"
      error = "En Passant value of '14' is not valid.\n"
      self.assertFalse(self.fen.parse(testFen))
      self.assertEqual(error, self.fen.getParseErrors())
   
   def test_parse_bad_halfmove(self):
      testFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - a 1"
      error = "Halfmove clock is not an integer.\n"
      self.assertFalse(self.fen.parse(testFen))
      self.assertEqual(error, self.fen.getParseErrors())
   
   def test_parse_bad_fullmove(self):
      testFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 b"
      error = "Fullmove clock is not an integer.\n"
      self.assertFalse(self.fen.parse(testFen))
      self.assertEqual(error, self.fen.getParseErrors())
   
   def test_parse_bad_sky_is_falling(self):
      testFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNKBNR k KhQkq er h b"
      error = """Rank 1 should be 8 files, there are 6, or it has invalid pieces.
Next player token must be either b or w.
Invalid character 'h' in castle specification.
En Passant value of 'er' is not valid.
Halfmove clock is not an integer.
Fullmove clock is not an integer.
"""
      self.assertFalse(self.fen.parse(testFen))
      self.assertEqual(error, self.fen.getParseErrors())

   def test_getBlackPieces_Parse_Standard(self):
      self.assertTrue(self.fen.parse())
      black = self.fen.getBlackPieces()
      self.assertEqual(8, len(black.pawns))
      self.assertEqual("a7",black.pawns[0].position)
      self.assertEqual(True,black.pawns[0].canCharge)
      self.assertEqual("b7",black.pawns[1].position)
      self.assertEqual("c7",black.pawns[2].position)
      self.assertEqual("d7",black.pawns[3].position)
      self.assertEqual("e7",black.pawns[4].position)
      self.assertEqual("f7",black.pawns[5].position)
      self.assertEqual("g7",black.pawns[6].position)
      self.assertEqual("h7",black.pawns[7].position)
      self.assertEqual(True,black.pawns[7].canCharge)
      self.assertEqual(2, len(black.rooks))
      self.assertEqual("a8",black.rooks[0].position)
      self.assertEqual(Castle.QUEENSIDE, black.rooks[0].castleOption)
      self.assertEqual("h8",black.rooks[1].position)
      self.assertEqual(Castle.KINGSIDE, black.rooks[1].castleOption)
      self.assertEqual(2, len(black.knights))
      self.assertEqual("b8",black.knights[0].position)
      self.assertEqual("g8",black.knights[1].position)
      self.assertEqual(2, len(black.bishops))
      self.assertEqual("c8",black.bishops[0].position)
      self.assertEqual("f8",black.bishops[1].position)
      self.assertEqual(1, len(black.queens))
      self.assertEqual("d8",black.queens[0].position)
      self.assertEqual("e8",black.king.position)

   def test_getWhitePieces_Parse_Standard(self):
      self.assertTrue(self.fen.parse())
      white = self.fen.getWhitePieces()
      self.assertEqual(8, len(white.pawns))
      self.assertEqual("a2",white.pawns[0].position)
      self.assertEqual(True,white.pawns[0].canCharge)
      self.assertEqual("b2",white.pawns[1].position)
      self.assertEqual("c2",white.pawns[2].position)
      self.assertEqual("d2",white.pawns[3].position)
      self.assertEqual("e2",white.pawns[4].position)
      self.assertEqual("f2",white.pawns[5].position)
      self.assertEqual("g2",white.pawns[6].position)
      self.assertEqual("h2",white.pawns[7].position)
      self.assertEqual(True,white.pawns[7].canCharge)
      self.assertEqual(2, len(white.rooks))
      self.assertEqual("a1",white.rooks[0].position)
      self.assertEqual(Castle.QUEENSIDE, white.rooks[0].castleOption)
      self.assertEqual("h1",white.rooks[1].position)
      self.assertEqual(Castle.KINGSIDE, white.rooks[1].castleOption)
      self.assertEqual(2, len(white.knights))
      self.assertEqual("b1",white.knights[0].position)
      self.assertEqual("g1",white.knights[1].position)
      self.assertEqual(2, len(white.bishops))
      self.assertEqual("c1",white.bishops[0].position)
      self.assertEqual("f1",white.bishops[1].position)
      self.assertEqual(1, len(white.queens))
      self.assertEqual("d1",white.queens[0].position)
      self.assertEqual("e1",white.king.position)

   def test_add_white_king(self):
      testKing = Piece.King(colors.WHITE,"e1")
      self.fen.pieces.createPiece("e1","K","","")
      self.assertEqual(testKing.piece,self.fen.pieces.pieces[colors.WHITE].king.piece)
      self.assertEqual(testKing.position,self.fen.pieces.pieces[colors.WHITE].king.position)
      self.assertEqual(None,self.fen.pieces.pieces[colors.BLACK].king)
   
   def test_add_black_king(self):
      testKing = Piece.King(colors.BLACK,"e1")
      self.fen.pieces.createPiece("e1","k","","")
      self.assertEqual(testKing.piece,self.fen.pieces.pieces[colors.BLACK].king.piece)
      self.assertEqual(testKing.position,self.fen.pieces.pieces[colors.BLACK].king.position)
      self.assertEqual(None,self.fen.pieces.pieces[colors.WHITE].king)
   
   def test_add_queens(self):
      coord1 = "f3"
      coord2 = "a5"
      coord3 = "g4"
      testQueen1 = Piece.Queen(colors.BLACK,coord1)
      testQueen2 = Piece.Queen(colors.BLACK,coord2)
      testQueen3 = Piece.Queen(colors.WHITE,coord3)
      self.fen.pieces.createPiece(coord1,"q","","")
      self.fen.pieces.createPiece(coord2,"q","","")
      self.fen.pieces.createPiece(coord3,"Q","","")

      self.assertEqual(testQueen1.piece,self.fen.pieces.pieces[colors.BLACK].queens[0].piece)
      self.assertEqual(testQueen1.position,self.fen.pieces.pieces[colors.BLACK].queens[0].position)
      self.assertEqual(testQueen2.piece,self.fen.pieces.pieces[colors.BLACK].queens[1].piece)
      self.assertEqual(testQueen2.position,self.fen.pieces.pieces[colors.BLACK].queens[1].position)
   
      self.assertEqual(testQueen3.piece,self.fen.pieces.pieces[colors.WHITE].queens[0].piece)
      self.assertEqual(testQueen3.position,self.fen.pieces.pieces[colors.WHITE].queens[0].position)
   
   def test_add_bishops(self):
      coord1 = "c1"
      coord2 = "d7"
      coord3 = "e8"
      testBishop1 = Piece.Bishop(colors.BLACK,coord1)
      testBishop2 = Piece.Bishop(colors.WHITE,coord2)
      testBishop3 = Piece.Bishop(colors.WHITE,coord3)
      self.fen.pieces.createPiece(coord1,"b","","")
      self.fen.pieces.createPiece(coord2,"B","","")
      self.fen.pieces.createPiece(coord3,"B","","")

      self.assertEqual(testBishop1.piece,self.fen.pieces.pieces[colors.BLACK].bishops[0].piece)
      self.assertEqual(testBishop1.position,self.fen.pieces.pieces[colors.BLACK].bishops[0].position)

      self.assertEqual(testBishop2.piece,self.fen.pieces.pieces[colors.WHITE].bishops[0].piece)
      self.assertEqual(testBishop2.position,self.fen.pieces.pieces[colors.WHITE].bishops[0].position)
      self.assertEqual(testBishop3.piece,self.fen.pieces.pieces[colors.WHITE].bishops[1].piece)
      self.assertEqual(testBishop3.position,self.fen.pieces.pieces[colors.WHITE].bishops[1].position)
   
   def test_add_knights(self):
      coord1 = "a6"
      coord2 = "h2"
      coord3 = "b5"
      testKnight1 = Piece.Knight(colors.BLACK,coord1)
      testKnight2 = Piece.Knight(colors.BLACK,coord2)
      testKnight3 = Piece.Knight(colors.WHITE,coord3)
      self.fen.pieces.createPiece(coord1,"n","","")
      self.fen.pieces.createPiece(coord2,"n","","")
      self.fen.pieces.createPiece(coord3,"N","","")

      self.assertEqual(testKnight1.piece,self.fen.pieces.pieces[colors.BLACK].knights[0].piece)
      self.assertEqual(testKnight1.position,self.fen.pieces.pieces[colors.BLACK].knights[0].position)
      self.assertEqual(testKnight2.piece,self.fen.pieces.pieces[colors.BLACK].knights[1].piece)
      self.assertEqual(testKnight2.position,self.fen.pieces.pieces[colors.BLACK].knights[1].position)
   
      self.assertEqual(testKnight3.piece,self.fen.pieces.pieces[colors.WHITE].knights[0].piece)
      self.assertEqual(testKnight3.position,self.fen.pieces.pieces[colors.WHITE].knights[0].position)

   def test_add_rook_can_castle(self):
      testRook = Piece.Rook(colors.WHITE,"h1")
      self.fen.pieces.createPiece("h1","R","kqKQ", "")

      self.assertEqual(testRook.piece, self.fen.pieces.pieces[colors.WHITE].rooks[0].piece)
      self.assertEqual(testRook.position, self.fen.pieces.pieces[colors.WHITE].rooks[0].position)
      self.assertEqual(testRook.castleOption, self.fen.pieces.pieces[colors.WHITE].rooks[0].castleOption)
      self.assertEqual(Castle.KINGSIDE, self.fen.pieces.pieces[colors.WHITE].rooks[0].castleOption)
   
   def test_add_rook_cannot_castle_missing_letter(self):
      testRook = Piece.Rook(colors.BLACK,"a8")
      self.fen.pieces.createPiece("a8","r","kKQ", "")

      self.assertEqual(testRook.piece, self.fen.pieces.pieces[colors.BLACK].rooks[0].piece)
      self.assertEqual(testRook.position, self.fen.pieces.pieces[colors.BLACK].rooks[0].position)
      self.assertNotEqual(testRook.castleOption, self.fen.pieces.pieces[colors.BLACK].rooks[0].castleOption)
      self.assertEqual(Castle.NONE, self.fen.pieces.pieces[colors.BLACK].rooks[0].castleOption)
      self.assertEqual(Castle.QUEENSIDE, testRook.castleOption)
   
   def test_add_rook_cannot_castle_dash(self):
      testRook = Piece.Rook(colors.BLACK,"a8")
      self.fen.pieces.createPiece("a8","r","-", "")

      self.assertEqual(testRook.piece, self.fen.pieces.pieces[colors.BLACK].rooks[0].piece)
      self.assertEqual(testRook.position, self.fen.pieces.pieces[colors.BLACK].rooks[0].position)
      self.assertNotEqual(testRook.castleOption, self.fen.pieces.pieces[colors.BLACK].rooks[0].castleOption)
      self.assertEqual(Castle.NONE, self.fen.pieces.pieces[colors.BLACK].rooks[0].castleOption)
      self.assertEqual(Castle.QUEENSIDE, testRook.castleOption)
   
   def test_add_rook_cannot_castle_wrong_position(self):
      testRook = Piece.Rook(colors.WHITE,"h2")
      self.fen.pieces.createPiece("h2","R","kqKQ", "")

      self.assertEqual(testRook.piece, self.fen.pieces.pieces[colors.WHITE].rooks[0].piece)
      self.assertEqual(testRook.position, self.fen.pieces.pieces[colors.WHITE].rooks[0].position)
      self.assertEqual(testRook.castleOption, self.fen.pieces.pieces[colors.WHITE].rooks[0].castleOption)
      self.assertEqual(Castle.NONE, self.fen.pieces.pieces[colors.WHITE].rooks[0].castleOption)
   
   def test_add_pawn_std(self):
      testPawn = Piece.Pawn(colors.WHITE,"h2")
      self.fen.pieces.createPiece("h2","P","kqKQ", "-")

      self.assertEqual(testPawn.piece, self.fen.pieces.pieces[colors.WHITE].pawns[0].piece)
      self.assertEqual(testPawn.position, self.fen.pieces.pieces[colors.WHITE].pawns[0].position)
      self.assertEqual(testPawn.canCharge, self.fen.pieces.pieces[colors.WHITE].pawns[0].canCharge)
      self.assertEqual(True, self.fen.pieces.pieces[colors.WHITE].pawns[0].canCharge)
      self.assertEqual(testPawn.enPassantCapturable, self.fen.pieces.pieces[colors.WHITE].pawns[0].enPassantCapturable)
      self.assertEqual(False, self.fen.pieces.pieces[colors.WHITE].pawns[0].enPassantCapturable)
   
   def test_add_pawn_major(self):
      testPawn = Piece.Pawn(colors.BLACK,"h8")
      self.fen.pieces.createPiece("h8","p","kqKQ", "-")

      self.assertEqual(testPawn.piece, self.fen.pieces.pieces[colors.BLACK].pawns[0].piece)
      self.assertEqual(testPawn.position, self.fen.pieces.pieces[colors.BLACK].pawns[0].position)
      self.assertEqual(testPawn.canCharge, self.fen.pieces.pieces[colors.BLACK].pawns[0].canCharge)
      self.assertEqual(True, self.fen.pieces.pieces[colors.BLACK].pawns[0].canCharge)
      self.assertEqual(testPawn.enPassantCapturable, self.fen.pieces.pieces[colors.BLACK].pawns[0].enPassantCapturable)
      self.assertEqual(False, self.fen.pieces.pieces[colors.BLACK].pawns[0].enPassantCapturable)
   
   def test_add_pawn_middle(self):
      testPawn = Piece.Pawn(colors.WHITE,"h6")
      self.fen.pieces.createPiece("h6","P","kqKQ", "-")

      self.assertEqual(testPawn.piece, self.fen.pieces.pieces[colors.WHITE].pawns[0].piece)
      self.assertEqual(testPawn.position, self.fen.pieces.pieces[colors.WHITE].pawns[0].position)
      self.assertEqual(testPawn.canCharge, self.fen.pieces.pieces[colors.WHITE].pawns[0].canCharge)
      self.assertEqual(False, self.fen.pieces.pieces[colors.WHITE].pawns[0].canCharge)
      self.assertEqual(testPawn.enPassantCapturable, self.fen.pieces.pieces[colors.WHITE].pawns[0].enPassantCapturable)
      self.assertEqual(False, self.fen.pieces.pieces[colors.WHITE].pawns[0].enPassantCapturable)
   
   def test_add_pawn_middle_other_enpassant(self):
      testPawn = Piece.Pawn(colors.WHITE,"h6")
      self.fen.pieces.createPiece("h6","P","kqKQ", "e3")

      self.assertEqual(testPawn.piece, self.fen.pieces.pieces[colors.WHITE].pawns[0].piece)
      self.assertEqual(testPawn.position, self.fen.pieces.pieces[colors.WHITE].pawns[0].position)
      self.assertEqual(testPawn.canCharge, self.fen.pieces.pieces[colors.WHITE].pawns[0].canCharge)
      self.assertEqual(False, self.fen.pieces.pieces[colors.WHITE].pawns[0].canCharge)
      self.assertEqual(testPawn.enPassantCapturable, self.fen.pieces.pieces[colors.WHITE].pawns[0].enPassantCapturable)
      self.assertEqual(False, self.fen.pieces.pieces[colors.WHITE].pawns[0].enPassantCapturable)
   
   def test_add_pawn_white_enpassant(self):
      testPawn = Piece.Pawn(colors.WHITE,"e4")
      self.fen.pieces.createPiece("e4","P","kqKQ", "e3")

      self.assertEqual(testPawn.piece, self.fen.pieces.pieces[colors.WHITE].pawns[0].piece)
      self.assertEqual(testPawn.position, self.fen.pieces.pieces[colors.WHITE].pawns[0].position)
      self.assertEqual(testPawn.canCharge, self.fen.pieces.pieces[colors.WHITE].pawns[0].canCharge)
      self.assertEqual(False, self.fen.pieces.pieces[colors.WHITE].pawns[0].canCharge)
      self.assertNotEqual(testPawn.enPassantCapturable, self.fen.pieces.pieces[colors.WHITE].pawns[0].enPassantCapturable)
      self.assertEqual(True, self.fen.pieces.pieces[colors.WHITE].pawns[0].enPassantCapturable)
   
   def test_add_pawn_white_enpassant_opposite(self):
      testPawn = Piece.Pawn(colors.WHITE,"e4")
      self.fen.pieces.createPiece("e4","P","kqKQ", "e5")

      self.assertEqual(testPawn.piece, self.fen.pieces.pieces[colors.WHITE].pawns[0].piece)
      self.assertEqual(testPawn.position, self.fen.pieces.pieces[colors.WHITE].pawns[0].position)
      self.assertEqual(testPawn.canCharge, self.fen.pieces.pieces[colors.WHITE].pawns[0].canCharge)
      self.assertEqual(False, self.fen.pieces.pieces[colors.WHITE].pawns[0].canCharge)
      self.assertEqual(testPawn.enPassantCapturable, self.fen.pieces.pieces[colors.WHITE].pawns[0].enPassantCapturable)
      self.assertEqual(False, self.fen.pieces.pieces[colors.WHITE].pawns[0].enPassantCapturable)
   
   def test_add_pawn_black_enpassant(self):
      testPawn = Piece.Pawn(colors.BLACK,"c5")
      self.fen.pieces.createPiece("c5","p","kqKQ", "c6")

      self.assertEqual(testPawn.piece, self.fen.pieces.pieces[colors.BLACK].pawns[0].piece)
      self.assertEqual(testPawn.position, self.fen.pieces.pieces[colors.BLACK].pawns[0].position)
      self.assertEqual(testPawn.canCharge, self.fen.pieces.pieces[colors.BLACK].pawns[0].canCharge)
      self.assertEqual(False, self.fen.pieces.pieces[colors.BLACK].pawns[0].canCharge)
      self.assertNotEqual(testPawn.enPassantCapturable, self.fen.pieces.pieces[colors.BLACK].pawns[0].enPassantCapturable)
      self.assertEqual(True, self.fen.pieces.pieces[colors.BLACK].pawns[0].enPassantCapturable)
   
   def test_add_pawn_black_enpassant_opposite(self):
      testPawn = Piece.Pawn(colors.BLACK,"c5")
      self.fen.pieces.createPiece("c5","p","kqKQ", "c4")

      self.assertEqual(testPawn.piece, self.fen.pieces.pieces[colors.BLACK].pawns[0].piece)
      self.assertEqual(testPawn.position, self.fen.pieces.pieces[colors.BLACK].pawns[0].position)
      self.assertEqual(testPawn.canCharge, self.fen.pieces.pieces[colors.BLACK].pawns[0].canCharge)
      self.assertEqual(False, self.fen.pieces.pieces[colors.BLACK].pawns[0].canCharge)
      self.assertEqual(testPawn.enPassantCapturable, self.fen.pieces.pieces[colors.BLACK].pawns[0].enPassantCapturable)
      self.assertEqual(False, self.fen.pieces.pieces[colors.BLACK].pawns[0].enPassantCapturable)
   
if __name__ == "__main__":
    unittest.main()
