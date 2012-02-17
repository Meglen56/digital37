# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AssetSearch.ui'
#
# Created: Thu Feb 16 17:25:23 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Root(object):
    def setupUi(self, Root):
        Root.setObjectName(_fromUtf8("Root"))
        Root.resize(238, 343)
        Root.setWindowTitle(QtGui.QApplication.translate("Root", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(Root)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setText(QtGui.QApplication.translate("Root", "Asset Search:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.verticalLayout.addWidget(self.lineEdit)
        self.listWidget = QtGui.QListWidget(self.centralwidget)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.verticalLayout.addWidget(self.listWidget)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        Root.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(Root)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Root.setStatusBar(self.statusbar)

        self.retranslateUi(Root)
        QtCore.QMetaObject.connectSlotsByName(Root)

    def retranslateUi(self, Root):
        pass

