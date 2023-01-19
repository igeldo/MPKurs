import sys
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets


class Model:
    def __init__(self):
        self.username = ""
        self.password = ""

    def verify_password(self):
        return self.username == "USER" and self.password == "PASS"


class View(QtWidgets.QWidget):
    verifySignal = QtCore.pyqtSignal()

    def __init__(self):
        super(View, self).__init__()
        self.username = ""
        self.password = ""
        self.initUi()

    def initUi(self):
        lay = QtWidgets.QVBoxLayout(self)
        title = QtWidgets.QLabel("<b>LOGIN</b>")
        lay.addWidget(title, alignment=QtCore.Qt.AlignHCenter)

        fwidget = QtWidgets.QWidget()
        flay = QtWidgets.QFormLayout(fwidget)
        self.usernameInput = QtWidgets.QLineEdit()
        self.usernameInput.textChanged.connect(partial(setattr, self, "username"))
        self.passwordInput = QtWidgets.QLineEdit(echoMode=QtWidgets.QLineEdit.Password)
        self.passwordInput.textChanged.connect(partial(setattr, self, "password"))
        self.loginButton = QtWidgets.QPushButton("Login")
        self.loginButton.clicked.connect(self.verifySignal)

        flay.addRow("Username: ", self.usernameInput)
        flay.addRow("Password: ", self.passwordInput)
        flay.addRow(self.loginButton)

        lay.addWidget(fwidget, alignment=QtCore.Qt.AlignHCenter)
        lay.addStretch()

    def clear(self):
        self.usernameInput.clear()
        self.passwordInput.clear()

    def showMessage(self):
        messageBox = QtWidgets.QMessageBox(self)
        messageBox.setText("your credentials are valid\n Welcome")
        messageBox.exec_()
        self.close()

    def showError(self):
        messageBox = QtWidgets.QMessageBox(self)
        messageBox.setText("your credentials are not valid\nTry again...")
        messageBox.setIcon(QtWidgets.QMessageBox.Critical)
        messageBox.exec_()


class Controller:
    def __init__(self):
        self._app = QtWidgets.QApplication(sys.argv)
        self._model = Model()
        self._view = View()
        self.init()

    def init(self):
        self._view.verifySignal.connect(self.verify_credentials)

    def verify_credentials(self):
        self._model.username = self._view.username
        self._model.password = self._view.password
        self._view.clear()
        if self._model.verify_password():
            self._view.showMessage()
        else:
            self._view.showError()

    def run(self):
        self._view.show()
        return self._app.exec_()


if __name__ == '__main__':
    c = Controller()
    sys.exit(c.run())