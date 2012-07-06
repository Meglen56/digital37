import maya.cmds as cmds
import maya.mel as mel

class Panel():
    '''
    panel
    '''
    def __init__(self):
        pass
    
    def get_focus_panel(self):
        panel_focus = cmds.getPanel(withFocus=1)
        print 'panel_focus:%s' % panel_focus
        return panel_focus
        
    def set_named_panel_layout(self,panel_layout_name):
        mel.eval('setNamedPanelLayout "%s"' % panel_layout_name)
        
    def set_panel_display_mode(self,mode):
        mel.eval(mode)
        
    def set_outliner_persp(self):
        # set named panel layout
        self.set_named_panel_layout('Persp/Outliner')
        # get persp panel
        perspPanel = cmds.getPanel( withLabel='Persp View')
        # set foucs to persp panel
        cmds.setFocus(perspPanel)
        # set display mode to wireFrame
        mel.eval('DisplayWireframe')
        # set low quality display
        mel.eval('LowQualityDisplay')
