import pymel.core as pm

def main(unit_linear,unit_time,log=None):
    if not log:
        import logging
        log = logging.getLogger()
    
    # use ' ' as a fill char and center aligned
    log.debug('{0:-<40}'.format('check_unit'))
    
    # What is the current linear unit?
    #if pm.currentUnit( query=True, linear=True ) != u'cm' :
    if pm.currentUnit( query=True, linear=True ) != unit_linear :
        pm.currentUnit(linear=unit_linear)
        log.warning('current linear unit not match:%s' % unit_linear)
    else:
        log.debug('current linear unit match:%s' % unit_linear)
        
    #if pm.currentUnit( query=True, time=True ) != u'film' :
    if pm.currentUnit( query=True, time=True ) != unit_time :
        pm.currentUnit(linear=unit_time)
        log.warning('current time unit not match:%s' % unit_time)
    else:
        log.debug('current time unit match:%s' % unit_time)
