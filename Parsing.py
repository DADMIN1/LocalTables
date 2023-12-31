from enum import Enum   # required for Enums
import re   # regular-expression library
from dataclasses import dataclass


@dataclass
class Table:
    name: str
    header: list    # filled after iterating over the "header" section
    entries: list   # filled with completed Entry-class objects
    def __init__(self, *, myname="no_name"):    # asterisk makes "myname" keyword-only
        self.name = myname
        self.header = []    # filled after iterating over the "header" section
        self.entries = []   # filled with completed Entry-class objects


@dataclass
class Entry:
    rawsection: list
    data_parsed: list   # array instead of map because we'll just map it later (html should always be in order)
    datamap: dict   # keys are the Table's header's strings at the time of the entry's creation, mapped to data values
    def __init__(self, rawlines):
        self.rawsection = rawlines
        self.data_parsed = []
        self.datamap = {}


class Tagtype(Enum):
    header = 'th'
    section = 'tr'  # table-row
    data = 'td'     # cell
    #span = 'span'
    table = 'table'
    def __init__(self, extraAttr=None, isClosing=False):
        self.extraAttr = extraAttr
        self.isClosing = isClosing
    # TODO: handle opening/closing logic in here


def isKnownTag(tagstr): return tagstr in {x.value for x in Tagtype}


@dataclass
class ParsedLine:
    sourceline: str
    rawtags: list
    tags: list
    value: str
    endtags: list
    def __init__(self, sourceline):
        self.sourceline = sourceline
        # we're also storing the tags as text instead of converting all of them to Tagtypes because they might not be known
        self.rawtags = []   # note that the enclosing brackets have already been removed
        self.tags = []  # Tagtypes we found while parsing the raw tag-strings
        self.value = ''
        self.endtags = []   # Closing tags, with the leading slash already removed; </th> -> 'th'


def ParseLine(line):
    Result = ParsedLine(line)
    # finds all substrings that occur between characters '<' and '>'
    foundtags = re.findall(r"(?<=<).+?(?=>)", line)
    Result.rawtags = foundtags  # returns an array of matching substrings, without the enclosing delimiters

    for T in foundtags:
        isEndtag = False
        line = line.replace('<' + T + '>', '')  # re-adding enclosing brackets, then removing it from the original line

        if T.startswith('/'):
            isEndtag = True
            T = T.removeprefix('/')

        spl = T.split(' ')
        # if the tag contains a space, only the first word defines the type (the rest are HTML attributes)
        T = spl[0]
        # we're doing this to make the strings appropriate for Tagtype-enum conversion
        # TODO: parse/save the attributes within tags (ESPECIALLY ID!!!)
        attrs = [spl[x] for x in range(1, len(spl))]

        if isKnownTag(T):
            newtag = Tagtype(T)
            newtag.extraAttr = attrs
            if isEndtag:
                newtag.isClosing = True
                Result.endtags.append(newtag)
            else:
                Result.tags.append(newtag)

    # whatever's left in the line should be the value
    Result.value = line
    return Result


def DivideIntoSections(TableFile):
    dividedSections = []
    with open(TableFile, mode='r', encoding="utf-8") as F:
        # 'with' automatically closes file when done. 'r' opens as read-only
        inSection = False
        currentsection = []
        for line in F:
            line = line.strip('\n')
            match line:
                case '<tr>':
                    inSection = True
                    continue
                case '</tr>':
                    inSection = False
                    dividedSections.append(currentsection.copy())
                    currentsection.clear()
                    continue
            if inSection:
                currentsection.append(line)
    return dividedSections.copy()


def ConstructTable(TableFile, *, tablename=None):
    WorkingTable = Table()
    if tablename: WorkingTable.name = tablename
    sections = DivideIntoSections(TableFile)

    for rawsection in sections:
        WorkingTable.entries.append(Entry(rawsection))

    for E in WorkingTable.entries:
        for rawline in E.rawsection:
            E.data_parsed.append(ParseLine(rawline))

        # We're assuming that the file/table only has a single header,
        # or that all headers are identical?
        tempHeader = []
        currentindex = 0

        print(WorkingTable.header)
        print(E.data_parsed)
        for D in E.data_parsed:  # D is of class ParsedLine
            match D.tags:
                case [Tagtype.header]:  # these need to match up with whatever ParseLine is doing
                    tempHeader.append(D.value)
                case [Tagtype.data]:
                    if len(WorkingTable.header) == 0:   # workaround
                        if len(tempHeader) > currentindex:
                            E.datamap.update({tempHeader[currentindex]: D.value})
                            currentindex += 1
                        continue
                    E.datamap.update({WorkingTable.header[currentindex]: D.value})  # assuming that the header has already been written
                    currentindex += 1
            # we're ignoring the closing tags and also section/unknown tags

        if tempHeader:  # if we wrote any lines tagged as header
            WorkingTable.header = tempHeader.copy()

    return WorkingTable
