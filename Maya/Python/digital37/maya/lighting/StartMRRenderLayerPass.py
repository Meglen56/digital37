import sys
import sip
from PyQt4 import QtCore, QtGui
import maya.OpenMayaUI as mui

# Make MRRenderLayerPassUI by: pyuic4 MRRenderLayerPass.ui>MRRenderLayerPassUI.py
from digital37.maya.lighting.MRRenderLayerPassUI import Ui_root

class StartMRRenderLayerPass(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_root()
        self.ui.setupUi(self)
        
def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

def main():
    global MRRenderLayerPass_app
    global MRRenderLayerPass_myapp
    MRRenderLayerPass_app = QtGui.qApp
    MRRenderLayerPass_myapp = StartMRRenderLayerPass(getMayaWindow())
    MRRenderLayerPass_myapp.show()

if __name__ == "__main__":
    main()

