import os.path
import traceback
import pymel.core as pm

class Scene():
    def __init__(self):
        pass
    
    def get_scene_name(self):
        self.Scene_Name_Full_Path = pm.system.sceneName()
        self.Scene_Name_Full_Path_Without_Ext = os.path.splitext( self.Scene_Name_Full_Path )[0]
        self.Scene_Name_Short = os.path.basename( self.Scene_Name_Full_Path )
        self.Scene_Name_Short_Without_Ext = os.path.splitext( self.Scene_Name_Short )[0]
        
    def get_playback_info(self):
        return ( int(pm.playbackOptions(q=1, min=1)), int(pm.playbackOptions(q=1, max=1)) )
