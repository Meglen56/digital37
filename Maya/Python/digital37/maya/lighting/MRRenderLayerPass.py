# -*- coding: utf-8 -*- 
#Description:
#Author:honglou(hongloull@gmail.com)
#Create:2011.12.06
#Update: 
#Howto use : 
import logging 
#from idlelib.RemoteDebugger import traceback
LOG_LEVELS = {'debug': logging.DEBUG, 'info':logging.INFO, \
              'warning': logging.WARNING, 'error': logging.ERROR,\
              'critical': logging.CRITICAL}
LOG_LEVEL = LOG_LEVELS.get('debug')
logging.basicConfig(level=LOG_LEVEL)

import traceback
import maya.cmds as cmds
import pymel.core as pm
from pymel.all import mel
from pymel.core.general import PyNode

MRCMD = '''unifiedRenderGlobalsWindow;
//updateRendererUI;
//addOneTabToGlobalsWindow("mentalRay", "Common", "createMayaSoftwareCommonGlobalsTab");
//addOneTabToGlobalsWindow("mentalRay", "Passes", "createMayaRenderPassTab");
//addOneTabToGlobalsWindow("mentalRay", "Features", "createMentalRayFeaturesTab");
//addOneTabToGlobalsWindow("mentalRay", "Quality", "createMentalRayQualityTab");
//addOneTabToGlobalsWindow("mentalRay", "Indirect Lighting", "createMentalRayIndirectLightingTab");
//addOneTabToGlobalsWindow("mentalRay", "Options", "createMentalRayOptionsTab");
'''

PASSES_ALL = {'mv2DToxik':'2DMotionVector', 'mv3D':'3DMotionVector', 'ambient':'ambient',\
                  'ambientIrradiance':'ambientIrradiance','ambientRaw':'ambientMaterialColor',\
                  'AO':'ambientOcclusion', 'beauty':'beauty',\
                  'beautyNoReflectRefract':'beautyWithoutReflectionsRefractions',\
                  'blank':'blank', 'depth':'cameraDepth', \
                  'depthRemapped':'cameraDepthRemapped',\
                  'coverage':'coverage', 'customColor':'customColor',\
                  'customDepth':'customDepth','customLabel':'customLabel',\
                  'customVector':'customVector','diffuse':'diffuse',\
                  'diffuseMaterialColor':'diffuseMaterialColor',\
                  'diffuseNoShadow':'diffuseWithoutShadows',\
                  'directIrradiance':'directIrradiance',\
                  'directIrradianceNoShadow':'directIrradianceWithoutShadows',\
                  'glowSource':'glowSource', 'incandescence':'incandescence',\
                  'incidenceCN':'incidenceCamNorm', 'incidenceCNMat':'incidenceCamNormMaterial',\
                  'incidenceLN':'incidenceLightNorm', 'indirect':'indirect', \
                  'volumeLight':'lightVolume', 'matte':'matte', 'normalCam':'normalCam',\
                  'normalCamMaterial':'normalCamMaterial',\
                  'mv2DNormRemap':'normalized2DMotionVector',\
                  'normalObj':'normalObj','normalObjMaterial':'normalObjMaterial',\
                  'normalWorld':'normalWorld','normalWorldMaterial':'normalWorldMaterial',\
                  'volumeObject':'objectVolume', 'opacity':'opacity', 'shadowRaw':'rawShadow',\
                  'reflectedMaterialColor':'reflectedMaterialColor','reflection':'reflection',\
                  'refraction':'refraction','refractionMaterialColor':'refractionMaterialColor',\
                  'scatter':'scatter', 'volumeScene':'sceneVolume', 'shadow':'shadow',\
                  'specular':'specular', 'specularNoShadow':'specularWithoutShadows',\
                  'translucence':'translucence', 'translucenceNoShadow':'translucenceWithoutShadows',\
                  'UVPass':'UV', 'worldPosition':'worldPosition'}
PRESET_LAYER = ['Normal','Color','AO','AO_Transparency','Shadow']
    
# Load mental ray plugin first, else can not made some global var      
def loadMRPlugin():
    #Check MR plugin load or not
    if not cmds.pluginInfo( 'Mayatomr', query=True, loaded=True ) :
        logging.warning('Maya to MentalRay Plugin has not been loaded.Loading Mayatomr now.')
        cmds.loadPlugin( 'Mayatomr' )
loadMRPlugin()
#mel.eval(MRCMD)

def setAttr(attr,val):
    # Check if attr exists
    logging.debug('attr: ' + str(attr))
    if pm.objExists(attr) :
        logging.debug('attr: ' + str(attr))
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
        try :
            attr.set(val)
        except :
            logging.warning('set attr error:' + str(attr) + str(val))
                
        # Re lock again if locked before
        if isLock == 1 :
            attr.lock()
        else :
            logging.warning(str(attr) + ' does not exists')

DEFAULT_RENDER_GLOBALS = PyNode('defaultRenderGlobals')

# Let maya make some mr attr            
def setRendererToMR(): 
    renderer = DEFAULT_RENDER_GLOBALS.currentRenderer.get()
    logging.debug('current renderer: ' + str(renderer))
    if renderer != 'mentalRay' :
        DEFAULT_RENDER_GLOBALS.currentRenderer.set('mentalRay')
       
    # Display render settings window to fix some menetal ray attr do not exists
    #mel.eval('mentalrayAddTabs;')

setRendererToMR()

# Get some global var
MAYA_LOCATION = mel.getenv('MAYA_LOCATION')
MI_DEFAULT_OPTIONS = None
MI_DEFAULT_FRAME_BUFFER = None
try :
    MI_DEFAULT_OPTIONS = PyNode('miDefaultOptions')
except :
    logging.error('Get miDefaultOptions error.')
try :
    MI_DEFAULT_FRAME_BUFFER = PyNode('miDefaultFramebuffer')
except :
    logging.error('Get miDefaultFramebuffer error.')
                         
LIGHT_TYPES = ['<class \'pymel.core.nodetypes.SpotLight\'>',\
               '<class \'pymel.core.nodetypes.DirectionalLight\'>',\
               '<class \'pymel.core.nodetypes.VolumeLight\'>',\
               '<class \'pymel.core.nodetypes.AreaLight\'>',\
               '<class \'pymel.core.nodetypes.AmbientLight\'>',\
               '<class \'pymel.core.nodetypes.PointLight\'>']
GEOMETRY_TYEPS = ['<class \'pymel.core.nodetypes.Mesh\'>',\
                  '<class \'pymel.core.nodetypes.NurbsSurface\'>',\
                  '<class \'pymel.core.nodetypes.Subdiv\'>']   
SHADING_ENGINE_TYPE = '<class \'pymel.core.nodetypes.ShadingEngine\'>'
PASS_TYPE = '<class \'pymel.core.nodetypes.RenderPass\'>'
  
#source_list is a dict, remove_value_list is a list  
def dict_remove_by_value(source_list,remove_value_list):    
    for l in source_list :
        if l.values()[0] in remove_value_list :
            source_list.remove(l)
    return source_list

def get_dict_list_values(source_list):
    return_list = []
    for l in source_list :
        return_list.append( l.values()[0] )    
    return return_list

def dict_add(dict1,dict2):
    for k,v in dict2.items() :
        if not dict1.has_key(k) :
            dict1[k] = v
    print dict1
    return dict1

def log_dict(inputDict):
    if inputDict :
        s = ''
        try :
            s += str(inputDict)
        except :
            logging.warning('can not convert inputDict to string')        
        for k,v in inputDict.items() :
            s += '\t\t'
            s += 'key:'+str(k) + '\t'
            s += 'value:'+str(v)
        logging.debug(s)

def log_list(inputList):
    if inputList :
        s = ''
        if inputList :
            try :
                s += str(inputList)
            except :
                logging.warning('can not convert inputList to string')
            for i in inputList :
                s += '\t' + str(i)
        logging.debug(s)
    else:
        logging.debug('log_list:input is None')
            
def rename(node,name):
    try:
        pm.rename(node,name)
    except:
        traceback.print_exc()
    
def getSelection():
    logging.debug('MRRenderLayerPass getSelection')
    selObjShort = pm.ls(sl=1,l=1)
    logging.debug(str(selObjShort))
    if not selObjShort :
        logging.warning('select some objects first.')
        return None
    else :
        return selObjShort

def getSelection_dict():
    logging.debug('MRRenderLayerPass getSelection_dict')
    sels = pm.ls(sl=1,l=1)
    logging.debug(str(sels))
    if not sels :
        logging.warning('select some objects first.')
        return None
    else :
        sels_dict = {}
        for sel in sels :
            sels_dict[ sel.longName() ] = sel
        return sels_dict
        
def getDAGSelection():
    logging.debug('MRRenderLayerPass getDAGSelection')
    selObjShort = pm.ls(sl=1)
    selObj = pm.ls(sl=1,dag=1)
    logging.debug(str(selObjShort))
    if not selObjShort :
        logging.warning('select some objects first.')
        return None
    else :
        return selObj

def getGeometrySelection():
    logging.debug('MRRenderLayerPass getDAGSelection')
    selObj = pm.ls(sl=1,dag=1,lf=1,type=['mesh','nurbsSurface','subdiv'])
    if not selObj :
        logging.warning('select some objects first.')
        return None
    else :
        return selObj
    
def getLightSelection():
    logging.debug('MRRenderLayerPass getDAGSelection')
    selObj = pm.ls(sl=1,dag=1,lf=1,type=['spotLight','directionalLight',\
                                         'volumeLight','areaLight','ambientLight','pointLight'])
    if not selObj :
        logging.warning('select some objects first.')
        return None
    else :
        return selObj
    
def createShader(shaderType,shaderName):
    surfaceShader = pm.shadingNode(shaderType,n=shaderName,asShader=True)
    shadingSG = pm.sets(renderable=True,noSurfaceShader=True,empty=True,name=(shaderName+'_SG'))
    surfaceShader.outColor.connect(shadingSG.surfaceShader)
    return ( surfaceShader, shadingSG )

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
                logging.debug('displacement shader: '+str(dispConnections[0]))
    return displacementShader

# Flatten list with set
def flattenList(input):
    for i in input :
        if input.count(i) != 1 :
            input.remove(i)
    return input

def getDisplacementShader2(input):
    displacementShaders = []
    shapeFaces = []
    
    connectionAll = flattenList( input.connections(d=1) )
    logging.debug('input: '+str(input))
    logging.debug('connectionAll: '+str(connectionAll))
    for connection in connectionAll :
        if str( type(connection) ) == SHADING_ENGINE_TYPE :
            dispConnections = connection.displacementShader.connections(p=1,d=1)
            if len(dispConnections) >= 1 :
                
                logging.debug('displacement shader: '+str(dispConnections[0]))
                #Get ShadingSG's set member
                members = pm.sets(connection, q=1 )
                #Get shape's faces in shadingSG'set
                shape = None
                shapeFace = []
                for m in members :
                    logging.debug('members: ' + str(m))
                    # For pCubeShape1.f[0:1]
                    m = str(m)
                    if '.' in m :
                        shape,face = m.split('.')
                        logging.debug('shape: ' + str(shape))
                        logging.debug('input: ' + str(input))
                        if shape == str(input) :
                            shapeFace.append( m )
                    # For pCubeShape1
                    else :
                        if m == str(input) :
                            shapeFace.append( m )
                
                if shapeFace != [] :
                    shapeFaces.append(shapeFace)
                    displacementShaders.append( dispConnections[0] )
                    
    logging.debug('---------getDisplacementShader Start------------')
    logging.debug('input: ' + str(input))
    for displacementShader,shapeFace in zip(displacementShaders,shapeFaces) :
        logging.debug('displacementShader: ' + str(displacementShader))
        logging.debug('shapeFace: ' + str(shapeFace))
    logging.debug('---------getDisplacementShader Finish------------\n')
    return (displacementShaders, shapeFaces)

def getTransparencyShader(input):
    shapeFaces = []
    transparencyConnections = None
    connectionAll = flattenList( input.connections(d=1) )
    logging.debug('input: '+str(input))
    logging.debug('connectionAll: '+str(connectionAll))
    for connection in connectionAll :
        if str( type(connection) ) == SHADING_ENGINE_TYPE :
            transparency = None
            displacement = None
            dispConnections = connection.displacementShader.connections(p=1,d=1)
            # Get transparency's input connection
            try :
                surfAttr = PyNode(connection.surfaceShader)
            except :
                logging.error(str(input) + ' has no surface shader\'s connection')
            else :
                try :
                    surfaceShader = connection.surfaceShader.connections(p=0,d=1)
                except :
                    logging.error(str(input) + ' ' + str(PyNode(connection.surfaceShader).longName()) \
                                   + ' has no surface shader\'s connection')
                else :
                    #logging.debug( 'surfaceShader:', str( surfaceShader[0] ) )
                    # Some shader has no 'transparency' connection
                    try:
                        transparencyConnections = surfaceShader[0].transparency.connections(p=0,d=1)
                    except:
                        try :
                            transparencyConnections = surfaceShader[0].outTransparency.connections(p=0,d=1)
                        except :
                            pass
        
                    #Get ShadingSG's set member
                    members = pm.sets(connection, q=1 )
                    #Get shape's faces in shadingSG'set
                    shape = None
                    shapeFace = []
                    returnList = {}
                    for m in members :
                        logging.debug('members: ' + str(m))
                        # For pCubeShape1.f[0:1]
                        m = str(m)
                        if '.' in m :
                            shape,face = m.split('.')
                            logging.debug('shape: ' + str(shape))
                            logging.debug('input: ' + str(input))
                            if shape == str(input) :
                                shapeFace.append( m )
                        # For pCubeShape1
                        else :
                            if m == str(input) :
                                shapeFace.append( m )
                            
                    # Have displacement shader
                    if len(dispConnections) >= 1 :                
                        displacement = dispConnections[0] 
        
                    if len(transparencyConnections) >= 1 :
                        transparency = transparencyConnections[0]                
                        
                    if shapeFace != [] :
                        logging.debug( 'shapeFace:')
                        log_list(shapeFace)
                        if displacement :
                            #logging.debug( 'displacement:', PyNode(displacement) )
                            pass
                        else :
                            logging.debug( 'displacement:None' )
                        if transparency :
                            #logging.debug( 'transparency:', transparency )
                            pass
                        else :
                            logging.debug( 'transparency:None' )
                        # list can not be dict's key, so convert list to tuple
                        shapeFaces.append( {tuple(shapeFace):[displacement,transparency]} )

    logging.debug('---------getTransparencyShader Start------------')
    logging.debug('input: ' + str(input))
    for i in range( len(shapeFaces) ) :
        for k,v in shapeFaces[i].items() :
            logging.debug('shapeFace: ' + str(k))
            logging.debug('displacementShader: ' + str(v[0]))
            logging.debug('transparency: ' + str(v[1]))
    logging.debug('---------getTransparencyShader Finish------------\n')
    return shapeFaces
            
def setRenderStatus(renderStatus):
    sels = getGeometrySelection()
    if sels :
        for sel in sels :
            for k,v in renderStatus.items() :
                attr = PyNode(sel.longName()+'.'+k)
                setAttr(attr,v[1])
                                                        
class MRRenderLayerPass():

    
    def __init__(self):
        logging.debug('Init MRRenderLayerPass class')
        #
        self.PASSES_COLOR = ['beauty','depth','diffuse','incandescence','indirect','normalWorld',
                             'reflection','refraction','shadow','specular']
        self.PASSES_COLOR_AVAILABLE = [ x for x in PASSES_ALL.keys() if x not in self.PASSES_COLOR ]
        self.PASSES_SCENE = []
        self.PASSES_AVAILABLE = []
        self.LAYER_NAME = 'color'
        self.PREFIX_PASS = ''
        self.SUFFIX_PASS = ''
        self.LAYER_CURRENT = None
        self.LAYERS_SELECTED = []
        self.LAYERS = []
        self.LAYER_ACTIVE = {}
        self.getLayers()
        
    # Get current active layer
    def getLayerCurrent(self):
        layer_current = pm.editRenderLayerGlobals(q=1,crl=1)
        if layer_current :
            return PyNode(layer_current)
        else :
            return None
        
    def getNameByNode(self,inputObjList):
        if type(inputObjList) == type([]) :
            names_list = []
            for l in inputObjList :
                try:
                    name = l.longName()
                except:
                    traceback.print_exc()
                else:
                    names_list.append( name )
            return names_list
        elif type(inputObjList) == type('') or str( type(inputObjList) ) == PASS_TYPE :
            name = None
            try:
                name = inputObjList.name()
            except:
                traceback.print_exc()
            return name
        else:
            print type(inputObjList)
            
            logging.error('getNameByNode:input obj type is wrong')
            return None
            
    def getNodeByName(self,inputNameList):
        print type(inputNameList)
        if type(inputNameList) == type([]) :
            nodes_list = []
            for l in inputNameList :
                try:
                    node = PyNode( l )
                except:
                    traceback.print_exc()
                else :
                    nodes_list.append( node )
            return nodes_list
        elif type(inputNameList) == type('') :
            node = None
            try:
                node = PyNode( inputNameList )
            except:
                traceback.print_exc()
            return node
        else:
            # there are some bugs inputNameList maybe obj
            # For example : render layer
            # so try PyNode( inputNameList )
            try:
                node = PyNode( inputNameList )
            except:
                traceback.print_exc()
                logging.error('getNodeByName:input name type is wrong')
                return None
            else:
                return node
        
    def getLayers(self):
        self.LAYERS = []
        selObj = pm.ls(type='renderLayer')
        if selObj :
            selObj.remove(PyNode('defaultRenderLayer'))
            log_list(selObj)
            for l in selObj :
                try:
                    name = l.longName()
                except:
                    traceback.print_exc()
                else: 
                    self.LAYERS.append( name )
    
    def getScenePasses(self):
        self.PASSES_SCENE = []
        passes = pm.ls(type='renderPass')
        if passes :
            for p in passes :
                self.PASSES_SCENE.append( self.getNameByNode(p) )
        log_list(self.PASSES_SCENE)

    def getAvailablePasses(self):
        self.PASSES_AVAILABLE = []
        self.getScenePasses()
                
        if self.PASSES_SCENE :
            pNames = [ k for k in PASSES_ALL.keys() if k not in self.PASSES_SCENE ]
            for pn in pNames :
                self.PASSES_AVAILABLE.append( pn )
        # If scene has no pass
        else :
            for pn in PASSES_ALL.keys() :
                self.PASSES_AVAILABLE.append( pn )
                        
    def getObjInLayer(self,layer):
        obj_names_list = pm.editRenderLayerMembers(layer,q=1,fullNames=1)
        log_list(obj_names_list)
        return obj_names_list

    def addObj2Layer(self,layer,obj_list):
        l = get_dict_list_values(obj_list)
        log_list(l)
        #editRenderLayerMembers -noRecurse layer2 nurbsSphere2
        if layer and l :
            pm.editRenderLayerMembers(layer,l,noRecurse=1)
        else :
            if not layer :
                logging.warning('addObj2Layer: layer is None')
            if not l :
                logging.warning('addObj2Layer: selection is None')
                
    def removePassOfLayer(self,layer,obj_list):
        l = [x for x in obj_list.values()]
        log_list(l)
        #editRenderLayerMembers -noRecurse layer2 nurbsSphere2
        if layer and l :
            # Get layer obj from layer name
            logging.debug('removePassOfLaye:')
            #logging.debug('layer:',layer)
            print type(layer)
            layer = PyNode(layer)
            print layer
            print type(layer)
            for item in l :
                pm.editRenderLayerMembers(layer,item,remove=1)
        else :
            if not layer :
                logging.warning('removePassOfLaye: layer is None')
            if not l :
                logging.warning('removePassOfLaye: selection is None')
                                
    def removeObj2Layer(self,layer,obj_list):
        l = [x for x in obj_list.values()]
        log_list(l)
        #editRenderLayerMembers -noRecurse layer2 nurbsSphere2
        if layer and l :
            # Get layer obj from layer name
            logging.debug('removeObj2Layer:')
            #logging.debug('layer:',layer)
            print type(layer)
            layer = PyNode(layer)
            print layer
            print type(layer)
            pm.editRenderLayerMembers(layer,l,noRecurse=1,remove=1)
        else :
            if not layer :
                logging.warning('removeObj2Layer: layer is None')
            if not l :
                logging.warning('removeObj2Layer: selection is None')
                        
    def removeLayerByListWidget(self,layer_dict):
        layers = []
        try:
            layers = layer_dict.values()
        except:
            traceback.print_exc()
        else:
            if layers :
                for layer in layers:
                    print layer
                    try:
                        pm.delete( layer.longName() )
                    except:
                        traceback.print_exc()
                
    def removePass2Layer(self,layer,pass_list):
        # Get layer first
        layer = self.getNodeByName(layer)

        list_values = pass_list.values()
        
        if layer and list_values :
            #disconnectAttr -nextAvailable layer2.renderPass ambientRaw.owner
            for item in list_values :
                layer.renderPass.disconnect(item.owner, nextAvailable=1)
        else :
            if not layer :
                logging.warning('removePass2Layer: layer is None')
            if not list_values :
                logging.warning('removePass2Layer: pass is None')
                
    def removeOverrides2Layer(self,layer,obj_list):
        # Get layer first
        layer = self.getNodeByName(layer)
        
        l = get_dict_list_values(obj_list)
        log_list(l)
        #editRenderLayerMembers -noRecurse layer2 nurbsSphere2
        if layer and l :
            pm.editRenderLayerAdjustment(layer,noRecurse=1,remove=l)
        else :
            if not layer :
                logging.warning('removeOverrides2Layer: layer is None')
            if not l :
                logging.warning('removeOverrides2Layer: selection is None')
            
    def getObjsFromSelsInListWidget(self,listWidget):
        nodes_dict = {}
        items = listWidget.selectedItems()
        if items:
            for item in items :
                # Get item's node
                try :
                    nodes_dict[str(item.text())] = PyNode( str(item.text()) )
                except :
                    logging.warning('can not get pynode from listwidgetItem')
                    print traceback.print_exc()
        return nodes_dict

    def removeScenePasses(self,passesList_dict):
        try:
            pm.delete( passesList_dict.values() )
        except:
            traceback.print_exc()
        else:
            logging.debug('remove scenes passes success')
            
    def getPassByLayer(self,layer):
        passes = None
        passes_list = []
        # get layer by layer name
        try:
            layer = self.getNodeByName(layer)
        except:
            traceback.print_exc()
        else :
            if layer :
                try :
                    passes = layer.renderPass.connections(p=0,d=1)
                except :
                    logging.warning('can not get passes in input layer')
                else :
                    for p in passes :
                        passes_list.append( self.getNameByNode(p) )
        return passes_list
        
    def getOverridesInLayer(self,layer):
        overrides = None
        try :
            overrides = pm.editRenderLayerAdjustment(layer,layer=1,q=1)
            #print overrides
        except :
            logging.warning('can not get layer overrrides')

        #log_dict( overrides )
        return overrides
        
    def createNewMRLayer(self):
        newLayer = pm.createRenderLayer(n=self.LAYER_NAME)
        pm.editRenderLayerGlobals(currentRenderLayer=newLayer)
        pm.editRenderLayerAdjustment(DEFAULT_RENDER_GLOBALS.currentRenderer)
        DEFAULT_RENDER_GLOBALS.currentRenderer.set('mentalRay')    
        return newLayer     
        
    def createNewLayer(self):
        newLayer = pm.createRenderLayer()
        return newLayer   
        
    def setRenderLayerAttr(self,attr,val):
        # Check if attr exists
        logging.debug('attr: ' + str(attr))
        if pm.objExists(attr) :
            logging.debug('attr: ' + str(attr))
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
            try:   
                pm.editRenderLayerAdjustment(attr)
            except :
                logging.warning('editRenderLayerAdjustment error:' + str(attr) + 'skip set attr')
            try :
                attr.set(val)
            except :
                logging.warning('set attr error:' + str(attr) + str(val))
                
            # Re lock again if locked before
            if isLock == 1 :
                attr.lock()
        else :
            logging.warning(str(attr) + ' does not exists')
            
    def disConnectCamShader(self):
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
    
    def createPass2CurrentLayer(self,passName):
        logging.debug('self.PREFIX_PASS:' + self.PREFIX_PASS)
        logging.debug('self.SUFFIX_PASS:' + self.SUFFIX_PASS)
        renderPass = pm.createNode( 'renderPass', n=self.PREFIX_PASS \
                                    + '_' + passName + '_' + self.SUFFIX_PASS )
        #renderPass = pm.ls(sl=1)
        #logging.debug('MAYA_LOCATION: '+MAYA_LOCATION)
        self.applyPassPreset(renderPass, passName)

        self.CURRENT_LAYER.renderPass.connect(renderPass.owner,nextAvailable=1)
    
    def addPass(self,passName):
        renderPass = pm.createNode( 'renderPass',n=passName )
        #renderPass = pm.ls(sl=1)
        #logging.debug('MAYA_LOCATION: '+MAYA_LOCATION)
        self.applyPassPreset(renderPass,passName)

    def applyPassPreset(self,renderPass,passName) :

        passName =  PASSES_ALL[passName]

        presetMel = MAYA_LOCATION+'/presets/attrPresets/renderPass/'+passName+'.mel'
        logging.debug('presetMel: '+presetMel)   
        
        mel.applyAttrPreset(renderPass, presetMel, 1)     
        
    def removePass(self,passName) :
        try:
            pm.delete( PyNode(passName) )
        except:
            traceback.print_exc()
        else:
            logging.debug('success del ',passName)
                    
    def updateScenePasses(self,pass_names_list):
        if pass_names_list :
            print '*'
            print self.PASSES_SCENE
            print '*'
            print pass_names_list
            self.getScenePasses()
            addList = [x for x in pass_names_list \
                       if x not in self.PASSES_SCENE]
            removeList = [x for x in self.PASSES_SCENE \
                          if x not in pass_names_list]
            if addList :
                # add passes to scene
                for pass_name in addList:
                    print '*'
                    print pass_name
                    #logging.debug('add pass name:',pass_name)
                    try:
                        self.addPass( pass_name )
                    except:
                        traceback.print_exc()
                        
            if removeList :
                # add passes to scene
                for pass_name in removeList :
                    try:
                        self.removePass( pass_name )
                    except:
                        traceback.print_exc()
                        
    def updateAssociatedPasses(self,pass_names_list):
        print 'self.LAYERS_SELECTED:'
        print self.LAYERS_SELECTED
        print type(self.LAYERS_SELECTED)
        print type([])
        if self.LAYERS_SELECTED :
            # get layer frm layer name
            for layer in self.getNodeByName( self.LAYERS_SELECTED ) :
                # Get passes in layer
                passes_list = self.getPassByLayer(layer)
                addList = [x for x in pass_names_list \
                           if x not in passes_list]
                removeList = [x for x in passes_list \
                              if x not in pass_names_list]
                
                if addList :
                    for pass_name in addList :
                        try:
                            renderPass = PyNode(pass_name)
                        except:
                            traceback.print_exc()
                        else:
                            try:
                                layer.renderPass.connect(renderPass.owner,nextAvailable=1)
                            except:
                                traceback.print_exc()
                
                if removeList :
                    # add passes to scene
                    for pass_name in removeList :
                        try:
                            renderPass = PyNode(pass_name)
                        except:
                            traceback.print_exc()
                        else:
                            try:
                                layer.renderPass.disconnect(renderPass.owner)
                            except:
                                traceback.print_exc()
            
    def addPasses2Layers(self,layers,pass_names_list):
        if layers and pass_names_list :
            for layer in layers :
                for pass_name in pass_names_list :
                    try:
                        layer.values()[0].renderPass.connect(PyNode(pass_name).owner,nextAvailable=1)
                    except:
                        traceback.print_exc()

    def createAOTransparencyLayer(self,isAddPass):
        selObj = getGeometrySelection()
        
        self.CURRENT_LAYER = self.createNewMRLayer()
        
        shaderNoDis,shaderNoDisSG = createShader('surfaceShader',(self.LAYER_NAME+'_MAT'))
        
        AONode = pm.createNode('mib_fg_occlusion')
            
        AONode.outValue.connect(shaderNoDis.outColor)
        
        if selObj :
            for each in selObj :
                nodeType = type(each)
                logging.debug(str(nodeType))
                
                # Get dispalcement shader if input is geometry
                logging.debug('****'+str(each))
                eachSn = each.getParent()
                
                # Check shape has displacement shader or not
                shapeFaces = getTransparencyShader(each)
                
                # First assign no displacement shader to all
                logging.debug('First assign no displacement shader to all' )
                pm.select(each,r=1)
                pm.sets(shaderNoDisSG,e=1,forceElement=1)   
                                                
                for shapeFace in shapeFaces :
                    for k,v in shapeFace.items() :
                        # Have displacement shader
                        if v[0] :
                            # Have not transparency shader
                            if not v[1] :
                                shader,shaderSG = createShader('surfaceShader',(self.LAYER_NAME+'_MAT'))
                                v[0].connect(shaderSG.displacementShader)
                                AONode.outValue.connect(shader.outColor)
                                
                                pm.select(k,r=1)
                                pm.sets(shaderSG,e=1,forceElement=1)
                            # Have transparency texture
                            else :
                                shader,shaderSG = createShader('surfaceShader',(self.LAYER_NAME+'_MAT'))
                                v[0].connect(shaderSG.displacementShader)
                                AONode.outValue.connect(shader.outColor)
                                
                                tranNode = pm.createNode('mib_transparency')
                                v[1].outColor.connect( tranNode.transp )    
                                v[1].outAlpha.connect( tranNode.transpA )
                                tranNode.outValue.connect( shaderSG.miMaterialShader, f=1 )
                                AONode.outValue.connect( tranNode.input )    
                                AONode.outValueA.connect( tranNode.inputA )
                                
                                pm.select(k,r=1)
                                pm.sets(shaderSG,e=1,forceElement=1)                                
                        
                        else :
                            # Have not transparency texture
                            if not v[1] :
                                pass
                            # Have transparency texture
                            else :
                                shader,shaderSG = createShader('surfaceShader',(self.LAYER_NAME+'_MAT'))
                                AONode.outValue.connect(shader.outColor)
                                
                                tranNode = pm.createNode('mib_transparency')
                                v[1].outColor.connect( tranNode.transp )    
                                v[1].outAlpha.connect( tranNode.transpA )
                                AONode.outValue.connect( tranNode.input )    
                                AONode.outValueA.connect( tranNode.inputA )
                                tranNode.outValue.connect( shaderSG.miMaterialShader, f=1 )
                                
                                pm.select(k,r=1)
                                pm.sets(shaderSG,e=1,forceElement=1)

                pm.select(each)
                logging.debug('each: '+str(each))
                eachSn = pm.pickWalk(d='down')
                logging.debug('eachSn: '+str(eachSn[0]))
                if eachSn[0] != each :
                    pm.editRenderLayerMembers(self.CURRENT_LAYER,eachSn[0],remove=1)

        # Adjust render layer attr
        self.setRenderLayerAttr(MI_DEFAULT_OPTIONS.finalGather, 1)
        self.setRenderLayerAttr(MI_DEFAULT_OPTIONS.caustics, 0)
        self.setRenderLayerAttr(MI_DEFAULT_OPTIONS.globalIllum, 0)
        self.setRenderLayerAttr(MI_DEFAULT_FRAME_BUFFER.datatype, 2)
        self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.imageFormat, 7)
        self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.imfPluginKey, 'iff')
        self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.multiCamNamingMode, 1)
        self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.bufferName, '<RenderPass>')

        # Remove cam lens and env shader            
        self.disConnectCamShader()
        
        if isAddPass == True :
            # Add ao pass
            self.createPass2CurrentLayer('ambientOcclusion')
            
        pm.select(cl=1)


  
    def createAOLayer(self,isAddPass):
        selObj = getGeometrySelection()
        
        self.CURRENT_LAYER = self.createNewMRLayer()
        
        #AOMat = pm.shadingNode('surfaceShader',n='AO_mat',asShader=True)
        shaderNoDis,shaderNoDisSG = createShader('surfaceShader',(self.LAYER_NAME+'_MAT'))
        
        AONode = pm.createNode('mib_amb_occlusion')
        AONode.outValue.connect(shaderNoDis.outColor)
        AONode.samples.set(64)
        
        if selObj :
            for each in selObj :
                nodeType = type(each)
                logging.debug(str(nodeType))
                
                # Get dispalcement shader if input is geometry
                logging.debug('****'+str(each))
                eachSn = each.getParent()
                
                # Check shape has displacement shader or not
                displacementShaders, shapeFaces = getDisplacementShader2(each)
                
                # First assign no displacement shader to all
                logging.debug('First assign no displacement shader to all' )
                pm.select(each,r=1)
                pm.sets(shaderNoDisSG,e=1,forceElement=1)
                    
                # If shape has displacement shader,then assign displacement shader again    
                if displacementShaders != [] :
                    logging.debug('each: ' + str(each))
                    for displacementShader,shapeFace in zip(displacementShaders,shapeFaces) :
                        shader,shaderSG = createShader('surfaceShader',(self.LAYER_NAME+'_'+str(eachSn)+'_MAT'))
                        displacementShader.connect(shaderSG.displacementShader)
                        AONode = pm.createNode('mib_amb_occlusion')
                        AONode.outValue.connect(shader.outColor)
                        AONode.samples.set(64)
                                
                        pm.select(shapeFace,r=1)
                        pm.sets(shaderSG,e=1,forceElement=1)                        

                pm.select(each)
                logging.debug('each: '+str(each))
                eachSn = pm.pickWalk(d='down')
                logging.debug('eachSn: '+str(eachSn[0]))
                if eachSn[0] != each :
                    pm.editRenderLayerMembers(self.CURRENT_LAYER,eachSn[0],remove=1)

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
        logging.debug('isAddPass:'+str(isAddPass))
        if isAddPass == True :
            # Add ao pass
            self.createPass2CurrentLayer('ambientOcclusion')
                    
        pm.select(cl=1)
        
    def createColorPasses(self):
        for p in self.PASSES_COLOR :
            self.createPass2CurrentLayer(p)
            
    def createColorLayer(self):
        selObj = getDAGSelection()
        if selObj :
            self.CURRENT_LAYER = self.createNewMRLayer()
            self.createColorPasses()  
            self.setRenderLayerAttr(MI_DEFAULT_FRAME_BUFFER.datatype, 5)
            self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.imageFormat, 51)
            self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.imfPluginKey, 'exr')
            self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.multiCamNamingMode, 1)
            self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.bufferName, '<RenderPass>')
            self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.imageFilePrefix, 'images/<Scene>/<RenderLayer>/<RenderLayer>')

            pm.select(cl=1)
            
    def createShadowLayer(self,layerName='Shadow_Mask_Layer',shaderName='Shadow_Mask_MAT',outAlpha=1):
        sel = getGeometrySelection()
        newLayer = self.createNewMRLayer()
        # Create material
        MRMaterial().createShadowShader(shaderName,sel,outAlpha)
        pm.select(cl=1)

    def createLightLayer(self,name,color):
        selObj = getGeometrySelection()
        selLight = getLightSelection()
        if selObj == None :
            logging.warning('select some lights and some objects first.')
            return None
        elif selLight == None :
            logging.warning('select some lights and some objects first.')
            return None
        else :
            newLayer = self.createNewMRLayer(name)
            
#            luzMat = pm.shadingNode('lambert',n=(name+'_MAT'),asShader=True)
            shaderNoDis,shaderNoDisSG = createShader('lambert',(name+'_MAT'))
            shaderNoDis.diffuse.set(1)
            # For Key ligt assign green color
            MI_DEFAULT_OPTIONS.rayTracing.set(1)
        
            for each in selObj :
                nodeType = type(each)
                logging.debug(str(nodeType))
                
                # Get dispalcement shader if input is geometry
                eachSn = each.getParent()
                
                # Check shape has displacement shader or not
                displacementShaders, shapeFaces = getDisplacementShader2(each)
                
                # First assign no displacement shader to all
                logging.debug('First assign no displacement shader to all' )
                pm.select(each,r=1)
                pm.sets(shaderNoDisSG,e=1,forceElement=1)
                
                # If shape has displacement shader,then assign displacement shader again    
                if displacementShaders != [] :
                    logging.debug('each: ' + str(each))
                    for displacementShader,shapeFace in zip(displacementShaders,shapeFaces) :
                        logging.debug('has displaceMentShader' )
                        logging.debug('displaceMentShader: ' + str(displacementShader))
                        logging.debug('shapeFace: ' + str(shapeFace))
                        shader,shaderSG = createShader('lambert',(newLayer+'_'+str(eachSn)+'_MAT'))
                        shader.diffuse.set(1)
                        displacementShader.connect(shaderSG.displacementShader)
                            
                        pm.select(shapeFace,r=1)
                        pm.sets(shaderSG,e=1,forceElement=1)
                        
                pm.select(each,r=1)
                logging.debug('each: '+str(each))
                eachSn = pm.pickWalk(d='down')
                logging.debug('eachSn: '+str(eachSn[0]))
                if eachSn[0] != each :
                    pm.editRenderLayerMembers(newLayer,eachSn[0],remove=1)

            for light in selLight :
                self.setRenderLayerAttr(light.intensity, 5)
                self.setRenderLayerAttr(light.color, color)
                self.setRenderLayerAttr(light.shadowColor, [0,0,1])
                if each.hasAttr( 'lightAngle' ):
                    self.setRenderLayerAttr(light.lightAngle, 5)
                self.setRenderLayerAttr(light.useRayTraceShadows, 1)
                self.setRenderLayerAttr(light.shadowRays, 20)

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
            
            return True


class MRMaterial():
    def __init__(self):
        logging.debug('Init MRMaterial class')
        
    # Get shadingSG by shader name
    # Return type is string
    def getShadingSG(self,shaderName):
        try :
            shaderNoDisSG = PyNode(shaderName).outColor.connections(d=1,p=0,sh=1)
            shaderNoDisSG = shaderNoDisSG.longName()
            logging.debug('get shadingSG:' + str(shaderNoDisSG))
        except :
            logging.debug('can not get shadingSG')
            shaderNoDisSG = pm.sets(renderable=True,noSurfaceShader=True,\
                                    empty=True,name=(shaderName+'_SG'))
            PyNode(shaderName).outColor.connect(shaderNoDisSG.surfaceShader)
            
        return shaderNoDisSG
    
    # Create and assign black shader
    # createShader([0,0,0],[1,1,1],'BLACK')
    def createShader(self,outColor,outAlpha,shaderName):
        selObj = getGeometrySelection()
        shaderNoDis= None
        shaderNoDisSG = None
        shader = None
        shaderSG = None
        if selObj :
            for each in selObj :
                # Get dispalcement shader if input is geometry
                eachSn = each.getParent()
                
                # Check shape has displacement shader or not
                displacementShaders, shapeFaces = getDisplacementShader2(each)
                
                if not pm.objExists(shaderName) :
                    shaderNoDis,shaderNoDisSG = createShader('surfaceShader', shaderName)
                    shaderNoDis.outColor.set(outColor)
                    shaderNoDis.outMatteOpacity.set(outAlpha)
                else :
                    # Get shaderSG by shader name
                    if not shaderNoDisSG :
                        shaderNoDisSG = self.getShadingSG(shaderName)
                        
                logging.debug('shaderNoDisSG: ' + str(shaderNoDisSG))
                    
                # First assign no displacement shader to all
                logging.debug('First assign no displacement shader to all' )
                pm.select(each,r=1)
                pm.sets(shaderNoDisSG,e=1,forceElement=1)
                    
                # If shape has displacement shader,then assign displacement shader again    
                if displacementShaders != [] :
                    shaderNameWithDisp = shaderName + "_" + eachSn 
                    for displacementShader,shapeFace in zip(displacementShaders,shapeFaces) :
                        if pm.objExists(shaderNameWithDisp) :
                            # Get shadingSG
                            shaderSG = self.getShadingSG(shaderNameWithDisp)
                            logging.debug('shaderSG exists with shaderNameWithDisp: ' + str(shaderSG))
                        else :
                            shader,shaderSG = createShader('surfaceShader', shaderNameWithDisp)
                            shader.outColor.set(outColor)
                            shader.outMatteOpacity.set(outAlpha)
                            logging.debug('shaderSG exists with no shaderNameWithDisp: ' + str(shaderSG))
                        
                        displacementShader.connect(shaderSG.displacementShader)
                        pm.select(shapeFace,r=1)
                        pm.sets(shaderSG,e=1,forceElement=1)    
        pm.select(cl=1)
        
    # Create and assign black shader
    def createShadowShader(self,shaderName='Shadow_Mask_MAT',sel=None,outAlpha=1):
        selObj = sel
        if not selObj:
            selObj = getGeometrySelection()
        logging.debug('createShadowShader: ' + str(selObj))
        shaderNoDis= None
        shaderNoDisSG = None
        shader = None
        shaderSG = None
        if selObj :
            for each in selObj :
                logging.debug('each: ' + str(each))
                # Get dispalcement shader if input is geometry
                eachSn = each.getParent()
                
                # Check shape has displacement shader or not
                displacementShaders, shapeFaces = getDisplacementShader2(each)
                
                if not pm.objExists(shaderName) :
                    shaderNoDis,shaderNoDisSG = createShader('useBackground', shaderName)
                    shaderNoDis.specularColor.set([0,0,0])
                    shaderNoDis.reflectivity.set(0)
                    shaderNoDis.reflectionLimit.set(0)
                    shaderNoDis.matteOpacity.set(outAlpha)
                else :
                    # Get shaderSG by shader name
                    if not shaderNoDisSG :
                        shaderNoDisSG = self.getShadingSG(shaderName)
                        
                logging.debug('shaderNoDisSG: ' + str(shaderNoDisSG))
                    
                # First assign no displacement shader to all
                logging.debug('First assign no displacement shader to all' )
                pm.select(each,r=1)
                pm.sets(shaderNoDisSG,e=1,forceElement=1)
                    
                # If shape has displacement shader,then assign displacement shader again    
                if displacementShaders != [] :
                    logging.debug('each: ' + str(each))
                    shaderNameWithDisp = shaderName + "_" + eachSn
                    for displacementShader,shapeFace in zip(displacementShaders,shapeFaces) :
                        if pm.objExists(shaderNameWithDisp) :
                            # Get shadingSG
                            shaderSG = self.getShadingSG(shaderNameWithDisp)
                        else :
                            shader,shaderSG = createShader('useBackground', shaderNameWithDisp)
                            shader.specularColor.set([0,0,0])
                            shader.reflectivity.set(0)
                            shader.reflectionLimit.set(0)
                            shader.matteOpacity.set(outAlpha)
                        
                        displacementShader.connect(shaderSG.displacementShader)
                        pm.select(shapeFace,r=1)
                        pm.sets(shaderSG,e=1,forceElement=1)
        pm.select(cl=1)

    #Z-DEPTH
    def createZDepthNetwork(self,shaderName):
        shader,shaderSG = createShader('surfaceShader', shaderName)
                        
        zDepthRange = pm.shadingNode('setRange',n='Z_Depth_setRange',asUtility=1)
        zDepthRange.outValueX.connect(shader.outColorR,f=1)
        zDepthRange.outValueX.connect(shader.outColorG,f=1)
        zDepthRange.outValueX.connect(shader.outColorB,f=1)
        zDepthRange.minX.set(0)
        zDepthRange.maxX.set(1)
                        
        zDepthMultiDiv = pm.shadingNode('multiplyDivide',n='Z_Depth_multiplyDivide',asUtility=1)
        zDepthMultiDiv.input2X.set(-1)
        zDepthMultiDiv.outputX.connect(zDepthRange.valueX,f=1)
        
        zDepthSampInfo = pm.shadingNode('samplerInfo',n='Z_Depth_samplerInfo',asUtility=1)
        
        zDepthSampInfo.addAttr('cameraNearClipPlane1',at='double',dv=0.1)
        zDepthSampInfo.cameraNearClipPlane1.set(k=1)
        
        zDepthSampInfo.addAttr('cameraFarClipPlane1',at='double',dv=100)
        zDepthSampInfo.cameraFarClipPlane1.set(k=1)

        zDepthSampInfo.pointCameraZ.connect(zDepthMultiDiv.input1X)
        zDepthSampInfo.cameraNearClipPlane1.connect(zDepthRange.oldMinX)
        zDepthSampInfo.cameraFarClipPlane1.connect(zDepthRange.oldMaxX)
        
        return (shader,shaderSG)
                        
    def createZDepthShader(self,shaderName='Z_Depth_MAT'):
        selObj = getGeometrySelection()
        shaderNoDis= None
        shaderNoDisSG = None
        shader = None
        shaderSG = None
        if selObj :
            for each in selObj :
                # Get dispalcement shader if input is geometry
                eachSn = each.getParent()
                               
                # Check shape has displacement shader or not
                displacementShaders, shapeFaces = getDisplacementShader2(each)
                
                if not pm.objExists(shaderName) :
                    shaderNoDis,shaderNoDisSG = self.createZDepthNetwork(shaderName)
                else :
                    # Get shaderSG by shader name
                    if not shaderNoDisSG :
                        shaderNoDisSG = self.getShadingSG(shaderName)
                        
                logging.debug('shaderNoDisSG: ' + str(shaderNoDisSG))
                    
                # First assign no displacement shader to all
                logging.debug('First assign no displacement shader to all' )
                pm.select(each,r=1)
                pm.sets(shaderNoDisSG,e=1,forceElement=1)
                    
                # If shape has displacement shader,then assign displacement shader again    
                if displacementShaders != [] :
                    for displacementShader,shapeFace in zip(displacementShaders,shapeFaces) :
                        shaderNameWithDisp = shaderName + "_" + eachSn 
                        if pm.objExists(shaderNameWithDisp) :
                            # Get shadingSG
                            shaderSG = self.getShadingSG(shaderNameWithDisp)
                        else :
                            shader,shaderSG = self.createZDepthNetwork(shaderNameWithDisp)
                        
                        displacementShader.connect(shaderSG.displacementShader)
                        pm.select(shapeFace,r=1)
                        pm.sets(shaderSG,e=1,forceElement=1)
        pm.select(cl=1)

class MRRenderSubSet():
    def __init__(self):
        logging.debug('Init MRRenderSubSet class')     
        
    def createRenderSubSet(self,subSetName):
        selObj = getGeometrySelection()
#string $subsetShader=`mrCreateCustomNode -asUtility "" mip_render_subset`;
        subSetShader = pm.createNode('mip_render_subset',asUtility=1)
                                                                    
#MRRenderLayerPass()
#MRRenderLayerPass().createAOLayer()
#MRRenderLayerPass().createShadowLayer()
#MRRenderLayerPass().createColorLayer('color')
#MRMaterial().createShadowShader()
#MRMaterial().createZDepthShader()
#MRRenderLayerPass().createLightLayer('test',[0,1,0])
#MRRenderLayerPass().createColorLayer()

#if __name__ == "__main__":
#    loadMRPlugin()
#    setRendererToMR()
