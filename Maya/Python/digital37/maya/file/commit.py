# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'commit.ui'
#
# Created: Thu Mar 29 18:00:38 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_OptionWindow(object):
    def setupUi(self, OptionWindow):
        OptionWindow.setObjectName(_fromUtf8("OptionWindow"))
        OptionWindow.resize(184, 127)
        OptionWindow.setWindowTitle(QtGui.QApplication.translate("OptionWindow", "Commit Options", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(OptionWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.formLayout = QtGui.QFormLayout(self.centralwidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.checkBox_save = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_save.setText(QtGui.QApplication.translate("OptionWindow", "Save Before Commit", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_save.setObjectName(_fromUtf8("checkBox_save"))
        self.verticalLayout.addWidget(self.checkBox_save)
        self.checkBox_lock = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_lock.setText(QtGui.QApplication.translate("OptionWindow", "Lock After Commit", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_lock.setObjectName(_fromUtf8("checkBox_lock"))
        self.verticalLayout.addWidget(self.checkBox_lock)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_ok = QtGui.QPushButton(self.centralwidget)
        self.pushButton_ok.setText(QtGui.QApplication.translate("OptionWindow", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_ok.setObjectName(_fromUtf8("pushButton_ok"))
        self.horizontalLayout.addWidget(self.pushButton_ok)
        self.pushButton_close = QtGui.QPushButton(self.centralwidget)
        self.pushButton_close.setText(QtGui.QApplication.translate("OptionWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_close.setObjectName(_fromUtf8("pushButton_close"))
        self.horizontalLayout.addWidget(self.pushButton_close)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.formLayout.setLayout(0, QtGui.QFormLayout.LabelRole, self.verticalLayout)
        OptionWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(OptionWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        OptionWindow.setStatusBar(self.statusbar)
        self.menuBar = QtGui.QMenuBar(OptionWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 184, 18))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuEdit = QtGui.QMenu(self.menuBar)
        self.menuEdit.setTitle(QtGui.QApplication.translate("OptionWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuHelp = QtGui.QMenu(self.menuBar)
        self.menuHelp.setTitle(QtGui.QApplication.translate("OptionWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        OptionWindow.setMenuBar(self.menuBar)
        self.actionExit = QtGui.QAction(OptionWindow)
        self.actionExit.setText(QtGui.QApplication.translate("OptionWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setShortcut(QtGui.QApplication.translate("OptionWindow", "Esc", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuEdit.addAction(self.actionExit)
        self.menuBar.addAction(self.menuEdit.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(OptionWindow)
        QtCore.QObject.connect(self.pushButton_close, QtCore.SIGNAL(_fromUtf8("pressed()")), OptionWindow.close)
        QtCore.QObject.connect(self.pushButton_ok, QtCore.SIGNAL(_fromUtf8("pressed()")), OptionWindow.close)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("triggered()")), OptionWindow.close)
        QtCore.QMetaObject.connectSlotsByName(OptionWindow)

    def retranslateUi(self, OptionWindow):
        pass

