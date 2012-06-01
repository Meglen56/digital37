import pymel.core as pm

def main():
    debug=error = list()
    
    # use '*' as a fill char and center aligned
    debug.append('{0: ^80}'.format('remove_open_windows'))
    error.append('{0: ^80}'.format('remove_open_windows'))
    
    for x in pm.lsUI(wnd=True) :
        if ( pm.window(x,q=True,vis=True) and x != 'MayaWindow' ) :
            try:
                pm.deleteUI(x,window=True)
            except:
                error.append('delete window %s error' % x)
            else:
                debug.append('delete window %s success' % x)
    
    return ['\r\n'.join(debug), '\r\n'.join(error)]