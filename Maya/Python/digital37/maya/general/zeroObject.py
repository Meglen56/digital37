import maya.cmds as cmds
import logging

def main():

    loger = logging.getLogger()
    #loger.debug('{0:-<40}'.format('zeroObject'))
    
    allObj = ls(type = ['mesh', 'nurbsSurface', 'subdiv'])
    for all in allObj:
        trans = listRelatives(all, p = True, f = True)
        try:
            makeIdentity(trans, a = True, t = True, r = True, s = True, n = 0)
            loger.debug("%s zeroObject successful!" %trans)
        except:
            loger.debug("%s zeroObject error" %trans)
                
main()