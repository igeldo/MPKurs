# Import necessary modules:

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QComboBox, QPushButton, QGridLayout, QMessageBox, QAction)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (QFont, QIcon)
from serial.tools import list_ports


class Model:
    """With which data do we want to work?"""
    def __init__(self):
        self.tx_port = None
        self.rx_port = None
        self.ports = [port.device for port in list_ports.comports()]


class View(QtWidgets.QWidget):
    """How should the GUI look like?"""
    verifySignal = QtCore.pyqtSignal()

    def __init__(self):
        super(View, self).__init__()
        self.tx_port = None
        self.rx_port = None
        self.initUI()

    def initUI(self):
        lay = QGridLayout(self)
        title = Qt


class Controller:
    """How should the GUI behave?"""
    def __init__(self):
        self._app = QApplication(sys.argv)
        self._model = Model()
        self._view = View()
        self.init()




if __name__ == '__main__':
    c = Controller()
    sys.exit(c.run())
