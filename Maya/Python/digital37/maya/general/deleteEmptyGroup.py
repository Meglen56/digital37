import maya.cmds as cmds
import logging

def main():

    loger = logging.getLogger()
    
    allTran = cmds.ls(type = 'transform')
    for all in allTran:
        try:
            child = cmds.listRelatives(all, c = True)
            if(child == None):
                cmds.delete(all)
                loger.debug("%s delete successful" %all)
        except:
            loger.error("cant delete %s" %all)