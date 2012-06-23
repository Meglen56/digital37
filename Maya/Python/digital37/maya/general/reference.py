import re
import os.path
import traceback
import pymel.core as pm

import system.log as log
reload(log)

class Reference(log.Log):
    def __init__(self):
        self.Ref_Node_Top = set()
        self.Ref_Node_Unload = set()
        self.Ref_Node_No_File = set()
    
    def get_top_ref_node(self):
        ref_nodes = pm.ls(type='reference')
        if ref_nodes:
            # Get top level reference nodes
            for ref_node in ref_nodes :
                isTopRef = False
                # Get reference node's file name
                try:
                    isTopRef = pm.system.referenceQuery(ref_node,topReference=1,referenceNode=1)
                except:
                    # reference node is not associated with a reference file
                    self.Log.warning('%s is not associated with a reference file' % ref_node.name())
                    #self.Log.error( traceback.format_exc() )
                    self.Ref_Node_No_File.add(ref_node)
                else:
                    if isTopRef :
                        self.Ref_Node_Top.add(ref_node)

    def get_unload_ref_node(self):
        if self.Ref_Node_Top:
            for ref_node in self.Ref_Node_Top:
                # create FileReference object by reference node
                file_ref = pm.system.FileReference(ref_node)
                # Check reference node is loaded or not
                if not file_ref.isLoaded():
                    self.Ref_Node_Unload.add(ref_node)
        
    def remove_unload_ref_node(self):
        self.get_top_ref_node()
        self.get_unload_ref_node()
        self.remove_ref_node(self.Ref_Node_Unload)
        
    def remove_ref_node(self,ref_nodes):
        for ref_node in ref_nodes:
            try:
                pm.lockNode( ref_node, lock=False )
                file_ref = pm.system.FileReference(ref_node)
                file_ref.remove()
            except:
                self.Log.error( 'can not remove %s' % ref_node.name() )
                self.Log.error( traceback.format_exc() )
            else:
                self.Log.debug( 'remove %s success' % ref_node.name() )
        
    def convert_all_ref_nodes_to_relative_path(self):
        #get ref nodes
        self.get_top_ref_node()
        #convert to relative path
        self.convert_to_relative_path(self.Ref_Node_Top)
        
    def remove_ref_node_with_no_file_associated(self):
        self.get_top_ref_node()
        self.remove_ref_node(self.Ref_Node_No_File)
        
    def remove_failed_edits(self,ref_nodes):
        for ref_node in ref_nodes:
            #unload reference node first
            file_ref = pm.system.FileReference(ref_node)
            
            unload = False
            # if reference file is not load
            if not file_ref.isLoaded() :
                self.Log.warning('%s has not been loaded' % ref_node.name())
                unload = True
            else:
                file_ref.unload()
                
            # remove edits
            import maya.cmds as cmds
            try:
                cmds.referenceEdit(ref_node.name(),removeEdits=True,\
                                   successfulEdits=False,failedEdits=True)
            except:
                self.Log.error('%s remove reference edits error' % ref_node.name())
            else:
                self.Log.debug('%s remove reference edits success' % ref_node.name())
            
            if not unload:
                file_ref.load()
        
    def remove_all_failed_edits(self):
        self.get_top_ref_node()
        self.remove_failed_edits(self.Ref_Node_Top)
        
    def convert_to_relative_path(self,ref_nodes):
        for ref_node in ref_nodes:
            # create FileReference object by reference node
            file_ref = pm.system.FileReference(ref_node)
            isUnload = False
    
            # if reference file is not load
            if not file_ref.isLoaded() :
                self.Log.warning('%s has not been loaded' % ref_node.name())
                isUnload = True
                
            file_name = ''
            try:
                # use unresolvedName flag to get unresolvedName name
                file_name = file_ref.unresolvedPath()
            except:
                self.Log.error( traceback.format_exc() )
            else:
                if file_name:
                    #print file_name
                    #self.Reference_File_Names.add(file_name)
                    if not self.check_relative('scenes', file_name):
                        self.Log.warning('%s is not relative path' % file_name)
                        file_name_after = self.convert_to_relative('scenes', file_name)
                        # replace a reference without triggering reload with 'loadReferenceDepth' flag
                        file_ref.replaceWith(file_name_after,loadReferenceDepth='none')
                        if isUnload :
                            file_ref.unload()
                    else:
                        self.Log.debug('%s is relative path' % file_name)
        
    
    def convert_to_relative(self,parten,inputStr):
        '''
        example: convertToRelative('sourceimages','C:/AW/Maya5.0/sourceimages/maya.exe')
        result: 'sourceimages/maya.exe'
        '''
        #p = re.compile('^.*/sourceimages')
        inputStr = str(inputStr).replace('\\','/')
        returnStr = re.sub( ('^.*/(' + parten + ')'), parten, inputStr )
        self.Log.debug('source:\t%s' % inputStr)
        self.Log.debug('target:\t%s' % returnStr)
        return returnStr

    def check_relative(self,parten,inputStr):
        self.Log.debug('check relative path input:%s' % inputStr)
        if inputStr.startswith( parten ) :
            return True
        else:
            return False
        
def main():
    a = Reference()
    a.get_file_logger(None, 'debug')
    #a.convert_all_ref_nodes_to_relative_path()
    #a.remove_ref_node_with_no_file_associated()
    #a.remove_unload_ref_node()
    a.remove_all_failed_edits()
    
if __name__ == '__main__' :
    main()
    #pass
