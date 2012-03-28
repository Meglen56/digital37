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

import digital37.maya.file.SvnMaya as SvnMaya
reload(SvnMaya)

class StartSvnMaya(QtGui.QMainWindow,TextView.Ui_TextView, SvnMaya.SvnMaya):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        SvnMaya.SvnMaya.__init__(self)
                                     
def getMayaWindow():
    ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

def commit():
    global SvnMaya_com
    global SvnMaya_commit
    SvnMaya_com = QtGui.qApp
    SvnMaya_commit = StartSvnMaya(getMayaWindow())
    SvnMaya_commit.show()
    SvnMaya_commit.set_window(SvnMaya_commit.textBrowser)
    SvnMaya_commit.svn_commit()
    
def update():
    global SvnMaya_upd
    global SvnMaya_update
    SvnMaya_upd = QtGui.qApp
    SvnMaya_update = StartSvnMaya(getMayaWindow())
    SvnMaya_update.show()
    SvnMaya_update.set_window(SvnMaya_update.textBrowser)
    SvnMaya_update.update_associated_file()

if __name__ == "__main__":
    pass