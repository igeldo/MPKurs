"""This GUI has been created with the help of the following book:
Beginning PyQt - A Hands-on Approach to GUI Programming with PyQt6 by Joshua M Willmann"""

# Import necessary modules
import serial
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QComboBox, QCheckBox, QPushButton, QGridLayout,
                             QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import (QFont, QIcon, QAction)


def s_ports():
    # From: https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
    ports = ['COM%s' % (i + 1) for i in range(256)]
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except serial.SerialException:
            pass
    return result

# TODO: Add tabs, establish connection with pymmWave-functionality.


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
        self.tx_com_port_label = QLabel("TX COM Port:", self)
        self.tx_com_port_label.setFont(QFont("Helvetica", 12))
        self.tx_com_port = QComboBox()
        self.tx_com_port.addItems(s_ports())
        self.tx_com_port.activated.connect(self.portsChoose)

        self.rx_com_port_label = QLabel("RX COM Port:", self)
        self.rx_com_port_label.setFont(QFont("Helvetica", 12))
        self.rx_com_port = QComboBox()
        self.rx_com_port.addItems(s_ports())

        # ROS check box
        self.ros_enable_label = QLabel("Enable ROS?")
        self.ros_enable_label.setFont(QFont("Helvetica", 12))
        self.ros_enable = QCheckBox(self)
        self.ros_enable.toggled.connect(self.ROSenabled)

        # Connect and Disconnect Button in one
        self.times_pressed = 0
        self.button = QPushButton("Connect Radar", self)
        self.button.setFont(QFont("Helvetica", 12))
        self.button.clicked.connect(self.buttonClicked)

        # Close GUI button
        self.button_close = QPushButton("Close GUI")
        self.button_close.setFont(QFont("Helvetica", 12))
        self.button_close.clicked.connect(self.close)

        # Organize the left side widgets into column 0 of the QGridLayout
        main_grid = QGridLayout()
        main_grid.addWidget(header_label, 0, 0)
        main_grid.addWidget(self.tx_com_port_label, 1, 0)
        main_grid.addWidget(self.tx_com_port, 1, 1)
        main_grid.addWidget(self.rx_com_port_label, 2, 0)
        main_grid.addWidget(self.rx_com_port, 2, 1)
        main_grid.addWidget(self.ros_enable_label, 3, 0)
        main_grid.addWidget(self.ros_enable, 3, 1)
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

        # Create the actions for View menu
        self.full_screen_act = QAction("Full Screen", checkable=True)
        self.full_screen_act.setStatusTip("Switch to full screen mode.")
        self.full_screen_act.triggered.connect(self.switchToFullScreen)

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

        # Create View menu, Appearance submenu and add actions
        view_menu = self.menuBar().addMenu("View")
        appearance_submenu = view_menu.addMenu("Appearance")
        appearance_submenu.addAction(self.full_screen_act)

        # Create Help menu and add actions
        help_menu = self.menuBar().addMenu("Help")
        help_menu.addAction(self.about_act)

    def buttonClicked(self):
        """If button_clicked is uneven, then show 'Connect Radar',
        otherwise 'Disconnect Radar'"""
        self.times_pressed += 1
        if self.times_pressed % 2 == 0:
            self.button.setText("Connect Radar")
        else:
            self.button.setText("Disconnect Radar")

    def portsChoose(self):
        if self.rx_com_port == 0 and self.tx_com_port == 0:
            print("Please connect Radar System to your PC.")
        if self.rx_com_port == self.tx_com_port:
            print("Please choose different COM Ports for the RX and TX Port.")
        else:
            pass

    def ROSenabled(self):
        if self.sender().isChecked():
            print("ROS enabled")
        else:
            print("ROS is not enabled")

    def switchToFullScreen(self, state):
        """If state is True, then display the main window in full screen.
        Otherwise, return the window to normal."""
        if state:
            self.showFullScreen()
        else:
            self.showNormal()

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
