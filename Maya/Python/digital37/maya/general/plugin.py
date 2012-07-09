import maya.cmds as cmds

def reload_plugin(plugin_name):
    '''
    Safely reloading a plug-in without restarting Maya
    '''
    # clear the scene
    cmds.file(f=True, new=True)
    
    # Clear the undo queueW
    cmds.flushUndo()
    
    # Unload the plug-in
    cmds.unloadPlugin(plugin_name)
    
    # Reload the plug-in
    cmds.loadPlugin(plugin_name)
    
def load_plugin(plugin_name):
    '''
    loading a plug-in
    '''
    if not cmds.pluginInfo( plugin_name, query=True, loaded=True ) :
        cmds.loadPlugin( plugin_name )
    