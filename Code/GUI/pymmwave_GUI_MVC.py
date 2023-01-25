# Import necessary modules:
import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QComboBox, QPushButton, QGridLayout, QMessageBox)
from PyQt5.QtGui import (QFont, QIcon)
from serial.tools import list_ports
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, filename="application.log")


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

    def initUI(self, controller):
        logging.debug("Initializing GUI. Available serial ports: %s", self._model.ports)
        layout = QGridLayout()
        self.setMinimumSize(320, 150)
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
        self.tx_port.currentTextChanged.connect(controller.check_ports)

        # rx port
        rx_port_label = QLabel("Select the RX port:", self)
        rx_port_label.setFont(QFont("Helvetica", 12))
        self.rx_port = QComboBox()
        self.rx_port.addItems(controller._model.ports)
        self.rx_port.currentTextChanged.connect(controller.check_ports)

        # Connect and Disconnect Button in one
        self.times_pressed = 0
        self.button = QPushButton("Connect")
        self.button.setFont(QFont("Helvetica", 12))
        self.button.clicked.connect(controller.buttonClicked)

        # Quit Button
        self.quit_button = QPushButton("Quit")
        self.quit_button.setFont(QFont("Helvetica", 12))
        self.quit_button.clicked.connect(controller.close)

        # Add widgets to layout
        layout.addWidget(header_label, 0, 0)
        layout.addWidget(tx_port_label, 1, 0)
        layout.addWidget(self.tx_port, 1, 1)
        layout.addWidget(rx_port_label, 2, 0)
        layout.addWidget(self.rx_port, 2, 1)
        layout.addWidget(self.button, 4, 0)
        layout.addWidget(self.quit_button, 4, 1)

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
        help_action = help_menu.addAction("Help", controller.help)
        icon_help = QIcon("images/help.svg")
        help_action.setIcon(icon_help)
        help_menu.addSeparator()
        about_action = help_menu.addAction("About", controller.about)
        icon_about = QIcon("images/about.svg")
        about_action.setIcon(icon_about)


class Controller:
    """How should the GUI behave?"""
    def __init__(self):
        self._app = QApplication(sys.argv)
        self._model = Model()
        self._view = View(self._model, self)
        self._view.button.clicked.connect(self.buttonClicked)
        self.check_ports()

    def close(self):
        logging.debug("Closing the Application.")
        """Prompt the user to confirm that they want to close the application."""
        result = QMessageBox.question(self._view, "Confirm Exit", "Are you sure you want to exit?", QMessageBox.Yes |
                                      QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.Yes:
            self._app.quit()

    def connect(self):
        """Connect the radar"""
        tx_port = self._view.tx_port.currentText()
        rx_port = self._view.rx_port.currentText()
        self._model.tx_port = tx_port # Should be COM3
        self._model.rx_port = rx_port # Should be COM4
        print(f'Connected to {tx_port} and {rx_port}')
        os.chdir(r'C:\Users\Olive\PycharmProjects\MPKurs\Code\pymmw-master\source')
        os.system('python pymmw.py -c ' + rx_port + ' -d ' + tx_port)
        print("pymmwave started.")
        print("python pymmw.py -c {tx_port} -d {rx_port}")

    def disconnect(self):
        print("Disconnected.")

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
        logging.debug("Refreshing serial ports.")
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
        logging.debug("Connect button clicked. TX port: %s, RX port: %s", self._model.tx_port, self._model.rx_port)
        if self._view.times_pressed % 2 != 0:
            self.disconnect()
            self.button.setText("Connect")
        else:
            self.connect()
            self._view.button.setText("Disconnect")
            self._view.times_pressed += 1

    def about(self):
        """Show an about-dialog."""
        logging.debug("About button clicked.")
        """Show an about-dialog."""
        QMessageBox.about(self._view, "About", """<p>This GUI should help you control TI Radars</p>
        <p>Created by Oliver Jovanović</p>""")

    def help(self):
        """Show a help-dialog."""
        QMessageBox.about(self._view, "Help", "Select the tx and rx ports and click 'connect' "
                                              "to establish a connection.<p> The creator of the GUI recommends: "
                                              "TX = COM3 and RX = COM4.</p>")

    def run(self):
        self._view.show()
        sys.exit(self._app.exec_())


if __name__ == '__main__':
    c = Controller()
    sys.exit(c.run())
