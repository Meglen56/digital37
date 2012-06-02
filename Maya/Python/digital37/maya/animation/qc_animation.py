import os
import pymel.core as pm
import maya.cmds as cmds

import system.log as log
reload(log)
import system.system as system

class QC_Animation(log.Log,system.System):
    def __init__(self):
        self.Scene_Name = ''
        self.Options = dict()
        self.Frame_Info = dict()
        
    def set_log(self,logDir):
        self.Log = self.get_logger( logDir, 'qc_animation.log' )

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
                k,v0,v1 = x.strip().split()
                self.Frame_Info[k] = (v0,v1)


def main(logDir=None,generalSettingsFile=None,playbackSettingsFile=None):
    
    a = QC_Animation()
    
    info=list()
    debug=list()
    error=list()
    s = '\r\nscenes:\t%s' % a.get_scene_name()
    info.append( (s,s) )
    
    # set logger
    a.set_log(logDir)
    
    # if generalSettingsFile then do some general checking
    if generalSettingsFile:
        a.get_general_settings(generalSettingsFile)
        # set defaultResolution's width and height
        import digital37.maya.lighting.set_render_resolution as set_render_resolution
        reload(set_render_resolution)
        info.append( set_render_resolution.main( a.Options['defaultResolution.w'],a.Options['defaultResolution.h'] ) )
    
    # if playbackSettingsFile then do playback setting
    if playbackSettingsFile:
        a.get_playback_settings(playbackSettingsFile)
        if a.Scene_Name_Short in a.Frame_Info.iterkeys() :
            import digital37.maya.animation.set_playback as set_playback
            reload(set_playback)
            info.append( set_playback.main(a.Frame_Info[a.Scene_Name_Short][0],\
                                           a.Frame_Info[a.Scene_Name_Short][1]) )
        
    import digital37.maya.general.check_camera as check_camera
    reload(check_camera)
    info.append( check_camera.main() )

    import digital37.maya.general.delete_unknow_node as delete_unknow_node
    reload(delete_unknow_node)
    info.append( delete_unknow_node.main() )
    
    import digital37.maya.general.remove_open_windows as remove_open_windows
    reload(remove_open_windows)
    info.append( remove_open_windows.main() )

#    print info
#    for i in info:
#        print 'i:',i
#        print type(i)
#        debug.append(i[0])
#        error.append(i[1])
    [(debug.append(i[0]),error.append(i[1])) for i in info]
        
    debug = '\r\n'.join(debug)
    error = '\r\n'.join(error)

    a.Log.debug( debug+'\r\n\r\n' )
    a.Log.error( error+'\r\n\r\n' )
    
if __name__ == '__main__' :
    #main()
    pass
    