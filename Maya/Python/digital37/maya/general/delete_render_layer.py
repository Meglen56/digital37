import maya.cmds as cmds

def main(log=None):

    if not log:
        import logging
        log = logging.getLogger()
    
    allRenderLayer = cmds.ls(type = 'renderLayer')
    allRenderLayer.remove('defaultRenderLayer')
    if allRenderLayer:
        for x in allRenderLayer:
            try:
                cmds.editRenderLayerGlobals( currentRenderLayer='defaultRenderLayer' )
                cmds.delete(x)
            except:
                log.error("delete render layer error:%s" %x)
                import traceback
                log.error(traceback.format_exc())
            else:
                log.warning("render layer delete successful:%s" %x)
    else:
        log.debug('There is no render layer in the scene')        