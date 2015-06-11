#!/usr/bin/env python3
import io, os
from pychess.app.pgn import PgnFile

def isDebugEnabled():
    config = ConfigFile()
    debug = config.getConfigItem(ValidConfig.Debug["name"])
    debug = booleanConfigItemIsTrue(debug)
    del config
    return debug

def booleanConfigItemIsTrue(configValue):
   """This is necessary because config items are stored as strings"""
   if configValue == "True":
      return True
   else:
      return False



class ValidConfig(object):
      validConfigItems = ["defImportFile","defExportFile","playerName","location","debug","strict","files"]
      ImportFile       = {"name" : validConfigItems[0], "default" : "savegame.pgn"}
      ExportFile       = {"name" : validConfigItems[1], "default" : "savegame.pgn"}
      PlayerName       = {"name" : validConfigItems[2], "default" : "Unknown"}
      Location         = {"name" : validConfigItems[3], "default" : "Unknown"}
      Debug            = {"name" : validConfigItems[4], "default" : "False", "values" : ["True", "False"]}
      StrictParse      = {"name" : validConfigItems[5], "default" : "False", "values" : ["True", "False"]}
      FileDir          = {"name" : validConfigItems[6], "default" : "."}
      configMap = {"import":ImportFile, "export":ExportFile, "name":PlayerName, \
                   "location":Location, "debug":Debug, "strict":StrictParse, \
                   "files":FileDir}

class ConfigFile(object):
   """A class that deals with reading, writing and storing config"""

   def __init__(self):
      configFileName = os.path.join(os.path.dirname(__file__), '.chessrc')
      try:
         self.configFile = open(configFileName, "r+")
      except (OSError,IOError):
         self.configFile = open(configFileName, "w")
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


class ChessFiles(ConfigFile):
   """This class handles all file reads and writes for the chess program"""

   def __init__(self):
      super(ChessFiles, self).__init__()
      self.inFileName = self.getConfigItem(ValidConfig.ImportFile["name"])
      self.outFileName = self.getConfigItem(ValidConfig.ExportFile["name"])

      self.attemptInputFileOpen(self.inFileName)
      self.attemptOutputFileOpen(self.outFileName)

      self.pgnFile = PgnFile()


   def __del__(self):
      super(self.__class__, self).__del__()
      self.closeInFile()
      self.closeOutFile()

   def attemptInputFileOpen(self, filename):
      self.inFileStatus = "Ready"
      fileDir = os.path.abspath(self.getConfigItem(ValidConfig.FileDir["name"]))
      filename = os.path.join(fileDir, filename)
      try:
         self.inFile = open(filename)
      except (OSError,IOError):
         self.inFile = None
         self.inFileStatus = "Cannot open input file."

   def closeInFile(self):
      if self.inFile != None:
         self.inFile.close()

   def attemptOutputFileOpen(self, filename):
      self.outFileStatus = "Ready"
      fileDir = os.path.abspath(self.getConfigItem(ValidConfig.FileDir["name"]))
      filename = os.path.join(fileDir, filename)
      try:
         self.outFile = open(filename, "a");
      except (OSError,IOError):
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

   def resetPgnFile(self):
      self.pgnFile.reset()

   def appendMoveForWrite(self, move):
      self.pgnFile.saveMove(move)

   def writeGame(self):
      self.outFile.seek(0)
      self.outFile.truncate(0)
      self.outFile.write(str(self.pgnFile))
      self.outFile.flush()

   def getPgnErrorString(self):
      return self.pgnFile.getParseErrorString()

   def readPgn(self):
      self.resetPgnFile()
      self.inFile.seek(0)
      return self.pgnFile.parseFile(self.inFile)

   def getNumberOfGames(self):
      return self.pgnFile.getNumberOfGames()

   def readMoves(self, gameIndex):
      for move in self.pgnFile.getMoves():
         yield move.san


if __name__ == "__main__":
   files = ChessFile(infile = "input.txt")
   if files.inFileStatus != "Ready":
      print(files.inFileStatus)
   else:
      for move in files.getMoves():
         print(move)
