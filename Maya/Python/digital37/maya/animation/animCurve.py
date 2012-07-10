import maya.cmds as cmds

def get_animCurve():
    return cmds.ls(type='animCurve')

def check_nurbsCurve_with_key(log=None):
    if not log:
        import logging
        log = logging.getLogger()
        
    # get control curve, control curve is nurbs curve
    for x in cmds.ls(type='nurbsCurve'):
        # get parent transform node
        trans = cmds.listRelatives(x,parent=True)
        if trans:
            # get transform's input connection
            connections = trans[0].connections(d=1)
            if connections:
                for c in connections :
                    # is animCurve node or not
                    if cmds.nodeType( c ) == 'animCurve':
                        # get animCurve's input connection
                        con_anim = c.connections(d=1)
                        if not con_anim:
                            # animCurve has no input connection
                            # so animCurve is key animation and not set driven key animation curve
                            log.warning('The transform node has animation key:%s' % trans[0])
                        else:
                            log.debug('The transform node has set driven animation key:%s' % trans[0])
                        