# -*- coding: utf-8 -*-
import os
import logging 
import threading
import tempfile, subprocess, traceback, time
import pymel.core as pm
from pymel.all import mel
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
            
class SvnMaya(General):
    def __init__(self):
        # set logger
        self.setLog('debug')
        self.Maya_Ref_File = set()
        self.Texture_File = set()
        self.Ref_Dir = set()
        self.Cmd_Update = 'svn update '
        self.Window = None
        self.Reference_File = None
        
    def set_window(self,window):
        self.Window = window
        
    def get_texture_file(self):
        self.Texture_File = set()
        # Get texture file
        texturesList = cmds.ls(textures=True)
        if texturesList :
            for tex in texturesList:
                if cmds.attributeQuery( 'fileTextureName',node=tex,exists=1 ):
                    texFile = cmds.getAttr( (tex+'.fileTextureName') )
                    self.Texture_File.add(texFile)
        self.log_list( self.Texture_File )
        
    def get_reference_file(self):
        # check scene name is not set or not
        if pm.system.sceneName():
            # Get reference file
            self.Reference_File = set( cmds.file(q=True,l=True) )
            self.log_list( self.Reference_File )
        
    def get_associated_file(self):
        #self.get_reference_file()
        if self.Reference_File:
            self.get_texture_file()
            
            dirs = set( os.path.dirname(f) for f in ( self.Reference_File | self.Texture_File ) )
            
            for d in dirs :
                
                while True :
                    if not os.path.exists(d) :
                        # Get parent dir
                        d = os.path.dirname(d)
                    else:
                        break
                
                self.Ref_Dir.add(d)
                    
            cmd = self.Cmd_Update + ' '.join(self.Ref_Dir)
            self.svn_update(cmd)
                 
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
        self.Log = 'SvnMaya.' + str(int(time.time())) + '.log'
        f = None
        logDir = tempfile.tempdir
        if not os.path.exists( logDir ):
            os.mkdir( logDir )
        try:
            f = open( ( logDir + '/' + self.Log ),'a' )
        except:
            raise('SvnMaya:Can not write logs file.')
        logging.debug( 'logDir:%s',logDir )
        
        # use subprocess to start command
        p = subprocess.Popen(data, shell=True, bufsize=512,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        self.writeMessage(f,p)
        
        threadName = threading.Thread( target=self.writeMessage,args=( f,p ) )
        threadName.setDaemon(1)
        threadName.start()
                    
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
            
def main():
    SvnMaya().get_associated_file()
    
if __name__ == '__main__' :
    pass
    #main()
    