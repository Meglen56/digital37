import os
import pymel.core as pm
import traceback
import maya.cmds as cmds

import sys
sys.path.append( 'D:/BatchTool/command/maya/qc' )
import Log
import System

class QC(Log.Log,System.System):
    def __init__(self):
        self.Scene_Name = ''
        self.Settings = dict()
        self.Frame_Info = dict()
        self.Set_Playback = False
        
    def set_log(self,currentDir):
        self.Log = self.get_logger( currentDir, 'Explorer' )
        self.LogFile = currentDir + '/explorer.log'

    def get_scene_name(self):
        #self.Scene_Name = os.path.splitext( os.path.basename( pm.system.sceneName() ) )[0]
        self.Scene_Name = pm.system.sceneName()
        self.Scene_Name_Short = os.path.splitext( os.path.basename( pm.system.sceneName() ) )[0]
        return self.Scene_Name
        
    def getSettings(self,f,frameInfo):
        try:
            f = open( f ,'r' )
        except IOError:
            self.Log.error('Could not open %s' % f)
        else:
            for x in f.readlines():
                k = x.strip().split(':')[0]
                v = x.strip().split(':')[1]
                self.Settings[k] = v
                    
                f.close()
        #self.log_dict(self.Settings)
        
        if frameInfo != None:
            self.Set_Playback = True
            self.get_Playback_info(frameInfo)
        
    def get_Playback_info(self,frameInfo):
        try:
            f = open( frameInfo ,'r' )
        except IOError:
            self.Log.error('Could not open %s' % f)
        else:
            for x in f.readlines():
                k = x.strip().split()[0]
                v0 = x.strip().split()[1]
                v1 = x.strip().split()[2]
                self.Frame_Info[k] = (v0,v1)
                    
                f.close()
        #self.log_dict(self.Frame_Info)
            
    def set_Playback(self):
        if self.Set_Playback :
            if self.Scene_Name_Short in self.Frame_Info.iterkeys() :
                pm.playbackOptions( minTime=self.Frame_Info[self.Scene_Name_Short][0],\
                                    maxTime=self.Frame_Info[self.Scene_Name_Short][1] )
        
    def checkCamera(self):
        # set persp to can not be renderable
        if pm.PyNode('perspShape').renderable.get() == True :
            pm.PyNode('perspShape').renderable.set(False)
            
        cams_default = set(['perspShape','sideShape','topShape','frontShape'])
        cams = set( cmds.ls(type='camera') )
        cam = cams - cams_default
        cams_renderable=set()
        if cam :
            for c in cam:
                if cmds.getAttr( c + '.renderable' ) :
                    cams_renderable.add(c)
                    
                    # get camera transform node
                    c = cmds.listRelatives(c,parent=True)[0]
                    # lock camera
                    for x in set(['tx','ty','tz','rx','ry','rz','sx','sy','sz']):
                        try:
                            cmds.setAttr((c + '.' + x),lock=True)
                        except:
                            traceback.print_exc()
                            self.Log.warning('can not lock camera:%s\r\n' % c)
                        else:
                            self.Log.debug('lock camera success:%s\r\n'% c)
        
        # no camera can be renderable
        if not cams_renderable :
            for c in cam:
                cmds.setAttr((c+'.renderable'),True)
            return False
        # more than one cameras can be renderable
        elif len(cams_renderable) > 1 :
            return False
        else :
            return True
    
    def checkPlayback(self):
        returnVar = True
        # What is the current linear unit?
        if pm.playbackOptions( query=True, min=True ) != 1.0 :
            pm.currentUnit(linear='cm')
            returnVar = False
        if pm.playbackOptions( query=True, min=True ) != 1.0 :
            pm.currentUnit(linear='film')
            returnVar = False
        return returnVar
        
    def checkUnit(self):
        returnVar = True
        # What is the current linear unit?
        if pm.currentUnit( query=True, linear=True ) != u'cm' :
            pm.currentUnit(linear='cm')
            returnVar = False
        if pm.currentUnit( query=True, time=True ) != u'film' :
            pm.currentUnit(linear='film')
            returnVar = False
        return returnVar
                    
    def remove_unknow_node(self):
        returnVar = True
        allUnknow = cmds.ls(dep = True)
        if allUnknow:
            for n in allUnknow:
                if(cmds.nodeType(n) == 'unknown'):
                    returnVar = False
                    try:
                        cmds.lockNode(n, l = False)
                        cmds.delete(n)
                    except:
                        self.Log.warning('can not delete%s' % n)
                    else:
                        self.Log.warning('success deleted %s' % n)
        return returnVar
                        
    def setResolution(self):
        defaultResolution = pm.PyNode('defaultResolution')
        if defaultResolution.w.get() != self.Settings['defaultResolution.w'] :
            try:
                defaultResolution.w.set( int(self.Settings['defaultResolution.w']) )
            except:
                traceback.print_exc()
                return False
        if defaultResolution.h.get() != self.Settings['defaultResolution.h'] :
            try:
                defaultResolution.h.set( int(self.Settings['defaultResolution.h']) )
            except:
                traceback.print_exc()
                return False
        return True

def main(frameInfo=None):
    
    currentDir = 'D:/BatchTool/command/maya/qc'
    generalSettings = 'Z:/d031seer/QC/techical/anim/qc.txt'
    if not frameInfo:
        frameInfo = 'Z:/d031seer/QC/techical/anim/Frames_All.txt'
    
    a = QC()
    
    # set logger
    a.set_log(currentDir)
    a.get_scene_name()
    a.getSettings(generalSettings,frameInfo)
    
    info = list()
    info.append( 'scenes:\t%s' % a.get_scene_name() )
    info.append( 'camera check:\t%s' % a.checkCamera() )
    info.append( 'set resolution:\t%s' % a.setResolution() )
    info.append( 'check unit:\t%s' % a.checkUnit() )
    info.append( 'remove unknow node:\t%s' % a.remove_unknow_node() )
    
    info = '\r\n'.join(info)
    a.Log.debug( info+'\r\n\r\n' )
    
    a.set_Playback()
#    import RelativePath
#    # check relative path
#    RelativePath.RelativePath().convert_reference_to_relative()
    
if __name__ == '__main__' :
    main()
    