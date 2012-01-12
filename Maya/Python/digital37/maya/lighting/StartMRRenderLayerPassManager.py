import logging 
LOG_LEVELS = {'debug': logging.DEBUG, 'info':logging.INFO, \
              'warning': logging.WARNING, 'error': logging.ERROR,\
              'critical': logging.CRITICAL}
LOG_LEVEL = LOG_LEVELS.get('debug')
logging.basicConfig(level=LOG_LEVEL)

import sip
from PyQt4 import QtCore, QtGui
import maya.OpenMayaUI

# Make MRRenderLayerPassUI by: pyuic4 MRRenderLayerPassManager.ui>MRRenderLayerPassManagerUI.py
import digital37.maya.lighting.MRRenderLayerPassManagerUI as MRRenderLayerPassManagerUI
# reload only for tests
reload(MRRenderLayerPassManagerUI)

import digital37.maya.lighting.MRRenderLayerPass as RLP
# reload only for tests
reload(RLP)

class StartMRRenderLayerPassManager(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = MRRenderLayerPassManagerUI.Ui_root()
        self.ui.setupUi(self)
        self.ui.listWidget_L.itemSelectionChanged.connect( self.updateAll )
        self.RLP = RLP.MRRenderLayerPass()
        # init lists
        self.updateLayerList()
        self.updateAssociatedObjectList()
        self.updateAssociatedPassList()
        self.updateScenePassList()
        self.updateAvailablePassList()
        
    def insertListWidgetItem(self,listWidget,inputStringList):
        # Clear listWidget first
        listWidget.clear()
        self.appendListWidgetItem(listWidget, inputStringList)

    def appendListWidgetItem(self,listWidget,inputStringList):
        # Clear listWidget first
        if inputStringList :
            listItem = []
            for s in inputStringList :
                #logging.debug( 's: ' + str(type(s)) )
                if type(s) != type({}) :
                    listItem.append( QtGui.QListWidgetItem(s) )
                else :
                    listItem.append( QtGui.QListWidgetItem(s.keys()[0]) )
            for i in range(len(listItem)) :
                listWidget.insertItem(i,listItem[i])
                        
    def updateLayerList(self):
        # Get render layers first
        self.RLP.getLayers()
        self.insertListWidgetItem(self.ui.listWidget_L, self.RLP.LAYERS)
        
    def updateAssociatedObjectList(self):
        logging.debug('updateAssociatedObjectList')
        self.getActiveLayer()
        if self.RLP.LAYER_ACTIVE :
            objs = self.RLP.getObjInLayer( self.RLP.LAYER_ACTIVE.values()[0] )
            self.insertListWidgetItem(self.ui.listWidget_AO, objs)
        
    def updateAssociatedPassList(self):
        logging.debug('updateAssociatedPassList')
        # Get active layer first
        self.getActiveLayer()
        if self.RLP.LAYER_ACTIVE :
            passes = self.RLP.getPassByLayer(self.RLP.LAYER_ACTIVE.values()[0])
            self.insertListWidgetItem(self.ui.listWidget_ASP, passes)
        
    def updateScenePassList(self):
        logging.debug('updateScenePassList')
        # Get active layer first
        self.RLP.getScenePasses()
        if self.RLP.PASSES_SCENE :
            self.insertListWidgetItem(self.ui.listWidget_SP, self.RLP.PASSES_SCENE)                
        
    def updateAvailablePassList(self):
        logging.debug('updateAvailablePassList')
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
        #currentItem = self.ui.listWidget_L.currentItem()
        try:
            currentItem = self.ui.listWidget_L.selectedItems()[-1]
        except :
            logging.debug('can not get active layer')
        else :
            try:
                layerName = str( currentItem.text() )
            except:
                logging.debug('can not find text()')
            else:
                logging.debug('currentItem: ' + layerName )
                layer = self.RLP.getLayerByName( layerName )
                self.RLP.LAYER_ACTIVE = {layerName:layer}
        # logging debug
        RLP.log_dict(self.RLP.LAYER_ACTIVE)
    
#    def setActiveLayer(self):
#        self.ui.listWidget_L.setCurrentItem(  )
        
    def updateAll(self):
        # Get current render layer
        self.getSelectedLayers()
        self.updateAssociatedObjectList()
        self.updateAssociatedPassList()
        self.updateScenePassList()
        self.updateAvailablePassList()
        
    def on_pushButton_L_refresh_pressed(self):
        # Get selection layer first
        #self.getActiveLayer()
        
        
        self.updateAll()
        
        # Reselect active layer
        #self.setActiveLayer( self.RLP.LAYER_ACTIVE )

    def on_pushButton_AO_add_pressed(self):
        # Get selection obj
        sels_dict = RLP.getSelection_dict()
        # Get layer active
        self.getActiveLayer()
        if self.RLP.LAYER_ACTIVE and sels_dict:
            # Get current obj in list
            objs = self.RLP.getObjInLayer( self.RLP.LAYER_ACTIVE.values()[0] )
            logging.debug('objs:')
            RLP.log_list( objs )
            # Remove objs
            sels_dict = RLP.dict_remove_by_value( sels_dict, objs )
            logging.debug('sels_dict:')
            RLP.log_list( sels_dict )
            self.appendListWidgetItem(self.ui.listWidget_AO, sels_dict)
            # Add objs to layer
            self.RLP.addObj2Layer( self.RLP.LAYER_ACTIVE.values()[0], sels_dict )
    
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

