# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TextView.ui'
#
# Created: Wed Feb 15 21:37:52 2012
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
        TextView.resize(220, 120)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Adobe Arabic"))
        TextView.setFont(font)
        TextView.setWindowTitle(QtGui.QApplication.translate("TextView", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout = QtGui.QGridLayout(TextView)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.textBrowser = QtGui.QTextBrowser(TextView)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setMinimumSize(QtCore.QSize(200, 100))
        font = QtGui.QFont()
