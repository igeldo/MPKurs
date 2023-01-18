"""This GUI has been created with the help of the following book:
Beginning PyQt - A Hands-on Approach to GUI Programming with PyQt6 by Joshua M Willmann"""
# TODO: Refactor in MVC-pattern!
# Import necessary modules

from serial.tools import list_ports
import os
import serial
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QComboBox, QPushButton, QGridLayout, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import (QFont, QIcon, QAction)


def s_ports():
    return [port.device for port in list_ports.comports()]


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.about_act = None
        self.full_screen_act = None
        self.ros_enable = None
        self.quit_act = None
        self.rx_com_port = None
        self.tx_com_port = None
        self.initializeUI()
        self.check_ports()

    def initializeUI(self):
        """Set up the application's GUI."""
        self.setMinimumSize(300, 150)
        self.setWindowTitle("GUI for PymmWave")
        self.setWindowIcon(QIcon("images/pyqt_logo.png"))

        self.setUpMainWindow()
        self.createActions()
        self.createMenu()
        self.show()

    def setUpMainWindow(self):
        """Create and arrange widgets in the main window."""
        # Headline
        header_label = QLabel("Properties")
        header_label.setFont(QFont("Helvetica", 14))
        header_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Select Ports
        tx_com_port_label = QLabel("TX COM Port:", self)
        tx_com_port_label.setFont(QFont("Helvetica", 12))
        self.tx_com_port = QComboBox()
        self.tx_com_port.addItems(s_ports())
        self.tx_com_port.activated.connect(self.txPortsChoose)

        rx_com_port_label = QLabel("RX COM Port:", self)
        rx_com_port_label.setFont(QFont("Helvetica", 12))
        self.rx_com_port = QComboBox()
        self.rx_com_port.addItems(s_ports())
        self.rx_com_port.activated.connect(self.rxPortsChoose)

        # Connect and Disconnect Button in one
        self.times_pressed = 0
        self.button = QPushButton("Connect Radar")
        self.button.setFont(QFont("Helvetica", 12))
        self.button.clicked.connect(self.buttonClicked)

        # Close GUI button
        self.button_close = QPushButton("Close GUI")
        self.button_close.setFont(QFont("Helvetica", 12))
        self.button_close.clicked.connect(self.close)

        # Organize the left side widgets into column 0 of the QGridLayout
        main_grid = QGridLayout()
        main_grid.addWidget(header_label, 0, 0)
        main_grid.addWidget(tx_com_port_label, 1, 0)
        main_grid.addWidget(self.tx_com_port, 1, 1)
        main_grid.addWidget(rx_com_port_label, 2, 0)
        main_grid.addWidget(self.rx_com_port, 2, 1)
        main_grid.addWidget(self.button, 4, 0)
        main_grid.addWidget(self.button_close, 4, 1)

        # Set the layout for the main window
        container = QWidget()
        container.setLayout(main_grid)
        self.setCentralWidget(container)

    def createActions(self):
        """Create the application's menu actions."""
        # Create the actions for File menu
        self.quit_act = QAction(QIcon("images/exit.png"), "Quit")
        self.quit_act.setShortcut("Ctrl+Q")
        self.quit_act.setStatusTip("Quit program")
        self.quit_act.triggered.connect(self.close)

        self.read_act = QAction("Read")
        self.read_act.setShortcut("Ctrl+R")
        self.read_act.setStatusTip("Read COM Ports in.")
        self.read_act.triggered.connect(self.update_ports)
        self.numbers_clicked = 0

        # Create actions for Help menu
        self.about_act = QAction("About")
        self.about_act.triggered.connect(self.aboutDialog)

    def createMenu(self):
        """Create the application's menu bar."""
        # For Mac
        self.menuBar().setNativeMenuBar(False)

        # Create File menu and add actions
        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(self.quit_act)
        file_menu.addAction(self.read_act)

        # Create Help menu and add actions
        help_menu = self.menuBar().addMenu("Help")
        help_menu.addAction(self.about_act)

    def buttonClicked(self):
        # Done: Implement starting pymmWave functionality by clicking it.
        """If button_clicked is uneven, then show 'Connect Radar',
        otherwise 'Disconnect Radar'"""
        self.times_pressed += 1
        if self.times_pressed % 2 != 0:
            self.update_ports()
            self.button.setText("Disconnect")
        else:
            # Changing the current working directory
            try:
                tx_port = self.tx_com_port.currentText()
                rx_port = self.rx_com_port.currentText()
                self.connect_radar(tx_port, rx_port)
                os.chdir(r'C:\Users\Olive\PycharmProjects\MPKurs\Code\pymmw-master\source')
                os.system('python pymmw.py -c', rx_port, '-d', tx_port)
                self.button.setText("Disconnect Radar")
            except:
                self.times_pressed -= 1
                self.button.setDisabled(True)
                print("No COM ports available.")

    def check_ports(self):
        available_ports = s_ports()
        if not available_ports:
            self.button.setEnabled(False)
            self.tx_com_port.setEnabled(False)
            self.rx_com_port.setEnabled(False)
            return
        self.tx_com_port.setEnabled(True)
        self.rx_com_port.setEnabled(True)
        tx_port = self.tx_com_port.currentText()
        rx_port = self.rx_com_port.currentText()
        if tx_port == rx_port:
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)

    def rxPortsChoose(self):
        self.check_ports()

    def txPortsChoose(self):
        self.check_ports()

    def connect_radar(self, tx_port, rx_port):
        try:
            self.ser_tx = serial.Serial(tx_port, 115200)
            self.ser_rx = serial.Serial(rx_port, 921600)
        except serial.SerialException as e:
            QMessageBox.critical(self, "Error", f"failed to connect: {e}")

    def aboutDialog(self):
        """Display the About dialog"""
        QMessageBox.about(self, "About pymmWave GUI",
                          """<p>This GUI should help you control TI Radars</p>
                          <p>Created by Oliver Jovanović</p>""")

    # Has no impact!
    def update_ports(self):
        self.tx_com_port.clear()
        self.tx_com_port.addItems(s_ports())
        self.rx_com_port.clear()
        self.rx_com_port.addItems(s_ports())

if __name__ == '__main__':
    # print(s_ports()) # For testing purposes.
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())