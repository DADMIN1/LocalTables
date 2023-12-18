import Pathinfo
import Extract
import Parsing
import pprint


def main(filename):
    extractedlines = Extract.ExtractHTMLTables(f"{filename}")
    #Extract.Printfile(f"./working_pages/StrippedTables/{filename}.Table")
    print("\n\n")
    print("#"*48)
    print("######__EXTRACTED_HTML__#__STRIPPED TABLE__######")
    print("#"*48)
    print("\n\n")
    print(extractedlines)
    print("\n\n")
    print("#"*36)
    print("######__END_OF_STRIPPED_TABLE__######")
    print("#"*36)
    print("\n\n")

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
    Pathinfo.CheckFolders()
    if len(Pathinfo.local_files['source']) > 0:
        print("found HTML files: ")
        for fpath in Pathinfo.local_files['source']:
            print(f"  {fpath.stem}{fpath.suffix}")
            main(fpath.stem)
        #main(Pathinfo.local_files['source'][0].stem)
