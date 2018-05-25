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


   class FENValidator(object):
      
      def __init__(self):
         self.boardSize = 8
         self.__resetErrString__()

      def __resetErrString__(self):
         self.errStr = "None"

      def validatePositions(self, positions):
         if not type(positions) == str:
            self.errStr = "Position string is not a string"
            return False

         rows = positions.split("/")
         if not len(rows) == self.boardSize:
            self.errStr = "Should be " + str(self.boardSize) + " rows, there are "+len(rows)+"."
            return False



         


