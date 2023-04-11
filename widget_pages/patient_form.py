import logging
import math
import sqlite3
import numpy as np

from util.util import encryptData, valid_blood_types, valid_all_types, valid_sex_types

from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QDateEdit,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QRadioButton,
    QScrollArea,
    QPushButton,
    QCheckBox,
    QSizePolicy,
    QSpacerItem
)
from PyQt6.QtGui import QDoubleValidator, QFont
from pyqtgraph import plot
from datetime import datetime

logging.getLogger().setLevel(logging.INFO)


class Label(QLabel):
    def __init__(self, text, width=400):
        super().__init__()
        self.setText(text)
        self.setFont(QFont("Avenir", 18))
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
        self.setFont(QFont("Avenir", 18))
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

        self.patientFormBigLayout = QVBoxLayout()
        self.patientFormBigLayout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setFixedWidth(820)
        self.scroll_area.setStyleSheet(
            """
            QScrollArea
            {
                background-color: #ffffff;
                border-radius: 20px;
                border: 1px solid #aaaaaa;
                height: auto;
                padding: 5px
            }
            """
        )
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setWidgetResizable(True)
        self.patientFormBigLayout.addWidget(self.scroll_area, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        self.patientFormWidget = QWidget()
        self.patientFormWidget.setContentsMargins(0, 0, 0, 0)
        self.patientFormWidget.setFixedWidth(810)
        self.patientFormWidget.setObjectName("PatientFormOverall")
        self.patientFormWidget.setStyleSheet(
            """
            QWidget#PatientFormOverall
            {
                background-color: #ffffff;
                border-radius: 20px;
            }
            """
        )
        self.scroll_area.setWidget(self.patientFormWidget)

        self.patientFormLayout = QVBoxLayout(self.patientFormWidget)
        self.patientFormLayout.setContentsMargins(0, 20, 0, 10)

        self.typeOfPatientForm = Label("")
        self.typeOfPatientForm.setContentsMargins(0, 10, 0, 10)
        self.typeOfPatientForm.setFont(QFont("Avenir", 30))
        self.typeOfPatientForm.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.typeOfPatientForm.setFixedWidth(self.scroll_area.width() - 60)
        self.typeOfPatientForm.setStyleSheet("background-color: rgba(170, 170, 238, 100); height: 60px; border-radius: 20px;")
        self.patientFormLayout.addWidget(self.typeOfPatientForm, alignment=Qt.AlignmentFlag.AlignCenter)

        self.patientLabel = Label("Patient Name")
        self.patientLabel.setContentsMargins(30, 20, 0, 0)
        self.patientFormLayout.addWidget(self.patientLabel, alignment=Qt.AlignmentFlag.AlignBottom)

        self.patientNameLayout = QHBoxLayout()
        self.patientNameLayout.setContentsMargins(0, 0, 0, 0)

        self.patientFirstNameLineEdit = QLineEdit()
        self.patientFirstNameLineEdit.setContentsMargins(30, 0, 0, 0)
        self.patientFirstNameLineEdit.setPlaceholderText("First Name")
        self.patientFirstNameLineEdit.setFont(QFont("Avenir", 18))
        self.patientFirstNameLineEdit.setStyleSheet(
            "background-color: #f5f5f5; height: 40px; border-radius: 10px; padding: 0px 10px"
        )
        self.patientNameLayout.addWidget(self.patientFirstNameLineEdit)

        self.patientLastNameLineEdit = QLineEdit()
        self.patientLastNameLineEdit.setContentsMargins(10, 0, 30, 0)
        self.patientLastNameLineEdit.setPlaceholderText("Last Name")
        self.patientLastNameLineEdit.setFont(QFont("Avenir", 18))
        self.patientLastNameLineEdit.setStyleSheet(
            "background-color: #f5f5f5; height: 40px; border-radius: 10px; padding: 0px 10px"
        )
        self.patientNameLayout.addWidget(self.patientLastNameLineEdit)
        self.patientFormLayout.addLayout(self.patientNameLayout)
        
        self.sexLabel = Label("Sex")
        self.sexLabel.setContentsMargins(30, 10, 0, 0)
        self.patientFormLayout.addWidget(self.sexLabel, alignment=Qt.AlignmentFlag.AlignBottom)

        self.sexLayout = QHBoxLayout()
        self.sexLayout.setContentsMargins(30, 0, 0, 0)

        self.maleRadioButton = QRadioButton("Male", self)
        self.maleRadioButton.setContentsMargins(0, 0, 0, 0)
        self.maleRadioButton.setChecked(True)
        self.maleRadioButton.setFont(QFont("Avenir", 18))
        self.maleRadioButton.toggled.connect(self.selectedSexType)
        self.sexLayout.addWidget(self.maleRadioButton)

        self.femaleRadioButton = QRadioButton("Female", self)
        self.femaleRadioButton.setContentsMargins(10, 0, 0, 0)
        self.femaleRadioButton.setFont(QFont("Avenir", 18))
        self.femaleRadioButton.toggled.connect(self.selectedSexType)
        self.sexLayout.addWidget(self.femaleRadioButton)
        self.sex = "Male"

        self.patientFormLayout.addLayout(self.sexLayout)

        self.birthdayLayout = QVBoxLayout()
        self.birthdayLayout.setContentsMargins(30, 0, 30, 0)
        
        self.birthdayLabel = Label("Birthday")
        self.birthdayLabel.setContentsMargins(0, 10, 0, 0)
        self.birthdayLayout.addWidget(self.birthdayLabel, alignment=Qt.AlignmentFlag.AlignBottom)

        self.birthdayEdit = QDateEdit()
        self.birthdayEdit.setContentsMargins(0, 0, 0, 0)
        self.birthdayEdit.setFont(QFont("Avenir", 15))
        self.birthdayLayout.addWidget(self.birthdayEdit)
        self.patientFormLayout.addLayout(self.birthdayLayout)

        self.bodyLayout = QGridLayout()
        self.bodyLayout.setContentsMargins(0, 0, 0, 0)

        self.weightLabel = Label("Weight (kg)")
        self.weightLabel.setContentsMargins(30, 10, 0, 0)
        self.bodyLayout.addWidget(self.weightLabel, 0, 0, alignment=Qt.AlignmentFlag.AlignBottom)

        self.heightLabel = Label("Height (cm)")
        self.heightLabel.setContentsMargins(10, 10, 0, 0)
        self.bodyLayout.addWidget(self.heightLabel, 0, 1, alignment=Qt.AlignmentFlag.AlignBottom)

        self.bodySurfaceAreaLabel = Label("Body Surface Area (m^2)")
        self.bodySurfaceAreaLabel.setContentsMargins(10, 10, 30, 0)
        self.bodyLayout.addWidget(self.bodySurfaceAreaLabel, 0, 2, alignment=Qt.AlignmentFlag.AlignBottom)

        self.weightEdit = QLineEdit()
        self.weightEdit.setContentsMargins(30, 0, 0, 0)
        self.weightEdit.setPlaceholderText("kg")
        self.weightEdit.setFont(QFont("Avenir", 18))
        self.weightEdit.setStyleSheet(
            "background-color: #f5f5f5; height: 40px; border-radius: 10px; padding: 0px 10px"
        )
        self.bodyLayout.addWidget(self.weightEdit, 1, 0)

        self.heightEdit = QLineEdit()
        self.heightEdit.setContentsMargins(10, 0, 0, 0)
        self.heightEdit.setPlaceholderText("cm")
        self.heightEdit.setFont(QFont("Avenir", 18))
        self.heightEdit.setStyleSheet(
            "background-color: #f5f5f5; height: 40px; border-radius: 10px; padding: 0px 10px"
        )
        self.bodyLayout.addWidget(self.heightEdit, 1, 1)

        self.bodySurfaceAreaMeasurement = QLineEdit()
        self.bodySurfaceAreaMeasurement.setContentsMargins(10, 0, 30, 0)
        self.bodySurfaceAreaMeasurement.setPlaceholderText("m^2")
        self.bodySurfaceAreaMeasurement.setReadOnly(True)
        self.bodySurfaceAreaMeasurement.setFont(QFont("Avenir", 18))
        self.bodySurfaceAreaMeasurement.setStyleSheet(
            "background-color: #f5f5f5; height: 40px; border-radius: 10px; padding: 0px 10px"
        )
        self.bodyLayout.addWidget(self.bodySurfaceAreaMeasurement, 1, 2)
        self.patientFormLayout.addLayout(self.bodyLayout)

        self.bloodAndALLLayout = QGridLayout()
        self.bloodAndALLLayout.setContentsMargins(30, 0, 30, 0)

        self.bloodTypeLabel = Label("Blood Type")
        self.bloodTypeLabel.setContentsMargins(0, 10, 0, 0)
        self.bloodAndALLLayout.addWidget(self.bloodTypeLabel, 0, 0, alignment=Qt.AlignmentFlag.AlignBottom)
        
        self.allTypeLabel = Label("ALL Type")
        self.allTypeLabel.setContentsMargins(10, 10, 0, 0)
        self.bloodAndALLLayout.addWidget(self.allTypeLabel, 0, 1, alignment=Qt.AlignmentFlag.AlignBottom)

        self.bloodTypeSelect = QComboBox()
        self.bloodTypeSelect.setContentsMargins(0, 0, 0, 0)
        self.bloodTypeSelect.setFont(QFont("Avenir", 15))
        self.bloodTypeSelect.addItems(
            ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
        )
        self.bloodTypeSelect.activated.connect(self.selectedBloodType)
        self.bloodAndALLLayout.addWidget(self.bloodTypeSelect, 1, 0)

        self.allTypeSelect = QComboBox()
        self.allTypeSelect.setContentsMargins(10, 0, 0, 0)
        self.allTypeSelect.setFont(QFont("Avenir", 15))
        self.allTypeSelect.addItems(
            [
                "Immunophenotype",
                "French-American-British (FAB)",
                "ALL Cytogenetic Risk Group",
            ]
        )
        self.allTypeSelect.activated.connect(self.selectedAllType)
        self.bloodAndALLLayout.addWidget(self.allTypeSelect, 1, 1)
        self.patientFormLayout.addLayout(self.bloodAndALLLayout)
        
        self.phoneNumberLabel = Label("Phone Number")
        self.phoneNumberLabel.setContentsMargins(30, 10, 0, 0)
        self.patientFormLayout.addWidget(self.phoneNumberLabel, alignment=Qt.AlignmentFlag.AlignBottom)

        self.phoneNumberEdit = QLineEdit()
        self.phoneNumberEdit.setContentsMargins(30, 0, 30, 0)
        self.phoneNumberEdit.setPlaceholderText("xxx-xxx-xxxx")
        self.phoneNumberEdit.setFont(QFont("Avenir", 18))
        self.phoneNumberEdit.setStyleSheet(
            "background-color: #f5f5f5; height: 40px; border-radius: 10px; padding: 0px 10px"
        )
        self.patientFormLayout.addWidget(self.phoneNumberEdit)

        self.consentLayout = QHBoxLayout()
        self.consentLayout.setContentsMargins(30, 0, 30, 0)

        self.consentLabel = QLabel("I authorize the use and storage of my information in this application")
        self.consentLabel.setFont(QFont("Avenir", 18))
        self.consentLabel.setContentsMargins(0, 10, 0, 0)
        self.consentLayout.addWidget(self.consentLabel, alignment=Qt.AlignmentFlag.AlignLeft)

        self.consentCheckBox = QCheckBox()
        self.consentCheckBox.setContentsMargins(10, 10, 0, 0)
        self.consentCheckBox.setFixedWidth(25)
        self.consentLayout.addWidget(self.consentCheckBox, alignment=Qt.AlignmentFlag.AlignRight)
        self.patientFormLayout.addLayout(self.consentLayout)

        self.spacer = QSpacerItem(
            1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.patientFormLayout.addSpacerItem(self.spacer)

        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.setContentsMargins(30, 0, 30, 0)

        self.errorLabel = Label("")
        self.errorLabel.setContentsMargins(0, 0, 0, 0)
        self.bottomLayout.addWidget(self.errorLabel, 8, alignment=Qt.AlignmentFlag.AlignLeft)
        self.patient = None
        self.weightEdit.setValidator(QDoubleValidator())
        self.heightEdit.setValidator(QDoubleValidator())

        self.phoneNumberEdit.editingFinished.connect(self.phoneNumberFormatter)
        self.weightEdit.textEdited.connect(self.calculateBodySurfaceArea)
        self.heightEdit.textEdited.connect(self.calculateBodySurfaceArea)

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.cancelFromPatientForm)
        self.cancelButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancelButton.setMinimumWidth(100)
        self.cancelButton.setMinimumHeight(40)
        self.cancelButton.setMaximumHeight(50)
        self.cancelButton.setFont(QFont("Avenir", 18))
        self.cancelButton.setStyleSheet(
            "background-color: #aaaaee; border-radius: 10px;"
        )
        self.bottomLayout.addWidget(self.cancelButton, 1, alignment=Qt.AlignmentFlag.AlignRight)

        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.savePatientInformation)
        self.saveButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.saveButton.setMinimumWidth(100)
        self.saveButton.setMinimumHeight(40)
        self.saveButton.setMaximumHeight(50)
        self.saveButton.setFont(QFont("Avenir", 18))
        self.saveButton.setStyleSheet(
            "background-color: #aaaaee; border-radius: 10px;"
        )
        self.bottomLayout.addWidget(self.saveButton, 1, alignment=Qt.AlignmentFlag.AlignRight)

        self.patientFormLayout.addLayout(self.bottomLayout)

        self.setLayout(self.patientFormBigLayout)

    def selectedSexType(self):
        sex = self.sender()
        if sex.isChecked():
            self.sex = sex.text()

    def selectedAllType(self, index):
        self.allType = self.allTypeSelect.itemText(index)  # Get the text at index.

    def selectedBloodType(self, index):
        self.bloodType = self.bloodTypeSelect.itemText(index)  # Get the text at index.

    def displayParameters(self):
        self.patientFirstNameLineEdit.clear()
        self.patientLastNameLineEdit.clear()
        self.weightEdit.clear()
        self.heightEdit.clear()
        self.phoneNumberEdit.clear()
        self.birthdayEdit.clear()
        self.birthdayEdit.setDate(QDate.currentDate())
        self.bodySurfaceAreaMeasurement.clear()
        self.consentCheckBox.setChecked(False)

        if self.patient is not None:
            self.getNames()
            self.typeOfPatientForm.setText("Edit Patient Data")
            self.weightEdit.setText(str(self.patient.weight))
            self.heightEdit.setText(str(self.patient.height))
            self.bloodTypeSelect.setCurrentText(self.patient.bloodType)
            self.allTypeSelect.setCurrentText(self.patient.allType)
            self.birthdayEdit.setDate(
                QDate.fromString(self.patient.birthday, "yyyyMMdd")
            )

            self.phoneNumberFormatterBegin()
            self.bodySurfaceAreaMeasurement.setText(str(self.patient.bsa))
            self.consentCheckBox.setChecked(True)
        else:
            self.typeOfPatientForm.setText("New Patient Enrollment")

    def getNames(self):
        self.nameTuple = self.patient.name.split(" ")
        self.patientFirstNameLineEdit.setText(self.nameTuple[0])
        self.patientLastNameLineEdit.setText(self.nameTuple[1])

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

    def cancelFromPatientForm(self):
        self.errorLabel.clear()
        if self.parent().parent().adding_new_patient:
            self.parent().parent().showPatientListWindow()
        else:
            self.parent().parent().showPatientInformationWindow()
        
    def savePatientInformation(self):
        try:
            name = self.patientFirstNameLineEdit.text() + " " + self.patientLastNameLineEdit.text()
            assert name != ""
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
            age = str(self.calculateAge())
            sex = self.sex
            assert sex in valid_sex_types
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
                      blood_type, all_type, body_surface_area, oncologist_id, sex)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                        encryptData(sex, password)
                    ),
                )

                res = conn.execute("SELECT last_insert_rowid()")
                patient_id = res.fetchone()[0]

            else:
                password = self.parent().parent().password
                conn.execute(
                    """
                        UPDATE patients 
                        SET name=?, weight=?, height=?, phone_number=?, birthday=?, age=?, blood_type=?, all_type=?, body_surface_area=?, sex=? 
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
                        encryptData(sex, password),
                        self.patient.id,
                    ),
                )

            conn.commit()

            self.parent().parent().updateSelectedPatient(patient_id)
            self.patient = self.parent().parent().selected_patient

        except sqlite3.Error as er:
            msg = "Existing entry in the database. Please check your inputs."
            self.errorLabel.setText(msg)
            self.errorLabel.setStyleSheet("color:red")
            logging.error(er)

        except Exception as er:
            er = str(er)
            if er != "Patient must provide consent to store data":
                msg = "Input fields must not be empty"
            else:
                msg = "Patient must provide consent to store data"
            self.errorLabel.setText(msg)
            self.errorLabel.setStyleSheet("color:red")
            logging.error(er)

        else:
            self.errorLabel.clear()
            msg = "Parameters saved successfully!"
            self.errorLabel.setText(msg)
            self.errorLabel.setStyleSheet("color:green")
            logging.info(msg)
            logging.info(vars(self.patient))
            self.errorLabel.clear()
            self.parent().parent().showPatientInformationWindow()

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

    def updatePatientInfo(self):
        self.patient = self.parent().parent().selected_patient
        # resetting fields 
        self.sex = "Male"
        self.maleRadioButton.setChecked(True)
        self.femaleRadioButton.setChecked(False)
        self.displayParameters()
