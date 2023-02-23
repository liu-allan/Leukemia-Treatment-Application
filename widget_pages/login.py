import bcrypt
import sys
import json
import logging
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QHBoxLayout,
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
from PyQt6.QtGui import QFont, QPixmap, QBrush

logging.getLogger().setLevel(logging.INFO)


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.mainPageLayout = QHBoxLayout()
        self.mainPageLayout.setContentsMargins(0, 0, 0, 0)

        self.login = QWidget()
        self.login.setContentsMargins(0, 0, 0, 0)
        self.login.setStyleSheet(
            "background-color: #ffffff; border-radius: 20px;"
        )
        self.mainPageLayout.addWidget(self.login)

        self.mainPicture = QPixmap('3EFB1109-FC90-45A4-A82A-6BC4F169C000_1_201_a.jpeg')

        self.picture = QLabel()
        self.picture.setFixedSize(1000, 1000)
        self.mainPageLayout.addWidget(self.picture)
        self.picture.setPixmap(self.mainPicture)
        self.picture.setMinimumSize(1, 1)
        self.picture.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.mainPageLayout)

        self.layout = QVBoxLayout(self.login)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.titleLabel = QLabel("Welcome!")
        self.titleLabel.setFont(QFont("Avenir", 45))
        self.titleLabel.setContentsMargins(10, 10, 10, 0)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setStyleSheet("font-weight: bold;")
        # self.titleLabel.setStyleSheet(
        #     "background-color: #a9c7c5; height : 100; border-radius: 20px"
        # )
        self.layout.addWidget(self.titleLabel)

        self.promptLabel = QLabel("Please input your username and password to log into the system.")
        self.promptLabel.setFont(QFont("Avenir", 15))
        self.promptLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.promptLabel.setStyleSheet(
            "color: #71797e;"
        )
        self.layout.addWidget(self.promptLabel)

        self.vSpacer = QSpacerItem(
            1, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )
        self.layout.addItem(self.vSpacer)

        self.usernameLineEdit = QLineEdit()
        self.usernameLineEdit.setPlaceholderText("Username")
        self.layout.addWidget(self.usernameLineEdit)

        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setPlaceholderText("Password")
        self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.passwordLineEdit)

        self.errorLabel = QLabel()
        self.errorLabel.setFont(QFont("Avenir", 12))
        self.errorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.errorLabel)

        self.loginPushButton = QPushButton("Login")
        self.loginPushButton.clicked.connect(self.loginPushed)
        self.loginPushButton.setFont(QFont("Avenir", 12))
        self.loginPushButton.setStyleSheet(
            "background-color: #aaaaee; border-radius: 5px; padding: 10px"
        )
        self.layout.addWidget(self.loginPushButton)

        self.spacer = QSpacerItem(
            1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        # self.layout.addItem(self.spacer, 0, 0)
        # self.layout.addItem(self.spacer, 0, 2)

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
            if (row[3] == "TRUE"):
                self.parent().parent().is_admin_user = True
            else:
                self.parent().parent().is_admin_user = False
            self.showPatientListWindow()

    def updateUsername(self, username):
        self.parent().parent().updateUsername(username)

    def showPatientListWindow(self):
        self.parent().parent().showPatientListWindow()
        self.usernameLineEdit.clear()
        self.passwordLineEdit.clear()
