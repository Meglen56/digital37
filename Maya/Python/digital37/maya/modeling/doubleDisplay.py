import maya.cmds as cmds
import logging

def main():

    loger = logging.getLogger()
    
    allObj = ls(type = ['mesh', 'nurbsSurface'])
    for all in allObj:
        try:
            select(all, r = True)
            displaySurface(two = True)
            loger.debug("doubleDisplay is successful")
        except:
            if self.boolUI:
                loger.debug("no object are selected in doubleDisplay, maybe cause by reference")
        select(cl = True)

main()