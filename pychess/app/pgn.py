#!/usr/bin/env python
#File for PGN parser and exporter
import string

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
    symbolAllowed = symbolStart + "_" + "+" + "#" + "=" + "-"

    stringStartEnd = '"'


    def __init__(self):
        pass

    def parseTag(self, tagString):
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
                if char == "[":
                    inTag = True
                    continue
                elif char in string.whitespace:
                    continue
                else:
                    return returnVal
            elif not foundName:
                if inSymbol:
                    if char in self.symbolAllowed:
                        name += char
                        continue
                    elif char in string.whitespace:
                        foundName = True
                        continue
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
                    if char == '"':
                        foundValue = True
                        continue
                    else:
                        value += char
                elif char == '"':
                    inValue = True
                    continue
                elif char in string.whitespace:
                    continue
                else:
                    return returnVal
            elif char == "]":
                inTag = False
                returnVal = Tag(name, value)
                break
            elif char in string.whitespace:
                continue
            else:
                return returnVal
        print(returnVal.name, returnVal.value)
        return returnVal
