import os
import traceback
import logging 
import tempfile
import shutil

import pymel.core as pm

import system.quicktime as quicktime
reload(quicktime)
import digital37.maya.general.scene as scene
reload(scene)

class PlayBlast(scene.Scene,quicktime.Quicktime):
    '''
    playblast
    '''
    def __init__(self):
        pass
        
    def set_pb_name(self,pb_name):
        self.PB_Name = pb_name
        
    # use folderName to replace maya scene's full path name's 'anim'
    # example: scenes/shot/ep01/ep01_sc0010/anim/project_an_ep01_sc0010.mb
    #          scenes/shot/ep01/ep01_sc0010/folderName/project_an_ep01_sc0010.mov
    def set_pb_name_by_folder(self,folderName='playblast'):
        self.get_scene_name()
        # self.Scene_Name_Full_Path defined in scene.Scene
        if self.Scene_Name_Full_Path:
            self.set_pb_name( self.Scene_Name_Full_Path_Without_Ext.replace( '/anim/', ('/%s/' % folderName) ) )
        else:
            return False
        
    def playBlast(self,width,height):
        # get info for playback start and end
        minTime, maxTime = self.get_playback_info()
        
        #set temp dir for xp
        #tempfile.tempdir = 'c:/Windows/Temp'
        self.Images = tempfile.mkstemp(prefix='PlayBlast')[1]
        
        #playblast  -format avi -sequenceTime 0 -clearCache 0 -viewer 1 -showOrnaments 1 -fp 4 -percent 50 -compression "none" -quality 70;
        #playblast  -format iff -filename "D:/mhxy/scenes/shot/seq001/shot053a/simPlayblast/mhxy_seq001_shot053a_anim_fin" -sequenceTime 0 -clearCache 1 -viewer 1 -showOrnaments 1 -fp 4 -percent 50 -compression "jpg" -quality 100;
        # if not set width and height, then use rendering settings
        pm.playblast(format='iff',sequenceTime=0,clearCache=1,viewer=0,\
                     showOrnaments=1,fp=1,percent=100,compression="jpg",\
                     widthHeight=(width,height),\
                     forceOverwrite=1,quality=100,filename=self.Images)
        
        # add frame number and extension to make movie 
        self.make_mov( (self.Images + ('.%s.jpeg' % minTime)), minTime, maxTime )

    # override do_after_execute_cmd in system module
    def do_after_execute_cmd(self):
        logging.debug( 'PlayBlast:Success\r\n' )
        # copy movie
        # check folder exists or not
        self.create_dir( os.path.dirname(self.PB_Name + '.mov') )
        shutil.copy( (self.Images + '.mov'), (self.PB_Name + '.mov') )
        cmd = 'start '
        cmd += self.PB_Name + '.mov'
        try:
            os.system(cmd)
        except:
            traceback.print_exc()
        logging.debug("PlayBlast: %s",(self.PB_Name + '.mov') )
        
def main(width=1280,height=720,quicktime_settings_file=None):
    a = PlayBlast()
    a.get_file_logger()
    a.set_quicktime_settings(quicktime_settings_file)
    a.set_pb_name_by_folder('playblast')
    #TODO 128 will be return in some pc when do playblast
    a.set_subprocess_returnCode([0,128])
    a.playBlast(width,height)
    
if __name__ == '__main__' :
    pass
    #main()
