import maya.mel as mel

import system.log
reload(system.log)

def main(logFile=None,logLevel='debug'):
    '''
    qc for modeling\
    return False or True
    '''
    stat = True
    
    # set logger 
    a=system.log.Log()
    # use file's log
    if logFile:
        # set logger
        a.get_file_logger( logFile, logLevel )
        
        import digital37.maya.general.scene as scene
        reload(scene)
        
        s = scene.Scene()
        s.get_scene_name()
        a.Log.error( '\r\n\r\n%s' % s.Scene_Name_Full_Path_Without_Ext )
    # use stream's log
    else:
        a.get_stream_logger(logLevel)
        
    log = a.Log
    
    # maya version
    import digital37.maya.general.version as version
    reload(version)
    if not version.check_version(log):
        stat = False
    
    # turn off double display
    import digital37.maya.modeling.turn_off_double_display as turn_off_double_display
    reload(turn_off_double_display)
    turn_off_double_display.main(log)
    
    # normal uv to 0-1
    import digital37.maya.modeling.normalizeUV as normalizeUV
    reload(normalizeUV)
    normalizeUV.main(log)
    
    # delete perspective cameras
    import digital37.maya.general.camera as camera
    reload(camera)
    camera.delete_perspective_camera(log)
    
    # zero transform
    import digital37.maya.general.make_identity as make_identity
    reload(make_identity)
    make_identity.main(log)
    
    # delete empty display layer
    # source cleanUpScene.mel first
    mel.eval('source "cleanUpScene.mel"')
    mel.eval( 'deleteEmptyLayers("Display")' )
    
    # delete empty render layer
    mel.eval( 'deleteEmptyLayers("Render")' )
    
    # remove unused locator
    mel.eval( 'deleteUnusedLocators()' )
    
    # remove unused rendering node
    # mel command
    mel.eval('MLdeleteUnused()')
    
    # remove empty transform
    mel.eval( 'deleteEmptyGroups()' )
    
    import digital37.maya.general.delete_history as delete_history
    reload(delete_history)
    delete_history.main(log)
    
    import digital37.maya.lighting.delete_light as delete_light
    reload(delete_light)
    delete_light.main(log)
    
    # remove light linker
    mel.eval('jrLightLinksCleanUp()')
        
    # convert file texture's file name to relative
    #fileTexture.FileTexture(log).convert_all_texture_to_relative()
    # check file texture exists or not
    import digital37.maya.lighting.fileTexture as fileTexture
    reload(fileTexture)
    fileTexture.FileTexture(log).check_file_texture_exists()
    
    # remove unknown node
    import digital37.maya.general.delete_unknow_node as delete_unknow_node
    reload(delete_unknow_node)
    delete_unknow_node.main(log)
    
    # remove opened windows
    import digital37.maya.general.remove_open_windows as remove_open_windows
    reload(remove_open_windows)
    remove_open_windows.main(log)
    
    # set "outliner/persp" view and set low quality display
    import digital37.maya.general.panel as panel
    reload(panel)
    panel.Panel().set_outliner_persp()
    
    # check face with more than 4 edges
    import digital37.maya.modeling.check_face_with_5_edge as check_face_with_5_edge
    reload(check_face_with_5_edge)
    if not check_face_with_5_edge.main(log):
        stat = False
    
    # write file info (time and qc value) to maya file
    import digital37.maya.general.fileInfo as fileInfo
    fileInfo.write(stat)
    
    return stat
    