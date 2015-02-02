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

    class WaitForSymbol(ParserState):
        def run(self, char, parser):
            if char in string.whitespace:
                return self
            elif char in PgnParser.tagStart:
                return PgnParser.ParsingStateMachine.inTag
            elif char in string.ascii_letters:
                parser.moveSan = char
                return PgnParser.ParsingStateMachine.moveSan
            elif char in string.digits:
                parser.parsedNumber = char
                return PgnParser.ParsingStateMachine.moveNumber
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
                return PgnParser.ParsingStateMachine.waitForSymbol
            else:
                return PgnParser.ParsingStateMachine.ErrorState

    class MoveNumber(ParserState):
        def run(self, char, parser):
            if char in string.digits:
                parser.parsedNumber += char
                return self
            elif char in string.whitespace:
                if parser.checkMoveNumber():
                    return PgnParser.ParsingStateMachine.moveWaitForSan
                else:
                    return PgnParser.ParsingStateMachine.ErrorState

    class MoveWaitForSan(ParserState):
        def run(self, char, parser):
            if char in string.whitespace:
                return self
            elif char in string.ascii_letters:
                parser.moveSan = char
                return PgnParser.ParsingStateMachine.moveSan
            else:
                return PgnParser.ParsingStateMachine.ErrorState

    class MoveSan(ParserState):
        def run(self, char, parser):
            if char in PgnParser.symbolAllowed:
                parser.moveSan += char
                return self
            elif char in string.whitespace:
                parser.saveMove()
                return PgnParser.ParsingStateMachine.waitForSymbol
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


    ParsingStateMachine.waitForSymbol = WaitForSymbol()
    ParsingStateMachine.inTag = InTag()
    ParsingStateMachine.tagName = TagName()
    ParsingStateMachine.tagWaitForStringValue = TagWaitForStringValue()
    ParsingStateMachine.tagStringValue = TagStringValue()
    ParsingStateMachine.tagWaitForEnd = TagWaitForEnd()

    ParsingStateMachine.moveNumber = MoveNumber()
    ParsingStateMachine.moveWaitForSan = MoveWaitForSan()
    ParsingStateMachine.moveSan = MoveSan()





    def __init__(self):
        self.tags = {}
        self.moves = []
        self.tagName = ""
        self.tagValue = ""
        self.parsedNumber = ""
        self.currentMoveNumber = 1
        self.incrementMoveNumber = False
        self.moveSan = ""
        self.debug = Debug.Debug()
        self.SM = PgnParser.ParsingStateMachine(PgnParser.ParsingStateMachine.waitForSymbol, self)

    def reset(self):
        self.tags = {}
        self.moves = []
        self.tagName = ""
        self.tagValue = ""
        self.parsedNumber = ""
        self.currentMoveNumber = 1
        self.incrementMoveNumber = False
        self.moveSan = ""
        self.SM.reset()

    def parseString(self, inString):
        return self.SM.run(inString)


    def saveTag(self):
        self.tags[self.tagName] = Tag(self.tagName, self.tagValue)
        self.debug.dprint(self.tags[self.tagName])
        self.tagName = ""
        self.tagValue = ""

    def checkMoveNumber(self):
        returnVal = str(self.currentMoveNumber) == self.parsedNumber
        self.parsedNumber = ""
        return returnVal

    def saveMove(self):
        self.moves.append(self.moveSan)
        self.moveSan = ""
        if self.incrementMoveNumber:
            self.currentMoveNumber += 1
        self.incrementMoveNumber =  not self.incrementMoveNumber
