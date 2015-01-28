#!/usr/bin/env python
#File for PGN parser and exporter

class Tag(object):

    def __init__(self, tagName, tagValue):
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

    def __init__(self):
        pass

    def parseTag(self, tagString):
        components = tagString.split()
        inTag = False
        foundName = False
        valueArray = []
        for piece in components:
            if not inTag:
                if piece == "[":
                    inTag = True
                    continue
            elif not foundName:
                name = piece
                foundName = True
            elif piece != "]":
                valueArray.append(piece)
            else:
                #Found the end of a tag
                name = components[1]
                value = " ".join(valueArray)
                if value[0] == '"' and value[-1] == '"':
                    value = value.strip('"')
                    tag = Tag(name, value)
                else:
                    return False
        return tag
