import sys
import json
import logging
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6 import uic

logging.getLogger().setLevel(logging.INFO)


class LoginWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/loginform.ui", self)

        with open("users.txt") as f:
            data = f.read()

        self.users = json.loads(data)

        self.loginPushButton.clicked.connect(self.loginPushed)
        self.signUpPushButton.clicked.connect(self.signUpPushed)

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
            logging.info("Login Successful")
            self.showPatientListWindow()

    def signUpPushed(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()

        try:
            assert username not in self.users, "User {} already exists".format(username)
        except AssertionError as msg:
            self.errorLabel.setText(str(msg))
            self.errorLabel.setStyleSheet("color:red")
            logging.error(msg)
        else:
            self.errorLabel.setText(
                "User {} has been succesfully created".format(username)
            )
            self.errorLabel.setStyleSheet("color:green")
            logging.info("User {} has been successfully created".format(username))
            self.users[username] = password
            with open("users.txt", "w") as f:
                f.write(json.dumps(self.users))

    def showPatientListWindow(self):
        self.parent().parent().showPatientListWindow()
