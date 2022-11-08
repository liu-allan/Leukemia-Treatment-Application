import sys
import logging
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic

logging.getLogger().setLevel(logging.INFO)


class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/loginform.ui", self)

        self.users = {"John": "password"}

        self.loginPushButton.clicked.connect(self.loginPushed)

    def loginPushed(self):
        try:
            username = self.usernameLineEdit.text()
            password = self.passwordLineEdit.text()
            assert username in self.users, "User does not exist"
            assert self.users[username] == password, "Password is incorrect"
        except AssertionError as msg:
            logging.error(msg)
        else:
            logging.info("Success")
            # TODO: Connect to patient list widget


app = QtWidgets.QApplication(sys.argv)
window = LoginWindow()
window.show()
app.exec()
