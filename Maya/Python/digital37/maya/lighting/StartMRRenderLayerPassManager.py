import logging 
LOG_LEVELS = {'debug': logging.DEBUG, 'info':logging.INFO, \
              'warning': logging.WARNING, 'error': logging.ERROR,\
              'critical': logging.CRITICAL}
LOG_LEVEL = LOG_LEVELS.get('debug')
logging.basicConfig(level=LOG_LEVEL)

import sip
from PyQt4 import QtCore, QtGui
import maya.OpenMayaUI

# Make MRRenderLayerPassUI by: pyuic4 MRRenderLayerPassManager.ui>RLPUI.py
import digital37.maya.lighting.MRRenderLayerPassManagerUI as RLPUI
# reload only for tests
reload(RLPUI)

import digital37.maya.lighting.MRRenderLayerPass as RLP
# reload only for tests
reload(RLP)

class StartMRRenderLayerPassManager(QtGui.QMainWindow,RLPUI.Ui_root):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        #self.ui.setupUi(self)
        self.setupUi(self)
        #self.ui = RLPUI.Ui_root()
        
        self.RLP = RLP.MRRenderLayerPass()
        
        #self.ui.listWidget_L.itemSelectionChanged.connect( self.updateAll )
        self.listWidget_L.itemSelectionChanged.connect( self.updateAllExceptLayer )
        
        self.listWidget_SP.dragMoveEvent = self.dragMoveEvent_SP
        self.listWidget_ASP.dragMoveEvent = self.dragMoveEvent_ASP
        self.listWidget_AVP.dragMoveEvent = self.dragMoveEvent_AVP
        
        # init lists
        self.updateAll()
        
    # listWidget_SP can only accept listWidget_AVP's drag and drop
    def dragMoveEvent_SP(self,e):
        logging.debug('custom dragMoveEvent')
        if e.source() == self.listWidget_AVP :
            e.accept()
        else :
            e.ignore()
        
    # listWidget_SP can only accept listWidget_SP's drag and drop
    # set drop action to copy
    def dragMoveEvent_ASP(self,e):
        logging.debug('custom dragMoveEvent')
        if e.source() == self.listWidget_SP :
            #self.listWidget_SP.setDefaultDropAction(QtCore.Qt.CopyAction)
            e.accept()
            e.setDropAction(QtCore.Qt.CopyAction)
        else :
            e.ignore()
        
    # listWidget_AVP can only accept listWidget_SP's drag and drop
    def dragMoveEvent_AVP(self,e):
        logging.debug('custom dragMoveEvent')
        if e.source() == self.listWidget_SP :
            e.accept()
        else :
            e.ignore()            
                    
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
                listWidget.insertItem(i+1,listItem[i])


    def removeListWidgetItem(self,listWidget,inputStringList):
        # Clear listWidget first
        if inputStringList :
            listWidgetItems_dict = self.getAllItemsInListWidget(listWidget)
            listItem = []
            for s in inputStringList :
                #logging.debug( 's: ' + str(type(s)) )
                if type(s) != type({}) :
                    if s in listWidgetItems_dict.keys():
                        listItem.append( listWidgetItems_dict[s] )
                else :
                    items = listWidget.findItems(s.keys()[0],QtCore.Qt.MatchFixedString)
                    if items :
                        listItem.append( items[0] )   

            for l in listItem :
                i = listWidget.row(l)
                logging.debug('list widget\' row: ' + str(i))
                listWidget.takeItem(i)
                logging.warning('can not remove itemWidget')
            
    def getAllItemsInListWidget(self,listWidget):
        items = listWidget.findItems('',QtCore.Qt.MatchRegExp)
        items_dict = []
        for item in items :
            items_dict.append({item.text():item})
        return items_dict
                
    def getItemsInListWidget(self,listWidget,item_text):
        items = listWidget.findItems(item_text,QtCore.Qt.MatchFixedString)
        items_dict = []
        for item in items :
            items_dict.append({item.text():item})
        return items_dict
                        
    def getMemberInListByName(self,inputList,inputStr):
        matchMember = None
        #logging.debug( 'inputStr:',str(inputStr) )
        for l in inputList:
            if inputStr == l.keys() :
                matchMember = l
        return matchMember
                
    def updateLayerList(self):
        # Get render layers first
        self.RLP.getLayers()
        self.insertListWidgetItem(self.listWidget_L, self.RLP.LAYERS)
        
    def updateAssociatedObjectList(self):
        logging.debug('updateAssociatedObjectList')
        self.getActiveLayer()
        if self.RLP.LAYER_ACTIVE :
            objs = self.RLP.getObjInLayer( self.RLP.LAYER_ACTIVE.values()[0] )
            self.insertListWidgetItem(self.listWidget_AO, objs)
        
    def updateOverridesList(self):
        logging.debug('updateOverridesList')
        self.getActiveLayer()
        if self.RLP.LAYER_ACTIVE :
            objs = self.RLP.getOverridesInLayer( self.RLP.LAYER_ACTIVE.values()[0] )
            self.insertListWidgetItem(self.listWidget_O, objs)    
        
    def updateAssociatedPassList(self):
        logging.debug('updateAssociatedPassList')
        # Get active layer first
        self.getActiveLayer()
        if self.RLP.LAYER_ACTIVE :
            passes = self.RLP.getPassByLayer(self.RLP.LAYER_ACTIVE.values()[0])
            self.insertListWidgetItem(self.listWidget_ASP, passes)
        
    def updateScenePassList(self):
        logging.debug('updateScenePassList')
        # Get active layer first
        self.RLP.getScenePasses()
        if self.RLP.PASSES_SCENE :
            self.insertListWidgetItem(self.listWidget_SP, self.RLP.PASSES_SCENE)                
        
    def updateAvailablePassList(self):
        logging.debug('updateAvailablePassList')
        # Get active layer first
        self.RLP.getAvailablePasses()
        if self.RLP.PASSES_AVAILABLE :
            self.insertListWidgetItem(self.listWidget_AVP, self.RLP.PASSES_AVAILABLE)  
        
    def updateAll(self):
        layer_current = None
        # First check if some layers in list have been selected
        self.getActiveLayer()
        if not self.RLP.LAYER_ACTIVE :
            # Then check if some layers in scene has been selected
            layer_current = self.RLP.getLayerCurrent()
            
        # Add all layers to list
        self.updateLayerList()
        
        # Select layer in layer list
        if layer_current : 
            # Set layer active
            self.setActiveLayer(layer_current)
        
        self.updateAllExceptLayer()     
                    
    def updateAllExceptLayer(self):
        self.getSelectedLayers()
        self.updateAssociatedObjectList()
        self.updateAssociatedPassList()
        self.updateScenePassList()
        self.updateAvailablePassList()
        self.updateOverridesList()      
                                        
    def getSelectedLayers(self):
        self.RLP.LAYERS_SELECTED = []
        #self.RLP.LAYERS_SELECTED = 
        for selItem in self.listWidget_L.selectedItems() :
            layerName = selItem.text()
            layer = self.RLP.getLayerByName( layerName )
            self.RLP.LAYERS_SELECTED.append( {layerName:layer} )
        
    def getActiveLayer(self):
        layerName = ''
        self.RLP.LAYER_ACTIVE = {}
        #currentItem = self.ui.listWidget_L.currentItem()
        try:
            currentItem = self.listWidget_L.selectedItems()[-1]
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
    
    def setActiveLayer(self,layer_current):
        # get widgetitem
        listItems = self.getItemsInListWidget(self.listWidget_L, layer_current.longName())
        print listItems
        self.listWidget_L.setCurrentItem( listItems[0].values()[0] )
        
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
            self.appendListWidgetItem(self.listWidget_AO, sels_dict)
            # Add objs to layer
            self.RLP.addObj2Layer( self.RLP.LAYER_ACTIVE.values()[0], sels_dict )

    def on_pushButton_O_remove_pressed(self):
        # Get layer active
        self.getActiveLayer()
        if self.RLP.LAYER_ACTIVE :
            sels_dict = []
            # For user select some widgetItems in listWidget
            sels_dict_listWidget = self.RLP.getObjsFromSelsInListWidget(self.listWidget_O)
            
            if sels_dict_listWidget :
                sels_dict.extend( sels_dict_listWidget )
            
            if sels_dict:
                logging.debug('sels_dict:')
                RLP.log_list( sels_dict )
                self.removeListWidgetItem(self.listWidget_O, sels_dict)
                # Remove objs to layer
                self.RLP.removeObj2Layer( self.RLP.LAYER_ACTIVE.values()[0], sels_dict )
            
    def on_pushButton_AO_remove_pressed(self):
        # Get layer active
        self.getActiveLayer()
        
        if self.RLP.LAYER_ACTIVE:
            # Get selection obj # For user select some objs in model view
            sels_dict = RLP.getSelection_dict()
            
            # For user select some widgetItems in listWidget
            sels_dict_listWidget = self.RLP.getObjsFromSelsInListWidget(self.listWidget_AO)
            
            if sels_dict_listWidget :
                # sels_dict may be None, so set to list to use extend func
                if not sels_dict :
                    sels_dict = []
                sels_dict.extend( sels_dict_listWidget )
                
            # Remove duplicate
            RLP.flattenList( sels_dict )
            
            if sels_dict:
                logging.debug('sels_dict:')
                RLP.log_list( sels_dict )
                self.removeListWidgetItem(self.listWidget_AO, sels_dict)
                # Remove objs to layer
                self.RLP.removeObj2Layer( self.RLP.LAYER_ACTIVE.values()[0], sels_dict )
                            
    def on_pushButton_ASP_remove_pressed(self):
        # Get layer active
        self.getActiveLayer()
        
        if self.RLP.LAYER_ACTIVE :
            sels_dict = []
            # For user select some widgetItems in listWidget
            sels_dict_listWidget = self.RLP.getObjsFromSelsInListWidget(self.listWidget_ASP)
            
            if sels_dict_listWidget :
                sels_dict.extend( sels_dict_listWidget )
            
            if sels_dict:
                logging.debug('sels_dict:')
                RLP.log_list( sels_dict )
                self.removeListWidgetItem(self.listWidget_ASP, sels_dict)
                # Remove pass to layer
                self.RLP.removePass2Layer( self.RLP.LAYER_ACTIVE.values()[0], sels_dict )
        
    def delSelItemsInListWidget(self,listWidget):
        items = listWidget.selectedItems()
        if items:
            for item in items :
                row = listWidget.row( item ) 
                try:
                    listWidget.takeItem( row )
                except:
                    logging.warning('delSelItemInListWidget error')
                                
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

