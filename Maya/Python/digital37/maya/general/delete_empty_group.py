import maya.cmds as cmds

def main(log=None):

    if not log:
        import logging
        log = logging.getLogger()
    
    isEmptyGroup = True
    allTran = cmds.ls(type = 'transform')
    for x in allTran:
        child = cmds.listRelatives(x, c = True)
        if(child == None):
            isEmptyGroup = False
            try:
                cmds.delete(x)
            except:
                log.error('delete empty group error: %s' % x)
                import traceback
                log.error(traceback.format_exc())
            else:
                log.warning("delete empty group success: %s" %x)
    if isEmptyGroup:
        log.debug("There is no empty group in the scene")