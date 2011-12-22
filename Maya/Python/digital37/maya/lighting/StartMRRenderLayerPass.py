import sys
import sip
from PyQt4 import QtCore, QtGui
import maya.OpenMayaUI

# Make MRRenderLayerPassUI by: pyuic4 MRRenderLayerPass.ui>MRRenderLayerPassUI.py
import digital37.maya.lighting.MRRenderLayerPassUI 
# reload only for tests
reload(digital37.maya.lighting.MRRenderLayerPassUI)

import digital37.maya.lighting.MRRenderLayerPass
# reload only for tests 
reload(digital37.maya.lighting.MRRenderLayerPass)

class StartMRRenderLayerPass(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = digital37.maya.lighting.MRRenderLayerPassUI.Ui_root()
        self.ui.setupUi(self)
        
    def on_pushButton_CRL_ao_pressed(self):
        MRRenderLayerPass.MRRenderLayer().createAmbientOcclusionLayer()
        
    def on_pushButton_RS_apply_pressed(self):
        #Get widget status
        #Define a dict
        renderStatus = {'castsShadows':[self.ui.checkBox_castsShadows,1],\
                        'receiveShadows':[self.ui.checkBox_receiveShadows,1],\
                        'motionBlur':[self.ui.checkBox_motionBlur,1],\
                        'primaryVisibility':[self.ui.checkBox_primaryVisibility,1],\
                        'smoothShading':[self.ui.checkBox_smoothShading,1],\
                        'visibleInReflections':[self.ui.checkBox_visibleInReflections,1],\
                        'visibleInRefractions':[self.ui.checkBox_visibleInRefractions,1],\
                        'doubleSided':[self.ui.checkBox_doubleSided,1],\
                        'opposite':[self.ui.checkBox_opposite,1]
                        }
        for k,v in renderStatus.items() :
            v[1] = v[0].isChecked()
        MRRenderLayerPass.setRenderStatus( renderStatus )
                
def getMayaWindow():
    ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

def main():
    global MRRenderLayerPass_app
    global MRRenderLayerPass_myapp
    MRRenderLayerPass_app = QtGui.qApp
    MRRenderLayerPass_myapp = StartMRRenderLayerPass(getMayaWindow())
    MRRenderLayerPass_myapp.show()

if __name__ == "__main__":
    main()

