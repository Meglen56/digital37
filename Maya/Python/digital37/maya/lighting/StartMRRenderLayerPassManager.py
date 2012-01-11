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
        self.ui.listWidget_L.currentRowChanged.connect( self.updateAll )
        self.RLP = digital37.maya.lighting.MRRenderLayerPass.MRRenderLayerPass()
        # init lists
        self.updateLayerList()
        self.updateAssociatedObjectList()
        self.updateAssociatedPassList()
        self.updateScenePassList()
        self.updateAvailablePassList()
        
    def insertListWidgetItem(self,listWidget,inputStringList):
        # Clear listWidget first
        listWidget.clear()
        if inputStringList :
            listItem = []
            for s in inputStringList :
                logging.debug( 's: ' + str(type(s)) )
                if type(s) != type({}) :
                    listItem.append( QtGui.QListWidgetItem(s) )
                else :
                    listItem.append( QtGui.QListWidgetItem(s.keys()[0]) )
            for i in range(len(listItem)) :
                listWidget.insertItem(i+1,listItem[i])
        
    def updateLayerList(self):
        # Get render layers first
        self.RLP.getLayers()
        self.insertListWidgetItem(self.ui.listWidget_L, self.RLP.LAYERS)
        
    def updateAssociatedPassList(self):
        # Get active layer first
        self.getActiveLayer()
        if self.RLP.LAYER_ACTIVE :
            passes = self.RLP.getPassByLayer(self.RLP.LAYER_ACTIVE.values()[0])
            self.insertListWidgetItem(self.ui.listWidget_ASP, passes)
        
    def updateScenePassList(self):
        # Get active layer first
        self.RLP.getScenePasses()
        if self.RLP.PASSES_SCENE :
            self.insertListWidgetItem(self.ui.listWidget_SP, self.RLP.PASSES_SCENE)                
        
    def updateAvailablePassList(self):
        # Get active layer first
        self.RLP.getAvailablePasses()
        if self.RLP.PASSES_AVAILABLE :
            self.insertListWidgetItem(self.ui.listWidget_AVP, self.RLP.PASSES_AVAILABLE)  
                    
    def getSelectedLayers(self):
        self.RLP.LAYERS_SELECTED = []
        #self.RLP.LAYERS_SELECTED = 
        for selItem in self.ui.listWidget_L.selectedItems() :
            layerName = selItem.text()
            layer = self.RLP.getLayerByName( layerName )
            self.RLP.LAYERS_SELECTED.append( {layerName:layer} )
        
    def getActiveLayer(self):
        layerName = ''
        self.RLP.LAYER_ACTIVE = {}
        currentItem = self.ui.listWidget_L.currentItem()
        #print type(currentItem)
        if currentItem :
            try:
                layerName = currentItem.text()
            except:
                logging.debug('can not find text()')
            else:
                layer = self.RLP.getLayerByName( layerName )
                self.RLP.LAYER_ACTIVE = {layerName:layer}
    
    def updateAll(self):
        # Get current render layer
        self.getSelectedLayers()
        self.updateAssociatedObjectList()
        self.updateAssociatedPassList()
        self.updateScenePassList()
        self.updateAvailablePassList()
        
    def updateAssociatedObjectList(self):
        logging.debug('updateAssociatedObjectList')
        self.getActiveLayer()
        if self.RLP.LAYER_ACTIVE :
            objs = self.RLP.getObjInLayer( self.RLP.LAYER_ACTIVE.values()[0] )
            self.insertListWidgetItem(self.ui.listWidget_AO, objs)
        
    def on_pushButton_L_refresh_pressed(self):
        self.updateLayerList()
        
        self.getSelectedLayers()
        self.updateAssociatedObjectList()
        self.updateScenePassList()
                
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

