import os
import pymel.core as pm

import system.log as log
reload(log)
import system.system as system
#import digital37.maya.general.RelativePath as relativePath
#reload(relativePath)

class QC_Animation(log.Log,system.System):
    def __init__(self):
        self.Scene_Name = ''
        self.Options = dict()
        self.Frame_Info = dict()
        #relativePath.RelativePath.__init__(self)

    def get_scene_name(self):
        self.Scene_Name = pm.system.sceneName()
        self.Scene_Name_Short = os.path.splitext( os.path.basename( self.Scene_Name ) )[0]
        return self.Scene_Name
    
    def get_general_settings(self,fileName):
        with open(fileName,'r') as f:
            for x in f:
                k,v = x.strip().split(':')
                self.Options[k] = v

#    def get_Playback_info(self,frameInfo):
#        try:
#            f = open( frameInfo ,'r' )
#        except IOError:
#            self.Log.error('Could not open %s' % f)
#        else:
#            for x in f.readlines():
#                k = x.strip().split()[0]
#                v0 = x.strip().split()[1]
#                v1 = x.strip().split()[2]
#                self.Frame_Info[k] = (v0,v1)
#                    
#                f.close()
    def get_playback_settings(self,fileName):
        with open( fileName ,'r' ) as f:
            for x in f:
                if x:
                    y = x.strip().split()
                    if len(y) == 3:
                        self.Frame_Info[y[0]] = (y[1],y[2])


def main(generalSettingsFile=None,playbackSettingsFile=None,logFile=None,logLevel='debug'):
    
    a = QC_Animation()
    
    # set logger
    a.get_file_logger( logFile, logLevel )
    
    a.Log.error( '\r\n\r\n%s' % a.get_scene_name() )
    
    # if generalSettingsFile then do some general checking
    if generalSettingsFile:
        a.get_general_settings(generalSettingsFile)
        # set defaultResolution's width and height
        import digital37.maya.lighting.set_render_resolution as set_render_resolution
        reload(set_render_resolution)
        set_render_resolution.main( a.Options['defaultResolution.w'],a.Options['defaultResolution.h'],a.Log ) 
    
    # if playbackSettingsFile then do playback setting
    if playbackSettingsFile:
        a.get_playback_settings(playbackSettingsFile)
        if a.Scene_Name_Short in a.Frame_Info.iterkeys() :
            import digital37.maya.animation.set_playback as set_playback
            reload(set_playback)
            set_playback.main(a.Frame_Info[a.Scene_Name_Short][0],a.Frame_Info[a.Scene_Name_Short][1],a.Log )
        
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
    