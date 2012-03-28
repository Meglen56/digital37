import sip
from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
import maya.OpenMayaUI

import digital37.qt.TextView as TextView

class StartTextView(QtGui.QMainWindow,TextView.Ui_TextView):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
                                     
def getMayaWindow():
    ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

def main():
    global TextView_app
    global TextView_myapp
    TextView_app = QtGui.qApp
    TextView_myapp = StartTextView(getMayaWindow())
    TextView_myapp.show()

if __name__ == "__main__":
    main()