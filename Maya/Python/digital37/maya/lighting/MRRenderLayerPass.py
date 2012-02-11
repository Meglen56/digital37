# -*- coding: utf-8 -*- 
#Description:
#Author:honglou(hongloull@gmail.com)
#Create:2011.12.06
#Update: 2012.02.01
#Howto use : 
import logging 
import traceback
import itertools
import os
import pymel.core as pm
from pymel.all import mel
from pymel.core.general import PyNode
import digital37.XmlParser as XmlParser
reload(XmlParser)

class MRRenderLayerPass(object):
    TYPE_LIST = type([])
#    TYPE_STR = type('')
    TYPE_DICT = type({})
    TYPE_SET = type(set())

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
    PASSES_COLOR = ['beauty','depth','diffuse','incandescence','indirect','normalWorld',\
                    'reflection','refraction','shadow','specular']
    LAYER_PRESET = ['Normal','AO','AO_Transparency','Shadow']
    LAYER_NAME_DEFAULT = 'layer'
    MODEL = ['Manager Render Layer','Create Render Layer']
    
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
    
    # Get some global var
    MAYA_LOCATION = mel.getenv('MAYA_LOCATION')
    MI_DEFAULT_OPTIONS = None
    MI_DEFAULT_FRAME_BUFFER = None
    MENTAL_RAY_ITEMS_LIST = None
    MENTAL_RAY_GLOBALS = None
    USER_DIR = None
                
    def __init__(self,debug=True):
        self.DEBUG = debug
        logging.debug('Init MRRenderLayerPass class')

        self.PASSES_COLOR_AVAILABLE = [ x for x in self.PASSES_ALL if x not in self.PASSES_COLOR ]
        self.PASSES_SCENE = []
        self.PASSES_AVAILABLE = []
        self.LAYER_NAME = 'color'
        self.PREFIX_PASS = ''
        self.SUFFIX_PASS = ''
        self.LAYER_CURRENT = None
        self.LAYERS_MANAGER_SELECTED = []
        self.LAYERS_CREATION_SELECTED = []
        self.LAYERS = []
        self.LAYER_MANAGER_ACTIVE = None
        # For create mode
        self.LAYER_CREATION_ACTIVE = None 
        self.LAYER_BEFORE_RENAME = None
        self.LAYER_CREATION = {}
        self.LAYER_SCENE_ACTIVE = None
        
        self.loadMRPlugin()
        self.initMentalRay()
        self.getLayers()
        
    def setLog(self,logLevel):
        LOG_LEVELS = {'debug': logging.DEBUG, 'info':logging.INFO, \
                  'warning': logging.WARNING, 'error': logging.ERROR,\
                  'critical': logging.CRITICAL}
        LOG_LEVEL = LOG_LEVELS.get(logLevel)
        logging.basicConfig(level=LOG_LEVEL)
                
    def setAttr(self,attr,val):
        # Check if attr exists
        logging.debug('attr: %s',attr)
        if pm.objExists(attr) :
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
    
    def log_dict(self,inputDict):
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
    
    def log_list(self,inputList):
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
                
    def rename(self,node,name):
        try:
            pm.rename(node,name)
        except:
            traceback.print_exc()
        
    def select_obj(self,input_set):
        pm.select(list(input_set),r=True)
        
    def getSelection(self):
        logging.debug('MRRenderLayerPass getSelection')
        selObjShort = pm.ls(sl=1,l=1)
        if not selObjShort :
            logging.warning('select some objects first.')
            return None
        else :
            return selObjShort
        
    def get_selection_names(self):
        sel = pm.ls(sl=1,l=1)
        if not sel :
            logging.warning('select some objects first.')
            return set()
        else :
            return set( itertools.imap(lambda x:x.longName(), sel ) )
    
    def getSelection_dict(self):
        logging.debug('MRRenderLayerPass getSelection_dict')
        sels = pm.ls(sl=1,l=1)
        if not sels :
            logging.warning('select some objects first.')
            return None
        else :
            sels_dict = {}
            for sel in sels :
                sels_dict[ sel.longName() ] = sel
            return sels_dict
            
    def getDAGSelection(self):
        logging.debug('MRRenderLayerPass getDAGSelection')
        selObjShort = pm.ls(sl=1)
        selObj = pm.ls(sl=1,dag=1)
        if not selObjShort :
            logging.warning('select some objects first.')
            return None
        else :
            return selObj
    
    def getShapeSelection(self,sels):
        logging.debug('MRRenderLayerPass get geometry Selection')
        selObj = pm.ls(sels,dag=1,lf=1,type=['mesh','nurbsSurface','subdiv'])
        if not selObj :
            logging.warning('select some objects first.')
            return None
        else :
            return selObj
            
    def getGeometrySelection(self):
        logging.debug('MRRenderLayerPass get geometry Selection')
        selObj = pm.ls(sl=1,dag=1,lf=1,type=['mesh','nurbsSurface','subdiv'])
        if not selObj :
            logging.warning('select some objects first.')
            return None
        else :
            return selObj
        
    def getLightSelection(self):
        logging.debug('MRRenderLayerPass getDAGSelection')
        selObj = pm.ls(sl=1,dag=1,lf=1,type=['spotLight','directionalLight',\
                                             'volumeLight','areaLight','ambientLight','pointLight'])
        if not selObj :
            logging.warning('select some objects first.')
            return None
        else :
            return selObj
        
    def getLightInScene(self):
        light_set = set()
        light_set.update( pm.ls(l=1,dag=1,lf=1,\
                                type=['spotLight','directionalLight',\
                                      'volumeLight','areaLight','ambientLight','pointLight']) )
        if self.DEBUG :
            print light_set
        return set(l.getParent().longName() for l in light_set if light_set)

    def getLightInSelection(self):
        light_set = set()
        light_set.update( pm.ls(sl=1,l=1,dag=1,lf=1,\
                                type=['spotLight','directionalLight',\
                                      'volumeLight','areaLight','ambientLight','pointLight']) )
        if self.DEBUG :
            print light_set
        return set(l.getParent().longName() for l in light_set if light_set)
            
    # Flatten list with set
    def flattenList(self,inputs):
        for i in inputs :
            if inputs.count(i) != 1 :
                inputs.remove(i)
        return inputs
                                             
        

    
    # Load mental ray plugin first, else can not made some global var      
    def loadMRPlugin(self):
        #Check MR plugin load or not
        if not pm.pluginInfo( 'Mayatomr', query=True, loaded=True ) :
            logging.warning('Maya to MentalRay Plugin has not been loaded.Loading Mayatomr now.')
            pm.loadPlugin( 'Mayatomr' )
            
    # Let maya make some mr attr
    def setRendererToMR(self): 
        renderer = self.DEFAULT_RENDER_GLOBALS.currentRenderer.get()
        logging.debug('current renderer: %s',renderer)
        if renderer != 'mentalRay' :
            self.DEFAULT_RENDER_GLOBALS.currentRenderer.set('mentalRay')
            
    def initMentalRay(self):
        try:
            PyNode('defaultRenderGlobals')
        except:
            logging.warning('Get defaultRenderGlobals error.')
            pm.createNode('defaultRenderGlobals')
        self.DEFAULT_RENDER_GLOBALS = PyNode('defaultRenderGlobals')
        
        try:
            PyNode('mentalrayGlobals')
        except:
            logging.warning('Get mentalrayGlobals error.')
            try:
                mel.eval('miCreateDefaultNodes')
            except:
                traceback.print_exc()
        self.MENTAL_RAY_GLOBALS = PyNode('mentalrayGlobals')
                
        try:
            PyNode('miDefaultOptions')
        except:
            logging.warning('Get miDefaultOptions error.')
            try:
                mel.eval('miCreateDefaultNodes')
            except:
                traceback.print_exc()
        self.MI_DEFAULT_OPTIONS = PyNode('miDefaultOptions')
            
        try:
            PyNode('miDefaultFramebuffer')
        except:
            logging.warning('Get miDefaultFramebuffer error.')
            try:
                mel.eval('miCreateDefaultNodes')
            except:
                traceback.print_exc()
        self.MI_DEFAULT_FRAME_BUFFER = PyNode('miDefaultFramebuffer')
        
        try:
            PyNode('mentalrayItemsList')
        except:
            logging.warning('Get mentalrayItemsList error.')
            try:
                mel.eval('miCreateDefaultNodes')
            except:
                traceback.print_exc()
        self.MENTAL_RAY_ITEMS_LIST = PyNode('mentalrayItemsList')
        
        # Connect attributes
        self.setRendererToMR()
        #=======================================================================
        # if not self.MENTAL_RAY_GLOBALS.options in self.MI_DEFAULT_OPTIONS.message.listConnections(d=1,p=1) :
        #    try:
        #        self.MI_DEFAULT_OPTIONS.message.connect( self.MENTAL_RAY_GLOBALS.options )
        #    except:
        #        traceback.print_exc()
        # 
        # if not self.MENTAL_RAY_GLOBALS.framebuffer in self.MI_DEFAULT_FRAME_BUFFER.message.listConnections(d=1,p=1) :
        #    try:
        #        self.MI_DEFAULT_FRAME_BUFFER.message.connect( self.MENTAL_RAY_GLOBALS.framebuffer )
        #    except:
        #        traceback.print_exc()
        #  
        # if not self.MENTAL_RAY_ITEMS_LIST.globals in self.MENTAL_RAY_GLOBALS.message.listConnections(d=1,p=1) :  
        #    try:
        #        self.MENTAL_RAY_GLOBALS.message.connect( self.MENTAL_RAY_ITEMS_LIST.globals )
        #    except:
        #        traceback.print_exc()
        #=======================================================================

    def setRenderStatus(self,renderStatus, layerOverride = False):
        logging.debug('setRenderStatus')
        sels = self.getGeometrySelection()
        if sels :
            for sel in sels :
                for k,v in renderStatus.iteritems() :
                    attr = PyNode(sel.longName()+'.'+k)
                    if layerOverride :
                        try:
                            pm.editRenderLayerAdjustment( attr )
                        except:
                            traceback.print_exc()
                    # set attr after layer overrides
                    try:
                        attr.set( v[1] )
                    except:
                        logging.debug('set attr error:')
                        logging.debug('attr:%s',attr)
                        traceback.print_exc()
    
    def createShader(self,shaderType,shaderName):
        surfaceShader = pm.shadingNode(shaderType,n=shaderName,asShader=True)
        shadingSG = pm.sets(renderable=True,noSurfaceShader=True,empty=True,name=(shaderName+'_SG'))
        surfaceShader.outColor.connect(shadingSG.surfaceShader)
        return ( surfaceShader, shadingSG )
                      
    def getActiveLayer(self):
        self.LAYER_MANAGER_ACTIVE = None
        if len(self.LAYERS_MANAGER_SELECTED) >= 1 :
            self.LAYER_MANAGER_ACTIVE = self.LAYERS_MANAGER_SELECTED[-1]
        self.LAYER_CREATION_ACTIVE = None
        if len(self.LAYERS_CREATION_SELECTED) >= 1 :
            self.LAYER_CREATION_ACTIVE = self.LAYERS_CREATION_SELECTED[-1]
                                  
    # Get LAYER_SCENE_ACTIVE
    def getCurrentLayer(self):
        #mel:editRenderLayerGlobals -q -crl
        layer = pm.editRenderLayerGlobals(q=1,crl=1)
        if layer:
            try:
                self.LAYER_SCENE_ACTIVE = PyNode(layer)
            except:
                traceback.print_exc()
        
    # Get current active layer
    def get_layer_current(self):
        layer_current = pm.editRenderLayerGlobals(q=1,crl=1)
        if layer_current :
            return PyNode(layer_current)
        else :
            return None
        
    def getNameByNode(self,inputObjList):
        if type(inputObjList) == self.TYPE_LIST :
            names_list = []
            for l in inputObjList :
                try:
                    name = l.longName()
                except:
                    traceback.print_exc()
                else:
                    names_list.append( name )
            return names_list
        elif type(inputObjList) == type('') or str( type(inputObjList) ) == self.PASS_TYPE :
            name = None
            try:
                name = inputObjList.name()
            except:
                traceback.print_exc()
            return name
        else:
            logging.debug('%s', type(inputObjList))
            
            logging.error('getNameByNode:input obj type is wrong')
            return None
            
    def getNodeByName(self,inputNameList):
        if type(inputNameList) == self.TYPE_LIST :
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
    
    def getDisplacementShader2(self,inputs):
        displacementShaders = []
        shapeFaces = []
        
        connectionAll = self.flattenList( inputs.connections(d=1) )
        logging.debug('inputs: %s',inputs)
        logging.debug('connectionAll: %s',connectionAll)
        for connection in connectionAll :
            if str( type(connection) ) == self.SHADING_ENGINE_TYPE :
                dispConnections = connection.displacementShader.connections(p=1,d=1)
                if len(dispConnections) >= 1 :
                    
                    logging.debug('displacement shader: %s',dispConnections[0])
                    #Get ShadingSG's set member
                    members = pm.sets(connection, q=1 )
                    #Get shape's faces in shadingSG'set
                    shape = None
                    shapeFace = []
                    for m in members :
                        logging.debug('members: %s',m)
                        # For pCubeShape1.f[0:1]
                        m = str(m)
                        if '.' in m :
                            #shape,face = m.split('.')
                            shape = m.split('.')[0]
                            logging.debug('shape: %s' ,shape)
                            logging.debug('inputs: %s',inputs)
                            if shape == str(inputs) :
                                shapeFace.append( m )
                        # For pCubeShape1
                        else :
                            if m == str(inputs) :
                                shapeFace.append( m )
                    
                    if shapeFace != [] :
                        shapeFaces.append(shapeFace)
                        displacementShaders.append( dispConnections[0] )
                        
        logging.debug('---------getDisplacementShader Start------------')
        logging.debug('inputs: %s' ,inputs)
        for displacementShader,shapeFace in zip(displacementShaders,shapeFaces) :
            logging.debug('displacementShader: %s',displacementShader)
            logging.debug('shapeFace: %s',shapeFace)
        logging.debug('---------getDisplacementShader Finish------------\n')
        return (displacementShaders, shapeFaces)


    def getTransparencyShader(self,inputs):
        shapeFaces = []
        transparencyConnections = None
        connectionAll = self.flattenList( inputs.connections(d=1) )
        logging.debug('inputs: %s',inputs)
        logging.debug('connectionAll: %s',connectionAll)
        for connection in connectionAll :
            if str( type(connection) ) == self.SHADING_ENGINE_TYPE :
                transparency = None
                displacement = None
                dispConnections = connection.displacementShader.connections(p=1,d=1)
                # Get transparency's inputs connection
                try :
                    PyNode(connection.surfaceShader)
                except :
                    logging.error(str(inputs) + ' has no surface shader\'s connection')
                else :
                    try :
                        surfaceShader = connection.surfaceShader.connections(p=0,d=1)
                    except :
                        logging.error(str(inputs) + ' ' + str(PyNode(connection.surfaceShader).longName()) \
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
                        for m in members :
                            logging.debug('members: %s', m)
                            # For pCubeShape1.f[0:1]
                            m = str(m)
                            if '.' in m :
                                #shape,face = m.split('.')
                                shape = m.split('.')[0]
                                logging.debug('shape: %s',shape)
                                logging.debug('inputs: %s',inputs)
                                if shape == str(inputs) :
                                    shapeFace.append( m )
                            # For pCubeShape1
                            else :
                                if m == str(inputs) :
                                    shapeFace.append( m )
                                
                        # Have displacement shader
                        if len(dispConnections) >= 1 :                
                            displacement = dispConnections[0] 
            
                        if len(transparencyConnections) >= 1 :
                            transparency = transparencyConnections[0]                
                            
                        if shapeFace != [] :
                            logging.debug( 'shapeFace:')
                            self.log_list(shapeFace)
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
        logging.debug('inputs: %s' ,inputs)
        for i in range( len(shapeFaces) ) :
            for k,v in shapeFaces[i].items() :
                logging.debug('shapeFace: %s',k)
                logging.debug('displacementShader: %s',v[0])
                logging.debug('transparency: %s',v[1])
        logging.debug('---------getTransparencyShader Finish------------\n')
        return shapeFaces
            
    def getLayers(self):
        self.LAYERS = []
        selObj = pm.ls(type='renderLayer')
        if selObj :
            selObj.remove(PyNode('defaultRenderLayer'))
            self.log_list(selObj)
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
        self.log_list(self.PASSES_SCENE)

    def getAvailablePasses(self):
        self.PASSES_AVAILABLE = []
        self.getScenePasses()
                
        if self.PASSES_SCENE :
            pNames = ( k for k in self.PASSES_ALL if k not in self.PASSES_SCENE )
            for pn in pNames :
                self.PASSES_AVAILABLE.append( pn )
        # If scene has no pass
        else :
            #for pn in PASSES_ALL.keys() :
            for pn in self.PASSES_ALL :
                self.PASSES_AVAILABLE.append( pn )
                        
    def getObjInLayer(self,layer):
        obj_names_list = pm.editRenderLayerMembers(layer,q=1,fullNames=1)
        return obj_names_list
    
    # Return set
    def get_obj_in_layer(self,layer):
        return set( pm.editRenderLayerMembers(layer,q=1,fullNames=1) )
      
    def get_light_in_layer(self,layer):
        obj_in_layer = pm.editRenderLayerMembers(layer,q=1,fullNames=1)
        if obj_in_layer: 
            light_set = self.getLightInScene()
            if light_set:
                return set( obj_in_layer ) & light_set
            else:
                return set( obj_in_layer ) 
        else:
            return None
            
    def get_creation_layer_attr(self,layer,attr):
        returnValue = layer_dict = None
        logging.debug('%s ',self.LAYER_CREATION)
        if self.DEBUG:
            print self.LAYER_CREATION
        if self.LAYER_CREATION.has_key(layer):
            if self.DEBUG:
                print 'layer:',
                print layer
            layer_dict = self.LAYER_CREATION.get(layer)
            if self.DEBUG:
                print 'layer_dict:',
                print layer_dict
            if layer_dict.has_key(attr):
                returnValue = layer_dict.get(attr)
                if self.DEBUG:
                    print 'returnValue:',
                    print returnValue
        else:
            logging.debug('get creation layer attr error:')
        return returnValue

    def get_creation_layer_attrs(self,layer):
        layer_dict = None
        logging.debug('%s ',self.LAYER_CREATION)
        if self.DEBUG:
            print self.LAYER_CREATION
        if self.LAYER_CREATION.has_key(layer):
            if self.DEBUG:
                print 'layer:',
                print layer
            layer_dict = self.LAYER_CREATION.get(layer)
            # Remove empty can not use iter
            for k,v in layer_dict.items() :
                if not v:
                    layer_dict.pop(k)
            if self.DEBUG:
                print 'layer_dict:',
                print layer_dict
        else:
            logging.debug('get creation layer attr error:')
        return layer_dict
    
    def create_user_settings_dir(self):
        # get user home dir
        MRRenderLayerPass.USER_DIR = os.path.expanduser('~') + '/RenderLayerManager/' 
        if not os.path.exists(  MRRenderLayerPass.USER_DIR ):
            os.makedirs( MRRenderLayerPass.USER_DIR )
    
    def writeFile(self,fileName,content):
        f = None
        try:
            f = open(fileName,'w')
        except IOError:
            logging.error('save error...',('Could not save to '+fileName) )
        else:
            f.write(content)
            f.close()
        
    def save_creation_layer_preset(self,presetName,layer):
        #layer_preset = self.get_creation_layer_attr(layer,'PRESET')
        layer_dict = self.get_creation_layer_attrs(layer)
        # convert set value to string value 
        for k,v in layer_dict.items() :
            if not v:
                layer_dict.pop(k)
            else:
                if type(v) == self.TYPE_SET :
                    layer_dict[k] = '***'.join(v)
        if layer_dict:
            # convert dict to xml
            xmlContent = XmlParser.MakeXml().createElements(layer,\
                                                            layer_dict)
            if self.DEBUG :
                print xmlContent
            # save xml to file
            self.create_user_settings_dir()
            fileName = MRRenderLayerPass.USER_DIR+presetName+'.lps'
            if self.DEBUG :
                print fileName
            self.writeFile( fileName, xmlContent)
        
    def add_obj_to_layers(self,layers,obj_names_list):
        for layer in layers :
            self.add_obj_to_layer(layer, obj_names_list)
        
    def add_obj_to_layer(self,layer,obj_names_list):
        #editRenderLayerMembers -noRecurse layer2 nurbsSphere2
        if layer and obj_names_list :
            if type(obj_names_list) == self.TYPE_SET :
                obj_names_list = list(obj_names_list)
            if self.DEBUG:
                print 'obj_names_list:',
                print obj_names_list
            pm.editRenderLayerMembers(layer,obj_names_list,noRecurse=True)
        else :
            if not layer :
                logging.warning('add_obj_to_layer: layer is None')
            if not obj_names_list :
                logging.warning('add_obj_to_layer: selection is None')

    def remove_obj_from_layers(self,layers,obj_list):
        if type(obj_list) == self.TYPE_SET : 
            obj_list=list(obj_list)
        if layers and obj_list :
            for layer in layers:
                self.remove_obj_from_layer(layer, obj_list)
        else :
            if not layers :
                logging.warning('remove_obj_from_layer: layer is None')
            if not obj_list :
                logging.warning('remove_obj_from_layer: selection is None')
                                                                
    def remove_obj_from_layer(self,layer,obj_list):
        #editRenderLayerMembers -noRecurse layer2 nurbsSphere2
        layer = PyNode(layer)
        pm.editRenderLayerMembers(layer,obj_list,noRecurse=1,remove=1)
                        
    def removeLayer(self,layer_set):
        if layer_set:
            layer_set = list(layer_set)
            try:
                pm.delete( layer_set )
            except:
                # If current layer is only the last layer then:
                #editRenderLayerGlobals -currentRenderLayer defaultRenderLayer;
                pm.editRenderLayerGlobals(currentRenderLayer='defaultRenderLayer')
                try:
                    pm.delete( layer_set )
                except:
                    traceback.print_exc()
                                                
    def remove_pass_from_layer(self,layer,pass_list):
        # Get layer first
        layer = PyNode(layer)
        if layer and pass_list :
            #disconnectAttr -nextAvailable layer2.renderPass ambientRaw.owner
            for item in pass_list :
                layer.renderPass.disconnect(PyNode(item).owner, nextAvailable=1)
        else :
            if not layer :
                logging.warning('remove_pass_from_layer: layer is None')
            if not pass_list :
                logging.warning('remove_pass_from_layer: pass is None')                
        
    def remove_pass_from_layers(self,layers,pass_list):
        if type(pass_list) == self.TYPE_SET : 
            pass_list=list(pass_list)
        if layers and pass_list :
            for layer in layers:
                self.remove_pass_from_layer(layer, pass_list)
        else :
            if not layers :
                logging.warning('remove_pass_from_layers: layer is None')
            if not pass_list :
                logging.warning('remove_pass_from_layers: selection is None')
        
    def remove_overrides_from_layers(self,layers,attr_list):
        if type(attr_list) == self.TYPE_SET : 
            attr_list=list(attr_list)
        if layers and attr_list :
            for layer in layers:
                self.remove_overrides_from_layer(layer, attr_list)
        else :
            if not layers :
                logging.warning('remove_pass_from_layers: layer is None')
            if not attr_list :
                logging.warning('remove_pass_from_layers: selection is None')
                          
    def remove_overrides_from_layer(self,layer,attr_list):
        #layer=PyNode(layer)
        if layer and attr_list:
            for attr in attr_list :
                # Important: use below command will cause maya crash
                pm.editRenderLayerAdjustment(attr,layer=layer,remove=1)
        else :
            if not layer :
                logging.warning('remove_overrides_from_layer: layer is None')
            if not attr_list :
                logging.warning('remove_overrides_from_layer: selection is None')
    
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
                    logging.warning('can not get passes in inputs layer')
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
        
    def createNewMRLayer(self,layerName):
        newLayer = pm.createRenderLayer(n=layerName)
        pm.editRenderLayerGlobals(currentRenderLayer=newLayer)
        pm.editRenderLayerAdjustment(self.DEFAULT_RENDER_GLOBALS.currentRenderer)
        self.DEFAULT_RENDER_GLOBALS.currentRenderer.set('mentalRay')    
        return newLayer     
        
    def createNewLayer(self):
        newLayer = pm.createRenderLayer()
        return newLayer   
        
    def setRenderLayerAttr(self,attr,val):
        # Check if attr exists
        logging.debug('attr: %s',attr)
        if pm.objExists(attr) :
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
        logging.debug('self.PREFIX_PASS:%s',self.PREFIX_PASS)
        logging.debug('self.SUFFIX_PASS:%s',self.SUFFIX_PASS)
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

        passName =  self.PASSES_ALL[passName]

        presetMel = self.MAYA_LOCATION+'/presets/attrPresets/renderPass/'+passName+'.mel'
        logging.debug('presetMel: %s',presetMel)   
        
        mel.applyAttrPreset(renderPass, presetMel, 1)     
        
    def removePass(self,passName) :
        try:
            pm.delete( PyNode(passName) )
        except:
            traceback.print_exc()
        else:
            logging.debug('success del: %s',passName)
                    
    def updateScenePasses(self,pass_names_list):
        if pass_names_list :
            if self.DEBUG:
                print self.PASSES_SCENE
                print pass_names_list
            self.getScenePasses()
            addList = [x for x in pass_names_list \
                       if x not in self.PASSES_SCENE]
            removeList = [x for x in self.PASSES_SCENE \
                          if x not in pass_names_list]
            if addList :
                # add passes to scene
                for pass_name in addList:
                    if self.DEBUG:
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
                        
    def updateAssociatedPasses(self,pass_names_list,model='M'):
        if model == 'M' :
            if self.DEBUG:
                print 'self.LAYERS_MANAGER_SELECTED:'
                print self.LAYERS_MANAGER_SELECTED
            if self.LAYERS_MANAGER_SELECTED :
                # get layer frm layer name
                for layer in self.getNodeByName( self.LAYERS_MANAGER_SELECTED ) :
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
        else:
            if self.LAYERS_CREATION_SELECTED :
                # AP may be add or remove, so use 'update' model
                self.set_creation_layers_attr('AP', pass_names_list,'Update')
                
    def remove_layers_from_creation_layers(self):
        for layer in self.LAYERS_CREATION_SELECTED :
            del self.LAYER_CREATION[layer]
        
    def set_creation_layers_attr(self,key,value,model):
        if self.DEBUG:
            print 'self.LAYER_CREATION:',
            print self.LAYER_CREATION
        # Convert list to set
        if type(value) == self.TYPE_LIST :
            value = set(value)
        for layer in self.LAYERS_CREATION_SELECTED :
            self.set_creation_layer_attr(layer, key, value, model)
        if self.DEBUG:
            print 'self.LAYER_CREATION:'
            print self.LAYER_CREATION
        
    def set_creation_layer_attr(self,layer,key,value,model):
        # Add elements
        if model == 'Add' :
            v = list( value - set( self.LAYER_CREATION[layer][key] ) )
            self.log_list(v)
            if v :
                self.LAYER_CREATION[layer][key].extend(v)
        # Remove elements
        elif model == 'Remove' :
            v = list( set( self.LAYER_CREATION[layer][key] ) - value )
            self.log_list(v)
            if not v:
                v = []
            self.LAYER_CREATION[layer].update({key:v})
        # For 'PRESET' attr
        elif model == 'Update':
            if self.DEBUG:
                print self.LAYER_CREATION
            self.LAYER_CREATION[layer][key] = value
            if self.DEBUG:
                print self.LAYER_CREATION
        else:
            logging.error('set_creation_layer_attr: inputs model is wrong')
            if self.DEBUG:
                print model
            
    def init_creation_layer_attr(self,layer):
        self.LAYER_CREATION[layer] = {'AO':[],'AL':[],'AP':[],'O':[],'PRESET':'Normal'}
        
    def rename_creation_layer(self,newName):
        logging.debug('rename_creation_layer:')
        if self.DEBUG:
            print 'self.LAYER_CREATION:',self.LAYER_CREATION
        # Copy value from old layer
        try:
            self.LAYER_CREATION[newName] = self.LAYER_CREATION[self.LAYER_BEFORE_RENAME]
        except:
            traceback.print_exc()
        else:
            if self.DEBUG:
                print 'self.LAYER_CREATION:',self.LAYER_CREATION
            # Remove old layer
            self.LAYER_CREATION.pop( self.LAYER_BEFORE_RENAME )
        if self.DEBUG:
            print 'self.LAYER_CREATION:',self.LAYER_CREATION
                            
    def create_creation_layers(self):
        for layerName in self.LAYER_CREATION :
            # Clear selection first, else selection will be add to layer
            pm.select(clear=True)
            
            # Create MR layer
            layer = self.createNewMRLayer(layerName)
            
            # Add objects
            obj_list = self.LAYER_CREATION[layerName].get('AO')
            # Get shape of objects
            #obj_list = self.getShapeSelection(obj_list)
            if obj_list :
                # Add objs to layer
                self.add_obj_to_layer(layer, obj_list)

            # Add lights
            light_list = self.LAYER_CREATION[layerName].get('AL')
            # Get shape of lightects
            #light_list = self.getShapeSelection(light_list)
            if light_list :
                # Add lights to layer
                self.add_obj_to_layer(layer, light_list)
                                
            # Add passes
            pass_list = self.LAYER_CREATION[layerName].get('AP')
            if pass_list :
                self.assign_pass_to_layer(layer,pass_list)
                
            # Add overrides
            overrides_list = self.LAYER_CREATION[layerName].get('O')
            if overrides_list :
                self.assign_overrides_to_layer(layer,overrides_list)
                
            # Material
            # Get layer preset
            preset = self.LAYER_CREATION[layerName].get('PRESET')
            #['Normal','Color','AO','AO_Transparency','Shadow']
            if preset == 'AO' :
                self.create_and_assign_AO_shader(obj_list)
            elif preset == 'AO_Transparency' :
                self.create_and_assign_AO_Transparency_shader(obj_list)
            elif preset == 'Shadow' :
                self.create_and_assign_shadow_shader(obj_list)
        # clear self.LAYER_CREATION
        # clear after loop because during iteration loop can not delete iteration
        self.LAYER_CREATION.clear()
        if self.DEBUG:
            print 'self.LAYER_CREATION:',self.LAYER_CREATION
        
    def assign_obj_to_layer(self,layer,obj_names_list):
        if layer and obj_names_list:
            for obj in obj_names_list :
                pm.editRenderLayerMembers(layer,obj,noRecurse=1)
        
    def assign_pass_to_layer(self,layer,pass_names_list):
        if layer and pass_names_list :
            for pass_name in pass_names_list :
                try:
                    layer.renderPass.connect(PyNode(pass_name).owner,nextAvailable=1)
                except:
                    traceback.print_exc()

    def assign_overrides_to_layer(self,layer,attr_list):
        if layer and attr_list:
            for attr in attr_list:
                pm.editRenderLayerAdjustment(attr,layer=layer)
            
    def createAOTransparencyLayer(self,isAddPass):
        selObj = self.getGeometrySelection()
        self.CURRENT_LAYER = self.createNewMRLayer()
        shaderNoDis,shaderNoDisSG = self.createShader('surfaceShader',(self.LAYER_NAME+'_MAT'))
        AONode = pm.createNode('mib_fg_occlusion')
        AONode.outValue.connect(shaderNoDis.outColor)
        if selObj :
            for each in selObj :
                nodeType = type(each)
                logging.debug(str(nodeType))
                
                # Get dispalcement shader if inputs is geometry
                logging.debug('****%s',each)
                eachSn = each.getParent()
                
                # Check shape has displacement shader or not
                shapeFaces = self.getTransparencyShader(each)
                
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
                                shader,shaderSG = self.createShader('surfaceShader',(self.LAYER_NAME+'_MAT'))
                                v[0].connect(shaderSG.displacementShader)
                                AONode.outValue.connect(shader.outColor)
                                
                                pm.select(k,r=1)
                                pm.sets(shaderSG,e=1,forceElement=1)
                            # Have transparency texture
                            else :
                                shader,shaderSG = self.createShader('surfaceShader',(self.LAYER_NAME+'_MAT'))
                                v[0].connect(shaderSG.displacementShader)
                                AONode.outValue.connect(shader.outColor)
                                
                                tranNode = pm.createNode('mib_transparency')
                                v[1].outColor.connect( tranNode.transp )    
                                v[1].outAlpha.connect( tranNode.transpA )
                                tranNode.outValue.connect( shaderSG.miMaterialShader, f=1 )
                                AONode.outValue.connect( tranNode.inputs )    
                                AONode.outValueA.connect( tranNode.inputsA )
                                
                                pm.select(k,r=1)
                                pm.sets(shaderSG,e=1,forceElement=1)                                
                        
                        else :
                            # Have not transparency texture
                            if not v[1] :
                                pass
                            # Have transparency texture
                            else :
                                shader,shaderSG = self.createShader('surfaceShader',(self.LAYER_NAME+'_MAT'))
                                AONode.outValue.connect(shader.outColor)
                                
                                tranNode = pm.createNode('mib_transparency')
                                v[1].outColor.connect( tranNode.transp )    
                                v[1].outAlpha.connect( tranNode.transpA )
                                AONode.outValue.connect( tranNode.inputs )    
                                AONode.outValueA.connect( tranNode.inputsA )
                                tranNode.outValue.connect( shaderSG.miMaterialShader, f=1 )
                                
                                pm.select(k,r=1)
                                pm.sets(shaderSG,e=1,forceElement=1)

                pm.select(each)
                logging.debug('each: %s',each)
                eachSn = pm.pickWalk(d='down')
                logging.debug('eachSn: %s',eachSn[0])
                if eachSn[0] != each :
                    pm.editRenderLayerMembers(self.CURRENT_LAYER,eachSn[0],remove=1)

        # Adjust render layer attr
        self.setRenderLayerAttr(self.MI_DEFAULT_OPTIONS.finalGather, 1)
        self.setRenderLayerAttr(self.MI_DEFAULT_OPTIONS.caustics, 0)
        self.setRenderLayerAttr(self.MI_DEFAULT_OPTIONS.globalIllum, 0)
        self.setRenderLayerAttr(self.MI_DEFAULT_FRAME_BUFFER.datatype, 2)
        self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.imageFormat, 7)
        self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.imfPluginKey, 'iff')
        self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.multiCamNamingMode, 1)
        self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.bufferName, '<RenderPass>')

        # Remove cam lens and env shader            
        self.disConnectCamShader()
        
        if isAddPass == True :
            # Add ao pass
            self.createPass2CurrentLayer('ambientOcclusion')
            
        pm.select(cl=1)
        
    def create_and_assign_AO_Transparency_shader(self,obj_name_list):
        shaderNoDis,shaderNoDisSG = self.createShader('surfaceShader',(self.LAYER_NAME+'_MAT'))
        AONode = pm.createNode('mib_fg_occlusion')
        AONode.outValue.connect(shaderNoDis.outColor)
        
        if obj_name_list:
            # Convert name list to node list
            obj_list = (PyNode(x) for x in obj_name_list)
            for each in obj_list :
                nodeType = type(each)
                logging.debug(str(nodeType))
                
                # Get dispalcement shader if inputs is geometry
                logging.debug('%s',each)
                eachSn = each.getParent()

                # Check shape has displacement shader or not
                shapeFaces = self.getTransparencyShader(each)
                
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
                                shader,shaderSG = self.createShader('surfaceShader',(self.LAYER_NAME+'_MAT'))
                                v[0].connect(shaderSG.displacementShader)
                                AONode.outValue.connect(shader.outColor)
                                
                                pm.select(k,r=1)
                                pm.sets(shaderSG,e=1,forceElement=1)
                            # Have transparency texture
                            else :
                                shader,shaderSG = self.createShader('surfaceShader',(self.LAYER_NAME+'_MAT'))
                                v[0].connect(shaderSG.displacementShader)
                                AONode.outValue.connect(shader.outColor)
                                
                                tranNode = pm.createNode('mib_transparency')
                                v[1].outColor.connect( tranNode.transp )    
                                v[1].outAlpha.connect( tranNode.transpA )
                                tranNode.outValue.connect( shaderSG.miMaterialShader, f=1 )
                                AONode.outValue.connect( tranNode.inputs )    
                                AONode.outValueA.connect( tranNode.inputsA )
                                
                                pm.select(k,r=1)
                                pm.sets(shaderSG,e=1,forceElement=1)                                
                        
                        else :
                            # Have not transparency texture
                            if not v[1] :
                                pass
                            # Have transparency texture
                            else :
                                shader,shaderSG = self.createShader('surfaceShader',(self.LAYER_NAME+'_MAT'))
                                AONode.outValue.connect(shader.outColor)
                                
                                tranNode = pm.createNode('mib_transparency')
                                v[1].outColor.connect( tranNode.transp )    
                                v[1].outAlpha.connect( tranNode.transpA )
                                AONode.outValue.connect( tranNode.inputs )    
                                AONode.outValueA.connect( tranNode.inputsA )
                                tranNode.outValue.connect( shaderSG.miMaterialShader, f=1 )
                                
                                pm.select(k,r=1)
                                pm.sets(shaderSG,e=1,forceElement=1)

        # Adjust render layer attr
        self.setRenderLayerAttr(self.MI_DEFAULT_OPTIONS.finalGather, 1)
        self.setRenderLayerAttr(self.MI_DEFAULT_OPTIONS.caustics, 0)
        self.setRenderLayerAttr(self.MI_DEFAULT_OPTIONS.globalIllum, 0)
        self.setRenderLayerAttr(self.MI_DEFAULT_FRAME_BUFFER.datatype, 2)
        self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.imageFormat, 7)
        self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.imfPluginKey, 'iff')
        self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.multiCamNamingMode, 1)
        self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.bufferName, '<RenderPass>')
  
  
    def create_and_assign_AO_shader(self,obj_name_list):
        # If no selection,then create shader only
        shaderNoDis,shaderNoDisSG = self.createShader('surfaceShader',(self.LAYER_NAME+'_MAT'))
        AONode = pm.createNode('mib_amb_occlusion')
        AONode.outValue.connect(shaderNoDis.outColor)
        AONode.samples.set(64)
                    
        if obj_name_list :
            # Convert name list to node list
            obj_list = (PyNode(x) for x in obj_name_list)
            if obj_list:
                for each in obj_list :
                    nodeType = type(each)
                    logging.debug(str(nodeType))
                    
                    # Get dispalcement shader if inputs is geometry
                    logging.debug('****%s',each)
                    eachSn = each.getParent()
                    
                    # Check shape has displacement shader or not
                    displacementShaders, shapeFaces = self.getDisplacementShader2(each)
                    
                    # First assign no displacement shader to all
                    logging.debug('First assign no displacement shader to all' )
                    pm.select(each,r=1)
                    pm.sets(shaderNoDisSG,e=1,forceElement=1)
                        
                    # If shape has displacement shader,then assign displacement shader again    
                    if displacementShaders != [] :
                        logging.debug('each: %s',each)
                        for displacementShader,shapeFace in zip(displacementShaders,shapeFaces) :
                            shader,shaderSG = self.createShader('surfaceShader',(self.LAYER_NAME+'_'+str(eachSn)+'_MAT'))
                            displacementShader.connect(shaderSG.displacementShader)
                            AONode = pm.createNode('mib_amb_occlusion')
                            AONode.outValue.connect(shader.outColor)
                            AONode.samples.set(64)
                                    
                            pm.select(shapeFace,r=1)
                            pm.sets(shaderSG,e=1,forceElement=1)
            
        # Adjust render layer attr
        self.setRenderLayerAttr(self.MI_DEFAULT_OPTIONS.finalGather, 0)
        self.setRenderLayerAttr(self.MI_DEFAULT_OPTIONS.caustics, 0)
        self.setRenderLayerAttr(self.MI_DEFAULT_OPTIONS.globalIllum, 0)
        self.setRenderLayerAttr(self.MI_DEFAULT_FRAME_BUFFER.datatype, 2)
        self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.imageFormat, 7)
        self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.imfPluginKey, 'iff')
        self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.multiCamNamingMode, 1)
        self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.bufferName, '<RenderPass>')
  
  
    def createAOLayer(self,isAddPass):
        selObj = self.getGeometrySelection()
        
        self.CURRENT_LAYER = self.createNewMRLayer()
        
        #AOMat = pm.shadingNode('surfaceShader',n='AO_mat',asShader=True)
        shaderNoDis,shaderNoDisSG = self.createShader('surfaceShader',(self.LAYER_NAME+'_MAT'))
        
        AONode = pm.createNode('mib_amb_occlusion')
        AONode.outValue.connect(shaderNoDis.outColor)
        AONode.samples.set(64)
        
        if selObj :
            for each in selObj :
                nodeType = type(each)
                logging.debug(str(nodeType))
                
                # Get dispalcement shader if inputs is geometry
                logging.debug('****%s',each)
                eachSn = each.getParent()
                
                # Check shape has displacement shader or not
                displacementShaders, shapeFaces = self.getDisplacementShader2(each)
                
                # First assign no displacement shader to all
                logging.debug('First assign no displacement shader to all' )
                pm.select(each,r=1)
                pm.sets(shaderNoDisSG,e=1,forceElement=1)
                    
                # If shape has displacement shader,then assign displacement shader again    
                if displacementShaders != [] :
                    logging.debug('each: %s',each)
                    for displacementShader,shapeFace in zip(displacementShaders,shapeFaces) :
                        shader,shaderSG = self.createShader('surfaceShader',(self.LAYER_NAME+'_'+str(eachSn)+'_MAT'))
                        displacementShader.connect(shaderSG.displacementShader)
                        AONode = pm.createNode('mib_amb_occlusion')
                        AONode.outValue.connect(shader.outColor)
                        AONode.samples.set(64)
                                
                        pm.select(shapeFace,r=1)
                        pm.sets(shaderSG,e=1,forceElement=1)                        

                pm.select(each)
                logging.debug('each: %s',each)
                eachSn = pm.pickWalk(d='down')
                logging.debug('eachSn: %s',eachSn[0])
                if eachSn[0] != each :
                    pm.editRenderLayerMembers(self.CURRENT_LAYER,eachSn[0],remove=1)

        # Adjust render layer attr
        self.setRenderLayerAttr(self.MI_DEFAULT_OPTIONS.finalGather, 0)
        self.setRenderLayerAttr(self.MI_DEFAULT_OPTIONS.caustics, 0)
        self.setRenderLayerAttr(self.MI_DEFAULT_OPTIONS.globalIllum, 0)
        self.setRenderLayerAttr(self.MI_DEFAULT_FRAME_BUFFER.datatype, 2)
        self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.imageFormat, 7)
        self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.imfPluginKey, 'iff')
        self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.multiCamNamingMode, 1)
        self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.bufferName, '<RenderPass>')

        # Remove cam lens and env shader            
        self.disConnectCamShader()
        logging.debug('isAddPass:%s',isAddPass)
        if isAddPass == True :
            # Add ao pass
            self.createPass2CurrentLayer('ambientOcclusion')
                    
        pm.select(cl=1)
        
  
    def create_and_assign_shadow_shader(self,obj_name_list):
        shaderName = 'Shadow_Mask'
        outAlpha = 1
        
        shaderNoDis= None
        shaderNoDisSG = None
        shader = None
        shaderSG = None        
        
        if obj_name_list :
            # Convert name list to node list
            obj_list = (PyNode(x) for x in obj_name_list)
            if obj_list:
                for each in obj_list :
                    logging.debug('each: %s',each)
                    # Get dispalcement shader if inputs is geometry
                    eachSn = each.getParent()
                    
                    # Check shape has displacement shader or not
                    displacementShaders, shapeFaces = self.getDisplacementShader2(each)
                    
                    if not pm.objExists(shaderName) :
                        shaderNoDis,shaderNoDisSG = self.createShader('useBackground', shaderName)
                        shaderNoDis.specularColor.set([0,0,0])
                        shaderNoDis.reflectivity.set(0)
                        shaderNoDis.reflectionLimit.set(0)
                        shaderNoDis.matteOpacity.set(outAlpha)
                    else :
                        # Get shaderSG by shader name
                        if not shaderNoDisSG :
                            shaderNoDisSG = self.getShadingSG(shaderName)
                            
                    logging.debug('shaderNoDisSG: %s', shaderNoDisSG)
                        
                    # First assign no displacement shader to all
                    logging.debug('First assign no displacement shader to all' )
                    pm.select(each,r=1)
                    pm.sets(shaderNoDisSG,e=1,forceElement=1)
                        
                    # If shape has displacement shader,then assign displacement shader again    
                    if displacementShaders != [] :
                        logging.debug('each: %s',each)
                        shaderNameWithDisp = shaderName + "_" + eachSn
                        for displacementShader,shapeFace in zip(displacementShaders,shapeFaces) :
                            if pm.objExists(shaderNameWithDisp) :
                                # Get shadingSG
                                shaderSG = self.getShadingSG(shaderNameWithDisp)
                            else :
                                shader,shaderSG = self.createShader('useBackground', shaderNameWithDisp)
                                shader.specularColor.set([0,0,0])
                                shader.reflectivity.set(0)
                                shader.reflectionLimit.set(0)
                                shader.matteOpacity.set(outAlpha)
                            
                            displacementShader.connect(shaderSG.displacementShader)
                            pm.select(shapeFace,r=1)
                            pm.sets(shaderSG,e=1,forceElement=1)
        else:
            shaderNoDis,shaderNoDisSG = self.createShader('useBackground', shaderName)
            shaderNoDis.specularColor.set([0,0,0])
            shaderNoDis.reflectivity.set(0)
            shaderNoDis.reflectionLimit.set(0)
            shaderNoDis.matteOpacity.set(outAlpha)
        pm.select(cl=1)
        
                                
    def createColorPasses(self):
        for p in self.PASSES_COLOR :
            self.createPass2CurrentLayer(p)
            
    def createColorLayer(self):
        selObj = self.getDAGSelection()
        if selObj :
            self.CURRENT_LAYER = self.createNewMRLayer()
            self.createColorPasses()  
            self.setRenderLayerAttr(self.MI_DEFAULT_FRAME_BUFFER.datatype, 5)
            self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.imageFormat, 51)
            self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.imfPluginKey, 'exr')
            self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.multiCamNamingMode, 1)
            self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.bufferName, '<RenderPass>')
            self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.imageFilePrefix, 'images/<Scene>/<RenderLayer>/<RenderLayer>')

            pm.select(cl=1)
            
    def createShadowLayer(self,layerName='Shadow_Mask_Layer',shaderName='Shadow_Mask_MAT',outAlpha=1):
        sel = self.getGeometrySelection()
        self.createNewMRLayer()
        # Create material
        self.createShadowShader(shaderName,sel,outAlpha)
        pm.select(cl=1)

    def createLightLayer(self,name,color):
        selObj = self.getGeometrySelection()
        selLight = self.getLightSelection()
        if selObj == None :
            logging.warning('select some lights and some objects first.')
            return None
        elif selLight == None :
            logging.warning('select some lights and some objects first.')
            return None
        else :
            newLayer = self.createNewMRLayer(name)
            
#            luzMat = pm.shadingNode('lambert',n=(name+'_MAT'),asShader=True)
            shaderNoDis,shaderNoDisSG = self.createShader('lambert',(name+'_MAT'))
            shaderNoDis.diffuse.set(1)
            # For Key ligt assign green color
            self.MI_DEFAULT_OPTIONS.rayTracing.set(1)
        
            for each in selObj :
                nodeType = type(each)
                logging.debug(str(nodeType))
                
                # Get dispalcement shader if inputs is geometry
                eachSn = each.getParent()
                
                # Check shape has displacement shader or not
                displacementShaders, shapeFaces = self.getDisplacementShader2(each)
                
                # First assign no displacement shader to all
                logging.debug('First assign no displacement shader to all' )
                pm.select(each,r=1)
                pm.sets(shaderNoDisSG,e=1,forceElement=1)
                
                # If shape has displacement shader,then assign displacement shader again    
                if displacementShaders != [] :
                    logging.debug('each: %s',each)
                    for displacementShader,shapeFace in zip(displacementShaders,shapeFaces) :
                        logging.debug('has displaceMentShader' )
                        logging.debug('displaceMentShader: %s' ,displacementShader)
                        logging.debug('shapeFace: %s',shapeFace)
                        shader,shaderSG = self.createShader('lambert',(newLayer+'_'+str(eachSn)+'_MAT'))
                        shader.diffuse.set(1)
                        displacementShader.connect(shaderSG.displacementShader)
                            
                        pm.select(shapeFace,r=1)
                        pm.sets(shaderSG,e=1,forceElement=1)
                        
                pm.select(each,r=1)
                logging.debug('each: %s',each)
                eachSn = pm.pickWalk(d='down')
                logging.debug('eachSn: %s',eachSn[0])
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
            self.setRenderLayerAttr(self.MI_DEFAULT_OPTIONS.finalGather, 0)
            self.setRenderLayerAttr(self.MI_DEFAULT_OPTIONS.caustics, 0)
            self.setRenderLayerAttr(self.MI_DEFAULT_OPTIONS.globalIllum, 0)
            self.setRenderLayerAttr(self.MI_DEFAULT_FRAME_BUFFER.datatype, 2)
            self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.imageFormat, 7)
            self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.imfPluginKey, 'iff')
            self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.multiCamNamingMode, 1)
            self.setRenderLayerAttr(self.DEFAULT_RENDER_GLOBALS.bufferName, '<RenderPass>')

            # Remove cam lens and env shader            
            self.disConnectCamShader()
        
            pm.select(cl=1)
            
            return True

    #make shader override layer
    def makeShaderOverrideLayer(self,shader,layer=None):
        logging.debug('makeShaderOverrideLayer')
        self.getCurrentLayer()
        if not layer:
            layer = self.LAYER_SCENE_ACTIVE
        if self.DEBUG :
            print 'layer: ',layer
        if not layer:
            logging.error('makeShaderOverrideLayer: can not get current active render layer')
        else:
            # If defaultRenderLayer skip
            if layer.longName() != 'defaultRenderLayer':
                try:
                    cmd = "hookShaderOverride(\""+layer.longName()+"\",\"\",\""+shader.longName()+"\")"
                except:
                    logging.error('makeShaderOverrideLayer:')
                    traceback.print_exc()
                else:
                    mel.eval(cmd)
       
    def create_surface_shader(self,outColor,outValue,shaderName,overrideLayer=False):
        # Get selection
        shader = self.createSurfaceShader(outColor,outValue,shaderName)
        if self.DEBUG :
            print 'shader:',
            print shader
        if overrideLayer :
            self.makeShaderOverrideLayer( shader )
       
    def create_shadow_shader(self,shaderName,overrideLayer=False):
        #shader = self.createShader([0,0,0],[1,1,1],'BLACK_MATTE')
        shader = self.createShadowShader(shaderName,None,1)
        if overrideLayer :
            self.makeShaderOverrideLayer( shader )
            
    # Get shadingSG by shader name
    # Return type is string
    def getShadingSG(self,shaderName):
        try :
            shaderNoDisSG = PyNode(shaderName).outColor.connections(d=1,p=0,sh=1)
            shaderNoDisSG = shaderNoDisSG.longName()
            logging.debug('get shadingSG:%s',shaderNoDisSG)
        except :
            logging.debug('can not get shadingSG')
            shaderNoDisSG = pm.sets(renderable=True,noSurfaceShader=True,\
                                    empty=True,name=(shaderName+'_SG'))
            PyNode(shaderName).outColor.connect(shaderNoDisSG.surfaceShader)
            
        return shaderNoDisSG
    
    # Create and assign black shader
    # createShader([0,0,0],[1,1,1],'BLACK')
    def createSurfaceShader(self,outColor,outAlpha,shaderName):
        selObj = self.getGeometrySelection()
        shaderNoDis= None
        shaderNoDisSG = None
        shader = None
        shaderSG = None
        if selObj :
            for each in selObj :
                # Get dispalcement shader if inputs is geometry
                eachSn = each.getParent()
                
                # Check shape has displacement shader or not
                displacementShaders, shapeFaces = self.getDisplacementShader2(each)
                
                if not pm.objExists(shaderName) :
                    shaderNoDis,shaderNoDisSG = self.createShader('surfaceShader', shaderName)
                    shaderNoDis.outColor.set(outColor)
                    shaderNoDis.outMatteOpacity.set(outAlpha)
                else :
                    # Get shader for return
                    try:
                        shader = PyNode( shaderName )
                    except:
                        traceback.print_exc()
                    # Get shaderSG by shader name
                    if not shaderNoDisSG :
                        shaderNoDisSG = self.getShadingSG(shaderName)
                        
                logging.debug('shaderNoDisSG: %s',shaderNoDisSG)
                    
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
                            logging.debug('shaderSG exists with shaderNameWithDisp: %s',shaderSG)
                        else :
                            shader,shaderSG = self.createShader('surfaceShader', shaderNameWithDisp)
                            shader.outColor.set(outColor)
                            shader.outMatteOpacity.set(outAlpha)
                            logging.debug('shaderSG exists with no shaderNameWithDisp: %s',shaderSG)
                        
                        displacementShader.connect(shaderSG.displacementShader)
                        pm.select(shapeFace,r=1)
                        pm.sets(shaderSG,e=1,forceElement=1)
        else:
            # create shader only
            shader,shaderSG = self.createShader('surfaceShader', shaderName)
            shader.outColor.set(outColor)
            shader.outMatteOpacity.set(outAlpha)
                        
        pm.select(cl=1)
        if not shader:
            shader = shaderNoDis
        return shader
        
    # Create and assign black shader
    def createShadowShader(self,shaderName='Shadow_Mask_MAT',sel=None,outAlpha=1):
        selObj = sel
        if not selObj:
            selObj = self.getGeometrySelection()
        logging.debug('createShadowShader: %s',selObj)
        shaderNoDis= None
        shaderNoDisSG = None
        shader = None
        shaderSG = None
        if selObj :
            for each in selObj :
                logging.debug('each: %s',each)
                # Get dispalcement shader if inputs is geometry
                eachSn = each.getParent()
                
                # Check shape has displacement shader or not
                displacementShaders, shapeFaces = self.getDisplacementShader2(each)
                
                if not pm.objExists(shaderName) :
                    shaderNoDis,shaderNoDisSG = self.createShader('useBackground', shaderName)
                    shaderNoDis.specularColor.set([0,0,0])
                    shaderNoDis.reflectivity.set(0)
                    shaderNoDis.reflectionLimit.set(0)
                    shaderNoDis.matteOpacity.set(outAlpha)
                else :
                    # Get shader for return
                    try:
                        shader = PyNode( shaderName )
                    except:
                        traceback.print_exc()
                    # Get shaderSG by shader name
                    if not shaderNoDisSG :
                        shaderNoDisSG = self.getShadingSG(shaderName)
                        
                logging.debug('shaderNoDisSG: %s',shaderNoDisSG)
                    
                # First assign no displacement shader to all
                logging.debug('First assign no displacement shader to all' )
                pm.select(each,r=1)
                pm.sets(shaderNoDisSG,e=1,forceElement=1)
                    
                # If shape has displacement shader,then assign displacement shader again    
                if displacementShaders != [] :
                    logging.debug('each: %s',each)
                    shaderNameWithDisp = shaderName + "_" + eachSn
                    for displacementShader,shapeFace in zip(displacementShaders,shapeFaces) :
                        if pm.objExists(shaderNameWithDisp) :
                            # Get shadingSG
                            shaderSG = self.getShadingSG(shaderNameWithDisp)
                        else :
                            shader,shaderSG = self.createShader('useBackground', shaderNameWithDisp)
                            shader.specularColor.set([0,0,0])
                            shader.reflectivity.set(0)
                            shader.reflectionLimit.set(0)
                            shader.matteOpacity.set(outAlpha)
                        
                        displacementShader.connect(shaderSG.displacementShader)
                        pm.select(shapeFace,r=1)
                        pm.sets(shaderSG,e=1,forceElement=1)
        else:
            shaderNoDis,shaderNoDisSG = self.createShader('useBackground', shaderName)
            shaderNoDis.specularColor.set([0,0,0])
            shaderNoDis.reflectivity.set(0)
            shaderNoDis.reflectionLimit.set(0)
            shaderNoDis.matteOpacity.set(outAlpha)
        pm.select(cl=1)
        if not shader:
            shader = shaderNoDis
        return shader
    
    def createZDepthNetwork(self,shaderName):
        shader,shaderSG = self.createShader('surfaceShader', shaderName)
                        
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
        selObj = self.getGeometrySelection()
        shaderNoDis= None
        shaderNoDisSG = None
        shader = None
        shaderSG = None
        if selObj :
            for each in selObj :
                # Get dispalcement shader if inputs is geometry
                eachSn = each.getParent()
                               
                # Check shape has displacement shader or not
                displacementShaders, shapeFaces = self.getDisplacementShader2(each)
                
                if not pm.objExists(shaderName) :
                    shaderNoDis,shaderNoDisSG = self.createZDepthNetwork(shaderName)
                else :
                    # Get shader for return
                    try:
                        shader = PyNode( shaderName )
                    except:
                        traceback.print_exc()
                    # Get shaderSG by shader name
                    if not shaderNoDisSG :
                        shaderNoDisSG = self.getShadingSG(shaderName)
                        
                logging.debug('shaderNoDisSG: %s',shaderNoDisSG)
                    
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
        if not shader:
            shader = shaderNoDis
        return shader

    def createSubSet(self,subSetName):
        selObj = self.getGeometrySelection()
        #string $subsetShader=`mrCreateCustomNode -asUtility "" mip_render_subset`;
        subSetShader = pm.createNode('mip_render_subset',asUtility=1)

if __name__ == "__main__":
    pass