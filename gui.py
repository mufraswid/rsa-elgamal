# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
import os
import time
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.uic import loadUi
from PyQt5.Qt import QAbstractItemView
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from elgamal import Elgamal
from rsa import RSA
from diffie_hellman import DiffieHellman


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi(os.getcwd() + '/gui.ui', self)
        self.constraint_input()
        self.connect_buttons()
        self.elgamal = Elgamal()
        self.rsa = RSA()
        self.dh = DiffieHellman()
        self.mode = None
        self.format = None
    
    def constraint_input(self):
        self.onlyInt = QIntValidator()

        self.RSA_key_e_value.setValidator(self.onlyInt)
        self.RSA_key_d_value.setValidator(self.onlyInt)
        self.RSA_key_n_value.setValidator(self.onlyInt)
        self.RSA_sess_n_value.setValidator(self.onlyInt)
        self.RSA_sess_g_value.setValidator(self.onlyInt)
        self.RSA_sess_x_value.setValidator(self.onlyInt)
        self.RSA_sess_y_value.setValidator(self.onlyInt)

        self.EG_key_p_value.setValidator(self.onlyInt)
        self.EG_key_g_value.setValidator(self.onlyInt)
        self.EG_key_x_value.setValidator(self.onlyInt)
        self.EG_key_y_value.setValidator(self.onlyInt)
        self.EG_sess_n_value.setValidator(self.onlyInt)
        self.EG_sess_g_value.setValidator(self.onlyInt)
        self.EG_sess_x_value.setValidator(self.onlyInt)
        self.EG_sess_y_value.setValidator(self.onlyInt)

        self.RSA_output_text.setReadOnly(True)
        self.EG_output_text.setReadOnly(True)


    def connect_buttons(self):
        # Main menu buttons
        self.rsabutton.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(1))
        self.egbutton.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(2))

        # RSA buttons
        self.RSA_key_savebutton.clicked.connect(self.rsa_save_key)
        self.RSA_act_execbutton.clicked.connect(self.rsa_execute)
        self.RSA_key_genbutton.clicked.connect(self.rsa_generate_key)
        self.RSA_key_filebutton.clicked.connect(self.rsa_import_key)
        self.RSA_act_decbutton.clicked.connect(self.set_mode_dec)
        self.RSA_act_encbutton.clicked.connect(self.set_mode_enc)
        self.RSA_input_filebutton.clicked.connect(self.rsa_get_input_file)
        self.RSA_fmt_txtbutton.clicked.connect(self.set_format_txt)
        self.RSA_fmt_filebutton.clicked.connect(self.set_format_file)
        self.RSA_returnbutton.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(0))
        self.RSA_sess_genbutton.clicked.connect(self.rsa_diffiehellman_generate_key)

        # Elgamal buttons
        self.EG_key_savebutton.clicked.connect(self.elgamal_save_key)
        self.EG_act_execbutton.clicked.connect(self.elgamal_execute)
        self.EG_key_genbutton.clicked.connect(self.elgamal_generate_key)
        self.EG_key_filebutton.clicked.connect(self.elgamal_import_key)
        self.EG_act_decbutton.clicked.connect(self.set_mode_dec)
        self.EG_act_encbutton.clicked.connect(self.set_mode_enc)
        self.EG_input_filebutton.clicked.connect(self.elgamal_get_input_file)
        self.EG_fmt_txtbutton.clicked.connect(self.set_format_txt)
        self.EG_fmt_filebutton.clicked.connect(self.set_format_file)
        self.EG_returnbutton.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(0))
        self.EG_sess_genbutton.clicked.connect(self.eg_diffiehellman_generate_key)

    # DIFFIE HELMAN STUFF
    def rsa_diffiehellman_generate_key(self):
        self.dh.generate_parameters()
        n, g, x, y = self.dh.get_parameters()
        self.RSA_sess_n_value.setText(str(n))
        self.RSA_sess_g_value.setText(str(g))
        self.RSA_sess_x_value.setText(str(x))
        self.RSA_sess_y_value.setText(str(y))
        sess_key = self.dh.get_session_key()
        self.RSA_sess_result.setText(str(sess_key))

    def eg_diffiehellman_generate_key(self):
        self.dh.generate_parameters()
        n, g, x, y = self.dh.get_parameters()
        self.EG_sess_n_value.setText(str(n))
        self.EG_sess_g_value.setText(str(g))
        self.EG_sess_x_value.setText(str(x))
        self.EG_sess_y_value.setText(str(y))
        sess_key = self.dh.get_session_key()
        self.EG_sess_result.setText(str(sess_key))

    # RSA STUFF
    def rsa_save_key(self):
        fileNamePub, _ = QFileDialog.getSaveFileName(None, "Save RSA Public Key", "", "Public Key File (*.pub)")
        fileNamePri, _ = QFileDialog.getSaveFileName(None, "Save RSA Private Key", "", "Private Key File (*.pri)")
        # self.rsa.generate_key()
        self.rsa.save_generated_keys(fileNamePub, fileNamePri)

    def rsa_set_public_key(self):
        e = int(self.RSA_key_e_value.text())
        n = int(self.RSA_key_n_value.text())
        self.rsa.set_public_key(e, n)

    def rsa_set_private_key(self):
        d = int(self.RSA_key_d_value.text())
        n = int(self.RSA_key_n_value.text())
        self.rsa.set_private_key(d, n)

    def rsa_execute(self):
        self.rsa_set_public_key()
        self.rsa_set_private_key()
        st = time.time()
        if self.mode == 'enc':
            if self.format == 'txt':
                self.rsa.get_input(
                    bytes(
                        self.RSA_input_text.toPlainText(),
                        'UTF-8',
                        errors='ignore'
                    )
                )
                self.rsa.encrypt()
                self.RSA_output_text.setText(self.rsa.get_cipher_text())
                # print("RSA get cipher text: ", bytes(self.rsa.get_cipher_text(), 'UTF-8'))
            elif self.format == 'file':
                if self.rsa_inpfile == None:
                    self.display_value_error("File belum dipilih")
                    return
                assert self.rsa_inpfile is not None
                self.rsa.enc_from_file(self.rsa_inpfile)
                self.rsa.encrypt()
                fileName, _ = QFileDialog.getSaveFileName(None, "Save Encrypted File", "", "All Files (*)")
                print("tes({})".format(fileName))
                if fileName == "":
                    return
                self.rsa.enc_write_file(fileName)
                # Print file size
                self.RSA_size_value.setText(str(os.path.getsize(fileName) / 1000))
            else:
                self.display_value_error("Format belum dipilih")
                return
        elif self.mode == 'dec':
            if self.format == 'txt':
                check = self.RSA_input_text.toPlainText()
                print("RSA_input toPlainText ", check)
                print("length of text = {}".format(len(check)))
                for c in check:
                    print(c, end='')
                print()
                self.rsa.get_input(
                    bytes(
                        self.RSA_input_text.toPlainText(),
                        'UTF-8',
                        errors='ignore'
                    )
                )
                self.rsa.parse_msg_to_enc()
                self.rsa.decrypt()
                self.RSA_output_text.setText(self.rsa.get_plain_text())
            elif self.format == 'file':
                if self.rsa_inpfile == None:
                    self.display_value_error("File belum dipilih")
                    return
                assert self.rsa_inpfile is not None
                self.rsa.dec_from_file(self.rsa_inpfile)
                self.rsa.decrypt()
                fileName, _ = QFileDialog.getSaveFileName(None, "Save Encrypted File", "", "All Files (*)")
                print("tes({})".format(fileName))
                if fileName == "":
                    return
                self.rsa.dec_write_file(fileName)
                # Print file size
                self.RSA_size_value.setText(str(os.path.getsize(fileName) / 1000))
            else:
                self.display_value_error("Format belum dipilih")
                return
        else:
            self.display_value_error("Aksi belum dipilih")
            return

        end = str(time.time() - st)
        # Set time execution
        self.RSA_time_value.setText(end)

    def rsa_generate_key(self):
        self.rsa.generate_key()
        d, n1 = self.rsa.get_private_key()
        e, n2 = self.rsa.get_public_key()
        assert n1 == n2
        self.RSA_key_n_value.setText(str(n1))
        self.RSA_key_d_value.setText(str(d))
        self.RSA_key_e_value.setText(str(e))

    def rsa_import_key(self):
        fileNamePub, _ = QFileDialog.getOpenFileName(None, "Import RSA Public Key", "", "Public Key File (*.pub)")
        fileNamePri, _ = QFileDialog.getOpenFileName(None, "Import RSA Private Key", "", "Private Key File (*.pri)")
        self.rsa.import_public_key(fileNamePub)
        self.rsa.import_private_key(fileNamePri)
        # display the imported key in the text box
        d, n1 = self.rsa.get_private_key()
        e, n2 = self.rsa.get_public_key()
        assert n1 == n2
        self.RSA_key_n_value.setText(str(n1))
        self.RSA_key_d_value.setText(str(d))
        self.RSA_key_e_value.setText(str(e))

    def rsa_get_input_file(self):
        fileName, _ = QFileDialog.getOpenFileName(None, "Get Input File", "", "All Files (*)")
        self.rsa_inpfile = fileName
        fileName = fileName.split('/')[-1]
        self.RSA_inp_file_label.setText("Chosen file: {}".format(fileName))

    # ELGAMAL STUFF
    def elgamal_save_key(self):
        fileNamePub, _ = QFileDialog.getSaveFileName(None, "Save Elgamal Public Key", "", "Public Key File (*.pub)")
        fileNamePri, _ = QFileDialog.getSaveFileName(None, "Save Elgamal Private Key", "", "Private Key File (*.pri)")
        self.elgamal.generate_key()
        self.elgamal.save_generated_keys(fileNamePub, fileNamePri)
    
    def elgamal_set_public_key(self):
        p = int(self.EG_key_p_value.text())
        g = int(self.EG_key_g_value.text())
        y = int(self.EG_key_y_value.text())
        self.elgamal.set_public_key(p, g, y)
    
    def elgamal_set_private_key(self):
        p = int(self.EG_key_p_value.text())
        x = int(self.EG_key_x_value.text())
        self.elgamal.set_private_key(p, x)
    
    def elgamal_execute(self):
        self.elgamal_set_public_key()
        self.elgamal_set_private_key()
        st = time.time()
        if self.mode == 'enc':
            if self.format == 'txt':
                self.elgamal.get_input(
                    bytes(
                        self.EG_input_text.toPlainText(),
                        'UTF-8',
                        errors='ignore'
                    )
                )
                self.elgamal.encrypt()
                self.EG_output_text.setText(self.elgamal.get_cipher_text())
            elif self.format == 'file':
                self.elgamal.enc_from_file(self.elgamal_inpfile)
                self.elgamal.encrypt()
                fileName, _ = QFileDialog.getSaveFileName(None, "Save Encrypted File", "", "All Files (*)")
                self.elgamal.enc_write_file(fileName)
                # Print file size
                self.EG_size_value.setText(str(os.path.getsize(fileName) / 1000))
            else:
                self.display_value_error("Format belum dipilih")
                return

        elif self.mode == 'dec':
            if self.format == 'txt':
                self.elgamal.get_input(
                    bytes(
                        self.EG_input_text.toPlainText(),
                        'UTF-8',
                        errors='ignore'
                    )
                )
                self.elgamal.parse_msg_to_enc()
                self.elgamal.decrypt()
                self.EG_output_text.setText(self.elgamal.get_plain_text())
            elif self.format == 'file':
                self.elgamal.dec_from_file(self.elgamal_inpfile)
                self.elgamal.decrypt()
                fileName, _ = QFileDialog.getSaveFileName(None, "Save Encrypted File", "", "All Files (*)")
                self.elgamal.dec_write_file(fileName)
                # Print file 
                self.EG_size_value.setText(str(os.path.getsize(fileName) / 1000))
            else:
                self.display_value_error("Format belum dipilih")
                return

        else:
            self.display_value_error("Aksi belum dipilih")
            return

        end = str(time.time() - st)
        # Set time execution
        self.EG_time_value.setText(end)
    
    def elgamal_get_input_file(self):
        fileName, _ = QFileDialog.getOpenFileName(None, "Get Input File", "", "All Files (*)")
        self.elgamal_inpfile = fileName
        fileName = fileName.split('/')[-1]
        self.EG_inp_file_label.setText("Chosen file: {}".format(fileName))

    def elgamal_import_key(self):
        fileNamePub, _ = QFileDialog.getOpenFileName(None, "Import Elgamal Public Key", "", "Public Key File (*.pub)")
        fileNamePri, _ = QFileDialog.getOpenFileName(None, "Import Elgamal Private Key", "", "Private Key File (*.pri)")
        self.elgamal.import_public_key(fileNamePub)
        self.elgamal.import_private_key(fileNamePri)
    
    def elgamal_generate_key(self):
        self.elgamal.generate_key()
        g, y, p = self.elgamal.get_public_key()
        x, p = self.elgamal.get_private_key()
        self.EG_key_p_value.setText(str(p))
        self.EG_key_g_value.setText(str(g))
        self.EG_key_x_value.setText(str(x))
        self.EG_key_y_value.setText(str(y))
           

    # OTHER STUFF
    def set_mode_enc(self):
        self.mode = 'enc'
    
    def set_mode_dec(self):
        self.mode = 'dec'
    
    def set_format_txt(self):
        self.format = 'txt'

    def set_format_file(self):
        self.format = 'file'

    # VALIDATION STUFF
    def display_value_error(self, err_msg : str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Error")
        msg.setInformativeText(err_msg)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
