import pymel.core as pm

def main(minTime,maxTime):
    debug = list()
    
    # use '*' as a fill char and center aligned
    debug.append('{0:-<40}'.format('set_playback'))
    error = debug
    
    min_before = pm.playbackOptions( q=True,minTime=True ) 
    max_before = pm.playbackOptions( q=True,maxTime=True )
    
    debug.append('playback minTime %s' % min_before)
    if min_before == minTime :
        debug.append('playback minTime %s is correct' % minTime)
    else :
        try:
            pm.playbackOptions( minTime=minTime )
        except:
            error.append('set playback minTime error')
        else:
            debug.append('set playback minTime to %s' % minTime)
    
    if max_before == maxTime :
        debug.append('playback maxTime %s is correct' % maxTime)
    else :
        try:
            pm.playbackOptions(maxTime=maxTime )
        except:
            error.append('set playback maxTime error')
        else:
            debug.append('set playback maxTime to %s' % maxTime)
    
    return ('\r\n'.join(debug), '\r\n'.join(error))
