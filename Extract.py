import pprint
import pickle
import jsonpickle
import Parsing

from Pathinfo import ValidateFilename, new_JSON_table_path, workingdir


# STILL REQUIRES FULL PATH!!!
def Printfile(P):
    print("reading out file:", P)
    with open(P, 'r', encoding="utf-8") as F:
        for line in F:
            print(line, end='')
    print('done printing file')
    if F.closed:
        print('file closed')
    else:
        print('file not closed!')

# possible alternative for operating on multiple files at once:
    #with fileinput.input(files=(Filename), mode='r') as F:


# scan through the HTML file and throw out everything that isn't a table
def ExtractHTMLTables(Filename):
    Filename = ValidateFilename(Filename)
    NameWithPath = "./working_pages/HTML/" + Filename + ".html"

    with open(NameWithPath, mode='r', encoding="utf-8") as F:
        print("Extracting tables from: ", NameWithPath)
        goodLines = []
        isInTable = False

        # TODO: account for nested tables
        for line in F:
            if line.startswith("<table>"):
                isInTable = True

            if isInTable:
                goodLines.append(line)

            if line.startswith("</table>"):
                isInTable = False

    dumpName = "./working_pages/StrippedTables/" + Filename + ".Table"
    print("dumping tables to :", dumpName)
    with open(dumpName, mode='w', encoding="utf-8") as D:  # mode 'w' overwrites existing files
        D.writelines(goodLines)

    print("done")
    return goodLines


# json.dumps : parses any serialized python-objects and returns a string of json-formatted data
# json.dump : takes a python object and writes it into a JSON file. requires a file-pointer as a parameter
def DumpTableToJSON(table, *, tablename=None):
    jsonpickle.set_encoder_options('json', indent=2)  # otherwise it puts everything on one line
    JSONtable = jsonpickle.encode(table, unpicklable=True)
    # 'unpicklable' needs to be 'True' if you want to use it to reconstruct the object later
    # the 'un-' prefix is meant to connotate reversal, not impossibility

    if not tablename:
        tablename = table.name  # "no_name" by default
    with open(new_JSON_table_path(tablename), mode='w', encoding="utf-8") as PE:
        PE.write(JSONtable)
    return


def LoadTableFromJSON(filename) -> Parsing.Table:
    jsonpickle.set_decoder_options('json')
    filename = new_JSON_table_path(filename)
    with open(filename, mode='r', encoding="utf-8") as F:
        decoded = jsonpickle.decode(F.read())
    return decoded


# instead of using jsonpickle, we can instead dump it as a binary, but then you can't inspect it, so it's dumb
def DumpTableToBinary(table):
    with open(new_JSON_table_path("noPickle"), mode='wb') as NP:
        pickle.dump(table, NP, pickle.HIGHEST_PROTOCOL)


def LoadTableFromBinary():
    dumb = pickle.load(open(new_JSON_table_path("noPickle"), "rb"))
    new_filepath = workingdir / "JSON_Tables" / "dumb.jsondump"
    # opening the file and then redumping it to a text file (results in a ton of hexadecimal)
    with open(new_filepath, "a", encoding="UTF-8") as wtf:
        pprint.pprint(pickle.dumps(dumb), stream=wtf)
