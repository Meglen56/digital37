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
        self.RLP = digital37.maya.lighting.MRRenderLayerPass.MRRenderLayerPass()
        # init lists
        self.updateRenderLayerList()
        self.ui.listWidget_RL.currentRowChanged.connect( self.updateAll )
                   
    def updateRenderLayerList(self):
        print self.RLP.RENDER_LAYERS
        if self.RLP.RENDER_LAYERS :
            listItem1 = []
            # self.RLP.RENDER_LAYERS is a dict
            for lst in self.RLP.RENDER_LAYERS:
                for k,v in lst.items() :
                    listItem1.append(QtGui.QListWidgetItem(k))
            for i in range(len(listItem1)):
                self.ui.listWidget_RL.insertItem(i+1,listItem1[i])
        
    def getSelectedRenderLayers(self):
        #self.RLP.LAYER_SELECTED = 
        for selItem in self.ui.listWidget_RL.selectedItems() :
            self.RLP.LAYER_SELECTED.append( selItem.text() )
        print self.ui.listWidget_RL.currentItem().text()
        
        
    def updateAll(self):
        # Get current render layer
        self.getSelectedRenderLayers()
        self.updateObjectList()
        
    def updateObjectList(self):
        print 'test'
        
        
    def on_pushButton_RL_refresh_pressed(self):
        pass
        # Get render layers
        #self.renderLayers = self.RLP.getRenderLayers()
        #if self.renderLayers
                
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

