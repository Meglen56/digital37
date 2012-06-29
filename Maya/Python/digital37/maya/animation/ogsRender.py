import os
import traceback
import subprocess
import logging 
import tempfile
import threading
import time
import shutil
import pymel.core as pm
import maya.cmds as cmds
    
class OgsRender(General):
    '''
    ogsRender playBlast
    '''
    def __init__(self):
        General.__init__(self)
        self.Cam = None
        
    #setNamedPanelLayout "Single Perspective View";
    def setPanelLayout(self):
        cmd = 'setNamedPanelLayout "Single Perspective View";'
        panel_current = cmds.getPanel(withFocus=1)
        print 'panel_current',panel_current
        #lookThroughModelPanel $cams[0] $currentPanel;
        
        cmd += 'lookThroughModelPanel ' + self.Cam + ' ' + panel_current + ';'
        pm.mel.eval(cmd)
        #modelEditor -e -udm false $currentPanel;
        #modelEditor -e -allObjects 0 $currentPanel;
        #modelEditor -e -polymeshes true $currentPanel;
        cmds.modelEditor(panel_current,e=1,udm=0)
        cmds.modelEditor(panel_current,e=1,allObjects=0)
        cmds.modelEditor(panel_current,e=1,polymeshes=1)
        cmds.modelEditor(panel_current,e=1,cameraName=self.Cam)

        #select -r `ls -dag -lf -type softModHandle -type clusterHandle` ;
        #string $layer = `createDisplayLayer -name "softHandle_layer" -number 1 -nr`;
        #layerEditorLayerButtonVisibilityChange $layer;
        #remove cluster and softModHandle
        pm.ls(dag=1,lf=1,type=('softModHandle','clusterHandle'))
        layer = pm.createDisplayLayer(name='softHandle_layer',number=1,mc=1)
        pm.mel.eval('layerEditorLayerButtonVisibilityChange ' + layer)

        
    def set_hardwareRenderingGlobals(self):
        pm.PyNode('hardwareRenderingGlobals').gammaCorrectionEnable.set(1)
        pm.PyNode('hardwareRenderingGlobals').multiSampleEnable.set(1)
        
    def get_cam(self):
        cams= cmds.ls(cameras=1)
        print cams
        cams_standard = set(["perspShape","frontShape","sideShape","topShape"])
        cam = list( set(cams) - cams_standard )
        if not cam:
            cam = ["perspShape"]
        self.Cam = cam[0]
        print self.Cam
        # set camera attr
        #camera -e -displayFilmGate off -displayResolution off -overscan 1.0 $cams[0];
        pm.camera(self.Cam,e=1,displayFilmGate=0,displayResolution=0,overscan=1.0)
    
    def ogsRender(self):
        self.get_cam()
        self.setPanelLayout()
        self.set_hardwareRenderingGlobals()
        # 6
        cmd = 'DisplayShadedAndTextured;'
        pm.mel.eval(cmd)
        # set osg render to current model panel
        cmd = '{  string $currentPanel = `getPanel -withFocus`;'
        cmd += 'string $panelType = `getPanel -to $currentPanel`;'
        cmd += 'if ($panelType ==  \"modelPanel\") {'
        cmd += 'setRendererInModelPanel \"ogsRenderer\" $currentPanel;'
        cmd += '} else if ($panelType ==  \"scriptedPanel\")'
        cmd += ' {  string $cmd = \"setRendererInModelPanel \\\"ogsRenderer\\\" \";'
        cmd += 'scriptedPanelRunTimeCmd( $cmd, $currentPanel );}};'
        pm.mel.eval(cmd)
        # playblast
        self.playBlast()
             
    def playBlast(self):
        self.get_scene_name()
        if self.Scene_Name:
            self.get_pb_name()
            
            #set temp dir for xp
            #tempfile.tempdir = 'c:/Windows/Temp'
            self.Images = tempfile.mkstemp(prefix='PlayBlast')[1]
            
            #playblast  -format avi -sequenceTime 0 -clearCache 0 -viewer 1 -showOrnaments 1 -fp 4 -percent 50 -compression "none" -quality 70;
            #playblast  -format iff -filename "D:/mhxy/scenes/shot/seq001/shot053a/simPlayblast/mhxy_seq001_shot053a_anim_fin" -sequenceTime 0 -clearCache 1 -viewer 1 -showOrnaments 1 -fp 4 -percent 50 -compression "jpg" -quality 100;
            pm.playblast(format='iff',sequenceTime=0,clearCache=1,viewer=0,\
                         showOrnaments=1,fp=1,percent=100,compression="jpg",\
                         widthHeight=(1280,720),\
                         forceOverwrite=1,quality=100,filename=self.Images)
            print self.PB_Name
            
            # convert sequence info for start and end
            self.get_frames_info()
            # make movie
            self.make_mov()
            
    def get_frames_info(self):
        # rename sequence from 1
        # get sequence
        self.Min = str(int(pm.playbackOptions(q=1,min=1)))
        self.Max = str(int(pm.playbackOptions(q=1,max=1)))
        
    def make_mov(self):
        ## deadlinequicktimegenerator.exe -CreateMovie d:/temp/test.0001.jpg d:/temp/quicktime_export_settings.xml "QuickTime Movie" 1 25 25 d:/temp/test3.mov
        #cmd = 'ffmpeg -i '
        cmd = 'deadlinequicktimegenerator -CreateMovie '
        cmd += self.Images + '.' + self.Min + '.jpeg '
        cmd += 'q:/mhxy/quicktime_export_settings.xml '
        cmd += '"QuickTime Movie" ' + self.Min + ' ' + self.Max + ' 25 '
        cmd += self.Images + '.mov'
        
        logging.debug( 'cmd:%s', cmd )
        #write received cmd to temp file
        fRender = tempfile.mkstemp(suffix='.bat',prefix='OgsRender')
        os.close(fRender[0])
        fObj = open(fRender[1],'w')
        fObj.write( cmd )
        fObj.flush()
        fObj.close()

        # write cmd output to log file
        self.Log = 'OgsRender.' + str(int(time.time())) + '.log'
        f = None
        logDir = tempfile.tempdir
        if not os.path.exists( logDir ):
            os.mkdir( logDir )
        try:
            f = open( ( logDir + '/' + self.Log ),'a' )
        except:
            raise('OgsRender:Can not write logs file.')
        logging.debug( 'logDir:%s',logDir )
                
        # use subprocess to start command
        p = subprocess.Popen(cmd, shell=True, bufsize=512,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        
        #self.writeMessage(f,p)
        
        threadName = threading.Thread( target=self.writeMessage,args=( f,p ) )
        threadName.setDaemon(1)
        threadName.start()
                                        
    def writeMessage(self,f,p):
        start_time = time.time()
        while True :
            #subprocess is not complete
            if p.poll() == None :
                if p.stdout and (time.time()-start_time<120):
                    try:
                        output = p.stdout.readline()
                    except:
                        traceback.print_exc()
                        break
                    else:
                        if output :
                            logging.debug(output)
                            f.write( output )
                            f.flush()
                else:
                    break
            #subprocess is complete
            else :
                #TODO 128 will be return in some pc
                if(p.returncode==0 or p.returncode==128):
                #if(p.returncode==0):
                    logging.debug( 'OgsRender:Success\r\n' )
                    # copy movie
                    # check folder exists or not
                    self.create_dir( os.path.dirname(self.PB_Name + '.mov') )
                    self.copy( (self.Images + '.mov'), (self.PB_Name + '.mov') )
                    cmd = 'start '
                    cmd += self.PB_Name + '.mov'
                    try:
                        os.system(cmd)
                    except:
                        traceback.print_exc()
                    logging.debug("OgsRender: %s",(self.PB_Name + '.mov') )
                else:
                    logging.debug("ReturnCode: %s",str(p.returncode) )
                break                    
        
        
def main():
    OgsRender().ogsRender()
    
if __name__ == '__main__' :
    #pass
    main()
