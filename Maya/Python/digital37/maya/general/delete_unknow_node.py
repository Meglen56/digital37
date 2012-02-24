import maya.cmds as cmds

allUnknow = cmds.ls(dep = True)
if allUnknow:
    for all in allUnknow:
        if(cmds.nodeType(all) == 'unknown'):
            try:
                cmds.lockNode(all, l = False)
                cmds.delete(all)
            except:
                print 'can not delete'