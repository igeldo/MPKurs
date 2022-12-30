# Improved GUI

"""""This GUI has been created with the help of the following book:
Beginning PyQt - A Hands-on Approach to GUI Programming with PyQt6 by Joshua M Willmann"""

# Import necessary modules
import serial
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QComboBox, QCheckBox, QPushButton, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import (QFont, QIcon)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Set up the application's GUI."""
        self.setMinimumSize(300, 150)
        self.setMaximumSize(640, 150)
        self.setWindowTitle("GUI for PymmWave")
        self.setWindowIcon(QIcon("images/pyqt_logo.png"))

        self.get_ports()
        self.setUpMainWindow()
        self.show()

    def setUpMainWindow(self):
        """Create and arrange widgets in the main window."""
        # Headline
        header_label = QLabel("Properties")
        header_label.setFont(QFont("Gothic", 14))
        header_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Select Ports
        tx_com_port_label = QLabel("TX COM Port:")
        tx_com_port_label.setFont(QFont("Helvetica", 12))
        self.tx_com_port = QComboBox()

        rx_com_port_label = QLabel("RX COM Port:")
        rx_com_port_label.setFont(QFont("Helvetica", 12))
        self.rx_com_port = QComboBox()

        # ROS check box
        ros_enable_label = QLabel("Enable ROS?")
        ros_enable_label.setFont(QFont("Helvetica", 12))
        self.ros_enable = QCheckBox()

        # Connect and Disconnect Buttons
        connect_button = QPushButton("Connect Radar")
        connect_button.setFont(QFont("Helvetica", 12))

        disconnect_button = QPushButton("Disconnect Radar")
        disconnect_button.setFont(QFont("Helvetica", 12))

        # Organize the left side widgets into column 0 of the QGridLayout
        main_grid = QGridLayout()
        main_grid.addWidget(header_label, 0, 0)
        main_grid.addWidget(tx_com_port_label, 1, 0)
        main_grid.addWidget(self.tx_com_port, 1, 1)
        main_grid.addWidget(rx_com_port_label, 2, 0)
        main_grid.addWidget(self.rx_com_port, 2, 1)
        main_grid.addWidget(ros_enable_label, 3, 0)
        main_grid.addWidget(self.ros_enable, 3, 1)
        main_grid.addWidget(connect_button, 4, 0)
        main_grid.addWidget(disconnect_button, 4, 1)

        # Set the layout for the main window
        container = QWidget()
        container.setLayout(main_grid)
        self.setCentralWidget(container)

    def get_ports(self):
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
