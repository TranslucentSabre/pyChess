#!/usr/bin/env python
#File for PGN parser and exporter

class Tag(object):

    def __init__(self, tagName, tagValue, tagType):
        self.name = tagName
        self.value = tagValue
        self.tagType = tagType

    def __eq__(self, other):
        if type(other) != Tag:
            return NotImplemented
        if self.name == other.name and \
           self.value == other.value and \
           self.tagType == other.tagType:
            return True
        else:
            return False


class PgnParser(object):

    def __init__(self):
        pass

    def parseTag(self, tagString):
        components = tagString.split()
        name = components[1]
        value = components[2]
        tagType = "other"
        if value[0] == "\"" and value[-1] == "\"":
            tagType = "string"
            value.strip('"')
        tag = Tag(name, value, tagType)
        print(tag.name, tag.value, tag.tagType)
        return tag
