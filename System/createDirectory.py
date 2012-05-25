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
        
    def file_dialog(self):
        fd = QtGui.QFileDialog(self,'','','')
        self.lineEdit_rootDir.setText( fd.getExistingDirectory() )
    
    def on_pushButton_rootDir_pressed(self):
        self.file_dialog()
        #self.lineEdit_rootDir.setText( self.Dir_Root )
    
    def on_pushButton_add_pressed(self):
        self.addTreeWidgetItem()
    
    def on_pushButton_remove_pressed(self):
        self.removeTreeWidgetItem()
    
    def on_pushButton_test_pressed(self):
        self.get_dir_framework()

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
    
    def get_dir_name(self):
        # only have two columns 0 for key 1 for value 
        for j in range(self.tableWidget.rowCount()) :
            if self.tableWidget.item(j,0) :
                k = str( self.tableWidget.item(j,0).text() )
                v = str( self.tableWidget.item(j,1).text() )
                self.Dir_Name[k] = v
        print self.Dir_Name
                
    def addTreeWidgetItem(self):
        widgetItem = None
        # Get selected treeWidget item first
        items = self.treeWidget.selectedItems()
        if items:
            item = items[0]
            widgetItem = QtGui.QTreeWidgetItem()
            item.addChild( widgetItem )
            #widgetItem.setText(i,'$A')
            widgetItem.setFlags(widgetItem.flags() | QtCore.Qt.ItemIsEditable)
            return widgetItem
        else :
            self.error_message('Select one parent item first.')
                    
    def removeTreeWidgetItem(self):
        # Get selected treeWidget item first
        items = self.treeWidget.selectedItems()
        if items:
            for i in items:
                try:
                    self.treeWidget.removeItemWidget(i,0)
                except:
                    traceback.print_exc()
                   
    def error_message(self,message):
        warningsDialog = QtGui.QErrorMessage(self)
        warningsDialog.showMessage(message)
         
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
