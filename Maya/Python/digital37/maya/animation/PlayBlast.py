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

class General():
    def __init__(self):
        self.Scene_Name = None
        self.PB_Name = None
        self.Scene_Full_Name = None
        self.Min = 1
        self.Max = 1

class PlayBlast(General,scene.Scene,quicktime.Quicktime):
    '''
    playblast
    '''
    def __init__(self):
        General.__init__(self)
        
    def set_pb_name(self,pb_name):
        self.PB_Name = pb_name
        
    def playBlast(self,width=1280,height=720):
        self.get_scene_name()
        # self.Scene_Name_Full_Path defined in scene.Scene
        if self.Scene_Name_Full_Path:
            self.set_pb_name( self.Scene_Name_Full_Path_With_Ext.replace('/anim/','/playblast/') )
            
            #set temp dir for xp
            #tempfile.tempdir = 'c:/Windows/Temp'
            self.Images = tempfile.mkstemp(prefix='PlayBlast')[1]
            
            #playblast  -format avi -sequenceTime 0 -clearCache 0 -viewer 1 -showOrnaments 1 -fp 4 -percent 50 -compression "none" -quality 70;
            #playblast  -format iff -filename "D:/mhxy/scenes/shot/seq001/shot053a/simPlayblast/mhxy_seq001_shot053a_anim_fin" -sequenceTime 0 -clearCache 1 -viewer 1 -showOrnaments 1 -fp 4 -percent 50 -compression "jpg" -quality 100;
            pm.playblast(format='iff',sequenceTime=0,clearCache=1,viewer=0,\
                         showOrnaments=1,fp=1,percent=100,compression="jpg",\
                         widthHeight=(width,height),\
                         forceOverwrite=1,quality=100,filename=self.Images)
            
            # convert sequence info for start and end
            minTime, maxTime = self.get_playback_info()
            # make movie
            self.make_mov(self.Images,minTime,maxTime)

        
#    def make_mov(self):
#        ## deadlinequicktimegenerator.exe -CreateMovie d:/temp/test.0001.jpg d:/temp/quicktime_export_settings.xml "QuickTime Movie" 1 25 25 d:/temp/test3.mov
#        #cmd = 'ffmpeg -i '
#        cmd = 'deadlinequicktimegenerator -CreateMovie '
#        cmd += self.Images + '.' + self.Min + '.jpeg '
#        cmd += 'q:/mhxy/quicktime_export_settings.xml '
#        cmd += '"QuickTime Movie" ' + self.Min + ' ' + self.Max + ' 25 '
#        cmd += self.Images + '.mov'
#        
#        logging.debug( 'cmd:%s', cmd )
#        #write received cmd to temp file
#        fRender = tempfile.mkstemp(suffix='.bat',prefix='PlayBlast')
#        os.close(fRender[0])
#        fObj = open(fRender[1],'w')
#        fObj.write( cmd )
#        fObj.flush()
#        fObj.close()
#
#        # write cmd output to log file
#        self.Log = 'PlayBlast.' + str(int(time.time())) + '.log'
#        f = None
#        logDir = tempfile.tempdir
#        if not os.path.exists( logDir ):
#            os.mkdir( logDir )
#        try:
#            f = open( ( logDir + '/' + self.Log ),'a' )
#        except:
#            raise('PlayBlast:Can not write logs file.')
#        logging.debug( 'logDir:%s',logDir )
#                
#        # use subprocess to start command
#        p = subprocess.Popen(cmd, shell=True, bufsize=512,
#                             stdin=subprocess.PIPE,
#                             stdout=subprocess.PIPE,
#                             stderr=subprocess.STDOUT)
#        
#        #self.writeMessage(f,p)
#        
#        threadName = threading.Thread( target=self.writeMessage,args=( f,p ) )
#        threadName.setDaemon(1)
#        threadName.start()
                  
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
        
def main():
    a = PlayBlast()
    a.set_quicktime_settings('q:/mhxy/quicktime_export_settings.xml')
    #a.set_deadline_group('none')
    #a.set_deadline_pool('none')
    #TODO 128 will be return in some pc when do playblast
    a.set_subprocess_returnCode([0,128])
    a.playBlast(1280,720)
    
if __name__ == '__main__' :
    pass
    #main()
