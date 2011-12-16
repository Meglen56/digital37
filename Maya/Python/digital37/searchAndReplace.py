import os
import fnmatch
import shutil
import tempfile
import sys

def replace(inputFile, pattern, subst):
    #Create temp file
    fh, abs_path = tempfile.mkstemp()
    new_file = open(abs_path,'w')
    old_file = open(inputFile)
    replaceFile = False
    for line in old_file:
        if pattern in line :
            replaceFile = True
            new_file.write(line.replace(pattern, subst))
        else :
            new_file.write(line)
    #close temp file
    new_file.close()
    os.close(fh)
    old_file.close()
    if replaceFile :
        #Remove original file
        os.remove(inputFile)
        #Move new file
        shutil.move(abs_path, inputFile)
        print inputFile, 'edited'
    else :
        print inputFile, 'not edited'
   
def listAllFiles (root,pattern='*',oneLevel = False, directory = False):
    pattern = pattern.split(';')
    for path, underDirectory, files in os.walk(root) :
        if directory :
            files.extend(underDirectory)
        files.sort()
        for name in files :
            for pat in pattern :
                if fnmatch.fnmatch(name, pat):
                    yield path, name
                    break
        if oneLevel :
            break
   

if __name__ == '__main__':
    for elem in listAllFiles(sys.argv[1], pattern='*.ma', directory = False) :
        filePath = os.path.join(elem[0], elem[1])
        try :
            replace(filePath, r'H:/Streamline_Quest_Featurette_11','$SNAP_PROJECT')
        except :
            print filePath, '*** ERROR ***'