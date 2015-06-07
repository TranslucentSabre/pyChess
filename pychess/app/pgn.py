#!/usr/bin/env python3
#File for PGN parser and exporter
import string, Debug

class Game(object):

    sevenTagRoster = ["Event", "Site", "Date", "Round", "White", "Black", "Result"]

    def __init__(self):
        self.strTags = { "Event" : "?", "Site" : "?", "Date" : "????.??.??", "Round" : "?", "White" : "?", "Black" : "?", "Result" : "*" }
        self.tags = {}
        self.moves = []
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
        
    def saveMove(self, moveNumber, moveSan):
        self.lastMove = Move(moveNumber, moveSan)
        self.moves.append(self.lastMove)

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
        for tag in self.sevenTagRoster:
            stringRep += str(self.strTags[tag])+"\n"
        for tag in sorted(self.tags):
            stringRep += str(self.tags[tag])+"\n"
        stringRep += "\n"
        
        turns = ["white", "black"]
        turnIndex = 0
            
        currentLine = ""
        for move in self.moves:
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
                    return PgnParser.ParsingStateMachine.moveWaitForSanOrDots
                else:
                    return PgnParser.ParsingStateMachine.ErrorState
            elif char in ".":
                if parser.checkMoveNumber():
                    return PgnParser.ParsingStateMachine.moveConsumeDots
                else:
                    return PgnParser.ParsingStateMachine.ErrorState
            elif char in PgnParser.terminationSpecialChars:
                parser.gameTerm = parser.parsedNumber
                parser.gameTerm += char
                parser.parsedNumber = ""
                return PgnParser.ParsingStateMachine.moveGameTermination
            else:
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
                return PgnParser.ParsingStateMachine.ErrorState

    class MoveConsumeDots(ParserState):
        def run(self, char, parser):
            if char in ".":
                return self
            elif char in string.whitespace:
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
                return PgnParser.ParsingStateMachine.moveWaitForNagOrSymbol
            elif char in PgnParser.moveSuffixAllowed:
                parser.saveMove()
                parser.moveSuffix = char
                return PgnParser.ParsingStateMachine.moveSuffixAnnotation
            elif char in PgnParser.nagStart:
                parser.saveMove()
                return PgnParser.ParsingStateMachine.moveNagDigits
            else:
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
                    return PgnParser.ParsingStateMachine.ErrorState
            else:
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
                    return PgnParser.ParsingStateMachine.ErrorState
            else:
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
                    return PgnParser.ParsingStateMachine.ErrorState
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
    ParsingStateMachine.moveWaitForSanOrDots = MoveWaitForSanOrDots()
    ParsingStateMachine.moveConsumeDots = MoveConsumeDots()
    ParsingStateMachine.moveWaitForSan = MoveWaitForSan()
    ParsingStateMachine.moveSan = MoveSan()
    ParsingStateMachine.moveSuffixAnnotation = MoveSuffixAnnotation()
    ParsingStateMachine.moveWaitForNagOrSymbol = MoveWaitForNagOrSymbol()
    ParsingStateMachine.moveNagDigits = MoveNagDigits()
    ParsingStateMachine.moveWaitForGameTermOrSymbol = MoveWaitForGameTermOrSymbol()
    ParsingStateMachine.moveGameTermination = MoveGameTermination()





    def __init__(self):
        self.games = []
        self.currentGame = Game()
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

    def reset(self):
        self.games = []
        self.currentGame = Game()
        self.tagName = ""
        self.tagValue = ""
        self.parsedNumber = ""
        self.currentMoveNumber = 1
        self.incrementMoveNumber = False
        self.moveSan = ""
        self.moveSuffix = ""
        self.moveNag = ""
        self.gameTerm = ""
        self.SM.reset()

    def parseString(self, inString):
        return self.SM.run(inString+"\n")


    def saveTag(self):
        self.currentGame.setTag(Tag(self.tagName, self.tagValue))
        self.debug.dprint(self.currentGame.getTag(self.tagName))
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
        self.currentGame.saveMove(moveNumber, self.moveSan)
        self.moveSan = ""
        if self.incrementMoveNumber:
            self.currentMoveNumber += 1
        self.incrementMoveNumber =  not self.incrementMoveNumber

    def saveMoveSuffix(self):
        returnVal = self.currentGame.saveMoveSuffix(self.moveSuffix)
        self.moveSuffix = ""
        return returnVal

    def saveNag(self):
        returnVal = self.currentGame.saveNag(int(self.moveNag))
        self.moveNag = ""
        return returnVal
        
    def saveGameTermination(self):
        self.currentGame.saveGameTermination(self.gameTerm)
        self.games.append(self.currentGame)
        self.currentGame = Game()
        

    def checkGameTermination(self):
        if self.gameTerm in self.validTermination:
            return True
        else:
            return False
