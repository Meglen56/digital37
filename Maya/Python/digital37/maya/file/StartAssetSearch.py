import sip
from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
import maya.OpenMayaUI

import digital37.maya.general.AssetSearchUI as AssetSearchUI
reload(AssetSearchUI)
import digital37.maya.general.AssetSearch as AssetSearch
reload(AssetSearch)

class StartAssetSearch(QtGui.QMainWindow,AssetSearchUI.Ui_Root,AssetSearch):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        AssetSearch.__init__(self)
        self.setupUi(self)
        
        self.lineEdit.textChanged.connect(self.search)
        
    def search(self):
        # Get input text
        self.Text_Input = str( self.lineEdit.text() )
        # perform search
        self.perform_search()
               
def getMayaWindow():
    ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

def main():
    global AssetSearch_app
    global AssetSearch_myapp
    AssetSearch_app = QtGui.qApp
    AssetSearch_myapp = StartAssetSearch(getMayaWindow())
    AssetSearch_myapp.show()

if __name__ == "__main__":
    main()