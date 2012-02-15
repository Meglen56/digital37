# -*- coding: utf-8 -*- 
import sip
from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
import maya.OpenMayaUI
 
import digital37.qt.TextView as TextView
reload(TextView)

import digital37.maya.general.SvnMaya as SvnMaya
reload(SvnMaya)

class StartSvnMaya(QtGui.QMainWindow,TextView.Ui_TextView, SvnMaya.SvnMaya):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        SvnMaya.SvnMaya.__init__(self)
                                     
def getMayaWindow():
    ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

def main():
    global SvnMaya_app
    global SvnMaya_myapp
    SvnMaya_app = QtGui.qApp
    SvnMaya_myapp = StartSvnMaya(getMayaWindow())
    SvnMaya_myapp.show()
    SvnMaya_myapp.set_window(SvnMaya_myapp.textBrowser)
    SvnMaya_myapp.get_associated_file()

if __name__ == "__main__":
    main()