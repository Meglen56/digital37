import sys
sys.path.append('D:/workspace/tools/DIGITAL37/Maya/Python')

import maya.cmds as cmds
import maya.standalone
maya.standalone.initialize()

fileName = sys.argv[1]
print 'fileName:%s' % fileName
# read file to maya
cmds.file( fileName,o=True,f=True,type="mayaAscii")

import digital37.maya.general.ma2mb as ma2mb
ma2mb.main()




