# Importing necessary libraries
import time

from PyQt6.QtGui import *
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QPushButton
from PyQt6.QtCore import QSize, Qt
import sys


class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        # Setting up Window properties:
        self.setWindowTitle("GUI for TI Radar Systems")
        self.setGeometry(100, 100, 1024, 768)

        # Calling method:
        self.UiComponents()

        # Showing all widgets:
        self.show()

    def UiComponents(self):
        # Creating connect button:
        buttonConnect = QPushButton("Establish connection", self)
        buttonConnect.setGeometry(200, 150, 150, 40)
        buttonConnect.clicked.connect(self.clickmeConnect)

        # Creating disconnect button:
        buttonDisonnect = QPushButton("Disconnect", self)
        buttonDisonnect.setGeometry(400, 150, 100, 40)
        buttonDisonnect.clicked.connect(self.clickmeDisconnect)

        buttonClose = QPushButton("Close Application", self)
        buttonClose.setGeometry(550, 150, 100, 40)
        buttonClose.clicked.connect(self.clickClose)

    def clickmeConnect(self):
        print("Please wait, connection is being established...")
        time.sleep(0.5)
        print("Connection established!")

    def clickmeDisconnect(self):
        print("Please wait, disconnection is being executed")
        time.sleep(1)
        print("Disconnection approved!")

    def clickClose(self):
        print("User pushed close button")
        sys.exit(0)

    def closeEvent(self, event):
        print("User has clicked the close button on the main window!")
        event.accept()



if __name__ == "__main__":
    # Create PyQt6 App:
    app = QApplication(sys.argv)

    # Create instance of the class Window:
    window = Window()

    # Starting the event loop / App:
    sys.exit(app.exec())
