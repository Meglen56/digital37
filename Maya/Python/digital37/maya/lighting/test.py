import maya.cmds as cmds
import re
import os

def getShadingSG(shapesList):
    for shape in shapesList :
        
    
#def SYH_changeMapDetail(detail):
#    
#    noTexture = False
#    pattern = "."
#    
#    sel = cmds.ls(sl = True)
#    if(len(sel) <= 0):
#        print "no object are selected"
#        return
#        
#    cmds.select(cl = True)
#
#    for s in sel:
#        print s
#        cmds.select(s, r = True)
#        cmds.hyperShade(s, smn = True)
#        temp = cmds.ls(sl = True)
#        file = cmds.listConnections(temp[0], type = "file")
#        if(file == None):
#            noTexture = True
#        else:
#            noTexture = False
#            
#        if(not noTexture):
#            texture = cmds.getAttr(file[0] + ".fileTextureName")
#            print texture
#            finFile = texture.replace('.','__' + detail + '.')
#            print finFile
#            #if os.path.isfile(finFile) or not os.path.isfile(finFile) :
#            finFile = finFile.replace('\\','/')
#            finFile = re.sub( ('^.*/(' + 'sourceimages' + ')'), 'sourceimages', finFile )
#            cmds.setAttr(file[0] + ".fileTextureName", finFile, type = "string")
#            print finFile
#            print "process ok!"
        
#SYH_changeMapDetail("M")