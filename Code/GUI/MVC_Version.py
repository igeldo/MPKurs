import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QComboBox, QPushButton, QGridLayout)

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
        self.tx_com_port = QComboBox()
        self.tx_com_port.addItems(parent.model.s_ports)
        self.rx_com_port = QComboBox()
        self.rx_com_port.addItems(parent.model.s_ports)
        self.button = QPushButton("Connect Radar")
        self.button_close = QPushButton("Close GUI")
        main_grid = QGridLayout()
        main_grid.addWidget(self.tx_com_port, 1, 1)
        main_grid.addWidget(self.rx_com_port, 2, 1)
        main_grid.addWidget(self.button, 4, 0)
        main_grid.addWidget(self.button_close, 4, 1)
        self.setLayout(main_grid)


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

    def handle_close(self):
        self.model.disconnect_radar()
        self.view.button.setText("Connect Radar")
        self.view.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
