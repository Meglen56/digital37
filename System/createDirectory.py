import sys
import traceback
import itertools
import sip
from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
from createDirectoryUI import Ui_MainWindow
from performCreateDirectory import PerformCreateDirectory

    
class StartQt4(QtGui.QMainWindow,Ui_MainWindow,PerformCreateDirectory):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        PerformCreateDirectory.__init__(self)
        
    def keyPressEvent(self, event):
        #print 'key press'
        # get treewidget's current index
        currentIndex = self.treeWidget.indexFromItem( self.treeWidget.currentItem() )
        #print self.treeWidget.currentColumn()
        if (event.key() == QtCore.Qt.Key_Control and self.treeWidget.currentColumn() == 0):
            shift = event.modifiers() & QtCore.Qt.ShiftModifier
            if shift:
                self.expand_all(currentIndex)
            else:
                expand = not(self.treeWidget.isExpanded(currentIndex))
                self.treeWidget.setExpanded(currentIndex, expand)
    
    def expand_all(self, index):
        """
        Expands/collapses all the children and grandchildren etc. of index.
        """
        print 'expand all'
        expand = not(self.treeWidget.isExpanded(index))
        if not expand:
            #if collapsing, do that first (wonky animation otherwise)
            self.treeWidget.setExpanded(index, expand)
        childCount = index.internalPointer().get_child_count()
        self.recursive_expand(index, childCount, expand)
        if expand:
            #if expanding, do that last (wonky animation otherwise)
            self.treeWidget.setExpanded(index, expand)   
            
    def recursive_expand(self, index, childCount, expand):
        """
        Recursively expands/collpases all the children of index.
        """
        for childNo in range(0, childCount):
            childIndex = index.child(childNo, 0)
            if expand: 
                #if expanding, do that first (wonky animation otherwise)
                self.treeWidget.setExpanded(childIndex, expand)
            subChildCount = childIndex.internalPointer().get_child_count()
            if subChildCount > 0:
                self.recursive_expand(childIndex, subChildCount, expand)
            if not expand: 
                #if collapsing, do it last (wonky animation otherwise)
                self.treeWidget.setExpanded(childIndex, expand)
                
    def expand_treeWidget_rootItem(self):
        items = self.treeWidget.findItems('.*',QtCore.Qt.MatchRegExp)
        currentIndex = self.treeWidget.indexFromItem( items[0] )
        self.expand_all(currentIndex)
        
    def file_dialog(self):
        fd = QtGui.QFileDialog(self,'','','')
        self.lineEdit_rootDir.setText( fd.getExistingDirectory() )
    
    def on_pushButton_rootDir_pressed(self):
        self.file_dialog()
        #self.lineEdit_rootDir.setText( self.Dir_Root )
    
    def on_pushButton_add_pressed(self):
        self.add_treeWidget_item()
    
    def on_pushButton_remove_pressed(self):
        self.remove_treeWidget_item()
    
    def on_pushButton_savePreset_pressed(self):
        self.save_preset()
    
    def on_pushButton_openPreset_pressed(self):
        self.open_preset()
        
    def on_pushButton_ok_pressed(self):
        self.main()
        
    def get_root_dir(self):
        self.Dir_Root = str( self.lineEdit_rootDir.text() )
        
    def get_dir_framework(self):
        items_dict = {}
        items = self.treeWidget.findItems('.*',QtCore.Qt.MatchRegExp)
        # refresh self.Dir_Framework to empty
        self.Dir_Framework = list()
        self.get_items_text_in_treeWidget(items[0],self.Dir_Framework)
        print self.Dir_Framework
        self.Dir_Framework = self.Dir_Framework[0]['Root']
        print self.Dir_Framework

    #[{'a': ['1', '']}, {'b': [{'2': ['I', 'II']}]}, 'c']
    def get_items_text_in_treeWidget(self,inputTreeWidgetItem,inputList):
        if inputTreeWidgetItem.childCount() >= 1:
            items_dict = dict()
            l = list()
            for i in xrange( inputTreeWidgetItem.childCount() ):
                self.get_items_text_in_treeWidget( inputTreeWidgetItem.child(i), l  )
            items_dict[str(inputTreeWidgetItem.text(0))] = l
            inputList.append( items_dict )
        else:
            inputList.append( str(inputTreeWidgetItem.text(0)) )
        print inputList

    #[{'a': ['1', '']}, {'b': [{'2': ['I', 'II']}]}, 'c']
    def set_items_text_in_treeWidget(self,inputList,parent):
        if inputList:
            items_dict = dict()
            l = list()
            for x in inputList:
                if type(x) is type('') :
                    # create widget item and set text
                    print 'x:\t%s' % x
                    self.add_treeWidget_item(parent, QtCore.QString(x))
                else:
                    #
                    for k,v in x.iteritems():
                        # create k
                        parentItem = self.add_treeWidget_item(parent, k)
                        # loop create widget
                        self.set_items_text_in_treeWidget(v, parentItem)
            
    def get_dir_name(self):
        # only have two columns 0 for key 1 for value 
        for j in range(self.tableWidget.rowCount()) :
            if self.tableWidget.item(j,0) :
                k = str( self.tableWidget.item(j,0).text() )
                v = str( self.tableWidget.item(j,1).text() )
                self.Dir_Name[k] = v
        print self.Dir_Name
                
    def add_treeWidget_item(self,parent=None,text=None):
        widgetItem = None
        if not parent:
            # Get selected treeWidget item first
            item = self.treeWidget.currentItem()
            if item:
                widgetItem = QtGui.QTreeWidgetItem()
                item.addChild( widgetItem )
                #widgetItem.setText(i,'$A')
                widgetItem.setFlags(widgetItem.flags() | QtCore.Qt.ItemIsEditable)
                if text:
                    widgetItem.setText(0,text)
                #expand parent widget item
                self.treeWidget.setExpanded( self.treeWidget.indexFromItem(item), True)
                return widgetItem
            else :
                self.error_message('Select one parent item first.')
        else:
            widgetItem = QtGui.QTreeWidgetItem()
            parent.addChild( widgetItem )
            #widgetItem.setText(i,'$A')
            widgetItem.setFlags(widgetItem.flags() | QtCore.Qt.ItemIsEditable)
            if text:
                widgetItem.setText(0,text)
            #expand parent widget item
            self.treeWidget.setExpanded( self.treeWidget.indexFromItem(parent), True)
            return widgetItem
                    
    def remove_treeWidget_item(self):
        # Get selected treeWidget item
        item = self.treeWidget.currentItem()
        if item:
            # get parent and then delete child item
            if item.parent():
                item.parent().removeChild(item)
                   
    def error_message(self,message):
        warningsDialog = QtGui.QErrorMessage(self)
        warningsDialog.showMessage(message)
         
    def save_preset(self):
        # get self.Dir_Framework
        self.get_dir_framework()
        if not self.Dir_Framework:
            self.error_message('Dir Framework error.')
            return False 
        #
        fileName = self.save_preset_dialog()
        if fileName: 
            import pickle
            with open(fileName,'w') as f:
                pickle.dump(self.Dir_Framework, f)
         
    def open_preset(self):
        fileName = self.open_preset_dialog()
        if fileName: 
            # clear tree widget items
            #self.treeWidget.takeTopLevelItem(0)
            self.treeWidget.clear()
            # re create root widget item
            item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
            self.treeWidget.topLevelItem(0).setText(0,"Root")
            # get parent widget item
            import pickle
            with open(fileName,'r') as f:
                # apply preset to widget
                self.set_items_text_in_treeWidget( pickle.load(f),item_0 )
            # set expand to tree widget
            self.treeWidget.setExpanded( self.treeWidget.indexFromItem(item_0), True)
                         
    def save_preset_dialog(self):
        text = None
        fd = QtGui.QFileDialog(self,'','','')
        fd.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        fd.setFileMode(QtGui.QFileDialog.AnyFile)
        filename = fd.getSaveFileName(self, 'Save file', '', '*.ini')
        return filename
                            
    def open_preset_dialog(self):
        text = None
        fd = QtGui.QFileDialog(self,'','','')
        filename = fd.getOpenFileName(self, 'Open file', '', '*.ini')
        return filename
        
    def main(self):
        # get root directory
        self.get_root_dir()
        if not self.Dir_Root :
            #bring up error messages
            self.error_message('Please select one root directory first.')
            return False 
        # get directory
        self.get_dir_framework()
        if not self.Dir_Framework:
            self.error_message('Dir Framework error.')
            return False 
        # get directory's key and value
        self.get_dir_name()
        if not self.Dir_Name:
            self.error_message('Dir Name error.')
            return False
        # create folder
        self.perform_create_directory()
        
    
def main():
    app = QtGui.QApplication(sys.argv)
    main = StartQt4()
    main.show()
    sys.exit(app.exec_())
    
if __name__=='__main__':
    main()
