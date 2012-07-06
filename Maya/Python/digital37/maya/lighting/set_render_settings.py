import maya.mel as mel

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
    if not log:
        import logging
        log = logging.getLogger()
    # use ' ' as a fill char and center aligned
    log.debug('{0:-<40}'.format('set_render_settings'))
    
    # if frameSettingsFile then do playback range settings
    import os
    renderSettingsFile = os.path.join(configureDirectory,'presets',\
                                      'resolutionPreset_renderSettings.mel')
    preset_path = os.path.normpath( os.path.join(configureDirectory,'preset') )
    if os.path.exists( renderSettingsFile ):
        # define MAYA_PRESET_PATH
        p = os.environ.get('MAYA_PRESET_PATH')
        if p:
            if p.find(preset_path) != -1 :
                p += ';' +  preset_path
        else:
            p = preset_path
        # set MAYA_PRESET_PATH
        os.environ.setdefault('MAYA_PRESET_PATH', p)
        log.debug('MAYA_PRESET_PATH:%s' % p)
        
        # apply preset
        try:
            mel.eval('loadNodePresets "renderSettings"')
        except:
            import traceback
            log.error(traceback.format_exc())
        else:
            log.debug('apply renderSettings prest success.')
    