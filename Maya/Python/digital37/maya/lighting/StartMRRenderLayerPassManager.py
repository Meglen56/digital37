import logging 
LOG_LEVELS = {'debug': logging.DEBUG, 'info':logging.INFO, \
              'warning': logging.WARNING, 'error': logging.ERROR,\
              'critical': logging.CRITICAL}
LOG_LEVEL = LOG_LEVELS.get('debug')
logging.basicConfig(level=LOG_LEVEL)

import traceback

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
        
        # Init widget
        self.initLayerPresetCombobox()
        
        #self.ui.listWidget_L.itemSelectionChanged.connect( self.updateAll )
        self.listWidget_SL.itemSelectionChanged.connect( self.updateAllExceptLayer )
        self.listWidget_CL.itemSelectionChanged.connect( self.updateLayerSettings_create )
        
        # for rename layer
        self.listWidget_SL.itemDoubleClicked.connect( self.getActiveLayer )
        self.listWidget_SL.itemChanged.connect( self.renameLayer_SL )
        #self.listWidget_CL.itemChanged.connect( self.renameLayer_CL )
        
        self.listWidget_SP.itemChanged.connect( self.updateScenePasses )
        self.listWidget_ASP.itemChanged.connect( self.updateAssociatedPasses )
        
        self.listWidget_SP.dragMoveEvent = self.dragMoveEvent_SP
        self.listWidget_ASP.dragMoveEvent = self.dragMoveEvent_ASP
        self.listWidget_AVP.dragMoveEvent = self.dragMoveEvent_AVP
        
        # init lists
        self.updateAll()
        
        self.createContextMenu()
        self.listWidget_CL.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #self.listWidget_CL.customContextMenuRequested.connect(self.showContextMenu)
        self.listWidget_CL.customContextMenuRequested.connect(self.showContextMenu)
        
    def createContextMenu(self):
        # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu  
        # 否则无法使用customContextMenuRequested信号  
        
        # we do not need set this
        #self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # set no contextmenu for default  
        #self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        
        #self.customContextMenuRequested.connect(self.showContextMenu)  
      
        self.contextMenu = QtGui.QMenu(self)  
        self.actionA = self.contextMenu.addAction(u'Add')  
        self.actionB = self.contextMenu.addAction(u'Remove')  

        self.actionA.triggered.connect(self.actionHandler_add)  
        self.actionB.triggered.connect(self.actionHandler_remove)  
      
    def showContextMenu(self, pos):  
        # mouse position
        #self.contextMenu.move(self.pos() + pos)  
        self.contextMenu.move(self.pos() + pos + self.listWidget_CL.pos() )  
        self.contextMenu.show()  

    def actionHandler_add(self):  
        # function for menu
        print 'action handler_add'
        self.listWidget_CL_add()
              
    def actionHandler_remove(self):  
        # function for menu
        print 'action handler_remove'
        self.listWidget_CL_remove()

    # listWidget_SP can only accept listWidget_AVP's drag and drop
    def dragMoveEvent_SP(self,e):
        logging.debug('custom dragMoveEvent')
        if e.source() == self.listWidget_AVP :
            e.accept()
            # Add passes to scenes
            #self.updateScenePasses()
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
            # add custom cmd to add passes to selected layers
            #self.addAssociatedPasses2Layers()
        else :
            e.ignore()
        
    # listWidget_AVP can only accept listWidget_SP's drag and drop
    def dragMoveEvent_AVP(self,e):
        logging.debug('custom dragMoveEvent')
        if e.source() == self.listWidget_SP :
            e.accept()
        else :
            e.ignore()            

    def initLayerPresetCombobox(self):
        self.comboBox_O.addItems( RLP.PRESET_LAYER )
        
    def insertListWidgetItem(self,listWidget,inputList):
        # Clear listWidget first
        listWidget.clear()
        self.appendListWidgetItem(listWidget, inputList)

    def appendListWidgetItem(self,listWidget,inputList):
        # Clear listWidget first
        if inputList :
            if type(inputList) == type([]) :
                listItem = []
                for l in inputList :
                    listItem.append( QtGui.QListWidgetItem( l ) )
                    
                for i in range(len(listItem)) :
                    listWidget.insertItem(i+1,listItem[i])
                    # Add editable to listWidget_L's item
                    if listWidget == self.listWidget_SL or listWidget == self.listWidget_CL:
                        listItem[i].setFlags(listItem[i].flags() | QtCore.Qt.ItemIsEditable)
            elif type(inputList) == type({}) :
                listItem = []
                for l in inputList.keys() :
                    listItem.append( QtGui.QListWidgetItem( l ) )
                    
                for i in range(len(listItem)) :
                    listWidget.insertItem(i+1,listItem[i])
                    # Add editable to listWidget_L's item
                    if listWidget == self.listWidget_SL :
                        listItem[i].setFlags(listItem[i].flags() | QtCore.Qt.ItemIsEditable)
            else :
                print type(inputList)
                logging.error('appendListWidget input arg error')
    
    # add menu cmd for listWidget_CL
    def listWidget_CL_add(self):
        self.appendListWidgetItem(self.listWidget_CL, {'layer':'layer'})
    
    # add menu cmd for listWidget_CL
    def listWidget_CL_remove(self):
        listItems = self.listWidget_CL.selectedItems()
        if listItems:
            for l in listItems :
                i = self.listWidget_CL.row(l)
                try:
                    self.listWidget_CL.takeItem(i)
                except:
                    traceback.print_exc()
                    logging.warning('can not remove itemWidget')
        
    def getLayerDict(self):
        pass


#    def removeListWidgetItem(self,listWidget,inputStringList):
#        # Clear listWidget first
#        if inputStringList :
#            listWidgetItems_dict = self.getAllItemsInListWidget(listWidget)
#            listItem = []
#            for s in inputStringList :
#                #logging.debug( 's: ' + str(type(s)) )
#                if type(s) != type({}) :
#                    if s in listWidgetItems_dict.keys():
#                        listItem.append( listWidgetItems_dict[s] )
#                else :
#                    items = listWidget.findItems(s.keys()[0],QtCore.Qt.MatchFixedString)
#                    if items :
#                        listItem.append( items[0] )   
#
#            for l in listItem :
#                i = listWidget.row(l)
#                logging.debug('list widget\' row: ' + str(i))
#                listWidget.takeItem(i)
#                logging.warning('can not remove itemWidget')

    def removeListWidgetItem(self,listWidget,inputStringList):
        # Clear listWidget first
        if inputStringList :
            listWidgetItems_dict = self.getAllItemsInListWidget(listWidget)
            if inputStringList == type([]) :
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
                    try:
                        listWidget.takeItem(i)
                    except:
                        traceback.print_exc()
                        logging.warning('can not remove itemWidget')
            else :
                #inputStringList = dict
                for k in inputStringList.keys() :
                    i = listWidget.row( listWidgetItems_dict[k] )
                    try:
                        listWidget.takeItem(i)
                    except:
                        traceback.print_exc()
                        logging.warning('can not remove itemWidget')                    
                        
    def getAllItemsInListWidget(self,listWidget):
        items_list = {}
        for i in xrange(listWidget.count()):
            item = listWidget.item(i)
            items_list[str(item.text())] = item
        return items_list
                
    def getItemsInListWidget(self,listWidget,item_text):
        items = listWidget.findItems(item_text,QtCore.Qt.MatchFixedString)
        items_list = {}
        for item in items :
            items_list[ str( item.text() ) ] = item
        return items_list
                        
    def getMemberInListByName(self,inputList,inputStr):
        matchMember = None
        #logging.debug( 'inputStr:',str(inputStr) )
        for l in inputList:
            if inputStr == l.keys() :
                matchMember = l
        return matchMember
                 
    def updateLayerList(self):
        # Get layers first
        self.RLP.getLayers()
        # Get render inputDict        self.RLP.getLayers()
        self.insertListWidgetItem(self.listWidget_SL, self.RLP.LAYERS)
        
    def updateAssociatedObjectList(self):
        logging.debug('updateAssociatedObjectList')
        self.getActiveLayer()
        if self.RLP.LAYER_ACTIVE :
            obj_names_list = self.RLP.getObjInLayer( self.RLP.LAYER_ACTIVE[0] )
            self.insertListWidgetItem(self.listWidget_AO, obj_names_list)
        
    def updateOverridesList(self):
        logging.debug('updateOverridesList')
        self.getActiveLayer()
        if self.RLP.LAYER_ACTIVE :
            objs = self.RLP.getOverridesInLayer( self.RLP.LAYER_ACTIVE[0] )
            self.insertListWidgetItem(self.listWidget_O, objs)    
    
    def updateAssociatedPassList(self):
        logging.debug('updateAssociatedPassList')
        # Get active layer first
        self.getActiveLayer()
        if self.RLP.LAYER_ACTIVE :
            passes_list = self.RLP.getPassByLayer(self.RLP.LAYER_ACTIVE[0])
            self.insertListWidgetItem(self.listWidget_ASP, passes_list)
        
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
                    
    def updateLayerSettings_create(self):
        self.getSelectedLayers()
        self.updateAssociatedObjectList()
        self.updateAssociatedPassList()
        self.updateScenePassList()
        self.updateAvailablePassList()
        self.updateOverridesList()      
                                        
    def getSelectedLayers(self):
        self.RLP.LAYERS_SELECTED = []
        #self.RLP.LAYERS_SELECTED = 
        for selItem in self.listWidget_SL.selectedItems() :
            # use str() to convert qstring to string
            layerName = str( selItem.text() )
            self.RLP.LAYERS_SELECTED.append( layerName )
        
    def getActiveLayer(self):
        logging.debug('get active layer')
        layerName = ''
        self.RLP.LAYER_ACTIVE = []
        #currentItem = self.ui.listWidget_L.currentItem()
        currentItems = self.listWidget_SL.selectedItems()
        if not currentItems:
            logging.debug('no active layer')
        else:
            try:
                currentItem = currentItems[-1]
            except :
                logging.debug('can not get active layer')
                traceback.print_exc()
            else :
                try:
                    layerName = str( currentItem.text() )
                except:
                    logging.debug('can not find text()')
                    traceback.print_exc()
                else:
                    logging.debug('currentItem: ' + layerName )
                    self.RLP.LAYER_ACTIVE.append( layerName )
        # logging debug
        RLP.log_list(self.RLP.LAYER_ACTIVE)
    
    def setActiveLayer(self,layer_current):
        # clear selection in listWidget_L
        self.listWidget_SL.clearSelection()
        # get widgetitem
        listItems = self.getItemsInListWidget(self.listWidget_SL, layer_current.longName())
        if listItems :
            self.listWidget_SL.setCurrentItem( listItems.values()[0] )
    
    def renameLayer_SL(self):
        logging.debug('rename layer_SL')
        # Get selected listWidgetItem
        # Important: no need for self.getActiveLayer
        # Because item double clicked connected self.getActiveLayer
        if self.RLP.LAYER_ACTIVE :
            item = self.listWidget_SL.currentItem()
            txt = str( item.text() )
            if txt :
                #logging.debug('layer text:',str(txt))
                try :
                    RLP.rename( self.RLP.LAYER_ACTIVE[0], txt )
                except :
                    traceback.print_exc()
    
    def renameLayer_CL(self):
        pass
    
    def updateScenePasses(self):
        logging.debug('updateScenePasses')
        # Get all widgetItems in listWidget_SP
        listWidgetItems = self.getAllItemsInListWidget(self.listWidget_SP)
        print '*-*'
        print listWidgetItems.keys()
        if listWidgetItems :
            self.RLP.updateScenePasses( listWidgetItems.keys() )
                        
    def updateAssociatedPasses(self):
        logging.debug('updateAssociatedPasses')
        
        # Get selected layers
        self.getSelectedLayers()
        
        # Only update if some layers selected
        if self.RLP.LAYERS_SELECTED :
            # Get all widgetItems in listWidget_SP
            listWidgetItems = self.getAllItemsInListWidget(self.listWidget_ASP)
            
            print '*-*'
            print listWidgetItems
            if listWidgetItems :
                self.RLP.updateAssociatedPasses( listWidgetItems.keys() )
                    
    def addAssociatedPasses2Layers(self):
        pass_names_list = []
        # Get selected widgetItems in listWidget_SP
        self.getSelectedLayers()
        listWidgetItems = self.listWidget_SP.selectedItems()
        for listWidgetItem in listWidgetItems :
            pass_names_list.append( str( listWidgetItem.text() ) )
        if self.RLP.LAYERS_SELECTED and pass_names_list :
            self.RLP.addPasses2Layers(self.RLP.LAYERS_SELECTED,pass_names_list)
        
    def on_pushButton_SL_add_pressed(self):
        newLayer = self.RLP.createNewLayer()
        # Add newlayer to listwidget
        self.appendListWidgetItem(self.listWidget_SL, {newLayer.longName():newLayer})
        
        # select newlayer in listwidget_L
        self.setActiveLayer(newLayer)
        # update other lists
        self.updateAllExceptLayer()     
                            
    def on_pushButton_SL_remove_pressed(self):
        sels_dict_listWidget = self.RLP.getObjsFromSelsInListWidget(self.listWidget_SL)
        if sels_dict_listWidget:
            self.removeListWidgetItem(self.listWidget_SL, sels_dict_listWidget)
            # Remove pass to layer
            self.RLP.removeLayerByListWidget( sels_dict_listWidget )        
        
    def on_pushButton_refresh_pressed(self):
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
            objs = self.RLP.getObjInLayer( self.RLP.LAYER_ACTIVE[0] )
            logging.debug('objs:')
            RLP.log_list( objs )
            # Remove objs
            sels_dict = RLP.dict_remove_by_value( sels_dict, objs )
            logging.debug('sels_dict:')
            RLP.log_list( sels_dict )
            self.appendListWidgetItem(self.listWidget_AO, sels_dict)
            # Add objs to layer
            self.RLP.addObj2Layer( self.RLP.LAYER_ACTIVE[0], sels_dict )

    def on_pushButton_O_remove_pressed(self):
        # Get layer active
        self.getActiveLayer()
        if self.RLP.LAYER_ACTIVE :
            # For user select some widgetItems in listWidget
            sels_dict = self.RLP.getObjsFromSelsInListWidget(self.listWidget_O)

            if sels_dict:
                logging.debug('sels_dict:')
                RLP.log_dict( sels_dict )
                self.removeListWidgetItem(self.listWidget_O, sels_dict)
                # Remove objs to layer
                self.RLP.removePassOfLayer( self.RLP.LAYER_ACTIVE[0], sels_dict )
            
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
                    sels_dict = {}
                #sels_dict.extend( sels_dict_listWidget )
                try:
                    sels_dict = RLP.dict_add(sels_dict,sels_dict_listWidget)
                except:
                    traceback.print_exc()
                
            if sels_dict:
                logging.debug('sels_dict:')
                RLP.log_list( sels_dict )
                self.removeListWidgetItem(self.listWidget_AO, sels_dict)
                # Remove objs to layer
                self.RLP.removeObj2Layer( self.RLP.LAYER_ACTIVE[0], sels_dict )
                            
    def on_pushButton_ASP_remove_pressed(self):
        # Get layer active
        self.getActiveLayer()
        
        if self.RLP.LAYER_ACTIVE :
            # For user select some widgetItems in listWidget
            sels_dict_listWidget = self.RLP.getObjsFromSelsInListWidget(self.listWidget_ASP)
            if sels_dict_listWidget:
                self.removeListWidgetItem(self.listWidget_ASP, sels_dict_listWidget)
                # Remove pass to layer
                self.RLP.removePass2Layer( self.RLP.LAYER_ACTIVE[0], sels_dict_listWidget )
                            
    def on_pushButton_SP_remove_pressed(self):
        sels_dict_listWidget = self.RLP.getObjsFromSelsInListWidget(self.listWidget_SP)
        if sels_dict_listWidget :
            self.removeListWidgetItem(self.listWidget_SP, sels_dict_listWidget)
            # Remove passes
            self.RLP.removeScenePasses( sels_dict_listWidget )
        
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

