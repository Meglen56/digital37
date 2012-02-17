import pymel.core as pm

def open():
    pm.mel.eval('EnableAll')
    #pm.currentUnit(l='centimeter',time='film')
    # get current project
    if 'mhxy' in pm.workspace(q=1,rd=1) :
        # SVN update
        import digital37.maya.general.StartSvnMaya
        digital37.maya.general.StartSvnMaya.main()