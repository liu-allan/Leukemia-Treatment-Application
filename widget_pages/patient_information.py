import sys
import json
import math
import datetime
import logging
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QDialogButtonBox
from PyQt6 import uic

from PyQt6.QtGui import QDoubleValidator

logging.getLogger().setLevel(logging.INFO)


class Patient:
    def __init__(self, name, weight, height, dosage, ancMeasurement):
        self.name = name
        self.weight = weight
        self.height = height
        self.dosage = dosage
        self.ancMeasurement = [ancMeasurement]

    def save(self, name, weight, height, dosage, bsa, ancMeasurement, ancEdited):
        self.name = name
        self.weight = weight
        self.height = height
        self.dosage = dosage
        self.bsa = bsa
        if ancEdited:
            self.ancMeasurement.append(ancMeasurement)
        print(self.ancMeasurement)


class PatientInformationWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/patientinformationform.ui", self)

        self.weightEdit.setValidator(QDoubleValidator())
        self.heightEdit.setValidator(QDoubleValidator())
        self.dosageEdit.setValidator(QDoubleValidator())
        self.ancMeasurementEdit.setValidator(QDoubleValidator())
        self.ancEdited = False

        self.ancMeasurementEdit.textEdited.connect(self.valueChanged)
        self.dateEdit.editingFinished.connect(self.valueChanged)
        self.weightEdit.textEdited.connect(self.calculateBodySurfaceArea)
        self.heightEdit.textEdited.connect(self.calculateBodySurfaceArea)

        self.buttonBox.button(self.buttonBox.standardButtons().Cancel).clicked.connect(
            self.showPatientListWindow
        )
        self.buttonBox.button(self.buttonBox.standardButtons().Save).clicked.connect(
            self.savePatientInformation
        )
        self.buttonBox.button(self.buttonBox.standardButtons().Ok).clicked.connect(
            self.showDashboardWindow
        )

        # TODO: Load selected patient from database

        self.patient = Patient("Allan", 175, 64, 50, (2, datetime.date(2022, 1, 1)))
        self.patientLineEdit.setText(self.patient.name)
        self.weightEdit.setText(str(self.patient.weight))
        self.heightEdit.setText(str(self.patient.height))
        self.dosageEdit.setText(str(self.patient.dosage))
        self.ancMeasurementEdit.setText(str(self.patient.ancMeasurement[-1][0]))
        self.calculateBodySurfaceArea()

    def calculateBodySurfaceArea(self):
        weight = self.weightEdit.text()
        height = self.heightEdit.text()
        try:
            weight = float(weight)
            height = float(height)
        except:
            return
        else:
            bsa = math.sqrt(height * weight / 3600)
            self.bodySurfaceAreaEdit.setText("{:.2f}".format(bsa))

    def savePatientInformation(self):
        name = self.patientLineEdit.text()
        weight = float(self.weightEdit.text())
        height = float(self.heightEdit.text())
        dosage = float(self.dosageEdit.text())
        date = self.dateEdit.date().toPyDate()
        bsa = float(self.bodySurfaceAreaEdit.text())
        ancMeasurement = float(self.ancMeasurementEdit.text())
        self.patient.save(
            name, weight, height, dosage, bsa, (ancMeasurement, date), self.ancEdited
        )
        self.ancEdited = False

    def showPatientListWindow(self):
        self.parent().parent().showPatientListWindow()

    def showDashboardWindow(self):
        self.parent().parent().showDashboardWindow()

    def valueChanged(self):
        self.ancEdited = True
