import maya.cmds as cmds
import pymel.core as pm
import traceback

def main():
    debug = list()
    error = list()
    # use '*' as a fill char and center aligned
    debug.append('{0: ^80}'.format('check_camera'))
    error.append('{0: ^80}'.format('check_camera'))
    
    # set persp to can not be renderable
    if pm.PyNode('perspShape').renderable.get() == True :
        pm.PyNode('perspShape').renderable.set(False)
        
    cams_default = set(['perspShape','sideShape','topShape','frontShape'])
    cams = set( cmds.ls(type='camera') )
    cam = cams - cams_default
    cams_renderable=set()
    if cam :
        for c in cam:
            if cmds.getAttr( c + '.renderable' ) :
                cams_renderable.add(c)
                
                # get camera transform node
                c = cmds.listRelatives(c,parent=True)[0]
                # lock camera
                for x in set(['tx','ty','tz','rx','ry','rz','sx','sy','sz']):
                    try:
                        cmds.setAttr((c + '.' + x),lock=True)
                    except:
                        traceback.print_exc()
                        error.append('can not lock camera:%s' % c)
                    else:
                        debug.append('lock camera success:%s'% c)
    
    # no camera can be renderable
    if not cams_renderable :
        for c in cam:
            try:
                cmds.setAttr((c+'.renderable'),True)
            except:
                traceback.print_exc()
                error.append('set %s renderable error' % c)
            else:
                debug.append('set %s renderable success' % c)
    # more than one cameras can be renderable
    elif len(cams_renderable) > 1 :
        error.append( 'more then one renderable camera' % ' '.join( list(cams_renderable) ) )
    else :
        debug.append('only have one renderable camera\t%s' % c)
        
    print '\r\n'.join(debug)
    print '\r\n'.join(error)
    return [ '\r\n'.join(debug), '\r\n'.join(error) ]