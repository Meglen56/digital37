import pymel.core as pm
print 'import pymel.core as pm'

import pymel.mayautils

import digital37.maya.general.menu
pymel.mayautils.executeDeferred(digital37.maya.general.menu.loadMenu)
print 'create 37digital custom menu'

import maya.mel
#Init deadline submission script
maya.mel.eval('source InitDeadlineSubmitter.mel')
print 'source InitDeadlineSubmitter.mel'
# load needed plugin


#import digital37.maya.AEgNodeTemplate

#import digital37.maya.general.scriptJobFonction
#pm.scriptJob (event=["SceneOpened",digital37.maya.general.scriptJobFonction.open],permanent=True)
#print 'activate open script job'

#print 'login'
#import digital37.maya.general.login
#pymel.mayautils.executeDeferred(digital37.maya.general.login.loginUI)