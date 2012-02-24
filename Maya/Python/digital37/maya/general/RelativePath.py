import re
import os.path
import traceback
import pymel.core as pm

class RelativePath(object):
    def __init__(self):
        self.Reference_File_Names=set()
        self.Texture_File_Names=list()
        self.get_workspace()
    
    def convert_reference_to_relative(self):
        ref_nodes = pm.ls(type='reference')
        ref_nodes_top = list()
        if ref_nodes:
            # Get top level reference nodes
            for ref_node in ref_nodes :
                a = False
                try:
                    a = pm.system.referenceQuery(ref_node,topReference=1,referenceNode=1)
                except:
                    traceback.print_exc()
                else:
                    if a :
                        ref_nodes_top.append(ref_node)
            if ref_nodes_top:
                print 'ref_nodes_top:',ref_nodes_top
                for ref_node in ref_nodes_top:
                    # Check reference node is loaded or not
                    print ref_node
                    if pm.system.referenceQuery(ref_node,isLoaded=1) :
                        file_name = ''
                        # Get reference node's file name
                        try:
                            # use unresolvedName flag to get unresolvedName name
                            file_name= pm.system.referenceQuery(ref_node,filename=1,unresolvedName=1)
                        except:
                            traceback.print_exc()
                        else:
                            if file_name:
                                #print file_name
                                #self.Reference_File_Names.add(file_name)
                                self.RuleEntry_Scenes = 'scenes'
                                if not self.check_relative(self.RuleEntry_Scenes, file_name):
                                    file_name_after = self.convert_to_relative(self.RuleEntry_Scenes, file_name)
                                    ext = os.path.splitext(file_name)[1]
                                    if ext=='.mb':
                                        ext = 'mayaBinary'
                                    else:
                                        ext = 'mayaAscii'
                                    #file -loadReference $ref -type $ext -options "v=0;p=17" $file
                                    pm.system.loadReference(file_name_after,type=ext,options='v=0;p=17')
                                
    def convert_texture_to_relative(self):
        self.Texture_Files = set()
        # Get texture file
        texturesList = pm.ls(textures=True)
        if texturesList :
            for tex in texturesList:
                if pm.attributeQuery( 'fileTextureName',node=tex,exists=1 ):
                    texFile = tex.fileTextureName.get()
                    tex.fileTextureName.set( self.convert_to_relative(self.RuleEntry_SourceImages, texFile) )
        
    def get_workspace(self):
        #self.WorkSpace_RootDir = pm.workspace(q=1,rd=1)
        self.RuleEntry_SourceImages = pm.workspace('sourceImages',fileRuleEntry=1,q=1 )
        self.RuleEntry_Scenes = pm.workspace('scenes',fileRuleEntry=1,q=1 )
        
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

    def check_relative(self,parten,inputStr):
        print 'inputStr',inputStr
        #inputStr = str(inputStr).replace('\\','/')
        p = re.compile('^.*//(' + parten + ')')
        # start with '//' is false
        p_0 = re.compile('^//(' + parten + ')')
        if p.search(inputStr) :
            if p_0.match(inputStr):
                return False
            else:
                print '//',inputStr
                return True
        else:
            p = re.compile('^(' + parten + ')')
            if p.search(inputStr) :
                print parten,p.search(inputStr).group()
                return True
            else:
                return False
             
    #def test():
    #    '''
    #    C:/AW/Maya5.0/sourceimages/maya.exe     sourceimages/maya.exe
    #    C:/AW/Maya5.0/sourceimages/maya.exe     sourceimages/maya.exe
    #    /sourceimages/maya.exe     sourceimages/maya.exe
    #    sourceimages/maya.exe     sourceimages/maya.exe
    #    //sourceimages/maya.exe     sourceimages/maya.exe
    #    '''
    #    nodes = ['C:/AW/Maya5.0/sourceimages/maya.exe','C:/AW/Maya5.0\\sourceimages/maya.exe',\
    #'\\sourceimages/maya.exe','sourceimages/maya.exe','//sourceimages/maya.exe','']
    #    convertToRelative('sourceimages',nodes)
    #    convertToRelative('sourceimages',nodes[0])
    #    
    #test()
def main():
    a = RelativePath()
    a.convert_reference_to_relative()
    
if __name__ == '__main__' :
    main()
    