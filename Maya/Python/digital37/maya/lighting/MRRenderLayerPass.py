#!/usr/bin/python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Description:
#Author:honglou(hongloull@gmail.com)
#Create:2011.12.06
#Update:
#How to use :
import logging
from pymel.core.general import PyNode
LOG_LEVELS = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL}
LOG_LEVEL = LOG_LEVELS.get('debug')
logging.basicConfig(level=LOG_LEVEL)

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
                                     
import maya.cmds as cmds
import pymel.core as pm
from pymel.all import mel

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
        self.defaultRenderGlobals = PyNode('defaultRenderGlobals')
        self.miDefaultOptions = PyNode('miDefaultOptions')
        self.miDefaultFrameBuffer = PyNode('miDefaultFramebuffer')
        
    def getSelection(self):
        logging.debug('MRREnderLayer getSelection')
        selObjShort = pm.ls(sl=1)
        selObj = pm.ls(sl=1,dag=1)
        logging.debug(str(selObjShort))
        if not selObjShort :
            logging.warning('select some objects first.')
            return None
        else :
            return selObj
    
    def createNewLayer(self,layerName):
        newLayer = pm.createRenderLayer(n=layerName)
        pm.editRenderLayerGlobals(currentRenderLayer=newLayer)
        #editRenderLayerAdjustment "defaultRenderGlobals.currentRenderer"
        defaultRenderGlobals = PyNode('defaultRenderGlobals')
        pm.editRenderLayerAdjustment(defaultRenderGlobals.currentRenderer)
        defaultRenderGlobals.currentRenderer.set('mentalRay')    
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
        # disconncet lensShader and envShader
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
        selObj = self.getSelection()
        
        newLayer = self.createNewLayer('AO')
        
        AOMat = pm.shadingNode('surfaceShader',n='AO_mat',asShader=True)
        AONode = pm.createNode('mib_amb_occlusion')
        AONode.outValue.connect(AOMat.outColor)
        AONode.samples.set(64)
        
        if selObj :
            for each in selObj :
                nodeType = type(each)
                logging.debug(str(nodeType))
                if str(nodeType) in GEOMETRY_TYEPS :
                    logging.debug('****'+str(each))
                    eachSn = each.getParent()
                    conAll = each.connections(d=1)
                    logging.debug('conAll: '+str(conAll))
                    for con in conAll :
                        conType = type(con) 
                        logging.debug(str(conType))
                        if str(conType) == SHADING_ENGINE_TYPE :
                            logging.debug('displacement shader: ')
                            dispCon = con.displacementShader.connections(p=1,d=1)
                            if len(dispCon) >= 1 :
                                logging.debug('displacement shader: '+str(dispCon[0]))
                                logging.debug('eachSn[0]: ' + str(eachSn))
                                AOObjMat = pm.shadingNode('lambert',n=(newLayer+'_'+str(eachSn)+'_MAT'),asShader=True)
                                AOObjMat.color.set([0,0,0])
                                AOObjMat.transparency.set([0,0,0])
                                
                                AOObjSG = pm.sets(renderable=True,noSurfaceShader=True,empty=True,name=(str(AOObjMat)+'_SG'))
                                AOObjMat.outColor.connect(AOObjSG+'.surfaceShader')
                                dispCon[0].connect(AOObjSG+'.displacementShader')
                                AONode = pm.createNode('mib_amb_occlusion')
                                AONode.outValue.connect(str(AOObjMat)+'.incandescence')
                                AONode.samples.set(64)
                                
                                pm.select(eachSn)
                                mel.hyperShade(assign=AOObjMat)
                                
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

#        if mrOptions.finalGather.isLocked() != 1:
#            pm.editRenderLayerAdjustment(mrOptions.finalGather)
#            mrOptions.finalGather.set(0) 
#        if mrOptions.caustics.get() == 1:
#            pm.editRenderLayerAdjustment(mrOptions.caustics)
#            mrOptions.caustics.set(0)
#        if mrOptions.globalIllum.get() == 1:
#            pm.editRenderLayerAdjustment(mrOptions.globalIllum)
#            mrOptions.globalIllum.set(0)
        
        '''editRenderLayerAdjustment "miDefaultFramebuffer.datatype";
        editRenderLayerAdjustment "defaultRenderGlobals.imageFormat";
        editRenderLayerAdjustment "defaultRenderGlobals.imfPluginKey";
        setAttr "miDefaultFramebuffer.datatype" 2;
        setAttr "defaultRenderGlobals.imageFormat" 7;
        setAttr -type "string" "defaultRenderGlobals.imfPluginKey" "iff";
        setAttr "defaultRenderGlobals.multiCamNamingMode" 1;
        setAttr -type "string" "defaultRenderGlobals.bufferName" "<RenderPass>";'''
       
#        pm.editRenderLayerAdjustment(mrFrameBuffer.datatype)
#        mrFrameBuffer.datatype.set(2)
#        pm.editRenderLayerAdjustment(self.defaultRenderGlobals.imageFormat)
#        self.defaultRenderGlobals.imageFormat.set(7)
#        pm.editRenderLayerAdjustment(self.defaultRenderGlobals.imfPluginKey)
#        self.defaultRenderGlobals.imfPluginKey.set('iff')
#        self.defaultRenderGlobals.multiCamNamingMode.set(1)
#        self.defaultRenderGlobals.bufferName.set('<RenderPass>')

        # Adjust render layer attr
        self.setRenderLayerAttr(self.miDefaultOptions.finalGather, 0)
        self.setRenderLayerAttr(self.miDefaultOptions.caustics, 0)
        self.setRenderLayerAttr(self.miDefaultOptions.globalIllum, 0)
        self.setRenderLayerAttr(self.miDefaultFrameBuffer.datatype, 2)
        self.setRenderLayerAttr(self.defaultRenderGlobals.imageFormat, 7)
        self.setRenderLayerAttr(self.defaultRenderGlobals.imfPluginKey, 'iff')
        self.setRenderLayerAttr(self.defaultRenderGlobals.multiCamNamingMode, 1)
        self.setRenderLayerAttr(self.defaultRenderGlobals.bufferName, '<RenderPass>')
                    
        # Remove cam lens and env shader            
        self.disConnectCamShader()
        
        pm.select(cl=1)
            
#MRRenderLayerPass()
MRRenderLayer().createAmbientOcclusionLayer()
