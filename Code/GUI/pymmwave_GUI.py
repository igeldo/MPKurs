"""This GUI has been created with the help of the following book:
Beginning PyQt - A Hands-on Approach to GUI Programming with PyQt6 by Joshua M Willmann"""

# Import necessary modules
import os
import serial
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QComboBox, QPushButton, QGridLayout, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import (QFont, QIcon, QAction)


def s_ports():
    # From: https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
    ports = ['COM%s' % (i + 1) for i in range(1)]
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except serial.SerialException:
            result.append('No COM port utilizable.')
    return result


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

        # Create Help menu and add actions
        help_menu = self.menuBar().addMenu("Help")
        help_menu.addAction(self.about_act)

    def buttonClicked(self):
        # Done: Implement starting pymmWave functionality by clicking it.
        # TODO: The COM ports have to be choosable!
        """If button_clicked is uneven, then show 'Connect Radar',
        otherwise 'Disconnect Radar'"""
        self.times_pressed += 1
        if self.times_pressed % 2 == 0:
            if serial.is_open(s_ports()):
                serial.close(s_ports())
            else:
                serial.open(s_ports())
            self.button.setText("Connect Radar")
        else:
            # Changing the current working directory
            try:
                os.chdir(r'C:\Users\Olive\PycharmProjects\MPKurs\Code\pymmw-master\source')
                #TODO: COM port has to be a "real" COM port.
                os.system('python pymmw.py -c', self.rx_com_port, '-d', self.tx_com_port)
                self.button.setText("Disconnect Radar")
            except:
                self.times_pressed -= 1
                self.button.setDisabled(True)
                print("No COM ports available.")



#TODO: TX and RX ports have to be choosable and mapped to the COM port.
    def rxPortsChoose(self, rx_idx):
        """Handle the RX COM port choices"""
        if rx_idx == None:
            print("No RX COM port available.")
        else:
            print("RX: ", self.rx_com_port, "ID: ", rx_idx)
        return rx_idx

    def txPortsChoose(self, tx_idx):
        """Handle the TX COM port choices"""
        if tx_idx == None:
            print("No TX COM port available.")
        else:
            print("TX: ", self.tx_com_port, "ID: ", tx_idx)
        return tx_idx

    def comparePorts(self, tx_idx, rx_idx):
        if tx_idx == rx_idx:
            print("Please consider two different ports for each signal.")
        else:
            print("Everything is fine!")

    def aboutDialog(self):
        """Display the About dialog"""
        QMessageBox.about(self, "About pymmWave GUI",
                          """<p>This GUI should help you control TI Radars</p>
                          <p>Created by Oliver Jovanović</p>""")


if __name__ == '__main__':
    # print(s_ports()) # For testing purposes.
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())