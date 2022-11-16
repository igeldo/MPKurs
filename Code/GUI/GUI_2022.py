# Importing necessary libraries
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QPushButton
import sys
import time


class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        # Setting up Window properties:
        self.setWindowTitle("GUI for TI Radar Systems")
        self.setGeometry(100, 100, 1024, 768)

        # Calling method:
        self.ui_components()

        # Showing all widgets:
        self.show()

    def ui_components(self):
        # Creating connect button:
        button_connect = QPushButton("Establish connection", self)
        button_connect.setGeometry(200, 150, 150, 40)
        button_connect.clicked.connect(self.clickme_connect)

        # Creating disconnect button:
        button_disonnect = QPushButton("Disconnect", self)
        button_disonnect.setGeometry(400, 150, 100, 40)
        button_disonnect.clicked.connect(self.clickme_disconnect)

        button_close = QPushButton("Close Application", self)
        button_close.setGeometry(550, 150, 100, 40)
        button_close.clicked.connect(self.click_close)

    def clickme_connect(self):
        print("Please wait, connection is being established...")
        time.sleep(0.5)
        print("Connection established.")

    def clickme_disconnect(self):
        print("Please wait, disconnecting device...")
        time.sleep(1)
        print("Disconnection executed.")

    def click_close(self):
        print("User closed App by Button.")
        sys.exit(0)

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
