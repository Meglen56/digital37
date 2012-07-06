import maya.cmds as cmds

def write(v):
    '''
    write qc date and qc value to file info
    '''
    import time
    cmds.fileInfo('qc_date',time.ctime())
    cmds.fileInfo('qc_value',str(v))
    
def read(log=None):
    r1=None
    r2=None
    qc_date = cmds.fileInfo('qc_date',query=True)
    if qc_date:
        log.debug('qc date:%s' % qc_date[0])
        r1 = qc_date[0]
    qc_value = cmds.fileInfo('qc_value',query=True)
    if qc_value:
        log.debug('qc value:%s' % qc_value[0])
        r2 = qc_value[0]
    return (r1,r2)