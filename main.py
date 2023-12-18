import Pathinfo
import Extract
import Parsing
import pprint


def main(filename):
    #Extract.Printfile(f"./working_pages/StrippedTables/{filename}.Table")
    #Extract.ExtractHTMLTables(f"{filename}")

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
    Pathinfo.PrintDirectoryInfo()
    main("Growth Rates")
