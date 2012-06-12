import maya.cmds as cmds
import logging

def main():

    loger = logging.getLogger()
    
    allObj = ls(type = ['mesh', 'nurbsSurface'])
    for all in allObj:
        try:
            delete(all, ch = True)
            loger.debug("delete %s history successful" %all)
        except:
            loger.warning("cant delete %s history" %all)

main()