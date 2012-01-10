import logging 
LOG_LEVELS = {'debug': logging.DEBUG, 'info':logging.INFO, \
              'warning': logging.WARNING, 'error': logging.ERROR,\
              'critical': logging.CRITICAL}
LOG_LEVEL = LOG_LEVELS.get('debug')
logging.basicConfig(level=LOG_LEVEL)

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
        self.updateLayerList()
        self.ui.listWidget_RL.currentRowChanged.connect( self.updateAll )
                   
    def insertListWidgetItem(self,listWidget,inputStringList):
        if inputStringList :
            listItem = []
            for s in inputStringList :
                logging.debug( 's: ' + str(type(s)) )
                if type(s) != type({}) :
                    listItem.append( QtGui.QListWidgetItem(s) )
                else :
                    listItem.append( QtGui.QListWidgetItem(s.keys()[0]) )
            for i in range(len(listItem)):
                listWidget.insertItem(i+1,listItem[i])
        
    def updateLayerList(self):
        self.insertListWidgetItem(self.ui.listWidget_RL, self.RLP.LAYERS)
        
    def getSelectedLayers(self):
        self.RLP.LAYERS_SELECTED = []
        #self.RLP.LAYERS_SELECTED = 
        for selItem in self.ui.listWidget_RL.selectedItems() :
            layerName = selItem.text()
            layer = self.RLP.getLayerByName( layerName )
            self.RLP.LAYERS_SELECTED.append( {layerName:layer} )
        
    def getActiveLayer(self):
        self.RLP.LAYER_ACTIVE = {}
        layerName = self.ui.listWidget_RL.currentItem().text()
        if layerName :
            layer = self.RLP.getLayerByName( layerName )
            self.RLP.LAYER_ACTIVE = {layerName:layer}
    
    def updateAll(self):
        # Get current render layer
        self.getSelectedLayers()
        self.updateObjectList()
        
    def updateObjectList(self):
        logging.debug('updateObjectList')
        self.getActiveLayer()
        if self.RLP.LAYER_ACTIVE :
            objs = self.RLP.getObjInLayer( self.RLP.LAYER_ACTIVE.values()[0] )
            self.insertListWidgetItem(self.ui.listWidget_OBJ, objs)
        
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

