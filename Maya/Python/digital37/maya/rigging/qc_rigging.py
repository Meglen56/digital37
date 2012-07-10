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
    
    # maya version
    import digital37.maya.general.version as version
    reload(version)
    if not version.check_version(a.Log):
        stat = False

    # delete perspective cameras
    import digital37.maya.general.camera as camera
    reload(camera)
    camera.delete_perspective_camera(a.Log)
    
    # zero transform
    import digital37.maya.general.make_identity as make_identity
    reload(make_identity)
    make_identity.main(a.Log)
    
    # delete display layer
    # source cleanUpScene.mel first
    #mel.eval('source "cleanUpScene.mel"')
    #mel.eval( 'deleteEmptyLayers("Display")' )
    import digital37.maya.general.delete_display_layer as delete_display_layer
    reload(delete_display_layer)
    delete_display_layer.main(a.Log)
    
    # delete empty render layer
    #mel.eval( 'deleteEmptyLayers("Render")' )
    import digital37.maya.general.delete_render_layer as delete_render_layer
    reload(delete_render_layer)
    delete_render_layer.main(a.Log)
    
    # source cleanUpScene.mel first
    mel.eval('source "cleanUpScene.mel"')
    
    # remove unused rendering node
    # mel command
    mel.eval('MLdeleteUnused()')

    import digital37.maya.lighting.delete_light as delete_light
    reload(delete_light)
    delete_light.main(a.Log)
    
    # remove light linker
    mel.eval('jrLightLinksCleanUp()')

    # remove unknown node
    import digital37.maya.general.delete_unknow_node as delete_unknow_node
    reload(delete_unknow_node)
    delete_unknow_node.main(a.Log)
    
    # remove opened windows
    import digital37.maya.general.remove_open_windows as remove_open_windows
    reload(remove_open_windows)
    remove_open_windows.main(a.Log)
    
    # set "outliner/persp" view and set low quality display
    import digital37.maya.general.panel as panel
    reload(panel)
    panel.Panel().set_outliner_persp()
    
    # check face with more than 4 edges
    import digital37.maya.modeling.check_face_with_5_edge as check_face_with_5_edge
    reload(check_face_with_5_edge)
    if not check_face_with_5_edge.main(a.Log):
        stat = False
    
    # check animCurve
    import digital37.maya.animation.animCurve as animCurve
    reload(animCurve)
    animCurve.check_nurbsCurve_with_key(a.Log)
    
    # write file info (time and qc value) to maya file
    import digital37.maya.general.fileInfo as fileInfo
    fileInfo.write(stat)
    
    # close logger file, so can open file with other application
    # stream logger has no attribute 'handler' 
    try:
        a.Handler.close()
    except:
        pass
    
    return stat