import pathlib
from dataclasses import dataclass


def PrintDirectoryInfo():
    print("""\nFiles you want to operate on are expected to be in subdirectories under:
(LocalTables) ./working_pages/
    /HTML/           -> source HTML files (expected to have a '.html' suffix)
    /TextFile/       -> source HTMLs downloaded as 'text_only' files (.txt or .textonly suffix)
    /StrippedTables/ -> The HTML gets stripped of everything 
                            that isn't marked as a <table> and dumped here as [filename.Table]

These directories get searched by associated functions.
Pass only the filename, without the full path or filetype suffix\n""")

# we need a function to scan the subdirectories for files
# we need a function to select a file or files to operate on
# we need a function to choose the operation to perform


### trying to create a system to cache parsing results ###
### to avoid unnecessary reruns ###

currentDir = pathlib.Path.cwd()
workingdir = currentDir / "working_pages"
dumplist_file = pathlib.Path(workingdir) / 'dumplist.json'

assert pathlib.Path('../LocalTables').exists(), "LocalTables folder does not exist"
assert currentDir.samefile(pathlib.Path('../LocalTables')), "current directory is not correct"

subdir_names = {
    'source': 'HTML',
    'stripped': 'StrippedTables',
    'JSONdump': 'JSON_Tables',
    'Testfiles': 'Testfiles',
}

filetype_suffix = {
    'source': '.html',
    'stripped': '.Table',
    'JSONdump': '.jsondump',
    'Testfiles': '.*',
}


# dict holding lists of pathlib.Path objects
local_files = {
    'source': [],
    'stripped': [],
    'JSONdump': [],
    'Testfiles': [],
}


def CheckFolders():
    if not workingdir.exists():
        print("workdir does not exist; creating")
        workingdir.mkdir()
    inputdir = currentDir / "downloadedPages"
    if not inputdir.exists():
        print("inputdir does not exist; creating")
        inputdir.mkdir()
    for key, dirname in subdir_names.items():
        subpath = workingdir / dirname
        if not subpath.exists():
            print(f"{subpath} does not exist; creating")
            subpath.mkdir()
            local_files[key] = []
        else:  # find all the files of the matching suffix under that path
            foundfiles = subpath.glob(f"*{filetype_suffix[key]}")
            local_files[key] = sorted(foundfiles)
            # glob is case sensitive, unfortunately, and it can't be changed?


@dataclass
class Dumprecord:  # maps file to md5sum of that file
    name: str
    source: tuple[pathlib.Path, str] = (None, None)
    stripped: tuple[pathlib.Path, str] = (None, None)
    JSONdump: tuple[pathlib.Path, str] = (None, None)

    # def Addfile(self, m_type:str, *, override_suffix = None):
    #     thePath = pathlib.Path(workingdir) / subdir_names[m_type] / self.name
    #     if override_suffix:
    #         thePath = thePath.with_suffix(override_suffix)
    #     else:
    #         thePath = thePath.with_suffix(filetype_suffix[m_type])
    #
    #     if thePath.exists():
    #         sum = md5(thePath.open())
    #     setattr(self, m_type, (thePath,))


class Dumplist:
    lookupdict = {str, Dumprecord}


def validate_record(R: Dumprecord):
    m = R.__dict__
    for P in m:
        print(P, m[P])


# prevents this test code from running when it's imported
if __name__ == '__main__':
    testrec = Dumprecord("Testfile")
    testrec.stripped = ((pathlib.Path(workingdir) / 'StrippedTables' / "Testfile.Table"), "55555555")
    validate_record(testrec)


### end of file caching work ###
### end of file caching work ###

# tries to strip the filetype suffix and leading path from a filename
def ValidateFilename(N):
    print('\n')
    newname = N.split("/").pop()  # removes the leading path; assuming the filename will always be last
    newname = newname.split(".")[0]  # removes the suffix; filename will always be first.
    # Important that we do this after stripping the path, since it could start with a relative path './' or '../'
    return newname


def GetStrippedTablePath(name):
    name = ValidateFilename(name)
    subdir = workingdir / "StrippedTables"
    assert subdir.is_dir(), "subdir does not exist"
    new_filename = name + ".Table"
    new_filepath = subdir / new_filename
    return pathlib.Path(new_filepath)


def new_JSON_table_path(name):
    name = ValidateFilename(name)
    subdir = workingdir / "JSON_Tables"
    assert subdir.is_dir(), "subdir does not exist"
    new_filename = name + ".jsondump"
    new_filepath = subdir / new_filename
    return pathlib.Path(new_filepath)
