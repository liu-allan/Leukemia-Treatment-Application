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
from widget_pages.oncologist_form import OncologistFormWindow
from widget_pages.toolbar import ToolBar

import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db_conn = sqlite3.connect("db.db")

        self.username = ""
        self.selected_patient = None
        self.current_page = "Login"
        self.is_admin_user = False

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
        self.oncologistFormWindow = OncologistFormWindow()
        self.stackLayout.addWidget(self.loginWindow)
        self.stackLayout.addWidget(self.patientListWindow)
        self.stackLayout.addWidget(self.patientInfoWindow)
        self.stackLayout.addWidget(self.dashboardWindow)
        self.stackLayout.addWidget(self.patientFormWindow)
        self.stackLayout.addWidget(self.oncologistFormWindow)

        widget = QWidget()
        widget.setLayout(pageLayout)
        self.setCentralWidget(widget)
        self.showMaximized()

    def updateUsername(self, username):
        self.username = username
        self.updateToolBar()

    def updateSelectedPatient(self, patient_id):
        res = self.db_conn.execute(
            # """SELECT name, weight, height, dosage, time, anc_measurement 
            """SELECT name, weight, height, patient_id, phone_number, birthday, age, 
                      blood_type, all_type, body_surface_area, time, dosage_measurement, anc_measurement, oncologist_id, user_id
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
            patient_id = records[0][3]
            phone_number = records[0][4]
            birthday = records[0][5]
            age = records[0][6]
            blood_type = records[0][7]
            all_type = records[0][8]
            body_surface_area = records[0][9]
            oncologist_id = records[0][13]
            user_id = records[0][14]
            anc_measurements = []
            dosage_measurements = []
            for row in records:
                dosage_measurements.append((row[11], row[10]))
                anc_measurements.append((row[12], row[10]))

            self.selected_patient = Patient(
                patient_id, user_id, name, weight, height, anc_measurements, birthday, dosage_measurements, phone_number, age, blood_type, all_type, body_surface_area, oncologist_id
            )

    def updateToolBar(self):
        self.toolBar.updateToolBar(self.current_page, self.username)

    def showLoginWindow(self):
        self.stackLayout.setCurrentIndex(0)
        self.current_page = "Login"
        self.updateToolBar()

    def showPatientListWindow(self):
        self.stackLayout.setCurrentIndex(1)
        if (self.is_admin_user):
            self.current_page = "Oncologist List"
        else:
            self.current_page = "Patient List"
        self.updateToolBar()
        self.patientListWindow.updatePatientList()

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

    def showOncologistFormWindow(self):
        self.stackLayout.setCurrentIndex(5)
        self.current_page = "Oncologist Form"
        self.updateToolBar()

    def getDatabaseConnection(self):
        return self.db_conn


app = QApplication([])

window = MainWindow()
window.setWindowTitle("Leukemia Treatment Application")
window.show()

app.exec()
window.db_conn.close()
