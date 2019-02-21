import re
import pychess.app.randomizer

class FEN(object):
   """Class used to parse and operate on a FEN string"""

   STANDARD_OPENING = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
   RANDOM_OPENING = "RANDOMIZE_ME w GENERATED - 0 1" 

   _position_index_ = 0
   _player_index_ = 1
   _castle_index_ = 2
   _en_passant_index_ = 3
   _halfmove_index_ = 4
   _fullmove_index_ = 5

   VALID_BLACK_PIECES = "rnbqkp"
   VALID_WHITE_PIECES = "RNBQKP"
   VALID_PLAYER = "bw"
   VALID_CASTLE = "KQkq"
   VALID_DASH = "-"

   def __init__(self):
      self.reset()

   def reset(self):
      self.fenString = ""
      self.parseValid = False
      self.parseErrors = "No parse attempted"
      self.whitePieces = []
      self.blackPieces = []

   def getParseValid(self):
      return self.parseValid

   def getParseErrors(self):
      return self.parseErrors

   def _getFENItem(self, index):
      items = self.fenString.split()
      if index <= len(items):
         return items[index]
      else:
         return ""

   def parse(self, fenString=STANDARD_OPENING):
      self.fenString = fenString

      if self.fenString == FEN.RANDOM_OPENING:
         #self.randomize_pieces()
         pass

      self.parseErrors = ""
      self.parseValid = True

      positionString = self._getFENItem(FEN._position_index_)
      if positionString == "":
         self.parseErrors += "Piece positions are not present"
         self.parseValid = False
         return self.parseValid

      successfulParse = True and self._validatePositions()

      return successfulParse



   def _validatePositions(self):
      ranks = self._getFENItem(FEN._position_index_).split("/")
      rankCount = len(ranks)
     
      for invRankNum, rank in enumerate(ranks):
         # Each number is that number of files, each other character is 1 file
         fileCount = len([ file for file in re.findall(r'[^0-9]', rank) ])
         fileCount += sum([ int(empty) for empty in re.findall(r'[0-9]+', rank) ])

         # Here we ensure that the board is square
         if not fileCount == rankCount:
            self.parseErrors += "Rank {} should be {} files, there are {}, or it has invalid pieces.\n".format(rankCount-invRankNum, rankCount, fileCount)
            self.parseValid = False
      
      return self.parseValid

   def _validateNextPlayer(self):
      firstPlayer = self.getNextPlayer()

      itemLength = len(firstPlayer)
      if itemLength != 1 or firstPlayer not in FEN.VALID_PLAYER:
         self.parseErrors += "Next player token must be either {}\n".format(" or ".join(FEN.VALID_PLAYER))
         self.parseValid = False

      return self.parseValid

   def _validateCastle(self):
      castle = self._getFENItem(FEN._castle_index_)

      

   def getBlackPieces(self):
      return self.blackPieces

   def getWhitePieces(self):
      return self.whitePieces

   def getNextPlayer(self):
      return self._getFENItem(FEN._player_index_)

   def getHalfmoveClock(self):
      clock = self._getFENItem(FEN._halfmove_index_)
      try:
         return int(clock)
      except ValueError:
         return ""

   def getFullmoveClock(self):
      clock = self._getFENItem(FEN._fullmove_index_)
      try:
         return int(clock)
      except ValueError:
         return ""

   def getFENString(self):
      return self.fenString

