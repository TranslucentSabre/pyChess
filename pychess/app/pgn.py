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

    def __str__(self):
        value1 = self.value.replace('\\', '\\\\')
        value2 = value1.replace('"', '\\"')
        return "["+self.name+' "'+value2+'"]'




class PgnParser(object):

    symbolStart = string.ascii_letters + string.digits
    tagNameAllowed = symbolStart + "_"
    symbolAllowed = tagNameAllowed + "+" + "#" + "=" + "-"

    tagStart = "["
    tagEnd = "]"
    stringStartEnd = '"'

    escapeChar = "\\"

    class ParserState(object):
        def run(self, input, parser):
            assert 0, "run not implemented"

    class NotInTag(ParserState):
        def run(self, char, parser):
            if char in string.whitespace:
                return self
            elif char in PgnParser.tagStart:
                return PgnParser.ParsingStateMachine.inTag
            else:
                return PgnParser.ParsingStateMachine.ErrorState

    class InTag(ParserState):
        def run(self, char, parser):
            if char in string.whitespace:
                return self
            elif char in PgnParser.symbolStart:
                parser.tagName = char
                return PgnParser.ParsingStateMachine.tagName
            else:
                return PgnParser.ParsingStateMachine.ErrorState

    class TagName(ParserState):
        def run(self, char, parser):
            if char in PgnParser.tagNameAllowed:
                parser.tagName += char
                return self
            elif char in string.whitespace:
                return PgnParser.ParsingStateMachine.tagWaitForStringValue
            elif char in PgnParser.stringStartEnd:
                return PgnParser.ParsingStateMachine.tagStringValue
            else:
                return PgnParser.ParsingStateMachine.ErrorState

    class TagWaitForStringValue(ParserState):
        def run(self, char, parser):
            if char in string.whitespace:
                return self
            elif char in PgnParser.stringStartEnd:
                return PgnParser.ParsingStateMachine.tagStringValue
            else:
                return PgnParser.ParsingStateMachine.ErrorState

    class TagStringValue(ParserState):
        def __init__(self):
            self.escape = False

        def run(self, char, parser):
            if self.escape:
                parser.tagValue += char
                self.escape = False
                return self
            else:
                if char in PgnParser.escapeChar:
                    self.escape = True
                    return self
                elif char in PgnParser.stringStartEnd:
                    return PgnParser.ParsingStateMachine.tagWaitForEnd
                else:
                    parser.tagValue += char
                    return self

    class TagWaitForEnd(ParserState):
        def run(self, char, parser):
            if char in string.whitespace:
                return self
            elif char in PgnParser.tagEnd:
                parser.saveTag()
                return PgnParser.ParsingStateMachine.notInTag
            else:
                return PgnParser.ParsingStateMachine.ErrorState

    class ParsingStateMachine(object):
        def __init__(self, initialState, parser):
            self.initialState = initialState
            self.currentState = initialState
            self.parser = parser
            self.debug = Debug.Debug()

        def reset(self):
            self.currentState = self.initialState

        ErrorState = False

        def run(self, input):
            for i in input:
                self.currentState = self.currentState.run(i, self.parser)
                self.debug.dprint(i, self.currentState)
                if self.currentState == PgnParser.ParsingStateMachine.ErrorState:
                    return PgnParser.ParsingStateMachine.ErrorState
            return True


    ParsingStateMachine.notInTag = NotInTag()
    ParsingStateMachine.inTag = InTag()
    ParsingStateMachine.tagName = TagName()
    ParsingStateMachine.tagWaitForStringValue = TagWaitForStringValue()
    ParsingStateMachine.tagStringValue = TagStringValue()
    ParsingStateMachine.tagWaitForEnd = TagWaitForEnd()





    def __init__(self):
        self.tags = {}
        self.tagName = ""
        self.tagValue = ""
        self.debug = Debug.Debug()
        self.SM = PgnParser.ParsingStateMachine(PgnParser.ParsingStateMachine.notInTag, self)

    def reset(self):
        self.tags = {}
        self.tagName = ""
        self.tagValue = ""
        self.SM.reset()

    def parseTags(self, tagString):
        return self.SM.run(tagString)

    def saveTag(self):
        self.tags[self.tagName] = Tag(self.tagName, self.tagValue)
        self.debug.dprint(self.tags[self.tagName])
        self.tagName = ""
        self.tagValue = ""
