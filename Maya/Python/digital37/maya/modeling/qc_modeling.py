import system.log as log
reload(log)

import digital37.maya.general.scene as scene
reload(scene)

import digital37.maya.modeling.turn_off_double_display as turn_off_double_display
reload(turn_off_double_display)

import digital37.maya.modeling.check_face_with_5_edge as check_face_with_5_edge
reload(check_face_with_5_edge)

import digital37.maya.modeling.normalizeUV as normalizeUV
reload(normalizeUV)

import digital37.maya.general.camera as camera
reload(camera)

import digital37.maya.general.make_identity as make_identity
reload(make_identity)

import digital37.maya.general.delete_display_layer as delete_display_layer 
reload(delete_display_layer)

import digital37.maya.general.delete_empty_group as delete_empty_group
reload(delete_empty_group)

import digital37.maya.general.delete_history as delete_history
reload(delete_history)

import digital37.maya.general.delete_render_layer as delete_render_layer
reload(delete_render_layer)

import digital37.maya.lighting.delete_light as delete_light
reload(delete_light)

import digital37.maya.lighting.fileTexture as fileTexture 
reload(fileTexture)

def main(logFile=None,logLevel='debug'):
    '''
    qc for modeling
    '''
    # use file's log
    if logFile:
        a=log.Log()
        
        # set logger
        a.get_file_logger( logFile, logLevel )
        
        s = scene.Scene()
        s.get_scene_name()
        a.Log.error( '\r\n\r\n%s' % s.Scene_Name_Full_Path_Without_Ext )
        log = a.Log
    # use stream's log
    else:
        import logging
        log = logging.getLogger()
        
    #
    turn_off_double_display.main(log)
    
    #
    check_face_with_5_edge.main(log)
    
    #
    normalizeUV.main(log)
    
    # delete perspective cameras
    camera.delete_perspective_camera(log)
    
    # zero transform
    make_identity.main(log)
    
    delete_display_layer.main(log)
    
    delete_empty_group.main(log)
    
    delete_render_layer.main(log)
    
    delete_history.main(log)
    
    delete_light.main(log)
    
    # convert file texture's file name to relative
    fileTexture.FileTexture(log).convert_all_texture_to_relative()