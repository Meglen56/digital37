def reload_plugin(plugin_name):
    '''
    Safely reloading a plug-in without restarting Maya
    '''
    import maya.cmds as cmds
    
    # clear the scene
    cmds.file(f=True, new=True)
    
    # Clear the undo queueW
    cmds.flushUndo()
    
    # Unload the plug-in
    cmds.unloadPlugin(plugin_name)
    
    # Reload the plug-in
    cmds.loadPlugin(plugin_name)
    
    