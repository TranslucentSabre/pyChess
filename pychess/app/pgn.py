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

class State:
    def run(self,input):
        assert 0, "run not implemented"

class StateMachine:
    def __init__(self, initialState):
        self.initialState = initialState
        self.currentState = initialState
        self.debug = Debug.Debug()

    def reset(self):
        self.currentState = self.initialState

    ErrorState = False

    def run(self, input):
        for i in input:
            self.currentState = self.currentState.run(i)
            self.debug.dprint(i, self.currentState)
            if self.currentState == StateMachine.ErrorState:
                return StateMachine.ErrorState
        return True


class PgnParser(object):

    symbolStart = string.ascii_letters + string.digits
    tagNameAllowed = symbolStart + "_"
    symbolAllowed = tagNameAllowed + "+" + "#" + "=" + "-"

    tagStart = "["
    tagEnd = "]"
    stringStartEnd = '"'

    escapeChar = "\\"

    class NotInTag(State):
        def run(self, char):
            if char in string.whitespace:
                return self
            elif char in PgnParser.tagStart:
                return PgnParser.ParsingSM.inTag
            else:
                return PgnParser.ParsingSM.ErrorState

    class InTag(State):
        def run(self, char):
            if char in string.whitespace:
                return self
            elif char in PgnParser.symbolStart:
                PgnParser.tagName = char
                return PgnParser.ParsingSM.tagName
            else:
                return PgnParser.ParsingSM.ErrorState

    class TagName(State):
        def run(self, char):
            if char in PgnParser.tagNameAllowed:
                PgnParser.tagName += char
                return self
            elif char in string.whitespace:
                return PgnParser.ParsingSM.tagWaitForStringValue
            elif char in PgnParser.stringStartEnd:
                return PgnParser.ParsingSM.tagStringValue
            else:
                return PgnParser.ParsingSM.ErrorState

    class TagWaitForStringValue(State):
        def run(self, char):
            if char in string.whitespace:
                return self
            elif char in PgnParser.stringStartEnd:
                return PgnParser.ParsingSM.tagStringValue
            else:
                return PgnParser.ParsingSM.ErrorState

    class TagStringValue(State):
        def __init__(self):
            self.escape = False

        def run(self, char):
            if self.escape:
                PgnParser.tagValue += char
                self.escape = False
                return self
            else:
                if char in PgnParser.escapeChar:
                    self.escape = True
                    return self
                elif char in PgnParser.stringStartEnd:
                    return PgnParser.ParsingSM.tagWaitForEnd
                else:
                    PgnParser.tagValue += char
                    return self

    class TagWaitForEnd(State):
        def run(self, char):
            if char in string.whitespace:
                return self
            elif char in PgnParser.tagEnd:
                #PgnParser.debug.dprint(self.tagName, self.tagValue)
                PgnParser.tags[PgnParser.tagName] = Tag(PgnParser.tagName, PgnParser.tagValue)
                PgnParser.tagName = ""
                PgnParser.tagValue = ""
                return PgnParser.ParsingSM.notInTag
            else:
                return PgnParser.ParsingSM.ErrorState

    class ParsingSM(StateMachine):
        def __init__(self, initialState):
            StateMachine.__init__(self, initialState)

    ParsingSM.notInTag = NotInTag()
    ParsingSM.inTag = InTag()
    ParsingSM.tagName = TagName()
    ParsingSM.tagWaitForStringValue = TagWaitForStringValue()
    ParsingSM.tagStringValue = TagStringValue()
    ParsingSM.tagWaitForEnd = TagWaitForEnd()


    tags = {}
    tagName = ""
    tagValue = ""


    def __init__(self):
        self.debug = Debug.Debug()
        self.SM = PgnParser.ParsingSM(PgnParser.ParsingSM.notInTag)

    def reset(self):
        PgnParser.tags = {}
        PgnParser.tagName = ""
        PgnParser.tagValue = ""
        self.SM.reset()



    def parseTags(self, tagString):
        return self.SM.run(tagString)
