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


    def __init__(self):
        self.tags = {}
        self.debug = Debug.Debug()

    def parseTags(self, tagString):
        returnVal = False
        inTag = False
        inSymbol = False
        inValue = False
        foundName = False
        foundValue = False
        name = ""
        value = ""
        for char in tagString:
            if not inTag:
                if char == self.tagStart:
                    inTag = True
                    continue
                elif char in string.whitespace:
                    continue
                else:
                    return returnVal
            elif not foundName:
                if inSymbol:
                    if char in self.tagNameAllowed:
                        name += char
                        continue
                    elif char in string.whitespace:
                        foundName = True
                        inSymbol = False
                        continue
                    elif char in self.stringStartEnd:
                        foundName = True
                        inValue = True
                        inSymbol = False
                        continue
                    else:
                        return returnVal
                elif char in self.symbolStart:
                    inSymbol = True
                    name += char
                    continue
                elif char in string.whitespace:
                    continue
                else:
                    return returnVal
            elif not foundValue:
                if inValue:
                    if char == self.stringStartEnd:
                        foundValue = True
                        inValue = False
                        continue
                    else:
                        value += char
                elif char == self.stringStartEnd:
                    inValue = True
                    continue
                elif char in string.whitespace:
                    continue
                else:
                    return returnVal
            elif char == self.tagEnd:
                inTag = False
                foundName = False
                foundValue = False
                self.debug.dprint(name, value)
                self.tags[name] = Tag(name, value)
                name = ""
                value = ""
                continue
            elif char in string.whitespace:
                continue
            else:
                return returnVal
        returnVal = True
        return returnVal
