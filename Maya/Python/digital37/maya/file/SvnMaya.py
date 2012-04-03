# -*- coding: utf-8 -*-
import os
import re
import logging 
import threading
import tempfile, subprocess, traceback
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
        
    def get_workspace(self):
        self.WorkSpace_RootDir = pm.workspace(q=1,rd=1)
        logging.debug('self.WorkSpace_RootDir:\t%s',self.WorkSpace_RootDir)
        self.RuleEntry_SourceImages = pm.workspace('sourceImages',fileRuleEntry=1,q=1 )
        logging.debug('self.RuleEntry_SourceImages:\t%s',self.RuleEntry_SourceImages)
        self.RuleEntry_3dPaintTextures = pm.workspace('3dPaintTextures',fileRuleEntry=1,q=1 )
        self.RuleEntry_Scenes = pm.workspace('scene',fileRuleEntry=1,q=1 )
        logging.debug('self.RuleEntry_Scenes:\t%s',self.RuleEntry_Scenes)
        
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
                            
    def writeMessage(self,f,p):
        while True :
            #subprocess is not complete
            if p.poll() == None :
                if p.stdout :
                    try:
                        output = p.stdout.readline()
                    except KeyboardInterrupt:
                        logging.debug( 'user canceled.\r\n' )
                        break
                    except:
                        traceback.print_exc()
                        break
                    else:
                        if output :
                            f.write( output )
                            f.flush()
                            # 
                            if self.Window:
                                try:
                                    output = unicode(output,'gbk','ignore')
                                    self.Window.insertPlainText( output )
                                except KeyboardInterrupt:
                                    logging.debug( 'user canceled.\r\n' )
                                except:
                                    traceback.print_exc()
                                    break
                                    
            #subprocess is complete
            else :
                if(p.returncode==0):
                    logging.debug( 'SvnMaya:Success\r\n' )
                else:
                    logging.debug("ReturnCode: %s",str(p.returncode) )
                break
        
    def execute_cmd(self,cmd,logPrefix):
        # write cmd output to log file
        fd,batch_file = tempfile.mkstemp(suffix='.bat',prefix=('.'+logPrefix))
        os.close(fd)
        fObj = open(batch_file,'w')
        fObj.write( cmd )
        fObj.flush()
        fObj.close()
        logging.debug( 'Batch File:\t%s',batch_file )
        
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
                    
class SvnMaya(General):
    def __init__(self):
        # set logger
        self.setLog('debug')
       
        self.Window = None
        self.Reference_File = None
        
        
    def set_window(self,window):
        self.Window = window
        
    def get_associated_file(self):
        self.Maya_Ref_File = set()
        self.Texture_Files = set()
        self.Ref_Dir = set()
        self.Texture_Files_Expand = set()
        
        self.get_workspace()
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
                    
        cmd = ' '.join(self.Ref_Dir)
        return cmd
                 
    def svn_cmd(self,cmdType,isLock=True,isSave=True):
        # get full path scene name
        scene_name = pm.system.sceneName()

        cmdList = list()
        
        if cmdType == 'commit' :
            if isSave == True :
                # save scene
                pm.mel.eval('file -s -f')
            cmdList.append('svn add \"%s\"'%scene_name)
            cmdList.append('svn commit -m \"\" \"%s\"'%scene_name)
            if isLock == True :
                cmdList.append('svn lock \"%s\"'%scene_name)
            else :
                cmdList.append('svn unlock \"%s\"'%scene_name)
        elif cmdType == 'update' :
            cmdList.append('svn update \"%s\"'%scene_name)
        elif cmdType == 'lock' :
            cmdList.append('svn lock \"%s\"'%scene_name)
        elif cmdType == 'unlock' :
            cmdList.append('svn unlock \"%s\"'%scene_name)
        elif cmdType == 'log' :
            cmdList.append('svn log \"%s\"'%scene_name)      
            # reload current opened scene
        elif cmdType == 'getLockStatus' :
            cmdList.append('svn status \"%s\"'%scene_name) 
        else:
            logging.error('svn_cmd:can not find match command type %s',cmdType)
        cmd = '\n'.join(cmdList)
        logging.debug( 'cmd:%s',cmd )
        # using subprocess to execute command and write log
        if cmdType != 'getLockStatus' :
            self.execute_cmd(cmd,cmdType)
        
    def svn_cleanup_path(self,fullPath):
        cmdList = list()
        cmdList.append('svn cleanup \"%s\"'%fullPath)
        cmd = '\n'.join(cmdList)
        logging.debug( 'cmd:%s',cmd )
        self.execute_cmd(cmd,'cleanup_path')
                
    def svn_update_path(self,fullPath):
        cmdList = list()
        cmdList.append('svn update \"%s\"'%fullPath)
        cmd = '\n'.join(cmdList)
        logging.debug( 'cmd:%s',cmd )
        self.execute_cmd(cmd,'update_path')
        
    def svn_update_project(self,ruleEntry):
        self.get_workspace()
        path = ''
        if ruleEntry == 'asset' :
            path = os.path.join(self.WorkSpace_RootDir,self.RuleEntry_Scenes,'asset')
        elif ruleEntry == 'sourceimages':
            path = os.path.join(self.WorkSpace_RootDir,self.RuleEntry_SourceImages)
        logging.debug('path of %s:\t%s',path,path)
        self.svn_update_path(path)
                        
    def svn_update_associated(self):
        # get associated files
        cmd = 'svn update ' + self.get_associated_file()
        self.execute_cmd(cmd,'update_associated')
            
def main():
    pass
    
if __name__ == '__main__' :
    pass
    