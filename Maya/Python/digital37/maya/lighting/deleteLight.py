import maya.cmds as cmds
import logging

def main():

    loger = logging.getLogger()
    
    allLight = cmds.ls(lights = True)
    for all in allLight:
        try:
            cmds.delete(all)
            loger.debug("%s delete successful" %all)
        except:
            if self.boolUI:
                loger.error("cant delete %s" %all)