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
        
        #infoFilePath = 'H:/Streamline_Quest_Featurette_11/Tools/Submitter/createQuicktime_info.job'
        jobInfoFilename = tempfile.mkstemp(prefix='Quicktime_job_',suffix='.job')[1]
        fObj = open(jobInfoFilename,'w')
        fObj.write( txt )
        fObj.flush()
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
        
        #jobFilePath = '//server-cgi/RND/temp/createQuicktime_job.job'
        pluginInfoFilename = tempfile.mkstemp(prefix='Quicktime_plugin_',suffix='.job')[1]
        fObj = open(pluginInfoFilename,'w')
        fObj.write( txt )
        fObj.flush()
        fObj.close()
        
        return pluginInfoFilename
    
    def run(self,start, end, inputFilePath, outputFilePath, taskName):
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
        deadlineCmd.replace('/','\\')
        
        print 'Deadline Command :', deadlineCmd
        os.system(deadlineCmd)

if __name__ == '__main__' :
    Quicktime().run(1, 25, 'd:/temp2/quicktime/colorBar.0001.tga', 'd:/temp2/quicktime/colorBar.mov', 'quicktime_test')
    