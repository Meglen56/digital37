import sys
import sip
from PyQt4 import QtCore, QtGui
import maya.OpenMayaUI

# Make MRRenderLayerPassUI by: pyuic4 MRRenderLayerPassManager.ui>MRRenderLayerPassManagerUI.py
import digital37.maya.lighting.MRRenderLayerPassManagerUI
# reload only for tests
reload(digital37.maya.lighting.MRRenderLayerPassManagerUI)

import digital37.maya.lighting.MRRenderLayerPass
# reload only for tests
reload(digital37.maya.lighting.MRRenderLayerPass)

class StartMRRenderLayerPassManager(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = digital37.maya.lighting.MRRenderLayerPassManagerUI.Ui_root()
        self.ui.setupUi(self)
        self.RLP = digital37.maya.lighting.MRRenderLayerPass()
        
    def on_pushButton_RL_refresh_pressed(self):
        # Get render layers
        self.renderLayers = self.RLP.getRenderLayers()
        if self.renderLayers
                
def getMayaWindow():
    ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

def main():
    global MRRenderLayerPassManager_app
    global MRRenderLayerPassManager_myapp
    MRRenderLayerPassManager_app = QtGui.qApp
    MRRenderLayerPassManager_myapp = StartMRRenderLayerPassManager(getMayaWindow())
    MRRenderLayerPassManager_myapp.show()

if __name__ == "__main__":
    main()

