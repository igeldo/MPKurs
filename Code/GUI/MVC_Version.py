import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QComboBox, QPushButton, QGridLayout, QMessageBox, QAction)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (QFont, QIcon)
from serial.tools import list_ports


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initializeUI()
        self.check_ports()

    def initializeUI(self):
        """Set up the application's GUI."""
        self.setMinimumSize(300, 150)
        self.setWindowTitle("GUI for PymmWave")
        self.setWindowIcon(QIcon("images/pyqt_logo.png"))

        # Create model
        self.model = Model()

        # Create view
        self.view = View(self.model)
        self.setCentralWidget(self.view)

        # Create controller
        self.controller = Controller(self.model, self.view)

        self.createActions()
        self.createMenu()
        self.show()

    def createActions(self):
        """Create the application's menu actions."""
        # Create the actions for File menu
        self.quit_act = QAction(QIcon("images/exit.png"), "Quit")
        self.quit_act.setShortcut("Ctrl+Q")
        self.quit_act.triggered.connect(self.close)

    def createMenu(self):
        """Create the application's menu bar."""
        self.file_menu = self.menuBar().addMenu("File")
        self.file_menu.addAction(self.quit_act)

    def check_ports(self):
        """Check if the selected ports are the same."""
        if self.model.tx_com_port == self.model.rx_com_port:
            QMessageBox.warning(self, "Warning", "TX and RX ports cannot be the same.")
            self.controller.disable_connect_button()

    def closeEvent(self, event):
        """Prompt the user to confirm that they want to close the application."""
        result = QMessageBox.question(self, "Confirm Exit", "Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No)
        event.accept() if result == QMessageBox.Yes else event.ignore()


class Model:
    def __init__(self):
        self.ports = [port.device for port in list_ports.comports()]
        self.tx_com_port = None
        self.rx_com_port = None


class View(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.initializeUI()

    def initializeUI(self):
        """Create and arrange widgets in the main window."""
        # Headline
        header_label = QLabel("Properties")
        header_label.setFont(QFont("Helvetica", 14))
        header_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Select Ports
        tx_com_port_label = QLabel("TX COM Port:", self)
        tx_com_port_label.setFont(QFont("Helvetica", 12))
        self.tx_com_port = QComboBox()
        self.tx_com_port.addItems(self.model.ports)
        self.tx_com_port.activated.connect(self.txPortsChoose)

        rx_com_port_label = QLabel("RX COM Port:", self)
        rx_com_port_label.setFont(QFont("Helvetica", 12))
        self.rx_com_port = QComboBox()
        self.rx_com_port.addItems(self.model.ports)
        self.rx_com_port.activated.connect(self.txPortsChoose)

        # Connect and Disconnect Button in one
        self.times_pressed = 0
        self.button = QPushButton("Connect Radar")
        self.button.setFont(QFont("Helvetica", 12))

        # Organize the left side widgets into column 0 of the QGridLayout
        main_grid = QGridLayout()
        main_grid.addWidget(header_label, 0, 0)
        main_grid.addWidget(tx_com_port_label, 1, 0)
        main_grid.addWidget(self.tx_com_port, 1, 1)
        main_grid.addWidget(rx_com_port_label, 2, 0)
        main_grid.addWidget(self.rx_com_port, 2, 1)
        main_grid.addWidget(self.button, 4, 0)

        # Set the layout for the main window
        self.setLayout(main_grid)

    def txPortsChoose(self):
        """Save the selected TX COM port."""
        self.model.tx_com_port = self.tx_com_port.currentText()

    def rxPortsChoose(self):
        """Save the selected RX COM port."""
        self.model.rx_com_port = self.rx_com_port.currentText()


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.button.clicked.connect(self.buttonClicked)
        self.view.tx_com_port.activated.connect(self.txPortsChoose)
        self.view.rx_com_port.activated.connect(self.rxPortsChoose)

    def buttonClicked(self):
        """Handle the button clicked event."""
        self.times_pressed += 1
        if self.times_pressed % 2 == 0:
            self.view.button.setText("Disconnect Radar")
            # Perform connect logic here
        else:
            self.view.button.setText("Connect Radar")
            # Perform disconnect logic here

    def disable_connect_button(self):
        """Disable the connect button."""
        self.view.button.setEnabled(False)

    def txPortsChoose(self):
        """Save the selected TX COM port."""
        self.model.tx_com_port = self.view.tx_com_port.currentText()

    def rxPortsChoose(self):
        """Save the selected RX COM port."""
        self.model.rx_com_port = self.view.rx_com_port.currentText()

    def close(self):
        """Close the application"""
        self.view.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
