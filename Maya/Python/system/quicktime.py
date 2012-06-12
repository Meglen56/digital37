import os
import tempfile
import system as system
import log as log
reload(log)

class Quicktime(system.System,log.Log):
    QUICKTIME_SETTINGS = 'q:/mhxy/quicktime_export_settings.xml'
    DEADLINE_POOL = 'none'
    DEADLINE_GROUP = 'none'
    
    def __init__(self):
        pass
    
    def set_quicktime_settings(self,fileName):
        Quicktime.QUICKTIME_SETTINGS = fileName

    def get_quicktime_settings(self):
        return Quicktime.QUICKTIME_SETTINGS
                
    def set_deadline_pool(self,poolName):
        Quicktime.DEADLINE_POOL = poolName
        
    def set_deadline_group(self,groupName):
        Quicktime.DEADLINE_GROUP = groupName

    def get_deadline_pool(self):
        return Quicktime.DEADLINE_POOL
                    
    def get_deadline_group(self):
        return Quicktime.DEADLINE_GROUP
    
    def buildJobInfoFile(self,start, end, outputFilePath,taskName):
        '''
        Build the info file.
        
        param :
        start
        end
        outputFilePath
        taskName
        '''
        txtList = list()
        txtList.append('Plugin=Quicktime')
        txtList.append('Name=%s' % taskName)
        txtList.append('Pool=%s' % self.get_deadline_pool() )
        txtList.append('Group=%s' % self.get_deadline_group() )
        txtList.append('Priority=95')
        txtList.append('MachineLimit=1')
        txtList.append('Frames=%s-%s'%(start, end))
        txtList.append('ChunkSize=100000')
        txtList.append('OutputFilename0=%s'% outputFilePath)
        
        txt = '\n'.join(txtList)
        
        #mkstemp returns both the OS file handle to and the filename of the temporary file. 
        #When you re-open the temp file, the original returned file handle is still open 
        #(no-one stops you from opening twice or more the same file in your program)
        fd,jobInfoFilename = tempfile.mkstemp(prefix='Quicktime_job_',suffix='.job')
        #fObj = open(jobInfoFilename,'w')
        fObj = os.fdopen(fd,'w')
        fObj.write( txt )
        fObj.close()
            
        return jobInfoFilename
    
    # Create plugin info file
    def buildPluginInfoFile (self,inputFilePath, outputFilePath):
        '''
        Build the job file.
        
        If fullRes is true create a quicktime with a resolution of 1920*1038 else
        use the resolution of the input file.
        
        param :
        inputFilePath
        outputFilePath
        taskName
        fullRes
        '''
        
        txtList = list()
        txtList.append('InputImages=%s'%inputFilePath)
        txtList.append('OutputFile=%s'%outputFilePath)
        txtList.append('FrameRate=25')
        txtList.append('Codec=QuickTime Movie')
        #txtList.append('SettingsFile=\"q:/mhxy/quicktime_export_settings.xml\"')
        
        txt = '\n'.join(txtList)
        
        #mkstemp returns both the OS file handle to and the filename of the temporary file. 
        #When you re-open the temp file, the original returned file handle is still open 
        #(no-one stops you from opening twice or more the same file in your program)
        fd,pluginInfoFilename = tempfile.mkstemp(prefix='Quicktime_plugin_',suffix='.job')
        #fObj = open(pluginInfoFilename,'w')
        fObj = os.fdopen(fd,'w')
        fObj.write( txt )
        fObj.close()
        
        return pluginInfoFilename
    
    # submit quicktime command to renderfarm(deadline)
    def submit_quicktime_cmd(self,start, end, inputFilePath, outputFilePath, movieSettingsFile,taskName):
        '''
        Build the info and the job file and submit to deadline.
        param :
        start
        end
        inputFilePath
        outputFilePath
        taskName
        fullRes
        '''
        jobInfoFilename = self.buildJobInfoFile(start, end, outputFilePath,taskName)
        pluginInfoFilename = self.buildPluginInfoFile (inputFilePath, outputFilePath)
        
        deadlineCmd = list()
        deadlineCmd.append('DeadlineCommand.exe ')
        deadlineCmd.append( jobInfoFilename + ' ' )
        deadlineCmd.append( pluginInfoFilename + ' ')
        # Important:must add movie settings file
        deadlineCmd.append(movieSettingsFile + ' ')
        deadlineCmd = ''.join(deadlineCmd)
        deadlineCmd.replace('/','\\')
        
        print 'Deadline Command :', deadlineCmd
        os.system(deadlineCmd)
        #os.popen(deadlineCmd)

    # make quicktime command local by deadlinequicktimegenerator
    def make_mov_cmd(self,sequence,startFrame,finishFrame,movieName=None):
        ## deadlinequicktimegenerator.exe -CreateMovie d:/temp/test.0001.jpg d:/temp/quicktime_export_settings.xml "QuickTime Movie" 1 25 25 d:/temp/test3.mov
        cmd = list()
        cmd.append('deadlinequicktimegenerator -CreateMovie ')
        cmd.append(sequence + ' ' )
        cmd.append(self.get_quicktime_settings() + ' ')
        cmd.append('"QuickTime Movie" ' + str(startFrame) + ' ' + str(finishFrame) + ' 25 ')
        if not movieName:
            movieName = sequence.split('.')[0] + '.mov'
        cmd.append( movieName )
        return ''.join(cmd)
        
    def make_mov(self,sequence,startFrame,finishFrame):
        # get make movie command        
        cmd = self.make_mov_cmd(sequence,startFrame,finishFrame)
        print 'make_mov_cmd:%s' % cmd
        self.Log.debug('make_mov_cmd:%s' % cmd)
        # run movie command
        self.execute_cmd(cmd)
        
# main('R:/project/pipelineProject/quicktime/quicktime_export_settings.xml','R:/project/pipelineProject/quicktime/images/colorBar.0001.jpg',1,10,None,'debug')
def main(quickTimeSettingsFile,imagesFile,startFrame,finishFrame,logFile=None,logLevel='debug'):
    a = Quicktime()
    a.get_file_logger(logFile,logLevel)
    #a.get_stream_logger()
    a.Log.debug('make_mov:')
    a.set_quicktime_settings(quickTimeSettingsFile)
    a.make_mov(imagesFile, startFrame, finishFrame)
#    a.submit_quicktime_cmd(1, 10, 'R:/project/pipelineProject/quicktime/images/colorBar.0001.jpg', \
#                           'R:/project/pipelineProject/quicktime/colorBar.mov', \
#                           'R:/project/pipelineProject/quicktime/quicktime_export_settings.xml','quicktime_test')
    
if __name__ == '__main__' :
    pass
#    main('R:/project/pipelineProject/quicktime/quicktime_export_settings.xml',\
#         'R:/project/pipelineProject/quicktime/images/colorBar.0001.jpg',1,10,'d:/temp2/quickTime.log','debug')
    