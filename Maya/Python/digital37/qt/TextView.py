# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TextView.ui'
#
# Created: Thu Mar 29 16:30:25 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_TextView(object):
    def setupUi(self, TextView):
        TextView.setObjectName(_fromUtf8("TextView"))
        TextView.resize(802, 280)
        TextView.setWindowTitle(QtGui.QApplication.translate("TextView", "TextView", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(TextView)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.textBrowser = QtGui.QTextBrowser(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setMinimumSize(QtCore.QSize(200, 100))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Adobe Arabic"))
        font.setPointSize(16)
        self.textBrowser.setFont(font)
        self.textBrowser.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.verticalLayout.addWidget(self.textBrowser)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_ok = QtGui.QPushButton(self.centralwidget)
        self.pushButton_ok.setText(QtGui.QApplication.translate("TextView", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_ok.setObjectName(_fromUtf8("pushButton_ok"))
        self.horizontalLayout.addWidget(self.pushButton_ok)
        self.pushButton_close = QtGui.QPushButton(self.centralwidget)
        self.pushButton_close.setText(QtGui.QApplication.translate("TextView", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_close.setObjectName(_fromUtf8("pushButton_close"))
        self.horizontalLayout.addWidget(self.pushButton_close)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        TextView.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(TextView)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        TextView.setStatusBar(self.statusbar)
        self.menuBar = QtGui.QMenuBar(TextView)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 802, 18))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuEdit = QtGui.QMenu(self.menuBar)
        self.menuEdit.setTitle(QtGui.QApplication.translate("TextView", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuHelp = QtGui.QMenu(self.menuBar)
        self.menuHelp.setTitle(QtGui.QApplication.translate("TextView", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        TextView.setMenuBar(self.menuBar)
        self.actionExit = QtGui.QAction(TextView)
        self.actionExit.setText(QtGui.QApplication.translate("TextView", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setShortcut(QtGui.QApplication.translate("TextView", "Esc", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuEdit.addAction(self.actionExit)
        self.menuBar.addAction(self.menuEdit.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(TextView)
        QtCore.QObject.connect(self.pushButton_ok, QtCore.SIGNAL(_fromUtf8("pressed()")), TextView.close)
        QtCore.QObject.connect(self.pushButton_close, QtCore.SIGNAL(_fromUtf8("pressed()")), TextView.close)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("triggered()")), TextView.close)
        QtCore.QMetaObject.connectSlotsByName(TextView)

    def retranslateUi(self, TextView):
        pass

