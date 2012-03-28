# -*- coding: utf-8 -*-
import os
import re
import logging 
import threading
import tempfile, subprocess, traceback, time
import pymel.core as pm
import maya.cmds as cmds

class General():
    def __init__(self):
        pass
            
    def setLog(self,logLevel):
        LOG_LEVELS = {'debug': logging.DEBUG, 'info':logging.INFO, \
                  'warning': logging.WARNING, 'error': logging.ERROR,\
                  'critical': logging.CRITICAL}
        LOG_LEVEL = LOG_LEVELS.get(logLevel)
        logging.basicConfig(level=LOG_LEVEL)
        
    def log_dict(self,inputDict):
        if inputDict :
            s = ''
            try :
                s += str(inputDict)
            except :
                logging.warning('can not convert inputDict to string')        
            for k,v in inputDict.items() :
                s += '\t\t'
                s += 'key:'+str(k) + '\t'
                s += 'value:'+str(v)
            logging.debug(s)
    
    def log_list(self,inputList):
        if inputList :
            s = ''
            if inputList :
                try :
                    s += str(inputList)
                except :
                    logging.warning('can not convert inputList to string')
                for i in inputList :
                    s += '\t' + str(i)
            logging.debug(s)
        else:
            logging.debug('log_list:input is None')
            
    def get_scene_name(self):
        self.Scene_Name = os.path.splitext( os.path.basename( pm.system.sceneName() ) )[0]
                        
    def writeMessage(self,f,p):
        while True :
            #subprocess is not complete
            if p.poll() == None :
                if p.stdout :
                    try:
                        output = p.stdout.readline()
                    except:
                        traceback.print_exc()
                        break
                    else:
                        if output :
                            f.write( output )
                            f.flush()
                            # 
                            if self.Window:
                                output = unicode(output,'gbk','ignore')
                                self.Window.insertPlainText( output )
                                    
            #subprocess is complete
            else :
                if(p.returncode==0):
                    logging.debug( 'SvnMaya:Success\r\n' )
                else:
                    logging.debug("ReturnCode: %s",str(p.returncode) )
                break
            
class SvnMaya(General):
    def __init__(self):
        # set logger
        self.setLog('debug')
        self.Maya_Ref_File = set()
        self.Texture_Files = set()
        self.Ref_Dir = set()
        self.Cmd_Update = 'svn update '
        self.Window = None
        self.Reference_File = None
        self.Texture_Files_Expand = set()
        self.get_workspace()
        
    def set_window(self,window):
        self.Window = window
        
    def expand_names_for_sourceimages(self):
        print 'self.WorkSpace_RootDir:',self.WorkSpace_RootDir
        print 'self.RuleEntry_SourceImages:',self.RuleEntry_SourceImages
        print 'self.RuleEntry_3dPaintTextures:',self.RuleEntry_3dPaintTextures
        for f in self.Texture_Files :
            # convert to expand name
            for partten in [self.RuleEntry_SourceImages,self.RuleEntry_3dPaintTextures] :
                f = self.convert_to_relative(partten, f)
            
            self.Texture_Files_Expand.add( os.path.join( self.WorkSpace_RootDir,\
                                                         f) )
        print 'self.Texture_Files_Expand:'
        self.log_list(self.Texture_Files_Expand)
    
    def convert_to_relative(self,parten,inputStr):
        '''
        example: convertToRelative('sourceimages','C:/AW/Maya5.0/sourceimages/maya.exe')
        result: 'sourceimages/maya.exe'
        '''
        #p = re.compile('^.*/sourceimages')
        inputStr = inputStr.replace('\\','/')
        returnStr = re.sub( ('^.*/' + parten), parten, inputStr )
        print inputStr,'\t',returnStr
        return returnStr
        
    def get_workspace(self):
        self.WorkSpace_RootDir = pm.workspace(q=1,rd=1)
        self.RuleEntry_SourceImages = pm.workspace('sourceImages',fileRuleEntry=1,q=1 )
        self.RuleEntry_3dPaintTextures = pm.workspace('3dPaintTextures',fileRuleEntry=1,q=1 )
        
    def get_texture_file(self):
        self.Texture_Files = set()
        # Get texture file
        texturesList = cmds.ls(textures=True)
        if texturesList :
            for tex in texturesList:
                if cmds.attributeQuery( 'fileTextureName',node=tex,exists=1 ):
                    texFile = cmds.getAttr( (tex+'.fileTextureName') )
                    print 'texFile:',texFile
                    self.Texture_Files.add(texFile)
        self.log_list( self.Texture_Files )
        
    def get_reference_file(self):
        # check scene name is not set or not
        if pm.system.sceneName():
            # Get reference file
            self.Reference_File = set( cmds.file(q=True,l=True) )
            self.log_list( self.Reference_File )
        
    def update_associated_file(self):
        self.get_reference_file()
        self.get_texture_file()
        # get file texture's expand name
        self.expand_names_for_sourceimages()
            
        dirs = set( os.path.dirname(f) for f in ( self.Reference_File | self.Texture_Files_Expand ) )
        print 'dirs:',dirs    
        for d in dirs :
            i = 0
            # TODO : loop will not more than 15
            while True and i < 15 :
                if not os.path.exists(d) :
                    # Get parent dir
                    d = os.path.dirname(d)
                    #logging.debug('dir:',str(d))
                    #print 'dir:',d 
                i += 1
                
            self.Ref_Dir.add(d)
                    
        cmd = self.Cmd_Update + ' '.join(self.Ref_Dir)
        self.svn_update(cmd)
                 
    def svn_commit(self,lock=True):
        # get full path scene name
        scene_name = pm.system.sceneName()
        #cmd = 'svn add \"' + scene_name + '\"\n'
        #write received cmd to temp file
        cmd = 'svn commit -m \"\" \"' + str(scene_name) + '\"'
        print cmd
        
        # write cmd output to log file
        fd,self.Log = tempfile.mkstemp(suffix='.log',prefix='SvnMaya_commit')
        os.close(fd)
        fObj = open(self.Log,'w')
        fObj.write( cmd )
        fObj.flush()
        fObj.close()
        logging.debug( 'log:\t%s',self.Log )
        
        fd,self.Log = tempfile.mkstemp(suffix='.log',prefix='SvnMaya_commit')
        os.close(fd)
        fObj = open(self.Log,'a')
                
        p = subprocess.Popen(cmd, shell=True, bufsize=512,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        
        threadName = threading.Thread( target=self.writeMessage,args=( fObj,p ) )
        threadName.setDaemon(1)
        threadName.start()

    def svn_update(self, data):        
        logging.debug( 'data:%s', data )
        #write received cmd to temp file
        fRender = tempfile.mkstemp(suffix='.bat',prefix='SvnMaya')
        os.close(fRender[0])
        fObj = open(fRender[1],'w')
        fObj.write( data )
        fObj.flush()
        fObj.close()

        # write cmd output to log file
        self.Log = 'SvnMaya.update' + str(int(time.time())) + '.log'
        f = None
        logDir = tempfile.tempdir
        if not os.path.exists( logDir ):
            os.mkdir( logDir )
        try:
            f = open( ( logDir + '/' + self.Log ),'a' )
        except:
            raise('SvnMaya:Can not write logs file.')
        logging.debug( 'logDir:%s',logDir )
        
        p = subprocess.Popen(data, shell=True, bufsize=512,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        
        threadName = threading.Thread( target=self.writeMessage,args=( f,p ) )
        threadName.setDaemon(1)
        threadName.start()
            
def main():
    #SvnMaya().update_associated_file()
    SvnMaya().svn_commit()
    
if __name__ == '__main__' :
    pass
    