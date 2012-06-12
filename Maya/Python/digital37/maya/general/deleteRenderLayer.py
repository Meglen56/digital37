import maya.cmds as cmds
import logging

def main():

    loger = logging.getLogger()
    
    allRenderLayer = ls(type = 'renderLayer')
    for all in allRenderLayer:
        if(all != 'defaultRenderLayer'):
            try:
                editRenderLayerGlobals( currentRenderLayer='defaultRenderLayer' )
                delete(all)
                loger.debug("renderLayer: %s delete successful" %all)
            except:
                loger.error("renderLayer: cant delete %s" %all)

main()