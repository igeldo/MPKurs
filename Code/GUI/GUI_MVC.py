# Import necessary modules:
import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QComboBox, QPushButton, QVBoxLayout, QMessageBox)
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
    def __init__(self, model, controller):
        super(View, self).__init__()
        self._model = model
        self.tx_port = None
        self.rx_port = None
        self.initUI()
        self.quit_button.clicked.connect(controller.close)
        self.button.clicked.connect(self.buttonClicked)

    def initUI(self):
        layout = QVBoxLayout()
        self.setMinimumSize(300, 150)
        self.setWindowTitle("PymmWave Execution GUI")
        self.setWindowIcon(QIcon("images/pyqt_logo.png"))

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Headline
        header_label = QLabel("Properties")
        header_label.setFont(QFont("Helvetica", 12))

        # Ports
        # tx port
        tx_port_label = QLabel("Select te TX port:", self)
        tx_port_label.setFont(QFont("Helvetica", 12))
        self.tx_port = QComboBox()
        self.tx_port.addItems(self._model.ports)

        # rx port
        rx_port_label = QLabel("Select the RX port:", self)
        rx_port_label.setFont(QFont("Helvetica", 12))
        self.rx_port = QComboBox()
        self.rx_port.addItems(self._model.ports)

        # Connect and Disconnect Button in one
        self.times_pressed = 0
        self.button = QPushButton("Connect")
        self.button.setFont(QFont("Helvetica", 12))

        # Quit Button
        self.quit_button = QPushButton("Quit")
        self.quit_button.setFont(QFont("Helvetica", 12))

        # Add widgets to layout
        layout.addWidget(header_label)
        layout.addWidget(tx_port_label)
        layout.addWidget(self.tx_port)
        layout.addWidget(rx_port_label)
        layout.addWidget(self.rx_port)
        layout.addWidget(self.button)
        layout.addWidget(self.quit_button)


class Controller:
    """How should the GUI behave?"""
    def __init__(self):
        self._app = QApplication(sys.argv)
        self._model = Model()
        self._view = View(self)

    def close(self):
        """Prompt the user to confirm that they want to close the application."""
        result = QMessageBox.question(self._view, "Confirm Exit", "Are you sure you want to exit?", QMessageBox.Yes |
                                      QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.Yes:
            self._app.quit()

    def connect_radar(self, rx_port, tx_port):
        """Connect the radar"""
        os.chdir(r'C:\Users\Olive\PycharmProjects\MPKurs\Code\pymmw-master\source')
        os.system('python pymmw.py -r ' + rx_port + ' -t ' + tx_port)

    def update_ports(self):
        """Updates the list of available ports in the Model class and updates the options in the
        QComboBox widgets of the View class accordingly."""
        self._model.ports = [port.device for port in list_ports.comports()]
        self._view.tx_port.clear()
        self._view.rx_port.clear()
        self._view.tx_port.addItems(self._model.ports)
        self._view.rx_port.addItems(self._model.ports)

    def buttonClicked(self):
        # Done: Implement starting pymmWave functionality by clicking it.
        """If button_clicked is uneven, then show 'Connect Radar',
        otherwise 'Disconnect Radar'"""
        if self.times_pressed % 2 != 0:
            self.update_ports()
            self.button.setText("Disconnect")
        else:
            # Changing the current working directory
            try:
                tx_port = self.tx_port.currentText()
                rx_port = self.rx_port.currentText()
                self.connect_radar(rx_port, tx_port)
                self.times_pressed += 1
                self.button.setText("Connect")
            except:
                self.button.times_pressed -= 1
                self.button.setText("Connect")
                self.button.setDisabled(True)
                print("No COM ports available.")

    def run(self):
        self._view.show()
        sys.exit(self._app.exec_())


if __name__ == '__main__':
    c = Controller()
    sys.exit(c.run())