#!/usr/bin/env python
#Description:Convert mb to ma 
#Author:honglou(hongloull@hotmail.com)
#Create:2008.04.18
#Update:2008.12.04
#
import re
import maya.cmds as cmds

#func for convert '.mb' files to '.ma'
def mb2ma():
    # del unknow nodes
    del_unknown_nodes()
    #open, rename and save cmd
    mayaFile = cmds.file(q=1,sn=1)
    cmds.file( rename = re.sub(r'(ma|mb)$',r'ma',mayaFile) )
    #-options \\"v=0;p=17\\"
    cmds.file(f=1,save=1,type='mayaAscii')

#func for convert '.ma' files to '.mb'
def ma2mb():
    # del unknow nodes
    del_unknown_nodes()
    #open, rename and save cmd
    mayaFile = cmds.file(q=1,sn=1)
    cmds.file( rename = re.sub(r'(ma|mb)$',r'mb',mayaFile) )
    #-options \\"v=0;p=17\\"
    cmds.file(f=1,save=1,type='mayaBinary')
    
def del_unknown_nodes():
    allUnknow = cmds.ls(dep = True)
    if allUnknow:
        for all in allUnknow:
            if(cmds.nodeType(all) == 'unknown'):
                try:
                    cmds.lockNode(all, l = False)
                    cmds.delete(all)
                except:
                    print 'can not delete'