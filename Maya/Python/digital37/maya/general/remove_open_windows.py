import maya.cmds as cmds

def main():
    debug = list()
    
    # use ' ' as a fill char and center aligned
    debug.append('{0:-<40}'.format('remove_open_windows'))
    error = debug
    
    for x in cmds.lsUI(wnd=True) :
        if ( cmds.window(x,q=True,vis=True) and x != 'MayaWindow' ) :
            print x
            #scriptEditorPanel1Window
            try:
                cmds.deleteUI(x,window=True)
            except:
                error.append('delete window %s error' % x)
            else:
                debug.append('delete window %s success' % x)
    
    return ('\r\n'.join(debug), '\r\n'.join(error))