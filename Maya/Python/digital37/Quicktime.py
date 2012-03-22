import os
import tempfile

class Quicktime():
    def __init__(self):
        pass
    
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
        txtList.append('Name=%s'%taskName)
        txtList.append('Pool=397')
        txtList.append('Group=none')
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
    
    def run(self,start, end, inputFilePath, outputFilePath, movieSettingsFile,taskName):
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
        
        deadlineCmd = ''
        deadlineCmd += 'DeadlineCommand.exe '
        deadlineCmd += jobInfoFilename + ' '
        deadlineCmd += pluginInfoFilename + ' '
        # Important:must add movie settings file
        deadlineCmd += movieSettingsFile + ' '
        deadlineCmd.replace('/','\\')
        
        print 'Deadline Command :', deadlineCmd
        os.system(deadlineCmd)
        #os.popen(deadlineCmd)

if __name__ == '__main__' :
    #Quicktime().run(1, 25, 'd:/temp2/quicktime/colorBar.0001.tga', 'd:/temp2/quicktime/colorBar.mov', 'quicktime_test')
    Quicktime().run(1, 25, 'd:/temp2/quicktime/colorBar.0001.tga', 'd:/temp2/quicktime/colorBar.mov', 'Q:/mhxy/quicktime_export_settings.xml','quicktime_test')
    