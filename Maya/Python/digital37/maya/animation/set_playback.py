import pymel.core as pm

def main(minTime,maxTime):
    debug,error = list()
    
    # use '*' as a fill char and center aligned
    debug.append('{0: ^80}'.format('set_playback'))
    error.append('{0: ^80}'.format('set_playback'))
    
    try:
        pm.playbackOptions( minTime=minTime,\
                            maxTime=maxTime )
    except:
        error.append('set_playback error')
    else:
        debug.append('set_playback success')
        
    print '\r\n'.join(debug)
    print '\r\n'.join(error)
    return ['\r\n'.join(debug), '\r\n'.join(error)]
