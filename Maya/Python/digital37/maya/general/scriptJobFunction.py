import pymel.core as pm

def open():
    pm.mel.eval('EnableAll')
    #pm.currentUnit(l='centimeter',time='film')
    # get current project
    if 'rovio' in pm.workspace(q=1,rd=1) :
        # SVN update
        import digital37.maya.file.StartSvnMaya
        digital37.maya.file.StartSvnMaya.update()