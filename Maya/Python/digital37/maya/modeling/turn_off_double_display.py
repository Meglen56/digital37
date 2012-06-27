import maya.cmds as cmds

def main(log=None):
    if not log:
        import logging
        log = logging.getLogger()
        
    allObj = cmds.ls( dag = True, type = ['mesh', 'nurbsSurface', 'subdiv'])
    try:
        cmds.displaySurface(allObj,twoSidedLighting = False)
        log.debug("turn off double display success")
    except:
        log.debug("turn off double display failure")
        for x in allObj:
            try:
                cmds.displaySurface(x,twoSidedLighting = False)
            except:
                log.error('can not set two side lighting false for %s' % x)
            else:
                pass