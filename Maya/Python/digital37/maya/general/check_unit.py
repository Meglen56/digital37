import pymel.core as pm

def main(unit_linear,unit_time):
    l = list()
    # use '*' as a fill char and center aligned
    l.append('{0: ^80}'.format('check_unit'))
    
    # What is the current linear unit?
    #if pm.currentUnit( query=True, linear=True ) != u'cm' :
    if pm.currentUnit( query=True, linear=True ) != unit_linear :
        pm.currentUnit(linear=unit_linear)
        return False
    #if pm.currentUnit( query=True, time=True ) != u'film' :
    if pm.currentUnit( query=True, time=True ) != unit_time :
        pm.currentUnit(linear=unit_time)
        return False
        
    print '\r\n'.join(l)
    return '\r\n'.join(l)