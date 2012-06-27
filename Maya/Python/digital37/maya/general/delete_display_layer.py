import maya.cmds as cmds

def main(log=None):
    if not log:
        import logging
        log = logging.getLogger()
    
    disLayers = cmds.ls(type = 'displayLayer')
    disLayers.remove('defaultLayer')
    
    if disLayers :
        for x in disLayers:
            try:
                cmds.delete(x)
                log.warning("delete display layer successful: %s" %x)
            except:
                log.error("delete display layer error: %s" %x)
                import traceback
                log.error(traceback.format_exc())
    else:
        log.debug('There is no display layer in the scene')