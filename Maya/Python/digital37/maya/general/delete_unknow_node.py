import maya.cmds as cmds

def main():
    l = list()
    # use '*' as a fill char and center aligned
    l.append('{0: ^80}'.format('delete_unknow_node'))
    allUnknow = cmds.ls(dep=True)
    if allUnknow:
        for n in allUnknow:
            if(cmds.nodeType(n) == 'unknown'):
                try:
                    cmds.lockNode(n, l=False)
                    cmds.delete(n)
                    print 'delete%s' % n
                except:
                    l.append('can not delete%s' % n)
                else:
                    l.append('delete %s success' % n)
    print '\r\n'.join(l)
    return '\r\n'.join(l)