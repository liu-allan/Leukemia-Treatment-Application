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

from util.patient import Patient
from widget_pages.dashboard import DashboardWindow
from widget_pages.login import LoginWindow
from widget_pages.patient_information import PatientInformationWindow
from widget_pages.patient_list import PatientListWindow
from widget_pages.patient_form import PatientFormWindow
from widget_pages.toolbar import ToolBar

import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db_conn = sqlite3.connect("db.db")

        self.username = ""
        self.selected_patient = None
        self.current_page = "Login"

        pageLayout = QVBoxLayout()
        self.stackLayout = QStackedLayout()
        self.toolBar = ToolBar(self.current_page, self.username)
        self.updateToolBar()

        pageLayout.addWidget(self.toolBar)
        pageLayout.addLayout(self.stackLayout)

        self.loginWindow = LoginWindow()
        self.patientListWindow = PatientListWindow()
        self.patientInfoWindow = PatientInformationWindow()
        self.dashboardWindow = DashboardWindow()
        self.patientFormWindow = PatientFormWindow()
        self.stackLayout.addWidget(self.loginWindow)
        self.stackLayout.addWidget(self.patientListWindow)
        self.stackLayout.addWidget(self.patientInfoWindow)
        self.stackLayout.addWidget(self.dashboardWindow)
        self.stackLayout.addWidget(self.patientFormWindow)

        widget = QWidget()
        widget.setLayout(pageLayout)
        self.setCentralWidget(widget)
        self.showMaximized()

    def updateUsername(self, username):
        self.username = username
        self.updateToolBar()

    def updateSelectedPatient(self, patient_id):
        res = self.db_conn.execute(
            """SELECT name, weight, height, dosage, time, anc_measurement 
               FROM measurements m 
               INNER JOIN patients p ON m.patient_id=p.id 
                    AND m.patient_id=? ORDER BY time ASC
            """,
            (patient_id,),
        )
        records = res.fetchall()
        if records is None:
            self.selected_patient = None
        else:
            name = records[0][0]
            weight = records[0][1]
            height = records[0][2]
            dosage = records[0][3]
            anc_measurements = []
            for row in records:
                anc_measurements.append((row[5], row[4]))

            self.selected_patient = Patient(
                patient_id, name, weight, height, dosage, anc_measurements
            )

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
        self.patientListWindow.updatePatientList(self.db_conn, self.username)

    def showPatientInformationWindow(self):
        self.stackLayout.setCurrentIndex(2)
        self.current_page = "Patient Information"
        self.updateToolBar()
        self.patientInfoWindow.updatePatientInfo()

    def showDashboardWindow(self):
        self.stackLayout.setCurrentIndex(3)
        self.current_page = "Dashboard"
        self.updateToolBar()
        self.dashboardWindow.updatePatientInfo()

    def showPatientFormWindow(self):
        self.stackLayout.setCurrentIndex(4)
        self.current_page = "Patient Form"
        self.updateToolBar()
        self.patientFormWindow.updatePatientInfo()

    def getDatabaseConnection(self):
        return self.db_conn


app = QApplication([])

window = MainWindow()
window.setWindowTitle("Leukemia Treatment Application")
window.show()

app.exec()
window.db_conn.close()
