# Import necessary modules:
import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QComboBox, QPushButton, QVBoxLayout, QMessageBox)
from PyQt5.QtGui import (QFont, QIcon)
from serial.tools import list_ports
from PyQt5.QtCore import QTimer


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
        self.initUI(controller)
        self.quit_button.clicked.connect(controller.close)

    def initUI(self, controller):
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
        self.tx_port.addItems(controller._model.ports)

        # rx port
        rx_port_label = QLabel("Select the RX port:", self)
        rx_port_label.setFont(QFont("Helvetica", 12))
        self.rx_port = QComboBox()
        self.rx_port.addItems(controller._model.ports)

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

        # Create menu bar
        menu_bar = self.menuBar()

        # Create File menu
        file_menu = menu_bar.addMenu("File")
        refresh_action = file_menu.addAction("Refresh", controller.update_ports)
        icon_refresh = QIcon("images/refresh.png")
        refresh_action.setIcon(icon_refresh)
        file_menu.addSeparator()
        exit_action = file_menu.addAction("Exit", controller.close)
        icon_exit = QIcon("images/exit.png")
        exit_action.setIcon(icon_exit)

        # Create Help menu
        help_menu = menu_bar.addMenu("Help")
        about_action = help_menu.addAction("About", controller.about)
        icon_about = QIcon("images/about.svg")
        about_action.setIcon(icon_about)

        self.tx_port.currentTextChanged.connect(controller.check_ports)
        self.rx_port.currentTextChanged.connect(controller.check_ports)


class Controller:
    """How should the GUI behave?"""
    def __init__(self):
        self._app = QApplication(sys.argv)
        self._model = Model()
        self._view = View(self._model, self)
        self._view.button.clicked.connect(self.buttonClicked)
        self.check_ports()

        self.timer = QTimer(self._app)
        self.timer.timeout.connect(self.check_ports)
        self.timer.start(1000)

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

    def check_ports(self):
        """Check if ports are not empty, if they are empty make them not choosable."""
        if not self._model.ports:
            self._view.tx_port.setEnabled(False)
            self._view.rx_port.setEnabled(False)
            self._view.button.setEnabled(False)
        else:
            self._view.tx_port.setEnabled(True)
            self._view.rx_port.setEnabled(True)
            self._view.button.setEnabled(True)
            tx_port = self._view.tx_port.currentText()
            rx_port = self._view.rx_port.currentText()
            """Check if ports are the same, if true, then disable the connect button!"""
            if tx_port == rx_port:
                self._view.button.setEnabled(False)
            else:
                self._view.button.setEnabled(True)

    def update_ports(self):
        """Updates the list of available ports in the Model class and updates the options in the
        QComboBox widgets of the View class accordingly."""
        self._model.ports = [port.device for port in list_ports.comports()]
        self._view.tx_port.clear()
        self._view.tx_port.addItems(self._model.ports)
        self._view.rx_port.clear()
        self._view.rx_port.addItems(self._model.ports)
        self.check_ports()

    def buttonClicked(self):
        """If button_clicked is uneven, then show "Connect", otherwise disconnect"""
        if self.times_pressed % 2 != 0:
            self.update_ports()
            self.button.setText("Disconnect")
        else:
            try:
                tx_port = self.tx_port.currentText()
                rx_port = self.rx_port.currentText()
                self.connect_radar(rx_port, tx_port)
            except:
                self.button.times_pressed -= 1
                self.button.setText("Connect")
                self.button.setDisabled(True)
                print("No COM ports available!")

    def about(self):
        """Show an about-dialog."""
        QMessageBox.about(self._view, "About", """<p>This GUI should help you control TI Radars</p>
        <p>Created by Oliver Jovanović</p>""")

    def run(self):
        self._view.show()
        sys.exit(self._app.exec_())


if __name__ == '__main__':
    c = Controller()
    sys.exit(c.run())
