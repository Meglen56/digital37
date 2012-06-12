import maya.cmds as cmds
import logging

def main():

    loger = logging.getLogger()
    
    allObj = cmds.ls(type = ['mesh', 'nurbsSurface'])
    for all in allObj:
        try:
            cmds.select(all, r = True)
            displaySurface(two = True)
            loger.debug("doubleDisplay is successful")
        except:
                loger.debug("no object are selected in doubleDisplay, maybe cause by reference")
        cmds.select(cl = True)