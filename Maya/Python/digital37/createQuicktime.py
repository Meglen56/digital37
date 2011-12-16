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
    txtList.append('Plugin=QuicktimeFusion')
    txtList.append('Name=%s'%taskName)
    txtList.append('Comment=')
    txtList.append('Department=')
    txtList.append('Pool=fusion61')
    txtList.append('Group=snap')
    txtList.append('Priority=95')
    txtList.append('MachineLimit=1')
    txtList.append('TaskTimeoutMinutes=0')
    txtList.append('Whitelist=')
    txtList.append('LimitGroups=32bit')
    txtList.append('JobDependencies=')
    txtList.append('OnJobComplete=Nothing')
    txtList.append('Frames=%s-%s'%(start, end))
    txtList.append('ChunkSize=100000')
    txtList.append('OutputFilename0=%s'%outputFilePath)
    
    txt = '\n'.join(txtList)
    
    infoFilePath = 'H:/Streamline_Quest_Featurette_11/Tools/Submitter/createQuicktime_info.job'
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
    txtList.append('FrameRate=24')
    txtList.append('Version=6')
    txtList.append('Comment=')
    txtList.append('Department=')
    txtList.append('BackgroundPlate=')
    
    if fullRes :
        txtList.append('Template=H:\\Streamline_Quest_Featurette_11\\Tools\DontTouch\\fusionPlayblastFullRes.comp')
    else :
        txtList.append('Template=H:\\Streamline_Quest_Featurette_11\\Tools\\DontTouch\\fusionPlayblastOriginalRes.comp')
        
    txtList.append('CurveCorrect=False')
    txtList.append('ArtistName=')
    txtList.append('ProjectTitle=%s'%taskName)
    txtList.append('Codec=MPEG-4 Video_mp4v')
    txtList.append('MissingFrames=2')
    txtList.append('Quality=80')
    txtList.append('Proxy=1')
    txtList.append('Gamma=1.8')
    txtList.append('ExpCompensation=0')
    txtList.append('FrameOverride=1')
    
    txt = '\n'.join(txtList)
    
    jobFilePath = 'H:/Streamline_Quest_Featurette_11/Tools/Submitter/createQuicktime_job.job'
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

        
    