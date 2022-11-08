import sys
import logging
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic

logging.getLogger().setLevel(logging.INFO)

class User():
    def __init__(self, name, password):
        self.name = name
        self.password = password

class LoginWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/loginform.ui", self)

        self.doctor = User("John", "password")

        self.loginPushButton.clicked.connect(self.loginPushed)

    def loginPushed(self):
        try:
            assert(self.doctor.name == self.usernameLineEdit.text())
            assert(self.doctor.password == self.passwordLineEdit.text())
        except:
            logging.error("Something went wrong")
        else:
            logging.info("Success")

app = QtWidgets.QApplication(sys.argv)
window = LoginWindow()
window.show()
app.exec()