import maya.mel as mel
import maya.cmds as cmds

def main(log=None,configureDirectory=None):
    '''
    apply render settings by preset
    configureDirectory: folder for store some project configure settings,\
    include frameInfo.ini and presets sub folder
    frameInfo.ini: seer_ani_ep13_sc0010    1    145
                   seer_ani_ep13_sc0020    1    210
    presets folder: renderGlobalsPreset_renderSettings.mel
                    resolutionPreset_renderSettings.mel  
    '''
    
    # use "renderSettings" for standard preset name
    PRESET_NAME = 'renderSettings'
    
    if not log:
        import logging
        log = logging.getLogger()
    # use ' ' as a fill char and center aligned
    log.debug('{0:-<40}'.format('set_render_settings'))
    
    # if frameSettingsFile then do playback range settings
    import os
    renderSettingsFile = os.path.join(configureDirectory,'presets',\
                                      ('resolutionPreset_%s.mel' % PRESET_NAME))
    preset_path = os.path.normpath( os.path.join(configureDirectory,'presets') )
    preset_path = preset_path.replace('\\','/')
    log.debug('preset_path:%s' % preset_path)
    # check preset exists or not
    if os.path.exists( renderSettingsFile ):
        log.debug('preset file exists')
        # define MAYA_PRESET_PATH
        preset_path_before = os.environ.get('MAYA_PRESET_PATH')
        p = None
        p = preset_path_before.split(';')
        if p:
            if preset_path not in p :
                p = preset_path_before + ';' +  preset_path
            else:
                p = preset_path_before
        else:
            p = preset_path
        # set MAYA_PRESET_PATH
        os.environ['MAYA_PRESET_PATH'] = p
        log.debug('MAYA_PRESET_PATH:%s' % p)
        
        # initialize mentalray
        import digital37.maya.lighting.mentalray as mentalray
        reload(mentalray)
        mentalray.init_mentalray(log)
        
        # TODO: only check mentalray presets
        print cmds.nodePreset( list='mentalrayGlobals' )
        
        if cmds.nodePreset( exists=('mentalrayGlobals', PRESET_NAME) ):
            # apply preset
            try:
                mel.eval('loadNodePresets "renderSettings"')
            except:
                import traceback
                log.error(traceback.format_exc())
            else:
                log.debug('apply renderSettings preset success.')
        # no preset file
        else:
            log.debug('set_render_settings: there is no preset file with the name:%s' % PRESET_NAME)
            
        