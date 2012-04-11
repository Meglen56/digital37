import re
import os
import pymel.core as pm
import tempfile, subprocess, traceback
import logging
import threading
import sys
import maya.utils
import maya.cmds as cmds

sys.path.append( 'D:/workspace/tools/DIGITAL37/Maya/Python/digital37/maya/general' )
import RelativePath

class General():
    def __init__(self):
        self.Scene_Name = ''
            
    def setLog(self,logLevel):
        LOG_LEVELS = {'debug': logging.DEBUG, 'info':logging.INFO, \
                  'warning': logging.WARNING, 'error': logging.ERROR,\
                  'critical': logging.CRITICAL}
        LOG_LEVEL = LOG_LEVELS.get(logLevel)
        logging.basicConfig(level=LOG_LEVEL)
        
    def setLog_maya(self):
        self.Log = logging.getLogger("MyLogger")
        self.Log.propagate = False
        handler = maya.utils.MayaGuiLogHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s %(message)s")
        handler.setFormatter(formatter)
        self.Log.addHandler(handler)
        
    def log_dict(self,inputDict):
        if inputDict :
            s = ''
            try :
                s += str(inputDict)
            except :
                self.Log.warning('can not convert inputDict to string')        
            for k,v in inputDict.items() :
                s += '\t\t'
                s += 'key:'+str(k) + '\t'
                s += 'value:'+str(v)
            self.Log.debug(s)
    
    def log_list(self,inputList):
        if inputList :
            s = ''
            if inputList :
                try :
                    s += str(inputList)
                except :
                    self.Log.warning('can not convert inputList to string')
                for i in inputList :
                    s += '\t' + str(i)
            self.Log.debug(s)
        else:
            self.Log.debug('log_list:input is None')
            
    def get_scene_name(self):
        #self.Scene_Name = os.path.splitext( os.path.basename( pm.system.sceneName() ) )[0]
        self.Scene_Name = pm.system.sceneName()
        self.Scene_Name_Short = os.path.splitext( os.path.basename( pm.system.sceneName() ) )[0]

    def writeMessage(self,f,p):
        while True :
            #subprocess is not complete
            if p.poll() == None :
                if p.stdout :
                    try:
                        output = p.stdout.readline()
                    except KeyboardInterrupt:
                        self.Log.debug( 'user canceled.\r\n' )
                        break
                    except:
                        traceback.print_exc()
                        break
                    else:
                        if output :
                            f.write( output )
                            f.flush()
            #subprocess is complete
            else :
                if(p.returncode==0):
                    self.Log.debug( 'QC:Success\r\n' )
                else:
                    self.Log.debug("ReturnCode: %s",str(p.returncode) )
                break
        
    def write_log(self,content):
        logPrefix = 'QC_'
        fd,self.Log_File = tempfile.mkstemp(suffix='.log',prefix=logPrefix)
        print self.Log_File
        os.close(fd)
        fObj = open(self.Log_File,'a')
        for s in content.split('\n'):
            fObj.write(s + '\n')
        fObj.close()
        
    def execute_cmd(self,cmd,logPrefix):
        # write cmd output to log file
        fd,batch_file = tempfile.mkstemp(suffix='.bat',prefix=('.'+logPrefix))
        os.close(fd)
        fObj = open(batch_file,'w')
        fObj.write( cmd )
        fObj.flush()
        fObj.close()
        self.Log.debug( 'Batch File:\t%s',batch_file )
        
        fd,self.Log = tempfile.mkstemp(suffix='.log',prefix=('.'+logPrefix))
        os.close(fd)
        fObj = open(self.Log,'a')
        
        # For multi-line command use bat file to execute
        p = subprocess.Popen(batch_file, shell=True, bufsize=512,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        
        threadName = threading.Thread( target=self.writeMessage,args=( fObj,p ) )
        threadName.setDaemon(1)
        threadName.start()
        
        
class QC(General):
    def __init__(self,fileName,frameInfo=None):
        self.Settings = dict()
        self.Frame_Info = dict()
        self.Set_Playback = False
        
        self.setLog_maya()
        
        self.get_scene_name()
        self.getSettings(fileName)
        if frameInfo != None:
            self.Set_Playback = True
            self.get_Playback_info(frameInfo)
        
    def getSettings(self,f):
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
        self.log_dict(self.Settings)
        
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
        self.log_dict(self.Frame_Info)
            
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

def main():
    
    generalSettings = 'D:/workspace/tools/DIGITAL37/Maya/Python/digital37/maya/general/qc.txt'
    frameInfo = 'Z:/d031seer/QC/techical/anim/Frames_EP29.txt'
    
    a = QC(generalSettings,frameInfo)
    info = list()
    info.append( 'scenes:\t%s' % a.get_scene_name() )
    info.append( 'camera check:\t%s' % a.checkCamera() )
    info.append( 'set resolution:\t%s' % a.setResolution() )
    info.append( 'check unit:\t%s' % a.checkUnit() )
    info.append( 'remove unknow node:\t%s' % a.remove_unknow_node() )
    
    a.set_Playback()
    
    info = '\n'.join(info)
    print type(info)
    a.Log.debug( info )
    a.write_log(info)
    
    # check relative path
    RelativePath.main()
    
if __name__ == '__main__' :
#    fileName = sys.argv[1]
#    if not fileName:
#        fileName = 'D:/workspace/tools/DIGITAL37/Maya/Python/digital37/maya/general/qc.txt'
    main()
    