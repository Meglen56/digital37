# -*- coding: utf-8 -*-
#Description:
#Author:honglou(hongloull@gmail.com)
#Create:2011.12.06
#Update:
#How to use :
import logging
LOG_LEVELS = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL}
LOG_LEVEL = LOG_LEVELS.get('debug')
logging.basicConfig(level=LOG_LEVEL)
                                     
import maya.cmds as cmds
import pymel.core as pm
from pymel.all import mel
from pymel.core.general import PyNode

LIGHT_TYPES = ['<class \'pymel.core.nodetypes.SpotLight\'>',\
               '<class \'pymel.core.nodetypes.DirectionLight\'>',\
               '<class \'pymel.core.nodetypes.VolumeLight\'>',\
               '<class \'pymel.core.nodetypes.AreaLight\'>',\
               '<class \'pymel.core.nodetypes.AmbientLight\'>',\
               '<class \'pymel.core.nodetypes.PointLight\'>']
GEOMETRY_TYEPS = ['<class \'pymel.core.nodetypes.Mesh\'>',\
                  '<class \'pymel.core.nodetypes.NurbsSurface\'>',\
                  '<class \'pymel.core.nodetypes.Subdiv\'>']   
SHADING_ENGINE_TYPE = '<class \'pymel.core.nodetypes.ShadingEngine\'>'

DEFAULT_RENDER_GLOBALS = PyNode('defaultRenderGlobals')
MI_DEFAULT_OPTIONS = PyNode('miDefaultOptions')
MI_DEFAULT_FRAME_BUFFER = PyNode('miDefaultFramebuffer')
            
def getSelection():
    logging.debug('MRREnderLayer getSelection')
    selObjShort = pm.ls(sl=1)
    selObj = pm.ls(sl=1,dag=1)
    logging.debug(str(selObjShort))
    if not selObjShort :
        logging.warning('select some objects first.')
        return None
    else :
        return selObj

def getGeometrySelection():
    logging.debug('MRREnderLayer getSelection')
    selObjShort = pm.ls(sl=1)
    selObj = pm.ls(sl=1,dag=1,lf=1,type=['mesh','nurbsSurface','subdiv'])
    logging.debug(str(selObjShort))
    if not selObjShort :
        logging.warning('select some objects first.')
        return None
    else :
        return selObj
    
def createShader(shaderType,shaderName):
    '''string $RGBObjMat = `shadingNode -n ("MATTE_" + $eachSn[0] + "_MAT") -asShader surfaceShader`;
        string $RGBObjSG = `sets -renderable true -noSurfaceShader true -empty -name ($RGBObjMat + "_SG")`;
        setAttr ($RGBObjMat + ".outColor") -type double3 0 0 0 ;
        setAttr ($RGBObjMat + ".outMatteOpacity") -type double3 1 1 1 ; 
        connectAttr -f ($RGBObjMat + ".outColor") ($RGBObjSG + ".surfaceShader");
        connectAttr -f $dispCon[0] ($RGBObjSG + ".displacementShader");'''
    surfaceShader = pm.shadingNode(shaderType,n=shaderName,asShader=True)
    shadingSG = pm.sets(renderable=True,noSurfaceShader=True,empty=True,name=(shaderName+'_SG'))
    surfaceShader.outColor.connect(shadingSG.surfaceShader)
    return ( surfaceShader, shadingSG )

#        if selObj :
#            for each in selObj :
#                nodeType = type(each)
#                logging.debug(str(nodeType))
#                if str(nodeType) in GEOMETRY_TYEPS :
#                    logging.debug('****'+str(each))
#                    eachSn = each.getParent()
#                    conAll = each.connections(d=1)
#                    logging.debug('conAll: '+str(conAll))
#                    for con in conAll :
#                        conType = type(con) 
#                        logging.debug(str(conType))
#                        if str(conType) == SHADING_ENGINE_TYPE :
#                            logging.debug('displacement shader: ')
#                            dispCon = con.displacementShader.connections(p=1,d=1)
#                            if len(dispCon) >= 1 :
#                                logging.debug('displacement shader: '+str(dispCon[0]))
#                                logging.debug('eachSn[0]: ' + str(eachSn))
def getDisplacementShader(input):
    displacementShader = None
    connectionAll = input.connections(d=1)
    logging.debug('input: '+str(input))
    logging.debug('connectionAll: '+str(connectionAll))
    for connection in connectionAll :
        if str( type(connection) ) == SHADING_ENGINE_TYPE :
            dispConnections = connection.displacementShader.connections(p=1,d=1)
            if len(dispConnections) >= 1 :
                displacementShader = dispConnections[0]
                logging.debug('displacement shader: '+str(displacementShader))
    return displacementShader
                                                
class MRRenderLayerPass():
    def __init__(self):
        logging.debug('Init MRRenderLayerPass class')
        self.loadMRPlugin()
    
    def loadMRPlugin(self):
        #Check MR plugin load or not
        if not cmds.pluginInfo( 'Mayatomr', query=True, loaded=True ) :
            logging.warning('Maya to MentalRay Plugin has not been loaded.Loading Mayatomr now.')
            cmds.loadPlugin( 'Mayatomr' )

class MRRenderLayer():
    def __init__(self):
        logging.debug('Init MRRenderLayer class')

    def createNewLayer(self,layerName):
        newLayer = pm.createRenderLayer(n=layerName)
        pm.editRenderLayerGlobals(currentRenderLayer=newLayer)
        #editRenderLayerAdjustment "defaultRenderGlobals.currentRenderer"
        pm.editRenderLayerAdjustment(DEFAULT_RENDER_GLOBALS.currentRenderer)
        DEFAULT_RENDER_GLOBALS.currentRenderer.set('mentalRay')    
        return newLayer     
    
    def setRenderLayerAttr(self,attr,val):
        # Unlock if locked
        isLock = 0
        if attr.isLocked() == 1:
            attr.unlock()
            isLock = 1
        
        # Break connections
        attrInputs = attr.connections(p=1,d=1)
        if len(attrInputs) >= 1 :
            attr.disconnect( attrInputs[0] )
        
        # Set attr    
        pm.editRenderLayerAdjustment(attr)
        attr.set(val)
        
        # Re lock again if locked before
        if isLock == 1 :
            attr.lock()
     
    def disConnectCamShader(self):
        '''        string $allCams[] = `ls -ca`;
        for ($each in $allCams){
            string $camRenderAttr = `getAttr ($each + ".renderable")`;
            if ($camRenderAttr == 1){
                string $renderCam = $each;
                string $renderCamLensSHD[] = `listConnections -d 1 ($renderCam + ".miLensShader")`;
                if ($renderCamLensSHD[0] != ""){
                    editRenderLayerAdjustment ($renderCam + ".miLensShader");
                    disconnectAttr ($renderCamLensSHD[0] + ".message") ($renderCam + ".miLensShader");
                }
                string $renderCamEnv[] = `getAttr ($each + ".miEnvironmentShader")`;
                if ($renderCamEnv[0] != ""){
                    editRenderLayerAdjustment ($renderCam + ".miEnvironmentShader");
                    disconnectAttr ($renderCamEnv[0] + ".message") ($renderCam + ".miEnvironmentShader");
                }                 
            }
        }'''
        # disconnecet lensShader and envShader
        allCams = pm.ls(type='camera')
        for cam in allCams :
            if cam.renderable.get() == 1 :
                renderCamLensSHD = cam.miLensShader.connections(d=1)
                if renderCamLensSHD :
                    pm.editRenderLayerAdjustment(cam.miLensShader)
                    renderCamLensSHD[0].message.disconnect(cam.miLensShader)
                renderCamEnv = cam.miEnvironmentShader.get()
                if renderCamEnv :
                    pm.editRenderLayerAdjustment(cam.miEnvironmentShader)
                    renderCamEnv[0].message.disconnect(cam.miEnvironmentShader)
                       
    def createAmbientOcclusionLayer(self):
        selObj = getSelection()
        
        newLayer = self.createNewLayer('AO')
        
        AOMat = pm.shadingNode('surfaceShader',n='AO_mat',asShader=True)
        AONode = pm.createNode('mib_amb_occlusion')
        AONode.outValue.connect(AOMat.outColor)
        AONode.samples.set(64)
        
        if selObj :
            for each in selObj :
                nodeType = type(each)
                logging.debug(str(nodeType))
                
                # Get dispalcement shader if input is geometry
                if str(nodeType) in GEOMETRY_TYEPS :
                    logging.debug('****'+str(each))
                    eachSn = each.getParent()
                    displacementShader = getDisplacementShader(each)
                    if displacementShader :
                        shader,shaderSG = createShader('lambert',(newLayer+'_'+str(eachSn)+'_MAT'))
                        shader.color.set([0,0,0])
                        shader.transparency.set([0,0,0])
                                
                        displacementShader.connect(shaderSG.displacementShader)
                        AONode = pm.createNode('mib_amb_occlusion')
                        AONode.outValue.connect(shader.incandescence)
                        AONode.samples.set(64)
                                
                        pm.select(eachSn)
                        mel.hyperShade(assign=shader)
                                
                    else :
                        pm.select(eachSn)
                        mel.hyperShade(assign=AOMat)
                else :
                    if str(nodeType) in LIGHT_TYPES :
                        lightSn = each.getParent()
                        pm.editRenderLayerMembers(newLayer,lightSn,remove=1)
                        pm.editRenderLayerMembers(newLayer,each,remove=1)
                
                pm.select(each)
                logging.debug('each: '+str(each))
                eachSn = pm.pickWalk(d='down')
                logging.debug('eachSn: '+str(eachSn[0]))
                if eachSn[0] != each :
                    pm.editRenderLayerMembers(newLayer,eachSn[0],remove=1)

        # Adjust render layer attr
        self.setRenderLayerAttr(MI_DEFAULT_OPTIONS.finalGather, 0)
        self.setRenderLayerAttr(MI_DEFAULT_OPTIONS.caustics, 0)
        self.setRenderLayerAttr(MI_DEFAULT_OPTIONS.globalIllum, 0)
        self.setRenderLayerAttr(MI_DEFAULT_FRAME_BUFFER.datatype, 2)
        self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.imageFormat, 7)
        self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.imfPluginKey, 'iff')
        self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.multiCamNamingMode, 1)
        self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.bufferName, '<RenderPass>')

        # Remove cam lens and env shader            
        self.disConnectCamShader()
        
        pm.select(cl=1)

class MRMaterial():
    def __init__(self):
        logging.debug('Init MRMaterial class')
    
    # Create and assign black shader
    def createBlackShader(self):
        shaderName = 'BLACK_mat'
        selObj = getGeometrySelection()
        if selObj :
            for each in selObj :
                # Get dispalcement shader if input is geometry
                eachSn = each.getParent()
                displacementShader = getDisplacementShader(each)
                if displacementShader :
                    shaderNameWithDisp = "MATTE_" + eachSn + "_MAT"
                    if pm.objExists(shaderNameWithDisp) :
                        pm.select(each,r=1)
                        pm.hyperShade(assign=PyNode(shaderNameWithDisp))
                    else :
                        shader,shaderSG = createShader('surfaceShader', shaderNameWithDisp)
                        displacementShader.connect(shaderSG.displacementShader)
                        shader.outColor.set([0,0,0])
                        shader.outMatteOpacity.set([1,1,1])
                        pm.select(each,r=1)
                        mel.hyperShade(assign=shader)
                else :
                    if not pm.objExists(shaderName) :
                        shader,shaderSG = createShader('surfaceShader', shaderName)
                        shader.outColor.set([0,0,0])
                        shader.outMatteOpacity.set([1,1,1])
                    pm.select(each,r=1)
                    pm.hyperShade(assign=PyNode(shaderName))
                            
#MRRenderLayerPass()
#MRRenderLayer().createAmbientOcclusionLayer()
MRMaterial().createBlackShader()
