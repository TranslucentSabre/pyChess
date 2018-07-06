import re
import pychess.app.randomizer

class FEN(object):
   """Class used to parse and operate on a FEN string"""

   def __init__(self, fenString):
      #Set defaults for standard chess opening
      self.positionString = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
      self.nextPlayer = "w"
      self.castling = "KQkq"
      self.enPassant = "-"
      self.halfmoveClock = "0"
      self.fullmoveNum = "1"

      fenList = []
      if fenString:
         pass


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

            


         


