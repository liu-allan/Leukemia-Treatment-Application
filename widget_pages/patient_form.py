import logging
import math
import sqlite3

from PyQt6.QtCore import QDate, Qt, QRect
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
    QCheckBox
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
        
        self.genderLabel = Label("Gender/Sex")
        self.genderLabel.setContentsMargins(30, 10, 0, 0)
        self.patientFormLayout.addWidget(self.genderLabel, alignment=Qt.AlignmentFlag.AlignBottom)

        self.genderLayout = QHBoxLayout()
        self.genderLayout.setContentsMargins(30, 0, 0, 0)

        self.radioButton = QRadioButton("Male")
        self.radioButton.setContentsMargins(0, 0, 0, 0)
        self.radioButton.setChecked(True)
        self.radioButton.gender = "Male"
        self.radioButton.setFont(QFont("Avenir", 18))
        self.radioButton.toggled.connect(self.selectedGenderType)
        self.genderLayout.addWidget(self.radioButton)

        self.radioButton = QRadioButton("Female")
        self.radioButton.setContentsMargins(10, 0, 0, 0)
        self.radioButton.setFont(QFont("Avenir", 18))
        self.radioButton.gender = "Female"
        self.radioButton.toggled.connect(self.selectedGenderType)
        self.genderLayout.addWidget(self.radioButton)

        self.patientFormLayout.addLayout(self.genderLayout)

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

        self.medicalLayout = QGridLayout()
        self.medicalLayout.setContentsMargins(0, 0, 0, 0)

        self.ancCountLabel = Label("ANC Measurement (# Cells/L) x 1e9")
        self.ancCountLabel.setContentsMargins(30, 10, 0, 0)
        self.medicalLayout.addWidget(self.ancCountLabel, 0, 0, alignment=Qt.AlignmentFlag.AlignBottom)

        self.dosageLabel = Label("6-MP Dosage (mg)")
        self.dosageLabel.setContentsMargins(10, 10, 30, 0)
        self.medicalLayout.addWidget(self.dosageLabel, 0, 1, alignment=Qt.AlignmentFlag.AlignBottom)

        self.ancMeasurementEdit = QLineEdit()
        self.ancMeasurementEdit.setContentsMargins(30, 0, 0, 0)
        self.ancMeasurementEdit.setPlaceholderText("# Cells/L x 1e9")
        self.ancMeasurementEdit.setFont(QFont("Avenir", 18))
        self.ancMeasurementEdit.setStyleSheet(
            "background-color: #f5f5f5; height: 40px; border-radius: 10px; padding: 0px 10px"
        )
        self.medicalLayout.addWidget(self.ancMeasurementEdit, 1, 0)

        self.dosageEdit = QLineEdit()
        self.dosageEdit.setContentsMargins(10, 0, 30, 0)
        self.dosageEdit.setPlaceholderText("mg")
        self.dosageEdit.setFont(QFont("Avenir", 18))
        self.dosageEdit.setStyleSheet(
            "background-color: #f5f5f5; height: 40px; border-radius: 10px; padding: 0px 10px"
        )
        self.medicalLayout.addWidget(self.dosageEdit, 1, 1)
        self.patientFormLayout.addLayout(self.medicalLayout)

        self.dateLayout = QVBoxLayout()
        self.dateLayout.setContentsMargins(30, 0, 30, 0)
        
        self.dateLabel = Label("Date of ANC Measurement")
        self.dateLabel.setContentsMargins(0, 10, 0, 0)
        self.dateLayout.addWidget(self.dateLabel, alignment=Qt.AlignmentFlag.AlignBottom)

        self.dateEdit = QDateEdit()
        self.dateEdit.setContentsMargins(0, 0, 0, 0)
        self.dateEdit.setFont(QFont("Avenir", 15))
        self.dateLayout.addWidget(self.dateEdit)
        self.patientFormLayout.addLayout(self.dateLayout)

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

        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.setContentsMargins(30, 0, 30, 0)

        self.errorLabel = Label("")
        self.errorLabel.setContentsMargins(0, 0, 0, 0)
        self.bottomLayout.addWidget(self.errorLabel, 8, alignment=Qt.AlignmentFlag.AlignLeft)
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
        
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.showPatientListWindow)
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

    def selectedGenderType(self):
        self.radioButton = self.sender()
        if self.radioButton.isChecked():
            print(self.radioButton.gender)

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
        self.dosageEdit.clear()
        self.ancMeasurementEdit.clear()
        self.dateEdit.setDate(QDate.currentDate())
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

    def savePatientInformation(self):
        try:
            name = self.patientFirstNameLineEdit.text() + " " + self.patientLastNameLineEdit.text()
            assert name != ""
            date = self.dateEdit.date().toString("yyyyMMdd")
            weight = float(self.weightEdit.text())
            height = float(self.heightEdit.text())
            allType = self.allTypeSelect.currentText()
            bloodType = self.bloodTypeSelect.currentText()
            birthday = self.birthdayEdit.date().toString("yyyyMMdd")
            phoneNumber = self.phoneNumberFormatterReverse()
            assert phoneNumber != ""
            assignedDoctor = self.parent().parent().username
            bsa = float(self.bodySurfaceAreaMeasurement.text())
            ancMeasurement = float(self.ancMeasurementEdit.text())
            dosageMeasurement = float(self.dosageEdit.text())
            age = self.calculateAge()
            user_id = self.createUserID(name)

            conn = self.parent().parent().getDatabaseConnection()
            patient_id = self.patient.id if self.patient else -1

            if not self.consentCheckBox.isChecked():
                raise Exception("Patient must provide consent to store data") 

            if self.patient is None:
                conn.execute(
                    """
                        INSERT INTO patients (user_id, name, weight, height, phone_number, birthday, age, 
                      blood_type, all_type, body_surface_area, oncologist_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        user_id,
                        name,
                        weight,
                        height,
                        phoneNumber,
                        birthday,
                        age,
                        bloodType,
                        allType,
                        bsa,
                        self.parent().parent().username,
                    ),
                )

                res = conn.execute("SELECT last_insert_rowid()")
                patient_id = res.fetchone()[0]

            else:
                conn.execute(
                    """
                        UPDATE patients 
                        SET name=?, weight=?, height=?, phone_number=?, birthday=?, age=?, blood_type=?, all_type=?, body_surface_area=? 
                        WHERE id=?
                    """,
                    (
                        name,
                        weight,
                        height,
                        phoneNumber,
                        birthday,
                        age,
                        bloodType,
                        allType,
                        bsa,
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

        except Exception as er:
            er = str(er)
            if er != "Patient must provide consent to store data":
                msg = "Input fields must not be empty"
            else:
                msg = "Patient must provide consent to store data"
            self.errorLabel.setText(msg)
            self.errorLabel.setStyleSheet("color:red")
            logging.error(msg)

        else:
            self.errorLabel.clear()
            self.patient.save(
                user_id,
                name,
                weight,
                height,
                bsa,
                allType,
                age,
                bloodType,
                birthday,
                phoneNumber,
                assignedDoctor,
                (dosageMeasurement, date),
                self.dosageEdited,
                (ancMeasurement, date),
                self.ancEdited,
            )
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
