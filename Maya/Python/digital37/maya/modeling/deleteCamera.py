import maya.cmds as cmds
import logging

def main():

    loger = logging.getLogger()
    
    allCam = listCameras()
    for all in allCam:
        if all != 'front' and all != 'persp' and all != 'side' and all != 'top':
            camera(all, e = True, sc = False)
            delete(all)
            loger.debug("%s delete successful" %all)

main()