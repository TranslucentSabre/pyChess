#!/usr/bin/env python3
#File for PGN parser and exporter
import string, Debug
from pychess.app import Util, Debug

class Game(object):

    sevenTagRoster = ["Event", "Site", "Date", "Round", "White", "Black", "Result"]

    def __init__(self):
        self.strTags = { "Event" : "?", "Site" : "?", "Date" : "????.??.??", "Round" : "?", "White" : "?", "Black" : "?", "Result" : "*" }
        self.tags = {}
        self.moves = {}
        self.lastMove = Move()
        self.gameTerm = ""
        
    def setTag(self, tagClass):
        if tagClass.name in Game.sevenTagRoster:
            self.strTags[tagClass.name] = tagClass
        else:
            self.tags[tagClass.name] = tagClass
            
    def getTag(self, tagName):
        if tagName in self.strTags:
            return self.strTags[tagName]
        elif tagName in self.tags:
            return self.tags[tagName]
        else:
            return ""

    def getTags(self):
        tags = []
        for tag in self.sevenTagRoster:
            tags.append(self.strTags[tag])
        for tag in sorted(self.tags):
            tags.append(self.tags[tag])
        return tags

    def saveMove(self, moveNumber, moveSan):
        self.lastMove = Move(moveNumber, moveSan)
        self.moves[moveNumber] = self.lastMove


    def getMove(self, moveNumber):
        if moveNumber in self.moves:
            return self.moves[moveNumber]
        else:
            return False

    def getMoves(self):
        moveNumber = "1."
        while True:
            if moveNumber in self.moves:
                yield self.moves[moveNumber]
            else:
                raise StopIteration()
            moveNumber = Util.getNextTurnString(moveNumber)

    def saveMoveSuffix(self, moveSuffix):
        returnVal = self.lastMove.setSuffixNag(moveSuffix)
        return returnVal

    def saveNag(self, moveNag):
        returnVal = self.lastMove.setNag(int(moveNag))
        return returnVal
        
    def saveGameTermination(self, gameTerm):
        self.gameTerm = gameTerm
        self.setTag(Tag("Result", gameTerm))
        
    def __str__(self):
        stringRep = ""
        for tag in self.getTags():
            stringRep += str(tag)+"\n"
        stringRep += "\n"
        
        turns = ["white", "black"]
        turnIndex = 0
            
        currentLine = ""
        for move in self.getMoves():
            startIndex = 0
            if turns[turnIndex] == "black":
                startIndex = 1
            turnIndex = (turnIndex + 1) % 2
            
            items = str(move).split()
            for itemIndex in range(startIndex, len(items)):
                if (len(currentLine) == 0):
                    currentLine += items[itemIndex]
                elif (len(currentLine) + len(" "+items[itemIndex])) < 80:
                    currentLine += " "+items[itemIndex]
                else:
                    stringRep += currentLine + "\n"
                    currentLine = items[itemIndex]
            
        stringRep += currentLine+" "+self.gameTerm
        return stringRep
            

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

class Move(object):

    def __init__(self, moveNumber = "", moveSan = ""):
        self.san = moveSan
        self.number = moveNumber
        self.nag = 0

    def setSuffixNag(self, suffixString):
        allowedSuffixes = { "!" : 1, "?" : 2, "!!" : 3, "??" : 4, "!?" : 5, "?!" : 6 }
        if suffixString in allowedSuffixes:
            return self.setNag(allowedSuffixes[suffixString])
        else:
            return False

    def setNag(self, nagInt):
        if type(nagInt) is int and nagInt >= 0 and nagInt <= 255:
            self.nag = nagInt
            return True
        else:
            return False
            
    def __str__(self):
        stringRep = self.number+" "+self.san
        if self.nag != 0:
            stringRep += " $"+str(self.nag)
        return stringRep




class PgnParser(object):

    symbolStart = string.ascii_letters + string.digits
    tagNameAllowed = symbolStart + "_"
    symbolAllowed = tagNameAllowed + "+" + "#" + "=" + "-"

    singleCharacterTermination = ["*"]
    validTermination = singleCharacterTermination + ["1-0", "0-1", "1/2-1/2"]

    tagStart = "["
    tagEnd = "]"
    stringStartEnd = '"'

    escapeChar = "\\"
    moveSuffixAllowed = "!?"
    nagStart = "$"
    terminationSpecialChars = "/-"

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
                self.parser.parserErrorString="Unexpected character waiting for symbol"
                return PgnParser.ParsingStateMachine.ErrorState

    class InTag(ParserState):
        def run(self, char, parser):
            if char in string.whitespace:
                return self
            elif char in PgnParser.symbolStart:
                parser.tagName = char
                return PgnParser.ParsingStateMachine.tagName
            else:
                self.parser.parserErrorString="Unexpected character looking for tag name"
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
                self.parser.parserErrorString="Unexpected character while parsing tag name"
                return PgnParser.ParsingStateMachine.ErrorState

    class TagWaitForStringValue(ParserState):
        def run(self, char, parser):
            if char in string.whitespace:
                return self
            elif char in PgnParser.stringStartEnd:
                return PgnParser.ParsingStateMachine.tagStringValue
            else:
                self.parser.parserErrorString="Unexpected character waiting for tag value"
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
                self.parser.parserErrorString="Unexpected character waiting for close of tag"
                return PgnParser.ParsingStateMachine.ErrorState

    class MoveNumber(ParserState):
        def run(self, char, parser):
            if char in string.digits:
                parser.parsedNumber += char
                return self
            elif char in string.whitespace:
                if parser.checkMoveNumber():
                    return PgnParser.ParsingStateMachine.moveWaitForSanOrDots
                else:
                    self.parser.parserErrorString="Parsed move number is not what is expected"
                    return PgnParser.ParsingStateMachine.ErrorState
            elif char in ".":
                if parser.checkMoveNumber():
                    return PgnParser.ParsingStateMachine.moveConsumeDots
                else:
                    self.parser.parserErrorString="Parsed move number is not what is expected"
                    return PgnParser.ParsingStateMachine.ErrorState
            elif char in PgnParser.terminationSpecialChars:
                parser.gameTerm = parser.parsedNumber
                parser.gameTerm += char
                parser.parsedNumber = ""
                return PgnParser.ParsingStateMachine.moveGameTermination
            else:
                self.parser.parserErrorString="Unexpected character while parsing number"
                return PgnParser.ParsingStateMachine.ErrorState

    class MoveWaitForSanOrDots(ParserState):
        def run(self, char, parser):
            if char in string.whitespace:
                return self
            elif char in ".":
                return PgnParser.ParsingStateMachine.moveConsumeDots
            elif char in string.ascii_letters:
                parser.moveSan = char
                return PgnParser.ParsingStateMachine.moveSan
            else:
                self.parser.parserErrorString="Unexpected character while waiting for move san or dots"
                return PgnParser.ParsingStateMachine.ErrorState

    class MoveConsumeDots(ParserState):
        def run(self, char, parser):
            if char in ".":
                return self
            elif char in string.ascii_letters:
                parser.moveSan = char
                return PgnParser.ParsingStateMachine.moveSan
            elif char in string.whitespace:
                return PgnParser.ParsingStateMachine.moveWaitForSan
            else:
                self.parser.parserErrorString="Unexpected character while consuming dots"
                return PgnParser.ParsingStateMachine.ErrorState

    class MoveWaitForSan(ParserState):
        def run(self, char, parser):
            if char in string.whitespace:
                return self
            elif char in string.ascii_letters:
                parser.moveSan = char
                return PgnParser.ParsingStateMachine.moveSan
            else:
                self.parser.parserErrorString="Unexpected character while waiting for move san"
                return PgnParser.ParsingStateMachine.ErrorState

    class MoveSan(ParserState):
        def run(self, char, parser):
            if char in PgnParser.symbolAllowed:
                parser.moveSan += char
                return self
            elif char in string.whitespace:
                parser.saveMove()
                return PgnParser.ParsingStateMachine.moveWaitForNagOrSymbol
            elif char in PgnParser.moveSuffixAllowed:
                parser.saveMove()
                parser.moveSuffix = char
                return PgnParser.ParsingStateMachine.moveSuffixAnnotation
            elif char in PgnParser.nagStart:
                parser.saveMove()
                return PgnParser.ParsingStateMachine.moveNagDigits
            else:
                self.parser.parserErrorString="Unexpected character while parsing move san"
                return PgnParser.ParsingStateMachine.ErrorState

    class MoveSuffixAnnotation(ParserState):
        def run(self, char, parser):
            if char in PgnParser.moveSuffixAllowed:
                parser.moveSuffix += char
                return self
            elif char in string.whitespace:
                if parser.saveMoveSuffix():
                    return PgnParser.ParsingStateMachine.moveWaitForGameTermOrSymbol
                else:
                    self.parser.parserErrorString="Invalid move suffix"
                    return PgnParser.ParsingStateMachine.ErrorState
            else:
                self.parser.parserErrorString="Unexpected character while parsing move suffix"
                return PgnParser.ParsingStateMachine.ErrorState

    class MoveWaitForNagOrSymbol(ParserState):
        def run(self, char, parser):
            if char in string.whitespace:
                return self
            elif char in PgnParser.nagStart:
                return PgnParser.ParsingStateMachine.moveNagDigits
            elif char in string.ascii_letters:
                parser.moveSan = char
                return PgnParser.ParsingStateMachine.moveSan
            elif char in string.digits:
                parser.parsedNumber = char
                return PgnParser.ParsingStateMachine.moveNumber
            elif char in PgnParser.singleCharacterTermination:
                parser.gameTerm = char
                return PgnParser.ParsingStateMachine.moveGameTermination
            else:
                self.parser.parserErrorString="Unexpected character while waiting for NAG or move symbol"
                return PgnParser.ParsingStateMachine.ErrorState

    class MoveNagDigits(ParserState):
        def run(self, char, parser):
            if char in string.digits:
                parser.moveNag += char
                return self
            elif char in string.whitespace:
                if parser.saveNag():
                    return PgnParser.ParsingStateMachine.moveWaitForGameTermOrSymbol
                else:
                    self.parser.parserErrorString="Invalid NAG"
                    return PgnParser.ParsingStateMachine.ErrorState
            else:
                self.parser.parserErrorString="Unexpected character while parsing NAG"
                return PgnParser.ParsingStateMachine.ErrorState

    class MoveWaitForGameTermOrSymbol(ParserState):
        def run(self, char, parser):
            if char in string.whitespace:
                return self
            elif char in string.ascii_letters:
                parser.moveSan = char
                return PgnParser.ParsingStateMachine.moveSan
            elif char in string.digits:
                parser.parsedNumber = char
                return PgnParser.ParsingStateMachine.moveNumber
            elif char in PgnParser.singleCharacterTermination:
                parser.gameTerm = char
                return PgnParser.ParsingStateMachine.moveGameTermination
            else:
                self.parser.parserErrorString="Unexpected character while waiting for move symbol or game termination"
                return PgnParser.ParsingStateMachine.ErrorState

    class MoveGameTermination(ParserState):
        def run(self, char, parser):
            if char in string.digits or char in PgnParser.terminationSpecialChars:
                parser.gameTerm += char
                return self
            elif char in string.whitespace:
                if parser.checkGameTermination():
                    parser.saveGameTermination()
                    return PgnParser.ParsingStateMachine.waitForSymbol
                else:
                    self.parser.parserErrorString="Invalid game termination"
                    return PgnParser.ParsingStateMachine.ErrorState
            else:
                self.parser.parserErrorString="Unexpected character while parsing game termination"
                return PgnParser.ParsingStateMachine.ErrorState


    class ParsingStateMachine(object):
        def __init__(self, initialState, parser):
            self.initialState = initialState
            self.currentState = initialState
            self.parser = parser
            self.line = 1
            self.character = 1
            self.debug = Debug.Debug()

        def reset(self):
            self.currentState = self.initialState

        ErrorState = False

        def run(self, input):
            for i in input:
                self.currentState = self.currentState.run(i, self.parser)
                self.debug.dprint(i, self.currentState)
                if self.currentState == PgnParser.ParsingStateMachine.ErrorState:
                    self.parser.parsingErrorString = "Error :"+self.line+":"+self.character+" :"+self.parser.parsingErrorString
                    return PgnParser.ParsingStateMachine.ErrorState
                if i == "\n":
                    self.line += 1
                    self.character = 1
                else:
                    self.character += 1

            return True


    ParsingStateMachine.waitForSymbol = WaitForSymbol()
    ParsingStateMachine.inTag = InTag()
    ParsingStateMachine.tagName = TagName()
    ParsingStateMachine.tagWaitForStringValue = TagWaitForStringValue()
    ParsingStateMachine.tagStringValue = TagStringValue()
    ParsingStateMachine.tagWaitForEnd = TagWaitForEnd()

    ParsingStateMachine.moveNumber = MoveNumber()
    ParsingStateMachine.moveWaitForSanOrDots = MoveWaitForSanOrDots()
    ParsingStateMachine.moveConsumeDots = MoveConsumeDots()
    ParsingStateMachine.moveWaitForSan = MoveWaitForSan()
    ParsingStateMachine.moveSan = MoveSan()
    ParsingStateMachine.moveSuffixAnnotation = MoveSuffixAnnotation()
    ParsingStateMachine.moveWaitForNagOrSymbol = MoveWaitForNagOrSymbol()
    ParsingStateMachine.moveNagDigits = MoveNagDigits()
    ParsingStateMachine.moveWaitForGameTermOrSymbol = MoveWaitForGameTermOrSymbol()
    ParsingStateMachine.moveGameTermination = MoveGameTermination()





    def __init__(self, pgnFile):
        self.pgnFile = pgnFile
        self.tagName = ""
        self.tagValue = ""
        self.parsedNumber = ""
        self.currentMoveNumber = 1
        self.incrementMoveNumber = False
        self.moveSan = ""
        self.moveSuffix = ""
        self.moveNag = ""
        self.gameTerm = ""
        self.debug = Debug.Debug()
        self.SM = PgnParser.ParsingStateMachine(PgnParser.ParsingStateMachine.waitForSymbol, self)
        self.parserErrorString = ""

    def reset(self):
        self.SM.reset()
        self.parserErrorString = ""
        self.resetForNewGame()

    def resetForNewGame(self):
        self.tagName = ""
        self.tagValue = ""
        self.parsedNumber = ""
        self.currentMoveNumber = 1
        self.incrementMoveNumber = False
        self.moveSan = ""
        self.moveSuffix = ""
        self.moveNag = ""
        self.gameTerm = ""

    def parseString(self, inString):
        return self.SM.run(inString+"\n")

    def getParseErrorString(self):
        return self.parserErrorString

    def saveTag(self):
        self.pgnFile.saveTag(self.tagName, self.tagValue)
        self.tagName = ""
        self.tagValue = ""

    def checkMoveNumber(self):
        returnVal = str(self.currentMoveNumber) == self.parsedNumber
        self.parsedNumber = ""
        return returnVal

    def saveMove(self):
        moveNumber = str(self.currentMoveNumber)+"."
        if self.incrementMoveNumber:
            moveNumber += ".."
        self.pgnFile.saveMove(moveNumber, self.moveSan)
        self.moveSan = ""
        if self.incrementMoveNumber:
            self.currentMoveNumber += 1
        self.incrementMoveNumber =  not self.incrementMoveNumber

    def saveMoveSuffix(self):
        returnVal = self.pgnFile.saveMoveSuffix(self.moveSuffix)
        self.moveSuffix = ""
        return returnVal

    def saveNag(self):
        returnVal = self.pgnFile.saveNag(int(self.moveNag))
        self.moveNag = ""
        return returnVal
        
    def saveGameTermination(self):
        self.pgnFile.saveGameTermination(self.gameTerm)
        self.resetForNewGame()
        

    def checkGameTermination(self):
        if self.gameTerm in self.validTermination:
            return True
        else:
            return False


class PgnFile(object):
    def __init__(self):
        self.parser = PgnParser(self)
        self.games = []
        self.currentGame = Game()
        self.debug = Debug.Debug()

    def reset(self):
        self.games = []
        self.currentGame = Game()
        self.parser.reset()

    def parseString(self, inString):
        return self.parser.parseString(inString)

    def getParseErrorString(self):
        return self.parser.getParseErrorString()

    def saveTag(self, tagName, tagValue):
        self.currentGame.setTag(Tag(tagName, tagValue))
        self.debug.dprint(self.currentGame.getTag(tagName))

    def saveMove(self, moveNumber, moveSan):
        self.currentGame.saveMove(moveNumber, moveSan)

    def saveMoveSuffix(self, moveSuffix):
        returnVal = self.currentGame.saveMoveSuffix(moveSuffix)
        return returnVal

    def saveNag(self, moveNag):
        returnVal = self.currentGame.saveNag(int(moveNag))
        return returnVal
        
    def saveGameTermination(self, gameTerm):
        self.currentGame.saveGameTermination(gameTerm)
        self.games.append(self.currentGame)
        self.currentGame = Game()
        self.parser.resetForNewGame()
        
    def __str__(self):
        stringRep = ""
        firstTimeThrough = True
        for game in self.games:
            if firstTimeThrough:
                firstTimeThrough = False
            else:
                stringRep += "\n\n"
            stringRep += str(game)

        return stringRep
