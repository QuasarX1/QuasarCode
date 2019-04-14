"""
Builds the project moving the compiled byte code to a seperate directory

Pass first paramiter as Debug for debug configuration or as Release for publishing configuration

Pass second paramiter as STANDARD for ordenary bytecode compilation, OPTIMIZE for opt-1 (uses -O), or OPTIMIZE2 for opt-2 (uses -OO)
"""

import os
import sys
import datetime

folderName = sys.argv[1]
print("Folder: {}".format(folderName))

configuration = sys.argv[2]
print("Configuration: {}".format(configuration))

optimization = sys.argv[3]
print("Optimization Mode: {}".format(optimization))

author = sys.argv[4] if len(sys.argv) >= 5 else ""
print("Author: {}".format(author))

sourceRoot = os.path.abspath("./{}".format(folderName))
buildRoot = os.path.abspath("./bin/{}/{}".format("Debug" if configuration == "Debug" else "Publish/LatestVersion", folderName))


def deleteDirectory(rootForDelete):
    if os.path.exists(rootForDelete):
        # Removes contence of buildRoot
        for root, dirs, files in os.walk(rootForDelete, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

        # Removes the root
        os.rmdir(rootForDelete)

def copy(file, target):
    string = "copy \"{}\" \"{}\"".format(file, target)

    os.makedirs(os.path.split(target)[0], exist_ok = True)

    os.system("copy \"{}\" \"{}\"".format(file, target))

def recursiveCopyFiles(dir, sourceRoot, copyRoot):
    # Ensure a folder path has been provided
    if os.path.isfile(dir):
        raise NotADirectoryError("The path \"{}\" dosn't reference a folder.".format(dir))

    for fName in os.listdir(dir):
        itemPath = os.path.join(dir, fName)

        # If a folder is present, try to copy its contence
        if os.path.isdir(itemPath):
            recursiveCopyFiles(itemPath, sourceRoot, copyRoot)

        ## If the item is an init file, copy the file as is
        #elif fName == "__init__.py":
        #    copy(itemPath, os.path.join(copyRoot, fName))

        # If a file is present and in a __pycache__ folder, copy and rename it
        elif os.path.split(dir)[1] == "__pycache__":
            if fName[-1] == "o":
                filetype = ".pyo"
            elif fName[-1] == "c":
                filetype = ".pyc"

            copy(itemPath, os.path.join(copyRoot, os.path.split(os.path.relpath(dir, start = sourceRoot))[0], fName.split(sep = ".")[0] + filetype))


# Delete all previous compilations
def recursivelyDeleteCompiled(dir):
    for fName in os.listdir(dir):
        itemPath = os.path.join(dir, fName)

        # If a folder is present
        if os.path.isdir(itemPath):
            # if it is a __pycache__ folder, delete it
            if fName  == "__pycache__":
                deleteDirectory(itemPath)
            # else, search the folder
            else:
                recursivelyDeleteCompiled(itemPath)

recursivelyDeleteCompiled(sourceRoot)

# Compile all files in the root
if optimization == "STANDARD":
    os.system("python -m compileall \"{}\"".format(sourceRoot))
elif optimization == "OPTIMIZE":
    os.system("python -O -m compileall \"{}\"".format(sourceRoot))
elif optimization == "OPTIMIZE2":
    os.system("python -OO -m compileall \"{}\"".format(sourceRoot))

# Delete old build
deleteDirectory(buildRoot)
# Re-creates buildRoot
os.mkdir(buildRoot)

# Copy all of the files to the build directory
recursiveCopyFiles(sourceRoot, sourceRoot, buildRoot)# TODO: copying twice??!

# Detail the configuration detaild of the build
time = datetime.datetime.now()
file = open(os.path.join(buildRoot, "configuration.txt"), "w")
file.writelines([
    "project_name={}\n".format(folderName),
    "version={}\n".format(0.3),
    "author={}\n".format(author),
    "configuration={}\n".format(configuration),
    "optimization={}\n".format(optimization),
    "date={}\n".format(time.strftime("%Y-%m-%d")),
    "time={}\n".format(time.strftime("%H:%M:%S:%f"))
    ])
file.close()