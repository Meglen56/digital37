import maya.cmds as cmds

def main(log=None):

    if not log:
        import logging
        log = logging.getLogger()
    
    allLight = cmds.ls(lights = True)
    if allLight:
        for x in allLight:
            try:
                cmds.delete(x)
                log.warning("delete light success:%s" %x)
            except:
                log.error("delete light error:%s" %x)
    else:
        log.debug("There is not light in the scene")