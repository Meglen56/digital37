import os
import traceback
import shutil
import logging
import re
import pymel.core as pm
import maya.cmds as cmds

class General():
    def __init__(self):
        self.Scene_Name = None
        self.PB_Name = None
        self.Scene_Full_Name = None
        self.Min = 1
        self.Max = 1
    
    def get_scene_name(self):
        self.Scene_Name = os.path.splitext( os.path.basename( pm.system.sceneName() ) )[0]
        self.Scene_Full_Name = os.path.splitext( pm.system.sceneName() )[0]
        self.Scene_Name_Short = os.path.splitext( os.path.basename( pm.system.sceneName() ) )[0]
    
    def get_pb_name(self):
        try:
            #self.PB_Name = self.Scene_Full_Name.replace('/anim/','/playblast/').replace('_an_','_')
            #self.PB_Name = 'Z:/D031SEER/pb/' + self.Scene_Name_Short.split('_')[-2] \
            self.PB_Name = 'd:/seer/pb/' + self.Scene_Name_Short.split('_')[-2] \
            + '/' + self.Scene_Name_Short.split('_')[-2] + '_' + self.Scene_Name_Short.split('_')[-1] \
            + '/' + self.Scene_Name_Short.split('_')[-2] + '_' + self.Scene_Name_Short.split('_')[-1]
            print self.PB_Name
        except :
            traceback.print_exc()
            print 'get pb name error'
            return False
        else:
            return True
        
    def convert_to_relative(self,parten,inputStr):
        '''
        example: convertToRelative('sourceimages','C:/AW/Maya5.0/sourceimages/maya.exe')
        result: 'sourceimages/maya.exe'
        '''
        #p = re.compile('^.*/sourceimages')
        inputStr = str(inputStr).replace('\\','/')
        returnStr = re.sub( ('^.*/(' + parten + ')'), parten, inputStr )
        print inputStr,'\t',returnStr
        return returnStr
    
    def create_dir(self,dirPath):
        if not os.path.exists( dirPath ):
            try:
                os.makedirs( dirPath )
            except:
                traceback.print_exc()
                print 'create dirs error'
                    
    def copy(self,src,dst):
        shutil.copy(src, dst)

class PlayBlast_Batch(General):
    '''
    playblast
    '''
    def __init__(self):
        General.__init__(self)
        self.Cam = None
        self.Frame_Info = dict()
        
    def playBlast(self):
        self.get_scene_name()
        if self.Scene_Name:
            #remove open windows
            pm.mel.eval('removeOpenWindows();')
            
            self.get_pb_name()
            
            self.get_Playback_info()
            self.set_Playback()
            
            #set temp dir for xp
            #tempfile.tempdir = 'c:/Windows/Temp'
            self.Images = self.PB_Name
            
            self.get_cam()
            self.setPanelLayout()
            #self.set_hardwareRenderingGlobals()
            # 6
            #cmd = 'DisplayShadedAndTextured;'
            cmd = 'DisplayShaded;'
            pm.mel.eval(cmd)
            print cmd
#            # set osg render to current model panel
#            cmd = '{  string $currentPanel = `getPanel -withFocus`;'
#            cmd += 'string $panelType = `getPanel -to $currentPanel`;'
#            cmd += 'if ($panelType ==  \"modelPanel\") {'
#            cmd += 'setRendererInModelPanel \"ogsRenderer\" $currentPanel;'
#            cmd += '} else if ($panelType ==  \"scriptedPanel\")'
#            cmd += ' {  string $cmd = \"setRendererInModelPanel \\\"ogsRenderer\\\" \";'
#            cmd += 'scriptedPanelRunTimeCmd( $cmd, $currentPanel );}};'
#            pm.mel.eval(cmd)
        
            #playblast  -format avi -sequenceTime 0 -clearCache 0 -viewer 1 -showOrnaments 1 -fp 4 -percent 50 -compression "none" -quality 70;
            #playblast  -format iff -filename "D:/mhxy/scenes/shot/seq001/shot053a/simPlayblast/mhxy_seq001_shot053a_anim_fin" -sequenceTime 0 -clearCache 1 -viewer 1 -showOrnaments 1 -fp 4 -percent 50 -compression "jpg" -quality 100;
            pm.playblast(format='iff',sequenceTime=0,clearCache=1,viewer=0,\
                         showOrnaments=1,fp=4,percent=100,compression="jpg",\
                         widthHeight=(1024,553),\
                         forceOverwrite=1,quality=100,filename=self.Images)

            print self.PB_Name
            cmds.quit(force=True)
        
    def get_cam(self):
        cams= cmds.ls(cameras=1)
        print cams
        cams_standard = set(["perspShape","frontShape","sideShape","topShape"])
        cam = list( set(cams) - cams_standard )
        if not cam:
            cam = ["perspShape"]
            
        if len(cam)>1 :
            for c in cam:
                if c.startswith('cam_'):
                    cam = [c]
        self.Cam = cam[0]
        print 'self.Cam:%s' % self.Cam
        # set camera attr
        #camera -e -displayFilmGate off -displayResolution off -overscan 1.0 $cams[0];
        pm.camera(self.Cam,e=1,displayFilmGate=0,displayResolution=0,overscan=1.0)
        
    #setNamedPanelLayout "Single Perspective View";
    def setPanelLayout(self):
        cmd = 'setNamedPanelLayout "Single Perspective View";'
        #cmd += 'lookThroughModelPanel persp modelPanel4;'
        #panel_current = cmds.getPanel(withFocus=1)
        

        
        panel_current = 'modelPanel4'
        #panel_current = ps[0]
        
        if cmds.modelPanel(panel_current,q=1,tearOff=1) :
            panel_v = set( cmds.getPanel(vis=1) )
            panel_m = set( cmds.getPanel(type='modelPanel') )
            ps = list( panel_v & panel_m )
            panel_current = ps[0]
                    
        print 'panel_current',panel_current
        #lookThroughModelPanel $cams[0] $currentPanel;
        cmd += 'lookThroughModelPanel ' + self.Cam + ' ' + panel_current + ';'
        print cmd
        pm.mel.eval(cmd)
        #modelEditor -e -udm false $currentPanel;
        #modelEditor -e -allObjects 0 $currentPanel;
        #modelEditor -e -polymeshes true $currentPanel;
        cmds.modelEditor(panel_current,e=1,udm=0)
        cmds.modelEditor(panel_current,e=1,allObjects=0)
        cmds.modelEditor(panel_current,e=1,polymeshes=1,nurbsSurfaces=1)
        cmds.modelEditor(panel_current,e=1,cameraName=self.Cam)
            
    def set_Playback(self):
        if self.Scene_Name_Short in self.Frame_Info.iterkeys() :
            pm.playbackOptions( minTime=self.Frame_Info[self.Scene_Name_Short][0],\
                                maxTime=self.Frame_Info[self.Scene_Name_Short][1] )
                        
    def get_Playback_info(self,frameInfo='Z:/D031SEER/QC/techical/anim/Frames_All.txt'):
        try:
            f = open( frameInfo ,'r' )
        except IOError:
            logging.error('Could not open %s' % f)
        else:
            for x in f.readlines():
                try:
                    k = x.strip().split()[0]
                    v0 = x.strip().split()[1]
                    v1 = x.strip().split()[2]
                    self.Frame_Info[k] = (v0,v1)
                    #print self.Frame_Info
                except:
                    traceback.print_exc()
                f.close()
                
    def get_frames_info(self):
        # rename sequence from 1
        # get sequence
        self.Min = str(int(pm.playbackOptions(q=1,min=1)))
        self.Max = str(int(pm.playbackOptions(q=1,max=1)))

#    def scriptJob(self):
#        cmds.scriptJob(event=['SceneOpened','PlayBlast_Batch().playBlast()'])

        
def main():
    PlayBlast_Batch().playBlast()
    
if __name__ == '__main__' :
    pass
    #main()
