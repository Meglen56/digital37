import maya.cmds as cmds
import traceback

def main(log=None):
    if not log:
        import logging
        log = logging.getLogger()
    # use ' ' as a fill char and center aligned
    log.debug('{0:-<40}'.format('remove_open_windows'))

    wins = cmds.lsUI(wnd=True)
    if wins:
        for x in wins  :
            if ( cmds.window(x,q=True,vis=True) and x != 'MayaWindow' ) :
                #print x
                # remove scriptEditor will cause maya crash ,so set scriptEditorPanel1Window vis to false
                if x != 'scriptEditorPanel1Window' :
                    try: 
                        cmds.deleteUI(x,window=True)
                    except:
                        log.error('delete window %s error' % x)
                        log.error(traceback.format_exc())
                    else:
                        log.debug('delete window %s success' % x)
                else:
                    # close scriptEditor
                    cmds.window(x,e=True,vis=False)
                    log.warning('close window %s' % x)