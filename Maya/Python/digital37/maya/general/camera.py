import maya.cmds as cmds
import pymel.core as pm
import traceback

def set_attr_for_pb(cameraShape):
    '''set camera attributes for playblast
    '''
    pm.camera(cameraShape,e=1,displayFilmGate=0,displayResolution=0,overscan=1.0)
        
def lock_camera(self,camera,log=None):
    '''lock camera shape and camera transform
    '''
    if not log:
        import logging
        log = logging.getLogger()
        
    # lock camera shape node
    status = True
    for x in ['hfa','vfa','fl','lsr','fs','fd','sa','coi']:
        # check attribute has been lock or not
        if not cmds.getAttr((camera + '.' + x),lock=True) :
            status = False
            try:
                cmds.setAttr((camera + '.' + x),lock=True)
            except:
                log.error('can not lock camera shape:%s' % camera)                            
                log.error(traceback.format_exc())

    if status:
        log.debug('lock camera shape success:%s'% camera)
    else:
        log.warning('%s has not been locked'% camera)
        
    # get camera transform node
    c = cmds.listRelatives(camera,parent=True)[0]
    # lock camera transform node
    status = True
    for x in set(['tx','ty','tz','rx','ry','rz','sx','sy','sz']):
        # check attribute has been lock or not
        if not cmds.getAttr((camera + '.' + x),lock=True) :
            status = False
            try:
                cmds.setAttr((camera + '.' + x),lock=True)
            except:
                status = False
                log.error(traceback.format_exc())
    if status:
        log.debug('lock camera transform success:%s'% c)
    else:
        log.warning('%s has not been locked'% c)
            
        
def delete_perspective_camera(log=None):
    '''
    delete all perspective cameras except 'persp'
    '''
    if not log:
        import logging
        log = logging.getLogger()
        
    cam_persp = cmds.listCameras(perspective=True)
    cam_persp.remove('persp')
    if cam_persp:
        for cam in cam_persp:
            try:
                cmds.delete( cam )
            except:
                log.error('can not delete camera:%s' % cam)
                log.error(traceback.format_exc())
            else:
                log.warning('delete camera success:%s' % cam)
    else:
        log.debug('There is no perspective camera in the scene.')
        
                        
class Camera():
    def __init__(self,log=None):
        self.Cam = set()
        self.Cam_Renderable = set()
        if not log:
            import logging
            self.Log = logging.getLogger()
            
    def get_renderable_camera(self):
        # set persp to can not be renderable
        if pm.PyNode('perspShape').renderable.get() == True :
            pm.PyNode('perspShape').renderable.set(False)
            self.Log.warning( 'persp is renderable' )
            
        cams_default = set(['perspShape','sideShape','topShape','frontShape'])
        cams = set( cmds.ls(type='camera') )
        self.Cam = cams - cams_default
        self.Cam_Renderable=set()
        if self.Cam :
            for c in self.Cam:
                if cmds.getAttr( c + '.renderable' ) :
                    self.Cam_Renderable.add(c)
        if not self.Cam_Renderable :
            self.Log.warning('no renderable camera')
            
    def check_attr(self,camera):
        '''
        check camera's attribute
        '''
        # check attr
        # check "fit resolution gate" is set to "Horizontal" or not
        if cmds.getAttr(camera + '.filmFit') != 1:
            try:
                cmds.setAttr((camera + '.filmFit'),1)
            except:
                self.Log.error('set camera fit resolution gate error:%s' % camera)
            else:
                self.Log.warning('set camera \"fit resolution gate\" attribute to \"Horizontal\" success:%s' % camera)
        
    def check_renderable_camera(self,camPrefix='cam_'):
        # use ' ' as a fill char and center aligned
        self.Log.debug('{0:-<40}'.format('check_renderable_camera'))
        
        # set persp to can not be renderable
        if pm.PyNode('perspShape').renderable.get() == True :
            pm.PyNode('perspShape').renderable.set(False)
            self.Log.warning( 'persp is renderable' )
        
        # no camera can be renderable
        if not self.Cam_Renderable :
            for c in self.Cam:
                if c.startswith(camPrefix):
                    try:
                        cmds.setAttr((c+'.renderable'),True)
                    except:
                        self.Log.error('set %s renderable error' % c)
                        self.Log.error(traceback.format_exc())
                    else:
                        self.Cam_Renderable.add(c)
                        self.Log.debug('set %s renderable success' % c)
        # more than one cameras can be renderable
        elif len(self.Cam_Renderable) > 1 :
            self.Log.warning( 'more then one renderable camera' % ' '.join( list(self.Cam_Renderable) ) )
        else :
            self.Log.debug('only have one renderable camera\t%s' % list(self.Cam_Renderable)[0] )
            
        for c in self.Cam_Renderable:
            # lock camera
            lock_camera(c, self.Log)
            # check camera attr
            self.check_attr(c)
