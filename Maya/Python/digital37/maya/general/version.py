import maya.cmds as cmds

def check_version(log=None,inputVersion='2012'):
    if not log:
        import logging
        log = logging.getLogger()
    v = cmds.about(v=True)
    if v.find(inputVersion) == 0:
        log.debug('maya file version:%s' % v)
        return True
    else:
        log.warning('maya file version:%s' % v)
        return False