from __future__ import print_function
from sys import stdout
#TODO: Add ability to write to specified file 

class Debug(object):

   def __init__(self):
      self.sections = []
      self.indent = 2
      self.indentString = ""
      self.enabled = False
      self.outputFile = stdout

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
