from __future__ import print_function
from sys import stdout

class Debug(object):

   def __init__(self):
      self.sections = []
      self.indent = 2
      self.indentString = ""
      self.errorString = ""
      self.enabled = False
      self.defaultOutputFile = stdout
      self.outputFile = stdout
      self.defaultOutputFileName = "STDOUT"
      self.outputFileName = "STDOUT"

   def dprint(self, *printables):
      if self.enabled:
         section = ""
         if len(self.sections) > 0:
            section = self.sections[-1]
         print(self.indentString, section, *printables, file=self.outputFile)

   def startSection(self, sectionName):
      self.sections.append(sectionName)
      self.updateIndentString()
      self.dprint("- begin")

   def endSection(self):
      self.dprint("- end")
      sectionName = self.sections.pop()
      self.updateIndentString()


   def updateIndentString(self):
      self.indentString = ""
      numSections = len(self.sections)
      if numSections > 1:
         self.indentString = "".center((numSections-1)*self.indent)

   def enableDebug(self, enabledFlag):
      self.enabled = enabledFlag

   def setDefaultOutput(self):
      return self.setOutputFileName(self.defaultOutputFileName)

   def setOutputFileName(self, outputFileName):
      if not self.enabled:
         if self.outputFileName != self.defaultOutputFileName:
            #Our current file is not STDOUT, we must close it
            self.outputFile.close()
         self.outputFileName = outputFileName
         if self.outputFileName != self.defaultOutputFileName:
            #We are using a file that is not STDOUT, we must open it
            try:
               self.outputFile = open(self.outputFileName, "a");
            except (OSError,IOError):
               self.outputFileName = self.defaultOutputFileName
               self.outputFile = self.defaultOutputFile
               self.errorStatus = "Cannot open output file. Defaulting to STDOUT"
               return False
         else:
            self.outputFile = self.defaultOutputFile
         self.errorString = ""
         return True
      else:
         self.errorString = "Output file cannot be changed while debug is enabled."
         return False
