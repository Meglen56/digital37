from maya.cmds import *
import maya.mel as mm

class rigCamera:
    grpName = 'cam_grp'
    camName = 'renderCam'
    def __init__(self):
        try:
            self.cam = ls(sl=1,type='transform')[0]
            self.cam = rename(self.cam,self.camName)
            self.shp = listRelatives(self.cam,s=1,f=1)[0]
        except:
            self.cam = None
    def setupShape(self):
        # Setup camShape.
        setAttr('%s.displayResolution'%self.shp,k=1)
        setAttr('%s.farClipPlane'%self.shp,k=1)
        setAttr('%s.nearClipPlane'%self.shp,k=1)
        setAttr('%s.horizontalFilmOffset'%self.shp,k=1)
        setAttr('%s.verticalFilmOffset'%self.shp,k=1)
        setAttr('%s.overscan'%self.shp,k=1)
        
        setAttr('%s.centerOfInterest'%self.shp,k=0)
        setAttr('%s.fStop'%self.shp,k=0)
        setAttr('%s.lensSqueezeRatio'%self.shp,k=0)
        setAttr('%s.shutterAngle'%self.shp,k=0)
        setAttr('%s.verticalFilmAperture'%self.shp,k=0)
        setAttr('%s.horizontalFilmAperture'%self.shp,k=0)
        
        setAttr('%s.displayResolution'%self.shp, 1)
        setAttr('%s.displaySafeAction'%self.shp, 0)
        setAttr('%s.renderable'%self.shp, 1)
        setAttr('%s.filmFit'%self.shp, 0)
        
        # 35mm Full Aperture
        setAttr('%s.verticalFilmAperture'%self.shp, 0.735)
        v = getAttr('%s.verticalFilmAperture'%self.shp) * 1.33333
        setAttr('%s.horizontalFilmAperture'%self.shp, v)
        '''
        # Same as global setting
        dar = getAttr('defaultResolution.deviceAspectRatio')
        addAttr(self.shp,ln='filmAspectRatio',at='double',dv=1.777)
        setAttr((self.shp+'.filmAspectRatio'),cb=1)
        #setAttr((self.shp+'.filmAspectRatio'), dar)
        connectAttr('defaultResolution.deviceAspectRatio', '%s.filmAspectRatio'%self.shp)
        expression(s = '%s.horizontalFilmAperture=%s.verticalFilmAperture*%s.filmAspectRatio;'%(self.shp,self.shp,self.shp), n=(self.shp+'_Exp'))
        '''
    def createShake(self,obj,rShake=0,tShake=1):
        '''
        1 - Add attr
        2 - Create grp
        3 - Connect attr (Only rShake)
        4 - Create exp
        5 - Lock attr
        6 - Parent
        '''
        # Add attr.
        if tShake:
            addAttr(obj,ln='tShake',at='double',min=0,dv=0)
            setAttr((obj+'.tShake'),e=1,keyable=1)
        if rShake:
            addAttr(obj,ln='rShake',at='double',min=0,dv=0)
            setAttr((obj+'.rShake'),e=1,keyable=1)
        if tShake:
            addAttr(obj,ln='tShakeSpeed',at='double',min=0,dv=1)
            setAttr((obj+'.tShakeSpeed'),e=1,keyable=1)
        if rShake:
            addAttr(obj,ln='rShakeSpeed',at='double',min=0,dv=1)
            setAttr((obj+'.rShakeSpeed'),e=1,keyable=1)
        # Create grp.
        grp = group(em=True)
        newname = obj.rsplit('|',1)[-1]
        grp = rename(grp,'%s_grp'%obj)
        # Connect attr.
        if rShake:
            connectAttr('%s.t'%obj, '%s.scalePivot'%grp)
            connectAttr('%s.t'%obj, '%s.rotatePivot'%grp)
        #connectAttr('%s.r'%obj, '%s.rotateAxis'%grp)
        # Create exp.
        str = '// Camera Rigging\r\n'
        if tShake:
            str += grp+'.tx = '+obj+'.tShake*0.2*noise('+obj+'.tShakeSpeed*0.5*time);\r\n'
            str += grp+'.ty = '+obj+'.tShake*0.2*noise('+obj+'.tShakeSpeed*0.5*(time+3));\r\n'
            str += grp+'.tz = 1.0 * '+obj+'.tShake*0.2*noise('+obj+'.tShakeSpeed*0.5*(time+7));\r\n'
        if rShake:
            str += grp+'.rx = '+obj+'.rShake*0.5*noise('+obj+'.rShakeSpeed*0.5*time) - '+grp+'.rotateAxisX;\r\n'
            str += grp+'.ry = '+obj+'.rShake*0.5*noise('+obj+'.rShakeSpeed*0.5*(time+5)) - '+grp+'.rotateAxisY;\r\n'
            str += grp+'.rz = 1.0 * '+obj+'.rShake*0.5*noise('+obj+'.rShakeSpeed*0.5*(time+11)) - '+grp+'.rotateAxisZ;\r\n'
        expression(s=str, n=(obj+'_Exp'))
        # Lock attr.
        
        setAttr('%s.tx'%grp, lock=1,keyable=0)
        setAttr('%s.ty'%grp, lock=1,keyable=0)
        setAttr('%s.tz'%grp, lock=1,keyable=0)
        setAttr('%s.rx'%grp, lock=1,keyable=0)
        setAttr('%s.ry'%grp, lock=1,keyable=0)
        setAttr('%s.rz'%grp, lock=1,keyable=0)
        setAttr('%s.sx'%grp, lock=1,keyable=0)
        setAttr('%s.sy'%grp, lock=1,keyable=0)
        setAttr('%s.sz'%grp, lock=1,keyable=0)
        setAttr('%s.v'%grp, lock=1,keyable=0)
        
        # Parent cam.
        cParent = listRelatives(obj,p=1,pa=1)
        if not cParent==None:
            grp = parent(grp, cParent[0])[0]
        obj = parent(obj, grp)[0]
        
        return [obj,grp]
            
    def rig(self):
        if self.cam==None:
            return
        self.setupShape()
        self.cam = self.createShake(self.cam,1)[0]
        select(self.cam,r=1)

class rigCameraOnly(rigCamera):
    def __init__(self):
        mm.eval('CreateCameraOnly;')
        rigCamera.__init__(self)
        self.rig()
class rigCameraAim(rigCamera):
    camOreder = 1
    def __init__(self):
        if self.camOreder==1:
            mm.eval('CreateCameraAim;')
        if self.camOreder==2:
            mm.eval('CreateCameraAimUp;')
        rigCamera.__init__(self)
        try:
            self.aim = ls(sl=1,type='transform')[self.camOreder]
        except:
            self.aim = None
        self.rig()
    def rig(self):
        rigCamera.rig(self)
        self.aim = self.createShake(self.aim)[0]
        connectAttr('%s.rShake'%self.cam,'%s.tShake'%self.aim)
        connectAttr('%s.rShakeSpeed'%self.cam,'%s.tShakeSpeed'%self.aim)
        select(self.cam,r=1)
class rigCameraAimUp(rigCameraAim):
    camOreder = 2


# Main -----------------
def CameraOnly():
    ins = rigCameraOnly()
def CameraAim():
    ins = rigCameraAim()
def CameraAimUp():
    ins = rigCameraAimUp()