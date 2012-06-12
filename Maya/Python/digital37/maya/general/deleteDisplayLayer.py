import maya.cmds as cmds
import logging

def main():

    loger = logging.getLogger()
    
    allDisLayer = cmds.ls(type = 'displayLayer')
    for all in allDisLayer:
        if(all != 'defaultLayer'):
            try:
                cmds.delete(all)
                loger.debug("%s delete successful" %all)

            except:
                loger.error("cant delete %s" %all)