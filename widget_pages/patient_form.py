import logging
import math
import sqlite3
import numpy as np

from util.util import encryptData, valid_blood_types, valid_all_types, valid_gender_types

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
    QCheckBox
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
    def __init__(self, label, widget, spacing=50):
        super().__init__()
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addSpacing(spacing)
        layout.addWidget(widget)
        self.setLayout(layout)


class PatientFormWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.patientFormLayout = QVBoxLayout()
        self.patientFormLayout.setContentsMargins(0, 0, 0, 0)

        self.patientLabel = Label("Patient Name")
        self.patientLineEdit = LineEdit("Patient")
        self.patientFormLayout.addWidget(
            FormRow(self.patientLabel, self.patientLineEdit)
        )

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
        self.patientFormLayout.addWidget(
            FormRow(self.bodySurfaceAreaLabel, self.bodySurfaceAreaMeasurement)
        )

        self.bloodTypeLabel = Label("Blood Type")
        self.bloodTypeSelect = QComboBox()
        self.bloodTypeSelect.addItems(
            ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
        )
        self.bloodTypeSelect.activated.connect(self.selectedBloodType)
        self.bloodTypeSelect.setFixedWidth(200)
        self.bloodTypeSelect.setFont(QFont("Avenir", 15))
        self.patientFormLayout.addWidget(
            FormRow(self.bloodTypeLabel, self.bloodTypeSelect)
        )

        self.birthdayLabel = Label("Birthday")
        self.birthdayEdit = QDateEdit()
        self.birthdayEdit.setFont(QFont("Avenir", 15))
        self.birthdayEdit.setFixedWidth(200)
        self.patientFormLayout.addWidget(FormRow(self.birthdayLabel, self.birthdayEdit))

        self.phoneNumberLabel = Label("Phone Number")
        self.phoneNumberEdit = LineEdit("xxx-xxx-xxxx")
        self.patientFormLayout.addWidget(
            FormRow(self.phoneNumberLabel, self.phoneNumberEdit)
        )

        self.allTypeLabel = Label("ALL Type")
        self.allTypeSelect = QComboBox()
        self.allTypeSelect.addItems(
            [
                "Immunophenotype",
                "French-American-British (FAB)",
                "ALL Cytogenetic Risk Group",
            ]
        )
        self.allTypeSelect.activated.connect(self.selectedAllType)
        self.allTypeSelect.setFixedWidth(200)
        self.allTypeSelect.setFont(QFont("Avenir", 10))
        self.patientFormLayout.addWidget(FormRow(self.allTypeLabel, self.allTypeSelect))

        self.dosageLabel = Label("6-MP Dosage (mg)")
        self.dosageEdit = LineEdit("mg")
        self.patientFormLayout.addWidget(FormRow(self.dosageLabel, self.dosageEdit))

        self.ancCountLabel = Label("ANC Measurement (# Cells/L) x 1e9")
        self.ancMeasurementEdit = LineEdit("# Cells/L x 1e9")
        self.patientFormLayout.addWidget(
            FormRow(self.ancCountLabel, self.ancMeasurementEdit)
        )

        self.dateLabel = Label("Date of ANC Measurement")
        self.dateEdit = QDateEdit()
        self.dateEdit.setFont(QFont("Avenir", 15))
        self.dateEdit.setFixedWidth(200)
        self.patientFormLayout.addWidget(FormRow(self.dateLabel, self.dateEdit))

        self.consentLabel = Label("I authorize the use and storage of my information in this application", 600)
        self.consentCheckBox = QCheckBox()
        self.consentCheckBox.setFixedWidth(25)
        self.consentCheckBox.setStyleSheet("QCheckBox::indicator { width: 25px; height: 25px;}")
        self.patientFormLayout.addWidget(FormRow(self.consentLabel, self.consentCheckBox, 25))

        self.errorLabel = Label("")
        self.patient = None
        self.weightEdit.setValidator(QDoubleValidator())
        self.heightEdit.setValidator(QDoubleValidator())
        self.dosageEdit.setValidator(QDoubleValidator())
        self.ancMeasurementEdit.setValidator(QDoubleValidator())
        self.ancEdited = False
        self.dosageEdited = False

        self.ancMeasurementEdit.textEdited.connect(self.valueChanged)
        self.dosageEdit.textEdited.connect(self.valueChangedDosage)
        self.dateEdit.editingFinished.connect(self.valueChanged)
        self.phoneNumberEdit.editingFinished.connect(self.phoneNumberFormatter)
        self.weightEdit.textEdited.connect(self.calculateBodySurfaceArea)
        self.heightEdit.textEdited.connect(self.calculateBodySurfaceArea)

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(self.buttonBox.standardButtons().Cancel)
        self.buttonBox.addButton(self.buttonBox.standardButtons().Save)
        self.buttonBox.setFont(QFont("Avenir", 12))
        self.buttonBox.setFixedWidth(200)
        self.buttonBox.setStyleSheet(
            "background-color: #aaaaee; border-radius: 5px; padding: 10px"
        )

        self.buttonBox.button(self.buttonBox.standardButtons().Cancel).clicked.connect(
            self.showPatientListWindow
        )
        self.buttonBox.button(self.buttonBox.standardButtons().Save).clicked.connect(
            self.savePatientInformation
        )

        self.buttonBox.setCursor(Qt.CursorShape.PointingHandCursor)
        self.patientFormLayout.addWidget(FormRow(self.errorLabel, self.buttonBox))

        self.setLayout(self.patientFormLayout)

    def selectedAllType(self, index):
        self.allType = self.allTypeSelect.itemText(index)  # Get the text at index.

    def selectedBloodType(self, index):
        self.bloodType = self.bloodTypeSelect.itemText(index)  # Get the text at index.

    def displayParameters(self):
        self.patientLineEdit.clear()
        self.weightEdit.clear()
        self.heightEdit.clear()
        self.phoneNumberEdit.clear()
        self.birthdayEdit.clear()
        self.birthdayEdit.setDate(QDate.currentDate())
        self.bodySurfaceAreaMeasurement.clear()
        self.dosageEdit.clear()
        self.ancMeasurementEdit.clear()
        self.dateEdit.setDate(QDate.currentDate())
        self.consentCheckBox.setChecked(False)

        if self.patient is not None:
            self.patientLineEdit.setText(self.patient.name)
            self.weightEdit.setText(str(self.patient.weight))
            self.heightEdit.setText(str(self.patient.height))
            self.bloodTypeSelect.setCurrentText(self.patient.bloodType)
            self.allTypeSelect.setCurrentText(self.patient.allType)
            self.birthdayEdit.setDate(
                QDate.fromString(self.patient.birthday, "yyyyMMdd")
            )

            self.phoneNumberFormatterBegin()

            self.bodySurfaceAreaMeasurement.setText(str(self.patient.bsa))
            self.ancMeasurementDate = [
                datetime.strptime(str(item[1]), "%Y%m%d")
                for item in self.patient.ancMeasurement
            ]
            self.ancMeasurement = [item[0] for item in self.patient.ancMeasurement]
            self.ancMeasurementEdit.setText(str(self.ancMeasurement[-1]))
            self.dateEdit.setDate(
                QDate.fromString(str(self.ancMeasurementDate[-1].date()), "yyyy-MM-dd")
            )

            self.dosagePrescribedDate = [
                datetime.strptime(str(item[1]), "%Y%m%d")
                for item in self.patient.dosageMeasurement
            ]
            self.dosageAmount = [item[0] for item in self.patient.dosageMeasurement]
            self.dosageEdit.setText(str(self.dosageAmount[-1]))
            self.consentCheckBox.setChecked(True)

    def phoneNumberFormatterBegin(self):
        self.phoneNumberEdit.setText(
            format(int(self.patient.phoneNumber[:-1]), ",").replace(",", "-")
            + self.patient.phoneNumber[-1]
        )

    def phoneNumberFormatter(self):
        self.phoneNumberEdit.setText(
            format(int(self.phoneNumberEdit.text()[:-1]), ",").replace(",", "-")
            + self.phoneNumberEdit.text()[-1]
        )

    def phoneNumberFormatterReverse(self):
        return self.phoneNumberEdit.text().replace("-", "")

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

    def savePatientInformation(self):
        try:
            name = self.patientLineEdit.text()
            assert name != ""
            date = self.dateEdit.date().toString("yyyyMMdd")
            weight = self.weightEdit.text()
            height = self.heightEdit.text()
            allType = self.allTypeSelect.currentText()
            assert allType in valid_all_types
            bloodType = self.bloodTypeSelect.currentText()
            assert bloodType in valid_blood_types
            birthday = self.birthdayEdit.date().toString("yyyyMMdd")
            phoneNumber = self.phoneNumberFormatterReverse()
            assert phoneNumber != ""
            assignedDoctor = self.parent().parent().username
            bsa = self.bodySurfaceAreaMeasurement.text()
            ancMeasurement = float(self.ancMeasurementEdit.text())
            dosageMeasurement = float(self.dosageEdit.text())
            age = str(self.calculateAge())
            user_id = self.createUserID(name)

            conn = self.parent().parent().getDatabaseConnection()
            patient_id = self.patient.id if self.patient else -1

            if not self.consentCheckBox.isChecked():
                raise Exception("Patient must provide consent to store data") 

            if self.patient is None:
                password = self.parent().parent().password
                conn.execute(
                    """
                        INSERT INTO patients (user_id, name, weight, height, phone_number, birthday, age, 
                      blood_type, all_type, body_surface_area, oncologist_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        encryptData(user_id, password),
                        encryptData(name, password),
                        encryptData(weight, password),
                        encryptData(height, password),
                        encryptData(phoneNumber, password),
                        encryptData(birthday, password),
                        encryptData(age, password),
                        encryptData(bloodType, password),
                        encryptData(allType, password),
                        encryptData(bsa, password),
                        self.parent().parent().username,
                    ),
                )

                res = conn.execute("SELECT last_insert_rowid()")
                patient_id = res.fetchone()[0]

            else:
                password = self.parent().parent().password
                conn.execute(
                    """
                        UPDATE patients 
                        SET name=?, weight=?, height=?, phone_number=?, birthday=?, age=?, blood_type=?, all_type=?, body_surface_area=? 
                        WHERE id=?
                    """,
                    (
                        encryptData(name, password),
                        encryptData(weight, password),
                        encryptData(height, password),
                        encryptData(phoneNumber, password),
                        encryptData(birthday, password),
                        encryptData(age, password),
                        encryptData(bloodType, password),
                        encryptData(allType, password),
                        encryptData(bsa, password),
                        self.patient.id,
                    ),
                )

            conn.execute(
                """
                    INSERT INTO measurements (time, anc_measurement, dosage_measurement, patient_id)
                    VALUES (?, ?, ?, ?)
                """,
                (date, ancMeasurement, dosageMeasurement, patient_id),
            )
            conn.commit()

            self.parent().parent().updateSelectedPatient(patient_id)
            self.patient = self.parent().parent().selected_patient

        except sqlite3.Error as er:
            msg = "Existing entry in the database. Please check your inputs."
            self.errorLabel.setText(msg)
            self.errorLabel.setStyleSheet("color:red")
            logging.error(er)

        except Exception as e:

            if not self.consentCheckBox.isChecked():
                msg = "Patient must provide consent to store data"
            else:
                msg = "Input fields must not be empty"
            self.errorLabel.setText(msg)
            self.errorLabel.setStyleSheet("color:red")
            logging.error(e)

        else:
            self.errorLabel.clear()
            msg = "Parameters saved successfully!"
            self.errorLabel.setText(msg)
            self.errorLabel.setStyleSheet("color:green")
            logging.info(msg)
            logging.info(vars(self.patient))
            self.ancEdited = False
            self.dosageEdited = False
            self.errorLabel.clear()
            self.showPatientListWindow()

    def calculateAge(self):
        today = datetime.today().date()
        return (
            today.year
            - self.birthdayEdit.date().year()
            - (
                (today.month, today.day)
                < (self.birthdayEdit.date().month(), self.birthdayEdit.date().day())
            )
        )

    # creates the unique user id for each patient
    def createUserID(self, patient_name):
        nameSplit = patient_name.split()
        firstName = nameSplit[0]
        lastName = "".join(nameSplit[1:])  # for patients with middle names
        microsecond = datetime.now().microsecond
        return firstName.lower() + lastName.lower() + str(microsecond)

    def showPatientListWindow(self):
        self.errorLabel.clear()
        self.parent().parent().showPatientListWindow()

    def valueChanged(self):
        self.ancEdited = True

    def valueChangedDosage(self):
        self.dosageEdited = True

    def updatePatientInfo(self):
        self.patient = self.parent().parent().selected_patient
        self.displayParameters()
