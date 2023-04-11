import logging
import math
import sqlite3

from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QWidget,
    QDateEdit,
    QToolBar,
    QSizePolicy,
    QMessageBox,
    QDialogButtonBox,
)
from PyQt6.QtGui import QFont, QPixmap, QColor, QIcon
from PyQt6.QtCore import Qt, QDate, QSize

class SideBar(QWidget):
    def __init__(self, pageName):
        super().__init__()

        self.bigLayout = QVBoxLayout()
        self.bigLayout.setContentsMargins(0, 0, 0, 0)

        self.sideBar = QWidget()
        self.sideBar.setObjectName("SideBar")
        self.sideBar.setContentsMargins(0, 0, 0, 0)
        self.sideBar.setStyleSheet(
            """
            QWidget#SideBar{
                background-color: #bfd8d2;
                height: auto;
                border-radius: 20px;
            }
            """
        )

        self.bigLayout.addWidget(self.sideBar)

        self.menuLayout = QVBoxLayout(self.sideBar)
        self.menuLayout.setContentsMargins(0, 0, 0, 0)

        self.backButton = QPushButton()
        if(pageName == "Patient List"):
            self.backButton.setIcon(QIcon("icons/user_black.png"))
        else:
            self.backButton.setIcon(QIcon("icons/user.png"))
        self.backButton.setIconSize(QSize(30, 30))
        self.backButton.setToolTip("Patient List")
        self.backButton.setContentsMargins(0, 70, 0, 0)
        self.backButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.backButton.setFont(QFont("Avenir", 18))
        self.backButton.setStyleSheet("background-color: #bfd8d2; border-radius: 20px")
        self.backButton.clicked.connect(self.backButtonClicked)
        self.menuLayout.addWidget(self.backButton)

        self.patientInformationButton = QPushButton()
        if(pageName == "Patient Information"):
            self.patientInformationButton.setIcon(QIcon("icons/information_black.png"))
        else:
            self.patientInformationButton.setIcon(QIcon("icons/information.png"))
        self.patientInformationButton.setIconSize(QSize(35, 35))
        self.patientInformationButton.setToolTip("Patient Information")
        self.patientInformationButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.patientInformationButton.setContentsMargins(0, 15, 0, 0)
        self.patientInformationButton.setFont(QFont("Avenir", 18))
        self.patientInformationButton.clicked.connect(self.patientInformationButtonClicked)
        self.patientInformationButton.setStyleSheet("background-color: #bfd8d2; border-radius: 20px")
        self.menuLayout.addWidget(self.patientInformationButton)

        self.dashboardButton = QPushButton()
        if(pageName == "Dashboard"):
            self.dashboardButton.setIcon(QIcon("icons/dashboard_black.png"))
        else:
            self.dashboardButton.setIcon(QIcon("icons/dashboard.png"))
        self.dashboardButton.setIconSize(QSize(30, 30))
        self.dashboardButton.setToolTip("Dashboard")
        self.dashboardButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.dashboardButton.setContentsMargins(0, 15, 0, 0)
        self.dashboardButton.setFont(QFont("Avenir", 18))
        self.dashboardButton.clicked.connect(self.dashboardButtonClicked)
        self.dashboardButton.setStyleSheet("background-color: #bfd8d2; border-radius: 20px")
        self.menuLayout.addWidget(self.dashboardButton)

        self.menuLayout.addSpacing(470)

        self.logoutButton = QPushButton()
        self.logoutButton.setIcon(QIcon("icons/power-on.png"))
        self.logoutButton.setIconSize(QSize(30, 30))
        self.logoutButton.setToolTip("Log Out")
        self.logoutButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.logoutButton.setContentsMargins(0, 0, 0, 0)
        self.logoutButton.setFont(QFont("Avenir", 18))
        self.logoutButton.clicked.connect(self.logoffButtonClicked)
        self.logoutButton.setStyleSheet("background-color: #bfd8d2; border-radius: 20px")
        self.menuLayout.addWidget(self.logoutButton)

        self.setLayout(self.bigLayout)
    
    def lockButtons(self, lock):
        enabled = not lock
        self.backButton.setEnabled(enabled)
        self.patientInformationButton.setEnabled(enabled)
        self.dashboardButton.setEnabled(enabled)
        self.logoutButton.setEnabled(enabled)

    def backButtonClicked(self):
        self.parent().backButtonClicked()
    
    def patientInformationButtonClicked(self):
        self.parent().patientInformationButtonClicked()

    def dashboardButtonClicked(self):
        self.parent().dashboardButtonClicked()

    def logoffButtonClicked(self):
        self.parent().logoffButtonClicked()