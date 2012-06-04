import pymel.core as pm

def main(minTime,maxTime,log=None):
    if not log:
        import logging
        log = logging.getLogger()
    # use '*' as a fill char and center aligned
    log.debug('{0:-<40}'.format('set_playback'))
    
    min_before = pm.playbackOptions( q=True,minTime=True ) 
    max_before = pm.playbackOptions( q=True,maxTime=True )
    
    if str(int(min_before)) == minTime :
        log.debug('playback minTime %s is correct' % minTime)
    else :
        log.warning('playback minTime %s is wrong' % min_before)
        try:
            pm.playbackOptions( minTime=minTime )
        except:
            log.error('set playback minTime error')
        else:
            log.debug('set playback minTime to %s' % minTime)
    
    if str(int(max_before)) == maxTime :
        log.debug('playback maxTime %s is correct' % maxTime)
    else :
        log.warning('playback maxTime %s is wrong' % max_before)
        try:
            pm.playbackOptions(maxTime=maxTime )
        except:
            log.error('set playback maxTime error')
        else:
            log.debug('set playback maxTime to %s' % maxTime)

