# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MRRenderLayerPassManager.ui'
#
# Created: Thu Dec 22 19:09:26 2011
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_root(object):
    def setupUi(self, root):
        root.setObjectName(_fromUtf8("root"))
        root.resize(1099, 800)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        root.setFont(font)
        root.setWindowTitle(QtGui.QApplication.translate("root", "Mental Ray Render Layer Manager V1.0 (37digital)", None, QtGui.QApplication.UnicodeUTF8))
        root.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.centralwidget = QtGui.QWidget(root)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 321, 421))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_RL_renderLayers = QtGui.QLabel(self.widget)
        self.label_RL_renderLayers.setText(QtGui.QApplication.translate("root", "Render Layers", None, QtGui.QApplication.UnicodeUTF8))
        self.label_RL_renderLayers.setObjectName(_fromUtf8("label_RL_renderLayers"))
        self.verticalLayout.addWidget(self.label_RL_renderLayers)
        self.listView_RL = QtGui.QListView(self.widget)
        self.listView_RL.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.listView_RL.setObjectName(_fromUtf8("listView_RL"))
        self.verticalLayout.addWidget(self.listView_RL)
        self.pushButton_RL_refresh = QtGui.QPushButton(self.widget)
        self.pushButton_RL_refresh.setText(QtGui.QApplication.translate("root", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_RL_refresh.setObjectName(_fromUtf8("pushButton_RL_refresh"))
        self.verticalLayout.addWidget(self.pushButton_RL_refresh)
        self.pushButton_RL_remove = QtGui.QPushButton(self.widget)
        self.pushButton_RL_remove.setText(QtGui.QApplication.translate("root", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_RL_remove.setObjectName(_fromUtf8("pushButton_RL_remove"))
        self.verticalLayout.addWidget(self.pushButton_RL_remove)
        self.pushButton_RL_goToMasterLayer = QtGui.QPushButton(self.widget)
        self.pushButton_RL_goToMasterLayer.setText(QtGui.QApplication.translate("root", "Go To Master Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_RL_goToMasterLayer.setObjectName(_fromUtf8("pushButton_RL_goToMasterLayer"))
        self.verticalLayout.addWidget(self.pushButton_RL_goToMasterLayer)
        root.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(root)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1099, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setTitle(QtGui.QApplication.translate("root", "help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        root.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(root)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        root.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(root)
        QtCore.QMetaObject.connectSlotsByName(root)

    def retranslateUi(self, root):
        pass

