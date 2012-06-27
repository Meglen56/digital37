import maya.cmds as cmds

def main(log=None):

    if not log:
        import logging
        log = logging.getLogger()
    
    allObj = cmds.ls(type = ['mesh', 'nurbsSurface', 'subdiv'])
    for x in allObj:
        trans = cmds.listRelatives(x, p = True, f = True)
        try:
            cmds.makeIdentity(trans, a = True, t = True, r = True, s = True, n = 0)
            #log.debug("%s zeroObject successful!" %trans)
        except:
            log.warning("%s zeroObject error" %trans)