# modernkripto
Tugas Kcil 3 IF4020 Kriptografi

## Overview
This is a project from course IF4020 Cryptography. This program implements three modern cryptography algorithms (RSA, Elgamal, and Diffie-Hellman),
is GUI based, and written in Python.

## Prereqs
- PyQT5 (for GUI), and also QTDesigner for GUI
```
pip3 install --user pyqt5  
sudo apt-get install python3-pyqt5  
sudo apt-get install pyqt5-dev-tools
sudo apt-get install qttools5-dev-tools
```
- PyCryptodome (for randomize prime)
```
pip3 install pycryptodome
```

## Running the Program
Simply do:
```
python3 gui.py
```

## Screenshots

- Main Menu
![Menu](/img/main.jpg)

- RSA
![RSA](/img/rsa.jpg)

- Elgamal
![Elgamal](/img/elgamal.jpg)

Diffie-Hellman session-key generation is available at both RSA and Elgamal (Kunci Sesi)

- Additional Features:
* Import private and public key (\*.pri, \*.pub)
* Encrypt external file
* Display ciphertext external file size and cipher running time

## Issues

Currently, directly copying and pasting the ciphertext when trying to decrypt might not work well due to encoding issues.

## Contributors
- M. Fauzan Rafi Sidiq W.
- Farras M. H. Faddila