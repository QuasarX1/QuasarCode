import os
import sys

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
            copy(itemPath, os.path.join(copyRoot, os.path.split(os.path.relpath(dir, start = sourceRoot))[0], fName.split(sep = ".")[0] + ".pyc"))



configuration = sys.argv[1]
print(configuration)

sourceRoot = os.path.abspath(".\\QuasarCode")
buildRoot = os.path.abspath(".\\bin\\{}\\QuasarCode".format("Debug" if configuration == "Debug" else "Publish\\LatestVersion"))

# Compile all files in the root
os.system("python -m compileall \"{}\"".format(sourceRoot))

# Delete old build
if os.path.exists(buildRoot):
    # Removes contence of buildRoot
    for root, dirs, files in os.walk(buildRoot, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

    # Removes buildRoot
    os.rmdir(buildRoot)

# Re-creates buildRoot
os.mkdir(buildRoot)

# Copy all of the files to the build directory
recursiveCopyFiles(sourceRoot, sourceRoot, buildRoot)# TODO: copying twice??!