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

   VALID_PLAYER = "bw"
   VALID_CASTLE = "-KQkq"
   VALID_NON_COORD_EN_PASSANT = "-"

   def __init__(self):
      self.reset()

   def reset(self):
      self.fenString = ""
      self.parseValid = False
      self.parseErrors = "No parse attempted"

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




   def getNextPlayer(self):
      return self._getFENItem(FEN._player_index_)

   def getHalfmoveClock(self):
      clock = self._getFENItems(FEN._halfmove_index_)
      try:
         return int(clock)
      except ValueError:
         return ""

   def getFullmoveClock(self):
      clock = self._getFENItems(FEN._fullmove_index_)
      try:
         return int(clock)
      except ValueError:
         return ""

   def getFENString(self):
      return self.fenString

class FENValidator(object):
   validPieces = "rnbqkpRNBQKP"
   
   def __init__(self, ranks=8, files=8):
      self.rankNum = ranks
      self.fileNum = files
      self.__resetErrString__()
  
   def __resetErrString__(self):
      self.errStr = "None"
   
   def validatePositions(self, positions):
      if not type(positions) == str:
         self.errStr = "Position string is not a string"
         return False
    
      errorState = False
      ranks = positions.split("/")
      if not len(ranks) == self.rankNum:
         self.errStr += "Should be {} ranks, there are {}.\n".format(self.rankNum, len(ranks))
         errorState = True
     
      for invRankNum, rank in enumerate(ranks):
         fileCount = len([ file for file in rank if file in FENValidator.validPieces])
         fileCount += sum([int(empty) for empty in re.findall(r'[0-9]+', rank)])
         if not fileCount == self.fileNum:
            self.errStr += "Rank {} should be {} files, there are {}, or it has invalid pieces.\n".format(self.rankNum-invRankNum, self.fileNum, fileCount)
            errorState = True
      
      return errorState

