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

        self.usernameLineEdit = QLineEdit()
        self.usernameLineEdit.setPlaceholderText("Username")
        self.layout.addWidget(self.usernameLineEdit, 0, 1)

        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setPlaceholderText("Password")
        self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.passwordLineEdit, 1, 1)

        self.errorLabel = QLabel()
        self.errorLabel.setFont(QFont("Avenir", 12))
        self.errorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.errorLabel, 2, 1)

        self.loginPushButton = QPushButton("Login")
        self.loginPushButton.clicked.connect(self.loginPushed)
        self.loginPushButton.setFont(QFont("Avenir", 12))
        self.loginPushButton.setStyleSheet(
            "background-color: #aaaaee; border-radius: 5px; padding: 10px"
        )
        self.layout.addWidget(self.loginPushButton, 3, 1)

        self.signUpPushButton = QPushButton("Sign Up")
        self.signUpPushButton.clicked.connect(self.signUpPushed)
        self.signUpPushButton.setFont(QFont("Avenir", 12))
        self.signUpPushButton.setStyleSheet(
            "background-color: #aaaaee; border-radius: 5px; padding: 10px"
        )
        self.layout.addWidget(self.signUpPushButton, 4, 1)
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
            assert password == row[1], "Password is incorrect"
        except AssertionError as msg:
            self.errorLabel.setText(str(msg))
            self.errorLabel.setStyleSheet("color:red")
            logging.error(msg)
        else:
            self.errorLabel.setText("")
            logging.info("Login Successful")
            self.updateUsername(username)
            self.showPatientListWindow()

    def signUpPushed(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()

        try:

            assert username and password, "Username or password must not be empty"

            db_conn = self.parent().parent().getDatabaseConnection()
            res = db_conn.execute(
                """SELECT * 
                   FROM oncologists 
                   WHERE username=?
                """,
                (username,),
            )

            row = res.fetchone()

            assert row is None, "User {} already exists".format(username)

            db_conn.execute(
                """
                        INSERT INTO oncologists (username, password)
                        VALUES (?, ?)
                    """,
                (username, password),
            )

            res = db_conn.execute("SELECT last_insert_rowid()")
            patient_id = res.fetchone()[0]

        except Exception as msg:
            self.errorLabel.setText(str(msg))
            self.errorLabel.setStyleSheet("color:red")
            logging.error(msg)
        else:
            self.errorLabel.setText(
                "User {} has been succesfully created".format(username)
            )
            self.errorLabel.setStyleSheet("color:green")
            logging.info("User {} has been successfully created".format(username))

    def updateUsername(self, username):
        self.parent().parent().updateUsername(username)

    def showPatientListWindow(self):
        self.parent().parent().showPatientListWindow()
        self.usernameLineEdit.clear()
        self.passwordLineEdit.clear()
