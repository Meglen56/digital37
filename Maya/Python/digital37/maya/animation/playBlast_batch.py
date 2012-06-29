import traceback
import os.path
import pymel.core as pm
import maya.cmds as cmds

import digital37.maya.animation.playBlast as playBlast
reload(playBlast)

class PlayBlast_Batch(playBlast.PlayBlast):
    '''
    playblast
    '''
    def __init__(self):
        pass
        
    def get_pb_name(self,outputDir):
        '''override get_pb_name in PlayBlast
        '''
        try:
            #self.PB_Name example: outputdir/ep01/ep01_sc0010/ep01_sc0010.####.jpeg
            self.PB_Name = os.path.join(outputDir,self.Scene_Name_Short_Without_Ext.split('_')[-2],
                                        self.Scene_Name_Short_Without_Ext.split('_')[-2] + '_' + self.Scene_Name_Short_Without_Ext.split('_')[-1],
                                        self.Scene_Name_Short_Without_Ext.split('_')[-2] + '_' + self.Scene_Name_Short_Without_Ext.split('_')[-1])
            print self.PB_Name
        except :
            traceback.print_exc()
            print 'get pb name error'
            return False
        else:
            return True

    def playBlast(self,outputDir,width,height):
        self.get_scene_name()
        # self.Scene_Name_Full_Path defined in scene.Scene
        if self.Scene_Name_Full_Path:
            self.get_pb_name(outputDir)
            
            self.Images = self.PB_Name
            
            # get renderable camera
            if self.get_cam():
                self.create_model_panel(width,height)
                #self.set_hardwareRenderingGlobals()
                # 6
                #cmd = 'DisplayShadedAndTextured;'
                pm.mel.eval('DisplayShaded;')
                #cmds.quit(force=True)
                self.evalDeferred_playblast(self.Images, width, height, 4)
                
                # quit maya force
                #pm.evalDeferred('import maya.cmds as cmds\ncmds.quit(f=1)')
                    
    def get_cam(self):
        import digital37.maya.general.camera as camera
        reload(camera)
        # get renderable camera
        a = camera.Camera()
        a.get_renderable_camera()
        if a.Cam_Renderable:
            self.Camera = list(a.Cam_Renderable)[0]
            # set camera attr
            #pm.camera(self.Cam,e=1,displayFilmGate=0,displayResolution=0,overscan=1.0)
            camera.set_attr_for_pb(self.Camera)
            return True
        else:
            print 'there is no renderable camera'
            return False
        
    def create_model_panel(self,width,height):
        '''create one tear off model panel for playblast
        '''
        # create tear off model panel
        panel_current = cmds.modelPanel(tearOff=True)
        
        # max model panel
        windows = set( cmds.lsUI( windows=True ) ) - set(u'MayaWindow')
        for win in windows:
            cmds.window( win, edit=True, widthHeight=(width+100, height+100) )

        cmds.modelEditor(panel_current,e=1,udm=0)
        cmds.modelEditor(panel_current,e=1,allObjects=0)
        cmds.modelEditor(panel_current,e=1,polymeshes=1,nurbsSurfaces=1)
        cmds.modelEditor(panel_current,e=1,cameraName=self.Camera)
        #
        #cmds.setFocus(panel_current)
        cmds.setFocus(panel_current)

def main(outputDir=None,width=1024,height=553):
    PlayBlast_Batch().playBlast(outputDir,width,height)
    
if __name__ == '__main__' :
    pass
    #main()
