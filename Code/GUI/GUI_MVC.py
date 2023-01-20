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


class View(QMainWindow):
    """How should the GUI look like?"""
    verifySignal = QtCore.pyqtSignal()

    def __init__(self):
        super(View, self).__init__()
        self.tx_port = None
        self.rx_port = None
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        self.setMinimumSize(300, 150)
        self.setWindowTitle("GUI for PymmWave")
        self.setWindowIcon(QIcon("images/pyqt_logo.png"))

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Headline
        header_label = QLabel("Properties")
        header_label.setFont(QFont("Helvetica", 14))
        header_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Ports
        # tx port
        tx_port_label = QLabel("TX COM Port:", self)
        tx_port_label.setFont(QFont("Helvetica", 12))
        self.tx_port = QComboBox()

        # rx port
        rx_port_label = QLabel("RX COM Port:", self)
        rx_port_label.setFont(QFont("Helvetica", 12))
        self.rx_port = QComboBox()

        # Connect and Disconnect Button in one
        self.times_pressed = 0
        self.button = QPushButton("Connect Radar")
        self.button.setFont(QFont("Helvetica", 12))

        # Add widgets to layout
        layout.addWidget(header_label, 0, 0)
        layout.addWidget(tx_port_label, 1, 0)
        layout.addWidget(self.tx_port, 1, 1)
        layout.addWidget(rx_port_label, 2, 0)
        layout.addWidget(self.rx_port, 2, 1)
        layout.addWidget(self.button, 3, 0, 1, 2)

    def createAction(self):
        self.quit_action = QAction("Quit", self)
        self.quit_action.setShortcut("Ctrl+Q")
        self.quit_action.triggered.connect(self.close)

    def createMenu(self):
        self.file_menu = self.menuBar().addMenu("Actions")
        self.file_menu.addAction(self.quit_action)


class Controller:
    """How should the GUI behave?"""
    def __init__(self):
        self._app = QApplication(sys.argv)
        self._model = Model()
        self._view = View()
        self.init()

    def init(self):
        self._view.verifySignal.connect(self.refresh_ports)

    def refresh_ports(self):
        available_ports = self._model.ports
        if not available_ports:
            self._view.button.setEnabled(False)
            self._view.tx_port.setEnabled(False)
            self._view.rx_port.setEnabled(False)
            return
        self._view.tx_port.setEnabled(True)
        self._view.rx_port.setEnabled(True)
        tx_port = self._view.tx_port.currentText()
        rx_port = self._view.rx_port.currentText()

        if tx_port == rx_port:
            self._view.button.setEnabled(False)
        else:
            self._view.button.setEnabled(True)

    def fill_tx_port(self):
        self.refresh_ports()

    def fill_rx_port(self):
        self.refresh_ports()

    def run(self):
        self._view.show()
        sys.exit(self._app.exec_())


if __name__ == '__main__':
    c = Controller()
    sys.exit(c.run())
