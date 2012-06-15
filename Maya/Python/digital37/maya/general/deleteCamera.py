import maya.cmds as cmds
import logging

def main():

    loger = logging.getLogger()
    
    allCam = cmds.listCameras()
    for all in allCam:
        if all != 'front' and all != 'persp' and all != 'side' and all != 'top':
            cmds.camera(all, e = True, sc = False)
            cmds.delete(all)
            loger.debug("%s delete successful" %all)