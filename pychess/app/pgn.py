#!/usr/bin/env python
#File for PGN parser and exporter
import string, Debug

class Tag(object):

    def __init__(self, tagName="UNKNOWN", tagValue="UNKNOWN"):
        self.name = tagName
        self.value = tagValue

    def __eq__(self, other):
        if type(other) != Tag:
            return NotImplemented
        if self.name == other.name and \
           self.value == other.value:
            return True
        else:
            return False


class PgnParser(object):

    symbolStart = string.ascii_letters + string.digits
    tagNameAllowed = symbolStart + "_"
    symbolAllowed = tagNameAllowed + "+" + "#" + "=" + "-"

    tagStart = "["
    tagEnd = "]"
    stringStartEnd = '"'

    escapeChar = "\\"


    def __init__(self):
        self.tags = {}
        self.debug = Debug.Debug()
        self.tagName = ""
        self.tagValue = ""

        self.inTag = False
        self.inSymbol = False
        self.inValue = False
        self.foundName = False
        self.foundValue = False
        self.valueEscape = False

    def parseTags(self, tagString):
        returnVal = False
        for char in tagString:
            if not self.inTag:
                if char == self.tagStart:
                    self.inTag = True
                    continue
                elif char in string.whitespace:
                    continue
                else:
                    return returnVal
            elif not self.foundName:
                if self.inSymbol:
                    if char in self.tagNameAllowed:
                        self.tagName+= char
                        continue
                    elif char in string.whitespace:
                        self.foundName = True
                        self.inSymbol = False
                        continue
                    elif char in self.stringStartEnd:
                        self.foundName = True
                        self.inValue = True
                        self.inSymbol = False
                        continue
                    else:
                        return returnVal
                elif char in self.symbolStart:
                    self.inSymbol = True
                    self.tagName += char
                    continue
                elif char in string.whitespace:
                    continue
                else:
                    return returnVal
            elif not self.foundValue:
                if self.inValue:
                    if self.valueEscape:
                        self.tagValue += char
                        self.valueEscape = False
                        continue
                    if char == self.stringStartEnd:
                        self.foundValue = True
                        self.inValue = False
                        continue
                    if char == self.escapeChar:
                        self.valueEscape = True
                        continue
                    else:
                        self.tagValue += char
                        continue
                elif char == self.stringStartEnd:
                    self.inValue = True
                    continue
                elif char in string.whitespace:
                    continue
                else:
                    return returnVal
            elif char == self.tagEnd:
                self.inTag = False
                self.foundName = False
                self.foundValue = False
                self.debug.dprint(self.tagName, self.tagValue)
                self.tags[self.tagName] = Tag(self.tagName, self.tagValue)
                self.tagName = ""
                self.tagValue = ""
                continue
            elif char in string.whitespace:
                continue
            else:
                return returnVal
        returnVal = True
        return returnVal
