## Usage:
## import sys
## sys.path.append('/q/devkit/scripts')
## import windowPyQt2
## reload(windowPyQt2)
## windowPyQt2.main()

import sip
import maya.OpenMayaUI as mui
from PyQt4 import QtCore, QtGui
from digital37.maya.general.edytor import Ui_notepad

class StartQt4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_notepad()
        self.ui.setupUi(self)
        # here we connect signals with our slots
        QtCore.QObject.connect(self.ui.button_open,QtCore.SIGNAL("clicked()"), self.file_dialog)
        
    def file_dialog(self):
        fd = QtGui.QFileDialog(self)
        self.filename = fd.getOpenFileName()
        from os.path import isfile
        if isfile(self.filename):
            text = open(self.filename).read()
            self.ui.editor_window.setText(text)

def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

def main():
    global app
    global form
    app = QtGui.qApp
    form = StartQt4(getMayaWindow())
    form.show()
