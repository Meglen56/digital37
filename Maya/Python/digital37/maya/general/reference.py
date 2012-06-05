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
    
    def get_top_ref_node(self):
        ref_nodes = pm.ls(type='reference')
        if ref_nodes:
            # Get top level reference nodes
            for ref_node in ref_nodes :
                isTopRef = False
                try:
                    isTopRef = pm.system.referenceQuery(ref_node,topReference=1,referenceNode=1)
                except:
                    self.Log.error( traceback.format_exc() )
                else:
                    if isTopRef :
                        self.Ref_Node_Top.add(ref_node)

    def get_unload_ref_node(self):
        if self.Ref_Node_Top:
            for ref_node in self.Ref_Node_Top:
                # Check reference node is loaded or not
                if ref_node.isLoaded():
                    self.Ref_Node_Unload.add(ref_node)
        
    def remove_ref_node(self,ref_nodes):
        for ref_node in ref_nodes:
            try:
                ref_node.remove()
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
        
    def convert_to_relative_path(self,ref_nodes):
        for ref_node in ref_nodes:
            # if reference file is not load
            if ref_node.isLoaded() :
                self.Log.warning('%s has not been loaded' % ref_node.name())
                
                file_name = ''
                # Get reference node's file name
                try:
                    # use unresolvedName flag to get unresolvedName name
                    file_name= pm.system.referenceQuery(ref_node,filename=1,unresolvedName=1)
                except:
                    self.Log.error( traceback.format_exc() )
                else:
                    if file_name:
                        #print file_name
                        #self.Reference_File_Names.add(file_name)
                        if not self.check_relative('scenes', file_name):
                            self.Log.warning('%s is not relative path' % file_name)
                            file_name_after = self.convert_to_relative('scenes', file_name)
                            ref_node.load(file_name_after)
                        else:
                            self.Log.debug('%s is relative path' % file_name)


def main():
    a = Reference()
    a.get_file_logger(None, 'debug')
    a.convert_all_ref_nodes_to_relative_path()
    
if __name__ == '__main__' :
    main()
    #pass
    
    