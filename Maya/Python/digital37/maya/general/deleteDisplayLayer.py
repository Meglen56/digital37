import maya.cmds as cmds
import logging

def main():

    loger = logging.getLogger()
    
    allDisLayer = ls(type = 'displayLayer')
    for all in allDisLayer:
        if(all != 'defaultLayer'):
            try:
                delete(all)
                loger.debug("%s delete successful" %all)

            except:
                loger.error("cant delete %s" %all)

main()