import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QComboBox, QPushButton, QGridLayout, QMessageBox, QAction)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (QFont, QIcon)
from serial.tools import list_ports


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = Model()
        self.view = View(self)
        self.controller = Controller(self.model, self.view)
        self.setCentralWidget(self.view)
        self.show()


class Model:
    def __init__(self):
        self.tx_com_port = None
        self.rx_com_port = None
        self.s_ports = [port.device for port in list_ports.comports()]

    def connect_radar(self):
        pass

    def disconnect_radar(self):
        pass


class View(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Headline
        header_label = QLabel("Properties")
        header_label.setFont(QFont("Helvetica", 14))
        header_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Select Ports
        # TX COM Port
        tx_com_port_label = QLabel("TX COM POrt:", self)
        tx_com_port_label.setFont(QFont("Helvetica", 12))
        self.tx_com_port = QComboBox()
        self.tx_com_port.addItems(parent.model.s_ports)

        # RX COM Port
        rx_com_port_label = QLabel("RX COM POrt:", self)
        rx_com_port_label.setFont(QFont("Helvetica", 12))
        self.rx_com_port = QComboBox()
        self.rx_com_port.addItems(parent.model.s_ports)

        # Connect and Disconnect Button in one
        self.button = QPushButton("Connect Radar")
        self.button_close = QPushButton("Close GUI")
        main_grid = QGridLayout()
        main_grid.addWidget(header_label, 0, 0)
        main_grid.addWidget(tx_com_port_label, 1, 0)
        main_grid.addWidget(self.tx_com_port, 1, 1)
        main_grid.addWidget(rx_com_port_label, 2, 0)
        main_grid.addWidget(self.rx_com_port, 2, 1)
        main_grid.addWidget(self.button, 4, 0)
        main_grid.addWidget(self.button_close, 4, 1)
        self.setLayout(main_grid)

    def createMenu(self):
        # For Apple Systems (MacOS):
        self.menuBar().setNativeMenuBar(False)

        # Create File menu and add actions
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(self.exit_action)
        file_menu.addAction(self.read_action)

        # Create Help menu and add actions
        help_menu = self.menuBar().addMenu("&Help")
        help_menu.addAction(self.about_action)


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.button.clicked.connect(self.handle_connect)
        self.view.button_close.clicked.connect(self.handle_close)

    def handle_connect(self):
        if self.model.tx_com_port is None or self.model.rx_com_port is None:
            pass
        else:
            self.model.connect_radar()
            self.view.button.setText("Disconnect Radar")

    def createActions(self):
        self.exit_action = QAction("&Exit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.read_action = QAction("&Read", self, shortcut="Ctrl+R", triggered=self.read)
        self.about_action = QAction("&About", self, shortcut="Ctrl+A", triggered=self.about)


    def handle_close(self):
        self.model.disconnect_radar()
        self.view.button.setText("Connect Radar")
        self.view.close()
        self.parent().close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
