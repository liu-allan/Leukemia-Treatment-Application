import logging
import math
import sqlite3
import numpy as np

from PyQt6 import uic
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QDateEdit,
    QDialogButtonBox,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtGui import QDoubleValidator, QFont
from widget_pages.patient_card import PatientCard
from pyqtgraph import plot
import pyqtgraph as pg
from datetime import datetime

logging.getLogger().setLevel(logging.INFO)


class Label(QLabel):
    def __init__(self, text, width=400):
        super().__init__()
        self.setText(text)
        self.setFont(QFont("Avenir", 15))
        self.setFixedWidth(width)

class LabelBolded(QLabel):
    def __init__(self, text, textSize, margins):
        super().__init__()
        self.setText(text)
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.setFont(QFont("Avenir", textSize))
        self.setContentsMargins(margins[0], margins[1], margins[2], margins[3])
        self.setStyleSheet("font-weight: bold;")

class LineEdit(QLineEdit):
    def __init__(self, placeholderText, width=200):
        super().__init__()
        self.setPlaceholderText(placeholderText)
        self.setFont(QFont("Avenir", 15))
        self.setFixedWidth(width)

class FormRow(QWidget):
    def __init__(self, label, widget):
        super().__init__()
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addItem(
            QSpacerItem(1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        )
        layout.addWidget(widget)

        self.setLayout(layout)

class PatientFormWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.patientFormLayout = QVBoxLayout()
        self.patientFormLayout.setContentsMargins(0, 0, 0, 0)

        self.patientLabel = Label("Patient Name")
        self.patientLineEdit = LineEdit("Patient")
        self.patientFormLayout.addWidget(FormRow(self.patientLabel, self.patientLineEdit))

        self.weightLabel = Label("Weight (kg)")
        self.weightEdit = LineEdit("kg")
        self.patientFormLayout.addWidget(FormRow(self.weightLabel, self.weightEdit))

        self.heightLabel = Label("Height (cm)")
        self.heightEdit = LineEdit("cm")
        self.patientFormLayout.addWidget(FormRow(self.heightLabel, self.heightEdit))

        self.bodySurfaceAreaLabel = Label("Body Surface Area (m^2)")
        self.bodySurfaceAreaMeasurement = LineEdit("m^2")
        self.bodySurfaceAreaMeasurement.setReadOnly(True)
        self.bodySurfaceAreaMeasurement.setFixedWidth(200)
        self.patientFormLayout.addWidget(FormRow(self.bodySurfaceAreaLabel, self.bodySurfaceAreaMeasurement))

        self.bloodTypeLabel = Label("Blood Type")
        self.bloodTypeSelect = QComboBox()
        self.bloodTypeSelect.addItems(['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'])
        self.bloodTypeSelect.activated.connect(self.selectedBloodType)
        self.bloodTypeSelect.setFixedWidth(210)
        self.patientFormLayout.addWidget(FormRow(self.bloodTypeLabel, self.bloodTypeSelect))

        self.birthdayLabel = Label("Birthday")
        self.birthdayEdit = QDateEdit()
        self.birthdayEdit.setFixedWidth(200)
        self.patientFormLayout.addWidget(FormRow(self.birthdayLabel, self.birthdayEdit))

        self.phoneNumberLabel = Label("Phone Number")
        self.phoneNumberEdit = LineEdit("xxx-xxx-xxxx")
        self.patientFormLayout.addWidget(FormRow(self.phoneNumberLabel, self.phoneNumberEdit))
        
        self.allTypeLabel = Label("ALL Type")
        self.allTypeSelect = QComboBox()
        self.allTypeSelect.addItems(['Immunophenotype', 'French-American-British (FAB)', 'ALL Cytogenetic Risk Group'])
        self.allTypeSelect.activated.connect(self.selectedBloodType)
        self.allTypeSelect.setFixedWidth(210)
        self.patientFormLayout.addWidget(FormRow(self.allTypeLabel, self.allTypeSelect))

        self.dosageLabel = Label("6-MP Dosage (mg)")
        self.dosageEdit = LineEdit("mg")
        self.patientFormLayout.addWidget(FormRow(self.dosageLabel, self.dosageEdit))

        self.ancCountLabel = Label("ANC Measurement (g/L)")
        self.ancMeasurementEdit = LineEdit("g/L")
        self.patientFormLayout.addWidget(FormRow(self.ancCountLabel, self.ancMeasurementEdit))

        self.dateLabel = Label("Date of ANC Measurement")
        self.dateEdit = QDateEdit()
        self.dateEdit.setFixedWidth(200)
        self.patientFormLayout.addWidget(FormRow(self.dateLabel, self.dateEdit))

        self.errorLabel = Label("")
        self.patient = None
        self.weightEdit.setValidator(QDoubleValidator())
        self.heightEdit.setValidator(QDoubleValidator())
        self.dosageEdit.setValidator(QDoubleValidator())
        self.ancMeasurementEdit.setValidator(QDoubleValidator())
        self.ancEdited = False

        self.ancMeasurementEdit.textEdited.connect(self.valueChanged)
        self.dateEdit.editingFinished.connect(self.valueChanged)
        self.weightEdit.textEdited.connect(self.calculateBodySurfaceArea)
        self.heightEdit.textEdited.connect(self.calculateBodySurfaceArea)

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(self.buttonBox.standardButtons().Cancel)
        self.buttonBox.addButton(self.buttonBox.standardButtons().Save)
        self.buttonBox.addButton(self.buttonBox.standardButtons().Ok)
        self.buttonBox.setFont(QFont("Avenir", 12))
        self.buttonBox.setFixedWidth(200)
        self.buttonBox.setStyleSheet(
            "background-color: #aaaaee; border-radius: 5px; padding: 10px"
        )

        self.buttonBox.button(self.buttonBox.standardButtons().Cancel).clicked.connect(
            self.showPatientListWindow
        )
        # self.buttonBox.button(self.buttonBox.standardButtons().Save).clicked.connect(
        #     self.savePatientInformation
        # )
        self.buttonBox.button(self.buttonBox.standardButtons().Ok).clicked.connect(
            self.showDashboardWindow
        )

        self.buttonBox.setCursor(Qt.CursorShape.PointingHandCursor)
        self.patientFormLayout.addWidget(FormRow(self.errorLabel, self.buttonBox))

        self.setLayout(self.patientFormLayout)

    def selectedAllType(self, index):
        self.allType = self.allTypeSelect.itemText(index)  # Get the text at index.
        print("Current ALL type: ", self.allType)

    def selectedBloodType(self, index):
        self.bloodType = self.bloodTypeSelect.itemText(index)  # Get the text at index.
        print("Current blood type: ", self.bloodType)

    def displayParameters(self):
        self.patientLineEdit.clear()
        self.weightEdit.clear()
        self.heightEdit.clear()
        self.dosageEdit.clear()
        self.ancMeasurementEdit.clear()
        self.dateEdit.setDate(QDate.currentDate())

        if self.patient is not None:
            self.patientLineEdit.setText(self.patient.name)
            self.weightEdit.setText(str(self.patient.weight))
            self.heightEdit.setText(str(self.patient.height))
            self.dosageEdit.setText(str(self.patient.dosage))
            
            self.calculateBodySurfaceArea()
            self.ancMeasurementDate = [datetime.strptime(str(item[1]), '%Y%m%d') for item in self.patient.ancMeasurement]
            self.ancMeasurement = [item[0] for item in self.patient.ancMeasurement]
            self.ancMeasurementEdit.setText(str(self.ancMeasurement[-1]))
            self.dateEdit.setDate(
                QDate.fromString(str(self.ancMeasurementDate[-1].date()), "yyyy-MM-dd")
            )

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
            self.bodySurfaceAreaMeasurement.setText("{:.2f}".format(bsa))

    # def savePatientInformation(self):
    #     try:
    #         name = self.patientLineEdit.text()
    #         assert name != ""
    #         date = self.dateEdit.date().toString("yyyyMMdd")
    #         weight = float(self.weightEdit.text())
    #         height = float(self.heightEdit.text())
    #         bloodType = self.bloodType
    #         birthday = self.birthdayEdit.date().toString("yyyyMMdd")
    #         phoneNumber = self.phoneNumberEdit.text()
    #         allType = self.allTypeSelect
    #         dosage = float(self.dosageEdit.text())
    #         bsa = float(self.bodySurfaceAreaMeasurement.text())
    #         ancMeasurement = float(self.ancMeasurementEdit.text())

    #         conn = self.parent().parent().getDatabaseConnection()
    #         patient_id = self.patient.id if self.patient else -1

            # if self.patient is None:
            #     conn.execute(
            #         """
            #             INSERT INTO patients (name, weight, height, blood_type, birthday, phone_number, all_type, dosage, body_surface_area, oncologist_id)
            #             VALUES (?, ?, ?, ?, ?, ?)
            #         """,
            #         (
            #             name,
            #             weight,
            #             height,
            #             bloodType,
            #             birthday,
            #             phoneNumber,
            #             allType,
            #             dosage,
            #             bsa,
            #             self.parent().parent().username,
            #         ),
            #     )

    #             res = conn.execute("SELECT last_insert_rowid()")
    #             patient_id = res.fetchone()[0]

    #         conn.execute(
    #             """
    #                 INSERT INTO measurements (time, anc_measurement, patient_id)
    #                 VALUES (?, ?, ?)
    #             """,
    #             (date, ancMeasurement, patient_id),
    #         )
    #         conn.commit()

    #         self.parent().parent().updateSelectedPatient(patient_id)
    #         self.patient = self.parent().parent().selected_patient

    #     except sqlite3.Error as er:
    #         msg = "Existing entry in the database. Please check your inputs."
    #         self.errorLabel.setText(msg)
    #         self.errorLabel.setStyleSheet("color:red")
    #         logging.error(er)

    #     except:
    #         msg = "Input fields must not be empty"
    #         self.errorLabel.setText(msg)
    #         self.errorLabel.setStyleSheet("color:red")
    #         logging.error(msg)

    #     else:
    #         self.errorLabel.clear()
    #         self.patient.save(
    #             name,
    #             weight,
    #             height,
    #             bloodType,
    #             birthday,
    #             phoneNumber,
    #             allType,
    #             dosage,
    #             bsa,
    #             (ancMeasurement, date),
    #             self.ancEdited,
    #         )
    #         msg = "Parameters saved successfully!"
    #         self.errorLabel.setText(msg)
    #         self.errorLabel.setStyleSheet("color:green")
    #         logging.info(msg)
    #         logging.info(vars(self.patient))
    #         self.ancEdited = False

    def showPatientListWindow(self):
        self.errorLabel.clear()
        self.parent().parent().showPatientListWindow()
        self.displayParameters()

    def showDashboardWindow(self):
        try:
            name = self.patientLineEdit.text()
            assert name != ""
            date = self.dateEdit.date().toPyDate()
            weight = float(self.weightEdit.text())
            height = float(self.heightEdit.text())
            dosage = float(self.dosageEdit.text())
            # bsa = float(self.bodySurfaceAreaMeasurement.text())
            ancMeasurement = float(self.ancMeasurementEdit.text())
        except:
            msg = "Input fields must not be empty"
            self.errorLabel.setText(msg)
            self.errorLabel.setStyleSheet("color:red")
            logging.error(msg)
        else:
            self.errorLabel.clear()
            self.parent().parent().showDashboardWindow()
            self.displayParameters()

    def valueChanged(self):
        self.ancEdited = True

    def updatePatientInfo(self):
        self.patient = self.parent().parent().selected_patient
        self.displayParameters()