import traceback
import os
import tempfile

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
        
    def set_pb_name_by_folder(self,outputDir):
        '''override get_pb_name in PlayBlast
        '''
        try:
            #self.PB_Name example: outputdir/ep01/ep01_sc0010/ep01_sc0010
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
        
    def before_playblast(self,outputDir=None,width=None,height=None):
        '''
        do before playBlast
        '''
        # get playBlast image's name
        self.get_scene_name()
        if self.Name_By_Folder:
            self.set_pb_name_by_folder(outputDir)
        else:
            if not outputDir:
                outputDir = tempfile.mkdtemp()
            #print outputDir
            # set image's name to output folder
            self.set_pb_name( os.path.abspath(os.path.join(outputDir,self.Scene_Name_Short_Without_Ext)))
        
        # get playBack range
        self.MinTime, self.MaxTime = self.get_playback_info()
        
        # get image's width and height
        # if not set width and height, then use rendering settings
        # get render settings's width and height
        if not width:
            import digital37.maya.lighting.get_render_resolution as get_render_resolution
            width,height = get_render_resolution.main()
        self.Width = width
        self.Height = height
        
        self.Images = self.PB_Name

        # ____create model panel view to playblast____
        # get renderable camera
        if self.get_cam():
            self.create_model_panel(self.Width,self.Height)
            #self.set_hardwareRenderingGlobals()
            #cmd = 'DisplayShadedAndTextured;'
            pm.mel.eval('DisplayShaded;')
        # ____create model panel view to playblast____
    
    def do_playblast(self,imageName=None):
        '''
        do plabyBlast 
        '''
        if not imageName:
            #set temp images name
            fd,imageName = tempfile.mkstemp(prefix='PlayBlast')
            fObj = os.fdopen(fd,'w')
            fObj.write( '' )
            fObj.close()
        self.Images = imageName
        
        print 'self.Images:%s' % self.Images
        cmds.setFocus(self.Panel_Current)
        self.evalDeferred_playblast(self.Images, self.Width, self.Height, 4)
        #self.eval_playblast(self.Images, self.Width, self.Height, 4)
    
    def after_playblast(self):
        '''
        do after playBlast
        '''
        # make movie from image sequence
        # add frame number and extension to make movie
        if self.Make_Movie: 
            self.make_mov( (self.Images + ('.%s.jpeg' % self.MinTime)), self.MinTime, self.MaxTime )
        
        # quit maya force
        #pm.evalDeferred('import maya.cmds as cmds\ncmds.quit(f=1)')
        
#    def playBlast(self,outputDir,width,height):
#        self.get_scene_name()
#        # self.Scene_Name_Full_Path defined in scene.Scene
#        if self.Scene_Name_Full_Path:
#            self.get_pb_name(outputDir)
#            
#            self.Images = self.PB_Name
#            
#            # get renderable camera
#            if self.get_cam():
#                self.create_model_panel(width,height)
#                #self.set_hardwareRenderingGlobals()
#                # 6
#                #cmd = 'DisplayShadedAndTextured;'
#                pm.mel.eval('DisplayShaded;')
#                #cmds.quit(force=True)
#                self.evalDeferred_playblast(self.Images, width, height, 4)
#                
#                # quit maya force
#                #pm.evalDeferred('import maya.cmds as cmds\ncmds.quit(f=1)')
                    
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
        self.Panel_Current = cmds.modelPanel(tearOff=True)
        
        # max model panel
        windows = set( cmds.lsUI( windows=True ) ) - set(u'MayaWindow')
        for win in windows:
            cmds.window( win, edit=True, widthHeight=(width+100, height+100) )

        cmds.modelEditor(self.Panel_Current,e=1,udm=0)
        cmds.modelEditor(self.Panel_Current,e=1,allObjects=0)
        cmds.modelEditor(self.Panel_Current,e=1,polymeshes=1,nurbsSurfaces=1)
        cmds.modelEditor(self.Panel_Current,e=1,cameraName=self.Camera)
        #
        #cmds.setFocus(self.Panel_Current)
        cmds.setFocus(self.Panel_Current)

def main(log=None,nameByFolder=False,outputDir='playblast',imageName=None,
         width=None,height=None,makeMovie=False,quicktime_settings_file=None,quicktime_time=None):
    a = PlayBlast_Batch()
    if not log:
        a.get_stream_logger()
    if makeMovie:
        a.playBlast_with_mov(nameByFolder, outputDir, imageName, width, height, quicktime_settings_file,quicktime_time)
    else:
        a.playBlast(nameByFolder, outputDir, imageName, width, height)
    
if __name__ == '__main__' :
    #pass
    main(None,True,'d:/temp2')
    #main(None,None,None,None,None,None,True,'D:/RND/project/pipelineProject/quicktime/quicktime_export_settings.xml')
