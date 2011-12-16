# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MRRenderLayerPass.ui'
#
# Created: Fri Dec 16 13:34:36 2011
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
        root.resize(764, 521)
        root.setWindowTitle(QtGui.QApplication.translate("root", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(root)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(180, 50, 190, 132))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.Tab_layer = QtGui.QWidget()
        self.Tab_layer.setObjectName(_fromUtf8("Tab_layer"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.Tab_layer)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(self.Tab_layer)
        self.label.setText(QtGui.QApplication.translate("root", "Render Layer:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.toolButton = QtGui.QToolButton(self.Tab_layer)
        self.toolButton.setText(QtGui.QApplication.translate("root", "Color", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.horizontalLayout.addWidget(self.toolButton)
        self.toolButton_ao = QtGui.QToolButton(self.Tab_layer)
        self.toolButton_ao.setText(QtGui.QApplication.translate("root", "AO", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_ao.setObjectName(_fromUtf8("toolButton_ao"))
        self.horizontalLayout.addWidget(self.toolButton_ao)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.toolButton_5 = QtGui.QToolButton(self.Tab_layer)
        self.toolButton_5.setText(QtGui.QApplication.translate("root", "Back Light", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_5.setObjectName(_fromUtf8("toolButton_5"))
        self.horizontalLayout_2.addWidget(self.toolButton_5)
        self.toolButton_4 = QtGui.QToolButton(self.Tab_layer)
        self.toolButton_4.setText(QtGui.QApplication.translate("root", "Fill Light", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_4.setObjectName(_fromUtf8("toolButton_4"))
        self.horizontalLayout_2.addWidget(self.toolButton_4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.toolButton_3 = QtGui.QToolButton(self.Tab_layer)
        self.toolButton_3.setText(QtGui.QApplication.translate("root", "Key Light", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_3.setObjectName(_fromUtf8("toolButton_3"))
        self.verticalLayout_2.addWidget(self.toolButton_3)
        self.tabWidget.addTab(self.Tab_layer, _fromUtf8(""))
        self.Tab_pass = QtGui.QWidget()
        self.Tab_pass.setObjectName(_fromUtf8("Tab_pass"))
        self.tabWidget.addTab(self.Tab_pass, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        root.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(root)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 764, 18))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setTitle(QtGui.QApplication.translate("root", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        root.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(root)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        root.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(root)
        self.actionOpen.setText(QtGui.QApplication.translate("root", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.menuFile.addAction(self.actionOpen)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(root)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(root)

    def retranslateUi(self, root):
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab_layer), QtGui.QApplication.translate("root", "Tab 1", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab_pass), QtGui.QApplication.translate("root", "页", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("root", "Tab 2", None, QtGui.QApplication.UnicodeUTF8))

