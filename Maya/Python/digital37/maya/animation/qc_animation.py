import system.log as log
reload(log)

import system.system as system

import digital37.maya.general.scene as scene
reload(scene)

class QC_Animation(log.Log,system.System,scene.Scene):
    def __init__(self):
        self.Scene_Name = ''
        self.Options = dict()
        self.Frame_Info = dict()
        #relativePath.RelativePath.__init__(self)
    
    def get_general_settings(self,fileName):
        with open(fileName,'r') as f:
            for x in f:
                k,v = x.strip().split(':')
                self.Options[k] = v

    def get_playback_settings(self,fileName):
        with open( fileName ,'r' ) as f:
            for x in f:
                if x:
                    y = x.strip().split()
                    if len(y) == 3:
                        self.Frame_Info[y[0]] = (y[1],y[2])


#def main(logFile=None,logLevel='debug',generalSettingsFile=None,playbackSettingsFile=None):
def main(logFile=None,logLevel='debug',configureDirectory=None):
    '''
    configureDirectory: folder for store some project configure settings,\
    include frameInfo.ini and presets sub folder
    frameInfo.ini: seer_ani_ep13_sc0010    1    145
                   seer_ani_ep13_sc0020    1    210
    presets folder: renderGlobalsPreset_renderSettings.mel
                    resolutionPreset_renderSettings.mel
    '''
    
    a = QC_Animation()
    
    # set logger
    a.get_file_logger( logFile, logLevel )
    
    a.get_scene_name()
    a.Log.error( '\r\n\r\n%s' % a.Scene_Name_Full_Path_Without_Ext )
    
#    # if generalSettingsFile then do some general checking
#    if generalSettingsFile:
#        a.get_general_settings(generalSettingsFile)
#        # set defaultResolution's width and height
#        import digital37.maya.lighting.set_render_resolution as set_render_resolution
#        reload(set_render_resolution)
#        set_render_resolution.main( a.Options['defaultResolution.w'],a.Options['defaultResolution.h'],a.Log ) 
    
    # if frameSettingsFile then do playback range settings
    import os.path
    frameSettingsFile = os.path.join(configureDirectory,'frameInfo.ini')
    if os.path.exists( frameSettingsFile ) :
        a.get_playback_settings(frameSettingsFile)
        if a.Scene_Name_Short_Without_Ext in a.Frame_Info.iterkeys() :
            import digital37.maya.animation.set_playback as set_playback
            reload(set_playback)
            set_playback.main(a.Frame_Info[a.Scene_Name_Short_Without_Ext][0],\
                              a.Frame_Info[a.Scene_Name_Short_Without_Ext][1],a.Log )
        
    # set render settings
    import digital37.maya.lighting.set_render_settings as set_render_settings
    reload(set_render_settings)
    set_render_settings.main(a.Log, configureDirectory)
    
    # get renderable camera 
    # lock camera
    # set camera's attribute
    import digital37.maya.general.camera as camera
    reload(camera)
    camera.Camera(a.Log).check_renderable_camera('cam_')

    import digital37.maya.general.delete_unknow_node as delete_unknow_node
    reload(delete_unknow_node)
    delete_unknow_node.main(a.Log)
    
    import digital37.maya.general.remove_open_windows as remove_open_windows
    reload(remove_open_windows)
    remove_open_windows.main(a.Log)
    
    # check relative path for reference
    #a.convert_reference_to_relative(a.Log)
    
if __name__ == '__main__' :
    #main()
    pass
    