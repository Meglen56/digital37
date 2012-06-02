import pymel.core as pm

def main(unit_linear,unit_time):
    debug = list()
    
    # use ' ' as a fill char and center aligned
    debug.append('{0: ^80}'.format('check_unit'))
    error = debug
    
    # What is the current linear unit?
    #if pm.currentUnit( query=True, linear=True ) != u'cm' :
    if pm.currentUnit( query=True, linear=True ) != unit_linear :
        pm.currentUnit(linear=unit_linear)
        debug.error('current linear unit not match:%s' % unit_linear)
    else:
        debug.debug('current linear unit match:%s' % unit_linear)
        
    #if pm.currentUnit( query=True, time=True ) != u'film' :
    if pm.currentUnit( query=True, time=True ) != unit_time :
        pm.currentUnit(linear=unit_time)
        debug.error('current time unit not match:%s' % unit_time)
    else:
        debug.debug('current time unit match:%s' % unit_time)
        
    print '\r\n'.join(debug)
    print '\r\n'.join(error)
    return ('\r\n'.join(debug), '\r\n'.join(error))
