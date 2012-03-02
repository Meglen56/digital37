import os


def buildInfoFile(start, end, outputFilePath, taskName):
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
    txtList.append('Comment=')
    txtList.append('Department=')
#    txtList.append('Pool=fusion61')
#    txtList.append('Group=snap')
    txtList.append('Priority=95')
    txtList.append('MachineLimit=1')
    txtList.append('TaskTimeoutMinutes=0')
    txtList.append('Whitelist=')
    txtList.append('JobDependencies=')
    txtList.append('OnJobComplete=Nothing')
    txtList.append('Frames=%s-%s'%(start, end))
    txtList.append('ChunkSize=100000')
    txtList.append('OutputFilename0=%s'%outputFilePath)
    
    txt = '\n'.join(txtList)
    
    infoFilePath = 'D:/temp/createQuicktime_info.job'
    with open(infoFilePath, 'w') as f:
        f.write(txt)
        
    return infoFilePath


def buildJobFile (inputFilePath, outputFilePath, taskName, fullRes=False):
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
    
    txtList.append('ProjectTitle=%s'%taskName)
    txtList.append('Codec=QuickTime Movie')
#    txtList.append('SettingsFile="D:/temp/quicktime_export_settings.xml"')
    

    
    txt = '\n'.join(txtList)
    
    jobFilePath = 'd:/temp/createQuicktime_job.job'
    with open(jobFilePath, 'w') as f :
        f.write(txt)
        
    return jobFilePath


def run(start, end, inputFilePath, outputFilePath, taskName, fullRes=False):
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
    
    infoFilePath = buildInfoFile(start, end, outputFilePath, taskName)
    jobFilePath = buildJobFile (inputFilePath, outputFilePath, taskName, fullRes=False)
    
    deadlineCmd = ''
    deadlineCmd += 'DeadlineCommand.exe '
    deadlineCmd += infoFilePath + ' '
    deadlineCmd += jobFilePath + ' '
    deadlineCmd.replace('/','\\')
    
    print 'Deadline Command :', deadlineCmd
    os.system(deadlineCmd)

run(1,25,'d:/temp/test.0001.jpg','d:/temp/test2.mov','test2')
    