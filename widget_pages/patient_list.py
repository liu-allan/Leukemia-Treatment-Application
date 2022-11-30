import sys
import json
import logging
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6 import uic

logging.getLogger().setLevel(logging.INFO)

class PatientListItem(QWidget):
    def __init__(self, patient_name):
        super(PatientListItem, self).__init__()

        self.patient_name = patient_name
        self.label = QLabel(self.patient_name)
        self.select_button = QPushButton("Information")

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.select_button)

        self.setLayout(self.layout)

        self.select_button.clicked.connect(self.showPatientInfo)
    
    def showPatientInfo(self):
        self.parent().parent().showPatientInformationWindow()

class PatientListWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # uic.loadUi("ui/patientlist.ui", self)

        # with open("patients.txt") as f:
        #     data = f.read()

        # self.patients = json.loads(data)

        # layout = QVBoxLayout()
        # button = QPushButton("Show Patient Information")
        # button.clicked.connect(self.showPatientInformationWindow)

        # layout.addWidget(QLabel("Patient List Window"))
        # layout.addWidget(button)

        # self.setLayout(layout)

    def showPatientInformationWindow(self):
        self.parent().parent().showPatientInformationWindow()
