# app.py

# Entry point to the entire application. This file contains the
# main infrastructure of the application.

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

from widget_pages.dashboard import DashboardWindow
from widget_pages.login import LoginWindow
from widget_pages.patient_information import PatientInformationWindow
from widget_pages.patient_list import PatientListWindow
from widget_pages.toolbar import ToolBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.username = ""
        self.current_page = "Login"

        pageLayout = QVBoxLayout()
        self.stackLayout = QStackedLayout()
        self.toolBar = ToolBar(self.current_page, self.username)
        self.updateToolBar()

        pageLayout.addWidget(self.toolBar)
        pageLayout.addLayout(self.stackLayout)

        self.stackLayout.addWidget(LoginWindow())
        self.stackLayout.addWidget(PatientListWindow())
        self.stackLayout.addWidget(PatientInformationWindow())
        self.stackLayout.addWidget(DashboardWindow())

        widget = QWidget()
        widget.setLayout(pageLayout)
        self.setCentralWidget(widget)
        self.showMaximized()

    def updateUsername(self, username):
        self.username = username
        self.updateToolBar()

    def updateToolBar(self):
        self.toolBar.updateToolBar(self.current_page, self.username)

    def showLoginWindow(self):
        self.stackLayout.setCurrentIndex(0)
        self.current_page = "Login"
        self.updateToolBar()

    def showPatientListWindow(self):
        self.stackLayout.setCurrentIndex(1)
        self.current_page = "Patient List"
        self.updateToolBar()

    def showPatientInformationWindow(self):
        self.stackLayout.setCurrentIndex(2)
        self.current_page = "Patient Information"
        self.updateToolBar()

    def showDashboardWindow(self):
        self.stackLayout.setCurrentIndex(3)
        self.current_page = "Dashboard"
        self.updateToolBar()


app = QApplication([])

window = MainWindow()
window.setWindowTitle("Leukemia Treatment Application")
window.show()

app.exec()
