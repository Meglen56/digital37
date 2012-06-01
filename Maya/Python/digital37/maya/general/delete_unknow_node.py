import maya.cmds as cmds

def main():
    debug = list()
    error = list()
    # use '*' as a fill char and center aligned
    debug.append('{0: ^80}'.format('delete_unknow_node'))
    error.append('{0: ^80}'.format('delete_unknow_node'))
    
    allUnknow = cmds.ls(dep=True)
    if allUnknow:
        for n in allUnknow:
            if(cmds.nodeType(n) == 'unknown'):
                try:
                    cmds.lockNode(n, l=False)
                    cmds.delete(n)
                    print 'delete%s' % n
                except:
                    error.append('can not delete%s' % n)
                else:
                    debug.append('delete %s success' % n)
                    
    print '\r\n'.join(debug)
    print '\r\n'.join(error)
    return [ '\r\n'.join(debug), '\r\n'.join(error) ]