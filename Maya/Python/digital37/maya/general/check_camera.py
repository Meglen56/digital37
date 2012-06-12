import maya.cmds as cmds
import pymel.core as pm
import traceback

def main(log=None):
    if not log:
        import logging
        log = logging.getLogger()
    # use ' ' as a fill char and center aligned
    log.debug('{0:-<40}'.format('check_camera'))
    
    # set persp to can not be renderable
    if pm.PyNode('perspShape').renderable.get() == True :
        pm.PyNode('perspShape').renderable.set(False)
        log.warning( 'persp is renderable' )
        
    cams_default = set(['perspShape','sideShape','topShape','frontShape'])
    cams = set( cmds.ls(type='camera') )
    cam = cams - cams_default
    cams_renderable=set()
    if cam :
        for c in cam:
            if cmds.getAttr( c + '.renderable' ) :
                cams_renderable.add(c)
                
                # lock camera shape node
                status = True
                for x in ['hfa','vfa','fl','lsr','fs','fd','sa','coi']:
                    # check attribute has been lock or not
                    if not cmds.getAttr((c + '.' + x),lock=True) :
                        status = False
                        try:
                            cmds.setAttr((c + '.' + x),lock=True)
                        except:
                            log.error('can not lock camera shape:%s' % c)                            
                            log.error(traceback.format_exc())

                if status:
                    log.debug('lock camera shape success:%s'% c)
                else:
                    log.warning('%s has not been locked'% c)
                    
                # get camera transform node
                c = cmds.listRelatives(c,parent=True)[0]
                # lock camera transform node
                status = True
                for x in set(['tx','ty','tz','rx','ry','rz','sx','sy','sz']):
                    # check attribute has been lock or not
                    if not cmds.getAttr((c + '.' + x),lock=True) :
                        status = False
                        try:
                            cmds.setAttr((c + '.' + x),lock=True)
                        except:
                            status = False
                            log.error(traceback.format_exc())
                if status:
                    log.debug('lock camera transform success:%s'% c)
                else:
                    log.warning('%s has not been locked'% c)
    
    # no camera can be renderable
    if not cams_renderable :
        for c in cam:
            if c.startswith('cam_'):
                try:
                    cmds.setAttr((c+'.renderable'),True)
                except:
                    log.error('set %s renderable error' % c)
                    log.error(traceback.format_exc())
                else:
                    log.debug('set %s renderable success' % c)
    # more than one cameras can be renderable
    elif len(cams_renderable) > 1 :
        log.warning( 'more then one renderable camera' % ' '.join( list(cams_renderable) ) )
    else :
        log.debug('only have one renderable camera\t%s' % list(cams_renderable)[0] )
