import os
import pymel.core as pm
from pymel.all import mel
import maya.cmds as cmds

class SvnMaya(object):
    def __init__(self):
        self.Maya_Ref_File = set()
        self.Texture_File = set()
        self.Ref_Dir = set()
        self.Cmd_Update = 'svn update '
        
    def get_texture_file(self):
        self.Texture_File = set()
        # Get texture file
        texturesList = cmds.ls(textures=True)
        if texturesList :
            for tex in texturesList:
                if cmds.attributeQuery( 'fileTextureName',node=tex,exists=1 ):
                    texFile = cmds.getAttr( (tex+'.fileTextureName') )
                    self.Texture_File.add(texFile)
        print self.Texture_File
        
    def get_reference_file(self):
        # Get reference file
        self.Reference_File = set( cmds.file(q=True,l=True) )
        print self.Reference_File
        
    def get_associated_file(self):
        self.get_reference_file()
        self.get_texture_file()
        
        dirs = set( os.path.dirname(f) for f in ( self.Reference_File | self.Texture_File ) )
        
        for d in dirs :
            
            while True :
                if not os.path.exists(d) :
                    # Get parent dir
                    d = os.path.dirname(d)
                else:
                    break
            
            self.Ref_Dir.add(d)
                
        cmd = self.Cmd_Update + ' '.join(self.Ref_Dir)
        print cmd
        os.system(cmd)

        
if __name__ == '__main__' :
    SvnMaya().get_associated_file()