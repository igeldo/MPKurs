# Improved GUI
# Import necessary modules
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QCheckBox, QTextEdit, QGridLayout)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont

class MainWindow(QWidget):

    def  __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Set up the application's GUI."""
        self.setMinimumSize(640, 480)
        self.setWindowTitle("GUI for PymmWave")

        self.setUpMainWindow()
        self.show()

    def setUpMainWindow(self):
        """Create and arrange widgets in the main window."""
        header_label = QLabel("I. Properties")
        header_label.setFont(QFont("Times", 18))
        header_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Create widgets for the left side of the window
        today_label = QLabel("TX COM Port:")
        today_label.setFont(QFont("Times", 16))
        self.today_tedit = QTextEdit()

        notes_label = QLabel("RX COM Port:")
        notes_label.setFont(QFont("Times", 16))
        self.notes_tedit = QTextEdit()

        # Organize the left side widgets into column 0 of the QGridLayout
        self.main_grid = QGridLayout()
        self.main_grid.addWidget(header_label, 0, 0)
        self.main_grid.addWidget(today_label, 1, 0)
        self.main_grid.addWidget(self.today_tedit, 2, 0, 3, 1)
        self.main_grid.addWidget(notes_label, 5, 0)
        self.main_grid.addWidget(self.notes_tedit, 6, 0, 3, 1)

        # Create widgets for the right side of the window
        today = QDate.currentDate().toString(Qt.DateFormat.ISODate)
        date_label = QLabel(today)
        date_label.setFont(QFont("Arial", 18))
        date_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        todo_label = QLabel(". To Do")
        todo_label.setFont(QFont("Arial", 14))

        # Organize the right side widgets into columns 1 and 2 of the QGridLayout
        self.main_grid.addWidget(date_label, 0, 2)
        self.main_grid.addWidget(todo_label, 1, 1, 1, 2)

        # Create 7 rows, from indexes 2-8
        for row in range(2, 9):
            item_cb = QCheckBox()
            item_edit = QLineEdit()
            self.main_grid.addWidget(item_cb, row, 1)
            self.main_grid.addWidget(item_edit, row, 2)

        # Set the layout for the main window
        self.setLayout(self.main_grid)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
