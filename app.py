# app.py

# Entry point to the entire application. This file contains the
# main infrastructure of the application.

from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

from widget_pages.dashboard import DashboardWindow
from widget_pages.login import LoginWindow
from widget_pages.patient_information import PatientInformationWindow
from widget_pages.patient_list import PatientListWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        pageLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()
        self.stackLayout = QStackedLayout()

        pageLayout.addLayout(buttonLayout)
        pageLayout.addLayout(self.stackLayout)

        button = QPushButton("Login")
        button.pressed.connect(self.showLoginWindow)
        buttonLayout.addWidget(button)
        self.stackLayout.addWidget(LoginWindow())

        button = QPushButton("Patient List")
        button.pressed.connect(self.showPatientListWindow)
        buttonLayout.addWidget(button)
        self.stackLayout.addWidget(PatientListWindow())

        button = QPushButton("Patient Information")
        button.pressed.connect(self.showPatientInformationWindow)
        buttonLayout.addWidget(button)
        self.stackLayout.addWidget(PatientInformationWindow())

        button = QPushButton("Dashboard")
        button.pressed.connect(self.showDashboardWindow)
        buttonLayout.addWidget(button)
        self.stackLayout.addWidget(DashboardWindow())

        widget = QWidget()
        widget.setLayout(pageLayout)
        self.setCentralWidget(widget)
        self.showMaximized()

    def showLoginWindow(self):
        self.stackLayout.setCurrentIndex(0)

    def showPatientListWindow(self):
        self.stackLayout.setCurrentIndex(1)

    def showPatientInformationWindow(self):
        self.stackLayout.setCurrentIndex(2)

    def showDashboardWindow(self):
        self.stackLayout.setCurrentIndex(3)


app = QApplication([])

window = MainWindow()
window.setWindowTitle("Leukemia Treatment Application")
window.show()

app.exec()
