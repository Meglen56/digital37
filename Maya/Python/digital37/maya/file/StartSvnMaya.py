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

import digital37.maya.file.commit as commit
reload(commit)

class StartSvnMaya(QtGui.QMainWindow,TextView.Ui_TextView,SvnMaya.SvnMaya):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        # connect exit action to exit function
        #self.connect(self.actionExit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        SvnMaya.SvnMaya.__init__(self)
            
    def file_dialog(self):
        self.get_workspace()
        fd = QtGui.QFileDialog(self,'',self.WorkSpace_RootDir,'')
        filename = fd.getExistingDirectory()
        print filename
        return filename

class CommitOption(QtGui.QMainWindow,commit.Ui_OptionWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        # connect exit action to exit function
        #self.connect(self.actionExit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        self.pushButton_ok.pressed.connect(self.commit)
        #SvnMaya.SvnMaya.__init__(self)
        self.IsLock = True
        self.IsSave = True
        
    def commit(self):
        win = QtGui.QMainWindow(self)
        win.ui = TextView.Ui_TextView()
        win.ui.setupUi(win)
        win.show()
        
        a = SvnMaya.SvnMaya()
        a.set_window(win.ui.textBrowser)
        self.IsLock = self.checkBox_lock.isChecked()
        self.IsSave = self.checkBox_save.isChecked()
        a.svn_cmd('commit', self.IsLock, self.IsSave)
        
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
    SvnMaya_commit.svn_cmd('commit')

def commit_option():
    global SvnMaya_com
    global SvnMaya_commit
    SvnMaya_com = QtGui.qApp
    SvnMaya_commit = CommitOption(getMayaWindow())
    SvnMaya_commit.show()
        
def update():
    global SvnMaya_upd
    global SvnMaya_update
    SvnMaya_upd = QtGui.qApp
    SvnMaya_update = StartSvnMaya(getMayaWindow())
    SvnMaya_update.show()
    SvnMaya_update.set_window(SvnMaya_update.textBrowser)
    SvnMaya_update.svn_cmd('update')
        
def lock():
    global SvnMaya_upd
    global SvnMaya_update
    SvnMaya_upd = QtGui.qApp
    SvnMaya_update = StartSvnMaya(getMayaWindow())
    SvnMaya_update.show()
    SvnMaya_update.set_window(SvnMaya_update.textBrowser)
    SvnMaya_update.svn_cmd('lock')
        
def unlock():
    global SvnMaya_upd
    global SvnMaya_update
    SvnMaya_upd = QtGui.qApp
    SvnMaya_update = StartSvnMaya(getMayaWindow())
    SvnMaya_update.show()
    SvnMaya_update.set_window(SvnMaya_update.textBrowser)
    SvnMaya_update.svn_cmd('unlock')
        
def log():
    global SvnMaya_upd
    global SvnMaya_update
    SvnMaya_upd = QtGui.qApp
    SvnMaya_update = StartSvnMaya(getMayaWindow())
    SvnMaya_update.show()
    SvnMaya_update.set_window(SvnMaya_update.textBrowser)
    SvnMaya_update.svn_cmd('log')
        
def getLockStatus():
    global SvnMaya_upd
    global SvnMaya_update
    SvnMaya_upd = QtGui.qApp
    SvnMaya_update = StartSvnMaya(getMayaWindow())
    SvnMaya_update.show()
    SvnMaya_update.set_window(SvnMaya_update.textBrowser)
    SvnMaya_update.svn_cmd('getLockStatus')
                        
def update_path(path):
    global SvnMaya_upd
    global SvnMaya_update
    SvnMaya_upd = QtGui.qApp
    SvnMaya_update = StartSvnMaya(getMayaWindow())
    SvnMaya_update.show()
    SvnMaya_update.set_window(SvnMaya_update.textBrowser)
    SvnMaya_update.svn_update_project(path)
    
def update_custom_path():
    global SvnMaya_upd
    global SvnMaya_update
    SvnMaya_upd = QtGui.qApp
    SvnMaya_update = StartSvnMaya(getMayaWindow())
    path = SvnMaya_update.file_dialog()
    SvnMaya_update.show()
    SvnMaya_update.set_window(SvnMaya_update.textBrowser)
    SvnMaya_update.svn_update_path(path)
    
def update_associated():
    global SvnMaya_upd
    global SvnMaya_update
    SvnMaya_upd = QtGui.qApp
    SvnMaya_update = StartSvnMaya(getMayaWindow())
    SvnMaya_update.show()
    SvnMaya_update.set_window(SvnMaya_update.textBrowser)
    SvnMaya_update.svn_update_associated()
    
def cleanup_custom_path():
    global SvnMaya_upd
    global SvnMaya_update
    SvnMaya_upd = QtGui.qApp
    SvnMaya_update = StartSvnMaya(getMayaWindow())
    path = SvnMaya_update.file_dialog()
    SvnMaya_update.show()
    SvnMaya_update.set_window(SvnMaya_update.textBrowser)
    SvnMaya_update.svn_cleanup_path(path)
            
if __name__ == "__main__":
    #commit()
    #commit_option()
    #update_custom_path()
    #cleanup_custom_path()
    pass