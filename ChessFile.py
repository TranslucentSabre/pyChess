#!/usr/bin/python3
import io

class ValidConfig(object):
      validConfigItems = ["defImportFile","defExportFile","playerName","location","debug"]
      ImportFile = {"name" : validConfigItems[0]}
      ExportFile = {"name" : validConfigItems[1]}
      PlayerName = {"name" : validConfigItems[2]}
      Location   = {"name" : validConfigItems[3]}
      Debug      = {"name" : validConfigItems[4], "values" : ["True", "False"]}

class ConfigFile(object):
   """A class that deals with reading, writing and storing config"""
   
   def __init__(self):
      self.configFile = open(".chessrc", "r+")
      self.configDict = {}
      self.readConfig()
      
   def __del__(self):
      self.configFile.close()
      
   def readConfig(self):
      self.configDict = {}
      for line in self.configFile:
         configItem = line.split(":")
         key = configItem[0]
         value = configItem[1].rstrip("\n")
         if key in ValidConfig.validConfigItems:
            self.configDict[key] = value
         
   def writeConfig(self):
      self.configFile.seek(0)
      self.configFile.truncate(0)
      for item in self.configDict:
         self.configFile.write(item+":"+self.configDict[item]+"\n")
      self.configFile.flush()
      
   def getConfigItem(self,key):
      if key in self.configDict:
         return self.configDict[key]
      else:
         return ""
      
   def setConfigItem(self,key,item):
      if key in ValidConfig.validConfigItems:
         self.configDict[key] = item
         
         
def isDebugEnabled():
   config = ConfigFile()
   debug = config.getConfigItem(ValidConfig.Debug["name"])
   if debug == "True":
      debug = True
   else:
      debug = False
   del config
   return debug
   
def debugPrint(*printables):
   if isDebugEnabled():
      print(printables)


class ChessFiles(ConfigFile):
   """This class handles all file reads and writes for the chess program"""

   def __init__(self):
      super(ChessFiles, self).__init__()
      self.inFileName = self.getConfigItem(ValidConfig.ImportFile["name"])
      self.outFileName = self.getConfigItem(ValidConfig.ExportFile["name"])

      self.attemptInputFileOpen(self.inFileName)
      self.attemptOutputFileOpen(self.outFileName)

      self.resetWriteString()
      self.moveSeekLocation = 0

      
   def __del__(self):
      super(ChessFiles, self).__del__()
      self.closeInFile()
      self.closeOutFile()

   def attemptInputFileOpen(self, filename):
      self.inFileStatus = "Ready"
      try:
         self.inFile = open(filename)
      except OSError:
         self.inFile = None
         self.inFileStatus = "Cannot open input file."

   def closeInFile(self):
      if self.inFile != None:
         self.inFile.close()

   def attemptOutputFileOpen(self, filename):
      self.outFileStatus = "Ready"
      try:
         self.outFile = open(filename, "a");
      except OSError:
         self.outFile = None
         self.outFileStatus = "Cannot open output file."

   def closeOutFile(self):
      if self.outFile != None:
         self.outFile.close()

   def changeInputFile(self, infile):
      self.closeInFile()
      self.attemptInputFileOpen(infile)

   def changeOutputFile(self, outfile):
      self.closeOutFile()
      self.attemptOutputFileOpen(outfile)

   def resetWriteString(self):
      self.writeString = ""
      self.moveCounter = 0
      self.turnCounter = 1

   def appendMoveForWrite(self, move):

      #The places at which the commas are written here are important for the parser
      if self.moveCounter & 1 == 0:
         self.writeString += str(self.turnCounter) + ". " + move
         self.turnCounter += 1
      else:
         self.writeString += " " + move + "\n"
      self.moveCounter += 1

   def writeGame(self):
      self.outFile.seek(0)
      self.outFile.truncate(0)
      self.outFile.write(self.writeString)
      self.outFile.flush()

   def readMoves(self):
      self._seekToMoves()
      return [move for move in self.getMoves()] 


   def getMoves(self):
      for line in self.inFile:
         if line != "":
            for move in line.split()[1:]:
               yield move

   def _seekToMoves(self):
      self.inFile.seek(self.moveSeekLocation)



if __name__ == "__main__":
   files = ChessFile(infile = "input.txt")
   if files.inFileStatus != "Ready":
      print(files.inFileStatus)
   else:
      for move in files.getMoves():
         print(move)
