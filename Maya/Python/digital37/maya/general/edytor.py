# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edytor.ui'
#
# Created: Wed May 26 11:03:46 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_notepad(object):
    def setupUi(self, notepad):
        notepad.setObjectName("notepad")
        notepad.resize(341, 269)
        self.button_open = QtGui.QPushButton(notepad)
        self.button_open.setGeometry(QtCore.QRect(20, 10, 151, 28))
        self.button_open.setObjectName("button_open")
        self.button_close = QtGui.QPushButton(notepad)
        self.button_close.setGeometry(QtCore.QRect(190, 10, 141, 28))
        self.button_close.setObjectName("button_close")
        self.editor_window = QtGui.QTextEdit(notepad)
        self.editor_window.setGeometry(QtCore.QRect(0, 50, 341, 221))
        self.editor_window.setObjectName("editor_window")

        self.retranslateUi(notepad)
        QtCore.QObject.connect(self.button_close, QtCore.SIGNAL("clicked()"), notepad.close)
        QtCore.QMetaObject.connectSlotsByName(notepad)

    def retranslateUi(self, notepad):
        notepad.setWindowTitle(QtGui.QApplication.translate("notepad", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.button_open.setText(QtGui.QApplication.translate("notepad", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.button_close.setText(QtGui.QApplication.translate("notepad", "Close", None, QtGui.QApplication.UnicodeUTF8))

