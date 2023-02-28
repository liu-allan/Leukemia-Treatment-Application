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
    QFrame,
    QGraphicsBlurEffect,
    QStyle,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QToolBar,
)
from PyQt6 import uic
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon
import qtawesome as qta

logging.getLogger().setLevel(logging.INFO)


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet('border-radius: 20px;')

        self.mainPageLayout = QHBoxLayout()
        self.mainPageLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainPageLayout)

        self.picture = QLabel()
        self.picture.setStyleSheet('border-image: url("icons/background.png"); background-repeat: no-repeat; background-position: center; height: auto; border-radius: 20px')
        self.picture.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainPageLayout.addWidget(self.picture, 50)

        self.quotes = QLabel()
        self.quotes.setObjectName("QuotesBackground")
        self.quotes.setFrameShape(QFrame.Shape.Box)
        self.quotes.setFixedWidth(400)
        self.quotes.setFixedHeight(350)
        self.quotes.setStyleSheet(
            """
            QLabel#QuotesBackground
            {
                border-radius: 20px;
                background-color: rgba(255, 255, 255, 180);
            }
            """
        )
        self.quotes.move(215, 290)
        self.mainPageLayout.addChildWidget(self.quotes)
        self.quotes.raise_()

        self.quotesLayout = QVBoxLayout(self.quotes)

        self.pictureTop = QLabel("A graphical tool in comparing two different dosage strategies used in Leukemia treatment")
        self.pictureTop.setObjectName("QuoteTop")
        self.pictureTop.setFont(QFont("Avenir", 25))
        # self.pictureTop.setFrameShape(QFrame.Shape.Box)
        self.pictureTop.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.pictureTop.setAlignment(Qt.AlignmentFlag.AlignBottom)
        # self.pictureTop.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.pictureTop.setWordWrap(True)
        # self.pictureTop.setFixedWidth(400)
        # self.pictureTop.setFixedHeight(350)
        self.pictureTop.setStyleSheet(
            """
            QLabel#QuoteTop
            {
                color: #5a5a5a; font-weight: bold; padding: 10px
            }
            """
        )
        self.pictureTop.setContentsMargins(30, 0, 30, 0)
        # self.pictureTop.move(215, 290)
        self.quotesLayout.addWidget(self.pictureTop, 2)
        # self.pictureTop.raise_()

        self.quoteBottom = QLabel("This can help oncologists to decide what strategy should be applied better for patient's health")
        self.quoteBottom.setObjectName("QuoteBottom")
        self.quoteBottom.setFont(QFont("Avenir", 13))
        self.quoteBottom.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.quoteBottom.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.quoteBottom.setWordWrap(True)
        self.quoteBottom.setStyleSheet(
            """
            QLabel#QuoteBottom
            {
                color: #5a5a5a; padding: 10px
            }
            """
        )
        self.quoteBottom.setContentsMargins(30, 0, 30, 0)
        self.quotesLayout.addWidget(self.quoteBottom, 1)

        self.login = QWidget()
        self.login.setContentsMargins(30, 10, 30, 0)
        self.login.setStyleSheet(
            "background-color: #ffffff; border-radius: 20px;"
        )
        self.mainPageLayout.addWidget(self.login, 50)

        self.layout = QVBoxLayout(self.login)
        
        self.title = QWidget()
        self.title.setContentsMargins(0, 0, 0, 0)

        self.titleLayout = QHBoxLayout(self.title)
        self.titleLayout.setContentsMargins(0, 0, 10, 0)
        self.titleLayout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.appNameIcon = QLabel()
        self.appNameIcon.setPixmap(QIcon("icons/comparation.png").pixmap(QSize(28, 28)))
        self.titleLayout.addWidget(self.appNameIcon)

        self.appName = QLabel()
        self.appName.setText('<font color="black">Leukemia</font><font color="#aaaaee">Compare</font>')
        self.appName.setFont(QFont("Avenir", 30))
        self.appName.setContentsMargins(0, 0, 0, 0)
        self.appName.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.appName.setStyleSheet("font-weight: bold;")
        self.titleLayout.addWidget(self.appName)

        self.layout.addWidget(self.title)

        self.spacer = QSpacerItem(
            1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.layout.addSpacerItem(self.spacer)

        self.titleLabel = QLabel("Welcome!")
        self.titleLabel.setFont(QFont("Avenir", 50))
        self.titleLabel.setContentsMargins(0, 0, 0, 40)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setStyleSheet("font-weight: bold;")
        self.layout.addWidget(self.titleLabel)

        self.usernameLineEdit = QLineEdit()
        self.usernameLineEdit.setFont(QFont("Avenir", 18))
        self.usernameLineEdit.setContentsMargins(0, 0, 0, 10)
        self.usernameLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.usernameLineEdit.setPlaceholderText("Username")
        self.usernameLineEdit.setStyleSheet(
            "background-color: #f5f5f5; height: 60px; border-radius: 20px;"
        )
        self.usernameLineEdit.setFixedWidth(500)
        self.layout.addWidget(self.usernameLineEdit, alignment=Qt.AlignmentFlag.AlignCenter)

        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setPlaceholderText("Password")
        self.passwordLineEdit.setFont(QFont("Avenir", 18))
        self.passwordLineEdit.setContentsMargins(0, 0, 0, 10)
        self.passwordLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.passwordLineEdit.setStyleSheet(
            "background-color: #f5f5f5; height: 60px; border-radius: 20px;"
        )
        self.passwordLineEdit.setFixedWidth(500)
        self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.passwordLineEdit, alignment=Qt.AlignmentFlag.AlignCenter)

        self.errorLabel = QLabel()
        self.errorLabel.setFont(QFont("Avenir", 12))
        self.errorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.errorLabel)

        self.loginPushButton = QPushButton("Login ")
        self.loginPushButton.setIcon(QIcon("icons/login.png"))
        self.loginPushButton.setIconSize(QSize(20, 20))
        self.loginPushButton.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.loginPushButton.clicked.connect(self.loginPushed)
        self.loginPushButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.loginPushButton.setFixedWidth(200)
        self.loginPushButton.setFont(QFont("Avenir", 18))
        self.loginPushButton.setShortcut("Return")
        self.loginPushButton.setStyleSheet(
            "background-color: #aaaaee; border-radius: 20px; padding: 10px"
        )
        self.layout.addWidget(self.loginPushButton, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.addSpacerItem(self.spacer)

        self.copyRightLabel = QLabel("Copyright @ 2023. LeukemiaCompare. All rights reserved.")
        self.copyRightLabel.setFont(QFont("Avenir", 12))
        self.copyRightLabel.setContentsMargins(0, 0, 0, 10)
        self.copyRightLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.copyRightLabel.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.copyRightLabel.setStyleSheet(
            "color: #5a5a5a"
        )

        self.layout.addWidget(self.copyRightLabel, alignment=Qt.AlignmentFlag.AlignCenter)

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
