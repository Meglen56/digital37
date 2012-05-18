import sys
import itertools
import sip
from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
from createDirectoryUI import Ui_MainWindow


    
class StartQt4(QtGui.QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        # here we connect signals with our slots
        #QtCore.QObject.connect(self.ui.button_open,QtCore.SIGNAL("clicked()"), self.file_dialog)
                
    def file_dialog(self):
        fd = QtGui.QFileDialog(self,'','','')
        self.Dir_Root = fd.getExistingDirectory()
    
    def on_pushButton_rootDir_pressed(self):
        filename = self.file_dialog()
        self.lineEdit_rootDir.setText( self.Dir_Root )
    
    def appendListWidgetItem(self,listWidget,inputList):
        returnItem = None
        # Get listWidget items first
        widgetListItems = self.getAllItemsInListWidget(listWidget)
        if self.DEBUG:
            print 'inputList',
            print inputList
        if inputList :
            widgetItem = None
            for i,name in itertools.izip( itertools.count(1), (x for x in inputList if x not in widgetListItems) ) :
                widgetItem = QtGui.QListWidgetItem(name)
                listWidget.insertItem( i, widgetItem )
                if listWidget == self.listWidget_SL or listWidget == self.listWidget_CL:
                    widgetItem.setFlags(widgetItem.flags() | QtCore.Qt.ItemIsEditable)
            if widgetItem :
                returnItem = widgetItem
        return returnItem
    
def main():
    app = QtGui.QApplication(sys.argv)
    main = StartQt4()
    main.show()
    sys.exit(app.exec_())
    
if __name__=='__main__':
    main()
