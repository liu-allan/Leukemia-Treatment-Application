import sys
import json
import logging
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic

logging.getLogger().setLevel(logging.INFO)


class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/loginform.ui", self)

        with open("users.txt") as f:
            data = f.read()

        self.users = json.loads(data)

        self.loginPushButton.clicked.connect(self.loginPushed)

    def loginPushed(self):
        try:
            username = self.usernameLineEdit.text()
            password = self.passwordLineEdit.text()
            assert username in self.users, "User {} does not exist".format(username)
            assert self.users[username] == password, "Password is incorrect"
        except AssertionError as msg:
            self.errorLabel.setText(str(msg))
            self.errorLabel.setStyleSheet("color:red")
            logging.error(msg)
        else:
            self.errorLabel.setText("")
            logging.info("Success")
            # TODO: Connect to patient list widget


app = QtWidgets.QApplication(sys.argv)
window = LoginWindow()
window.show()
app.exec()
