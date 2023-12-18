import Pathinfo
import Extract
import Parsing
import pprint

#from bs4 import BeautifulSoup  # html parser
#import logging     #instead of printing everything lol
#import requests    # html requests
#import pydantic    # table/data classes?
#import pathlib     # file/directory manipulation, instead of splicing paths by hand
#    #also, instead of passing filenames around, you should be passing IOstreams
#    #and instead of concatenating strings with '+', you could be using a StringIO buffer

# import numpy      #array operations
# import pandas     #general data analysis

# difflib - compares sequences, creates diff summaries
# filecmp - compares files and directories.
# reprlib - provides attributes for custom object representations


def main():
    filename = "Growth Rates"

    #Extract.ValidateFilename("./Invalid Directory/fakefilename.html.extraExtend")  # testing
    #Extract.PrintDirectoryInfo()
    #Parsing.Printfile("./working_pages/StrippedTables/Growth Rates.Table")
    #Extract.ExtractHTMLTables("Growth Rates")

    filepath = Pathinfo.GetStrippedTablePath(filename)
    ParsedTable = Parsing.ConstructTable(filepath, tablename=filename)
    Extract.DumpTableToJSON(ParsedTable)

    LTable = Extract.LoadTableFromJSON(filename)

    print(LTable.header)
    for E in LTable.entries:
        print()
        firstColumn = True  # extra tab for name column
        for D in E.data_parsed:
            column_spacing = '\t'
            if firstColumn and len(D.value) < 8:    # long names don't need extra tab
                column_spacing = '\t\t'
            firstColumn = False
            print(D.value, end=column_spacing)

    print("\n\n")
    pprint.pprint(LTable, width=240)


if __name__ == "__main__":
    main()
    # Filename = "Growth Rates"
    # ParsedTable = Parsing.ConstructTable(Pathinfo.GetStrippedTablePath(Filename))
    # pprint.pprint(ParsedTable, width=240)


#import html.parser    # lmao
# https://docs.python.org/3/library/html.parser.html
