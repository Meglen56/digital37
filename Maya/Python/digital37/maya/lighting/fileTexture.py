import logging 
import traceback
import os
import pymel.core as pm
import re

import system.log as log
reload(log)

class FileTexture(log.Log):
    SHADING_ENGINE_TYPE = '<class \'pymel.core.nodetypes.ShadingEngine\'>'
    FILE_TYPE = '<class \'pymel.core.nodetypes.File\'>'
    
    def __init__(self,log=None):
        self.Connections = set()
        self.Texture_Files = set()
        self.Texture_File_Nodes = set()
        if not log:
            log = self.get_stream_logger()
        self.Log = log
    
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
        
    def get_texture_file_node(self):
        # Get texture file node
        texturesList = pm.ls(textures=True)
        if texturesList :
            for tex in texturesList:
                if pm.attributeQuery( 'fileTextureName',node=tex,exists=1 ):
                    self.Texture_File_Nodes.add(tex)
                        
    def check_file_texture_exists(self):
        '''
        check file exists or not
        '''
        # Get texture file node
        self.get_texture_file_node()
        # get texture file name
        for x in self.Texture_File_Nodes:
            n = x.fileTextureName.get()
            if not os.path.isfile(n):
                self.Log.warning('file texture\'s fileTextureName is not exists: %s' % n)
                                            
    def get_sel_geometry_shape(self):
        selObj = pm.ls(sl=1,dag=1,lf=1,type=['mesh','nurbsSurface','subdiv'])
        if not selObj :
            logging.warning('select some objects first.')
            return None
        else :
            self.Log.debug('selection shapes:')
            self.log_list(selObj)
            return selObj
        
    def get_texture_file_node_from_selection(self):
        g_shape = self.get_sel_geometry_shape()
        if g_shape:
            shadingSG = self.get_shadingSG(g_shape)
            shader= self.get_shader(shadingSG)
            self.glob_connections(shader)
            self.Texture_File_Nodes = (x for x in self.Connections if str(type(x))==self.__class__.FILE_TYPE)
            #self.log_list(self.Texture_File_Nodes)
            
    def change_texture_file_detail(self,map_partten,map_detail):
        for x in self.Texture_File_Nodes:
            if pm.attributeQuery( 'fileTextureName',node=x,exists=1 ):
                n = x.fileTextureName.get()
                if n :
                    base,ext = os.path.splitext(n)
                    # file ends with '__L'
                    if re.search(map_partten,base) :
                        base = re.sub(map_partten,'',base)
                    # file not ends with '__L'
                    fn = base + map_detail + ext
                    print fn
                    #print os.path.isfile(fn)
                    #if os.path.isfile(fn):
                    x.fileTextureName.set( fn )
            
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
        
    def change_detail(self,map_partten='__[LMS]$',map_detail='__M'):
        # get texture files from selection
        self.get_texture_file_node_from_selection()
        self.change_texture_file_detail(map_partten,map_detail)
        
    def convert_to_relative(self,partten,inputStr):
        import digital37.maya.general.path as path
        reload(path)
        return path.convert_to_relative(partten, inputStr)
        
    def convert_all_texture_to_relative(self):
        self.get_texture_file_node()
        for x in self.Texture_File_Nodes:
            if pm.attributeQuery( 'fileTextureName',node=x,exists=1 ):
                n = x.fileTextureName.get()
                if n :
                    x.fileTextureName.set( self.convert_to_relative('sourceimages', n) )
                    
def main():
    pass
    
if __name__=='__main__':
    #main()
    pass