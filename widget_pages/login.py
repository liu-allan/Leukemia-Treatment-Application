import bcrypt
import sys
import json
import logging
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QToolBar,
)
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

logging.getLogger().setLevel(logging.INFO)


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.titleLabel = QLabel("Login")
        self.titleLabel.setFont(QFont("Avenir", 25))
        self.titleLabel.setMargin(10)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setStyleSheet(
            "background-color: #a9c7c5; height : 100; border-radius: 10px; padding 10px"
        )
        self.layout.addWidget(self.titleLabel, 0, 1)

        self.vSpacer = QSpacerItem(
            1, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )
        self.layout.addItem(self.vSpacer, 1, 1)

        self.usernameLineEdit = QLineEdit()
        self.usernameLineEdit.setPlaceholderText("Username")
        self.layout.addWidget(self.usernameLineEdit, 2, 1)

        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setPlaceholderText("Password")
        self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.passwordLineEdit, 3, 1)

        self.errorLabel = QLabel()
        self.errorLabel.setFont(QFont("Avenir", 12))
        self.errorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.errorLabel, 4, 1)

        self.loginPushButton = QPushButton("Login")
        self.loginPushButton.clicked.connect(self.loginPushed)
        self.loginPushButton.setFont(QFont("Avenir", 12))
        self.loginPushButton.setStyleSheet(
            "background-color: #aaaaee; border-radius: 5px; padding: 10px"
        )
        self.layout.addWidget(self.loginPushButton, 5, 1)

        self.spacer = QSpacerItem(
            1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        self.layout.addItem(self.spacer, 0, 0)
        self.layout.addItem(self.spacer, 0, 2)
        self.setLayout(self.layout)

    def loginPushed(self):
        try:
            username = self.usernameLineEdit.text()
            password = self.passwordLineEdit.text()
            passwordBytes = password.encode("utf-8")

            db_conn = self.parent().parent().getDatabaseConnection()
            res = db_conn.execute(
                """SELECT * 
                   FROM oncologists 
                   WHERE username=?
                """,
                (username,),
            )

            row = res.fetchone()

            assert (
                row is not None and username == row[0]
            ), "User {} does not exist".format(username)
            assert bcrypt.checkpw(passwordBytes, row[1]), "Password is incorrect"
        except AssertionError as msg:
            self.errorLabel.setText(str(msg))
            self.errorLabel.setStyleSheet("color:red")
            logging.error(msg)
        else:
            self.errorLabel.setText("")
            logging.info("Login Successful")
            self.updateUsername(username)
            self.showPatientListWindow()

    def updateUsername(self, username):
        self.parent().parent().updateUsername(username)

    def showPatientListWindow(self):
        self.parent().parent().showPatientListWindow()
        self.usernameLineEdit.clear()
        self.passwordLineEdit.clear()
