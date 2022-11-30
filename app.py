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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        pageLayout = QVBoxLayout()
        self.stackLayout = QStackedLayout()

        pageLayout.addLayout(self.stackLayout)

        self.stackLayout.addWidget(LoginWindow())
        self.stackLayout.addWidget(PatientListWindow())
        self.stackLayout.addWidget(PatientInformationWindow())
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
