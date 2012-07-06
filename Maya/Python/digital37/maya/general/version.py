import maya.cmds as cmds

def get_version():
    return cmds.about(version=True)

def check_version(log=None,inputVersion='2012'):
    if not log:
        import logging
        log = logging.getLogger()
    if get_version().find(inputVersion):
        return True
    else:
        log.warning('file version:%s' % get_version())
        return False