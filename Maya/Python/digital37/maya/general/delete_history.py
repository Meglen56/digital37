import maya.cmds as cmds

def main(log=None):

    if not log:
        import logging
        log = logging.getLogger()
    
    allObj = cmds.ls(dag=True,lf=True,type = ['mesh', 'nurbsSurface', 'subdiv'])
    delHis = set()
    for x in allObj:
        try:
            cmds.delete(x, ch = True)
            delHis.add(x)
        #TODO for some not exists polygon shape
        except ValueError:
            pass
        except:
            log.warning("delete history error:%s" %x)
            import traceback
            log.error(traceback.format_exc())
            
    if delHis:
        log.warning("delete history success:\n%s" % (' '.join(delHis)) )