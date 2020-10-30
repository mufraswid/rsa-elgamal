# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.uic import loadUi
from PyQt5.Qt import QAbstractItemView
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from elgamal import Elgamal


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi(os.getcwd() + '/gui.ui', self)
        self.connect_buttons()
        self.elgamal = Elgamal(17)
        # self.rsa = RSA()

    def connect_buttons(self):
        # Main menu buttons
        self.rsabutton.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(1))
        self.egbutton.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(2))

        # RSA buttons
        # self.RSA_act_decbutton.setText(_translate("MainWindow", "Dekripsi"))
        # self.RSA_key_savebutton.setText(_translate("MainWindow", "Simpan Kunci"))
        # self.RSA_key_filebutton.setText(_translate("MainWindow", "Pilih kunci dari file"))
        # self.RSA_act_execbutton.setText(_translate("MainWindow", "EXECUTE"))
        # self.RSA_key_genbutton.setText(_translate("MainWindow", "Bangkitkan Kunci"))
        # self.RSA_input_filebutton.setText(_translate("MainWindow", "Pilih dari file"))
        # self.RSA_act_encbutton.setText(_translate("MainWindow", "Enkripsi"))
        self.RSA_returnbutton.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(0))

        # Elgamal buttons
        self.EG_key_savebutton.clicked.connect(self.elgamal_save_key)
        self.EG_act_execbutton.clicked.connect(self.elgamal_save_key)
        self.EG_key_genbutton.clicked.connect(self.elgamal_save_key)
        self.EG_key_filebutton.clicked.connect(self.elgamal_save_key)
        self.EG_act_decbutton.clicked.connect(self.elgamal_save_key)
        self.EG_act_encbutton.clicked.connect(self.elgamal_save_key)
        self.EG_input_filebutton.clicked.connect(self.elgamal_save_key)
        self.EG_returnbutton.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(0))

    # DIFFIE HELMAN STUFF


    # RSA STUFF


    # ELGAMAL STUFF
    def elgamal_save_key(self):
        fileName_video, _ = QFileDialog.getSaveFileName(None, "Save Message Stego Video", "", "All (*)")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
