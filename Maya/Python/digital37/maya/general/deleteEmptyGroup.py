import maya.cmds as cmds
import logging

def main():

    loger = logging.getLogger()
    
    allTran = ls(type = 'transform')
    for all in allTran:
        try:
            child = listRelatives(all, c = True)
            if(child == None):
                delete(all)
                loger.debug("%s delete successful" %all)
        except:
            loger.error("cant delete %s" %all)

main()