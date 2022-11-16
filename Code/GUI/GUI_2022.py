# Importing necessary libraries
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
import sys
import time


class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        # Setting up Window properties:
        self.setWindowTitle("GUI for TI Radar Systems")
        self.setGeometry(100, 100, 640, 480)

        # Calling method:
        self.components()

        # Showing all widgets:
        self.show()

    def components(self):
        # Creating connect button:
        button_connect = QPushButton("Establish connection", self)
        button_connect.setGeometry(380, 50, 150, 40)
        button_connect.setCheckable(True)
        button_connect.clicked.connect(self.clickme_connect)

        # Creating disconnect button:
        button_disconnect = QPushButton("Disconnect", self)
        button_disconnect.setGeometry(540, 50, 100, 40)
        button_disconnect.setCheckable(True)
        button_disconnect.clicked.connect(self.clickme_disconnect)

        # Creating close Application button:
        button_close = QPushButton("Close Application", self)
        button_close.setGeometry(480, 100, 100, 40)
        button_close.setCheckable(True)
        button_close.clicked.connect(self.click_close)

        # Creating Label that should change color, when clicking button:
        self.label_connection = QLabel('Not connected', self)
        self.label_connection.setGeometry(540, 0, 100, 40)
        self.label_connection.setStyleSheet("background-color: white; border: 1px solid black;")

    # What happens, if you want to connect the device?
    def clickme_connect(self):
        print("Please wait, connection is being established...")
        time.sleep(0.5)
        print("Connection established.")
        self.label_connection.setText("Connected")
        self.label_connection.setStyleSheet("background-color: green; border: 1px solid black;")

    # What happens, if you want to disconnect the device?
    def clickme_disconnect(self):
        print("Please wait, disconnecting device...")
        time.sleep(1)
        print("Disconnection executed.")
        self.label_connection.setText("Disconnected")
        self.label_connection.setStyleSheet("background-color: red; border: 1px solid black;")

    # What happens when the Close Button is being pushed?
    @staticmethod
    def click_close():
        print("User closed App by Button.")
        sys.exit(0)

    # What happens, if main window is being closed?
    def closeEvent(self, event):
        print("User closed GUI by x on the main window.")
        event.accept()


if __name__ == "__main__":
    # Create PyQt6 App:
    app = QApplication(sys.argv)
    # Create instance of the class Window:
    window = Window()
    # Starting the event loop / App:
    sys.exit(app.exec())
