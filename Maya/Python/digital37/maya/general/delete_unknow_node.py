import maya.cmds as cmds

def main():
    allUnknow = cmds.ls(dep = True)
    if allUnknow:
        for n in allUnknow:
            if(cmds.nodeType(n) == 'unknown'):
                try:
                    cmds.lockNode(n, l = False)
                    cmds.delete(n)
                    print 'delete%s' % n
                except:
                    cmds.warning('can not delete%s' % n)