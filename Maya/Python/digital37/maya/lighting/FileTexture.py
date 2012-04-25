import logging 
import traceback
import os
import pymel.core as pm
import re

import digital37.maya.general.Log as Log
reload(Log)

class FileTexture(Log.Log):
    SHADING_ENGINE_TYPE = '<class \'pymel.core.nodetypes.ShadingEngine\'>'
    FILE_TYPE = '<class \'pymel.core.nodetypes.File\'>'
    
    def __init__(self,mapDetail):
        self.Map_Detail = mapDetail
        Log.Log.__init__(self)
        self.Connections = set()
        self.Texture_Files = set()
        self.Texture_Nodes = set()
    
    def get_shadingSG(self,geometryShapeSet):
        shadingSG = set()
        for g in geometryShapeSet:
            connections = g.connections(d=1)
            if connections:
                for c in connections :
                    # is shadingSG node
                    if str( type(c) ) == self.__class__.SHADING_ENGINE_TYPE :
                        shadingSG.add(c)
        self.Log.debug('selection shadingSG:')
        self.log_list(shadingSG)
        return shadingSG
    
    def get_shader(self,shadingSG):
        shader = set()
        for g in shadingSG:
            connections = g.surfaceShader.connections(d=1)
            if connections:
                for c in connections :
                    shader.add(c)
        self.Log.debug('selection shader:')
        self.log_list(shader)
        return shader
        
    def get_texture_file(self):
        # Get texture file
        texturesList = pm.ls(textures=True)
        if texturesList :
            for tex in texturesList:
                if pm.attributeQuery( 'fileTextureName',node=tex,exists=1 ):
                    self.Texture_Nodes.add(tex)
                        
    def get_sel_geometry_shape(self):
        selObj = pm.ls(sl=1,dag=1,lf=1,type=['mesh','nurbsSurface','subdiv'])
        if not selObj :
            logging.warning('select some objects first.')
            return None
        else :
            self.Log.debug('selection shapes:')
            self.log_list(selObj)
            return selObj
        
    def get_texture_file_from_selection(self):
        g_shape = self.get_sel_geometry_shape()
        if g_shape:
            shadingSG = self.get_shadingSG(g_shape)
            shader= self.get_shader(shadingSG)
            self.glob_connections(shader)
            self.Texture_Nodes = (x for x in self.Connections if str(type(x))==self.__class__.FILE_TYPE)
            #self.log_list(self.Texture_Nodes)
            self.get_texture_file_name()
            
    def get_texture_file_name(self):
        for x in self.Texture_Nodes:
            if pm.attributeQuery( 'fileTextureName',node=x,exists=1 ):
                n = x.fileTextureName.get()
                if n :
                    base,ext = os.path.splitext(n)
                    # file ends with '__L'
                    if re.search('__[LMS]$',base) :
                        base = re.sub('__[LMS]$','',base)
                    # file not ends with '__L'
                    fn = base + '__' + self.Map_Detail + ext
                    print fn
                    #print os.path.isfile(fn)
                    if os.path.isfile(fn):
                        x.fileTextureName.set( self.convert_to_relative('sourceimages', fn) )
            
    def glob_connections(self,connections):
        if connections:
            try:
                for c in connections:
                    #print 'c:',c
                    #print type(c)
                    connections = set(c.connections(d=0))
                    self.Connections = self.Connections.union(connections)
                    #print 'connections:',connections
                    self.glob_connections(connections)
                    
            except KeyboardInterrupt:
                print 'user cancel'
            except:
                traceback.print_exc()
        
    def convert_to_relative(self,parten,inputStr):
        '''
        example: convertToRelative('sourceimages','C:/AW/Maya5.0/sourceimages/maya.exe')
        result: 'sourceimages/maya.exe'
        '''
        #p = re.compile('^.*/sourceimages')
        inputStr = str(inputStr).replace('\\','/')
        returnStr = re.sub( ('^.*/(' + parten + ')'), parten, inputStr )
        print inputStr,'\t',returnStr
        return returnStr
    
def main(mapDetail='M'):
    a = FileTexture(mapDetail)
    a.get_texture_file()
    a.get_texture_file_from_selection()
    
if __name__=='__main__':
    main()
        
                
                