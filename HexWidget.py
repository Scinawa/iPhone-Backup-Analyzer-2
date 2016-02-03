__author__ = 'user'

import sys, sqlite3, datetime, os, hashlib, shutil, zipfile, collections, \
    posixpath
import mbdbdecoding, plistutils, magic, traceback

# homemade library to build html reports
import html_util

# libraries to deal with PLIST files
import biplist, plistlib

# PySide QT graphic libraries
from PySide import QtCore, QtGui

from hex_widget import Ui_HexWidget



class HexWidget(QtGui.QWidget):
    page = 0
    pageSize = 1024

    FILTER = ''.join(
        [(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])

    def hex2string(self, src, length=8):
        N = 0;
        result = ''
        while src:
            s, src = src[:length], src[length:]
            s = s.translate(self.FILTER)
            N += length
            result += s
        return result

    def hex2numsArray(self, src, length=1):
        N = 0;
        result = []
        while src:
            s, src = src[:length], src[length:]
            hexa = ' '.join(["%02X" % ord(x) for x in s])
            s = s.translate(self.FILTER)
            N += length
            result.append(hexa)
        return result

    def setTitle(self, title):
        self.setWindowTitle(title)

    def __init__(self, fileName=None):
        super(HexWidget, self).__init__(None)

        self.ui = Ui_HexWidget()
        self.ui.setupUi(self)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.fileName = fileName

        QtCore.QObject.connect(self.ui.buttonRight, QtCore.SIGNAL("clicked()"),
                               self.rightButtonClicked)
        QtCore.QObject.connect(self.ui.buttonLeft, QtCore.SIGNAL("clicked()"),
                               self.leftButtonClicked)
        QtCore.QObject.connect(self.ui.buttonTop, QtCore.SIGNAL("clicked()"),
                               self.topButtonClicked)

        self.updateTable()

    def updateTable(self):

        self.ui.hexTable.clear()

        for i in range(0, 16):
            newItem = QtGui.QTableWidgetItem("%X" % i)
            self.ui.hexTable.setHorizontalHeaderItem(i, newItem)

        try:
            fh = open(self.fileName, 'rb')
            fh.seek(self.pageSize * self.page)
            text = fh.read(self.pageSize)

            self.ui.hexTable.setRowCount(int(len(text) / 16))

            row = 0
            while text:
                s, text = text[:16], text[16:]

                col = 0
                for element in self.hex2numsArray(s):
                    newItem = QtGui.QTableWidgetItem(str(element))
                    self.ui.hexTable.setItem(row, col, newItem)
                    col = col + 1

                newItem = QtGui.QTableWidgetItem(str(self.hex2string(s)))
                self.ui.hexTable.setItem(row, 16, newItem)

                newItem = QtGui.QTableWidgetItem(
                    "%04X" % (row * 16 + self.page * self.pageSize))
                self.ui.hexTable.setVerticalHeaderItem(row, newItem)

                row = row + 1

            fh.close()

        except:
            print()
            "Unexpected error:", sys.exc_info()

        self.ui.hexTable.resizeColumnsToContents()
        self.ui.hexTable.resizeRowsToContents()

    def leftButtonClicked(self):
        if (self.page > 0):
            self.page = self.page - 1
            self.updateTable()

    def rightButtonClicked(self):
        self.page = self.page + 1
        self.updateTable()

    def topButtonClicked(self):
        self.page = 0
        self.updateTable()
