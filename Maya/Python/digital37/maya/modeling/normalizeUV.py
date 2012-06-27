import maya.cmds as cmds

def main(log=None):

    if not log:
        import logging
        log = logging.getLogger()
    
    allObj = cmds.ls(dag=True,type = 'mesh')
    for x in allObj:
        try:
            cmds.polyNormalizeUV(x, nt = 1, pa = False)
            #log.debug("normalize %s uv to 0-1 range successful" %x)
        except:
            log.warning("normalize %s uv to 0-1 range error" %x)