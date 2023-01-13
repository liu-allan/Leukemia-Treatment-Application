import logging
import math
import sqlite3

from PyQt6 import uic
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QDateEdit,
    QDialogButtonBox,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtGui import QDoubleValidator, QFont

logging.getLogger().setLevel(logging.INFO)


class Label(QLabel):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setFont(QFont("Avenir", 12))
        self.setFixedWidth(400)


class LineEdit(QLineEdit):
    def __init__(self, placeholderText):
        super().__init__()
        self.setPlaceholderText(placeholderText)
        self.setFont(QFont("Avenir", 12))
        self.setFixedWidth(200)


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
        

class PatientInformationWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.patientLabel = Label("Patient Name")
        self.patientLineEdit = LineEdit("Patient")
        self.layout.addWidget(FormRow(self.patientLabel, self.patientLineEdit))

        self.weightLabel = Label("Weight (kg)")
        self.weightEdit = LineEdit("kg")
        self.layout.addWidget(FormRow(self.weightLabel, self.weightEdit))

        self.heightLabel = Label("Height (cm)")
        self.heightEdit = LineEdit("cm")
        self.layout.addWidget(FormRow(self.heightLabel, self.heightEdit))

        self.bodySurfaceAreaLabel = Label("Body Surface Area (m^2)")
        self.bodySurfaceAreaMeasurement = Label("m^2")
        self.bodySurfaceAreaMeasurement.setFixedWidth(200)
        self.layout.addWidget(FormRow(self.bodySurfaceAreaLabel, self.bodySurfaceAreaMeasurement))

        self.dosageLabel = Label("6-MP Dosage (mg)")
        self.dosageEdit = LineEdit("mg")
        self.layout.addWidget(FormRow(self.dosageLabel, self.dosageEdit))

        self.ancCountLabel = Label("ANC Measurement (g/L)")
        self.ancMeasurementEdit = LineEdit("g/L")
        self.layout.addWidget(FormRow(self.ancCountLabel, self.ancMeasurementEdit))

        self.dateLabel = Label("Date of ANC Measurement")
        self.dateEdit = QDateEdit()
        self.dateEdit.setFixedWidth(200)
        self.layout.addWidget(FormRow(self.dateLabel, self.dateEdit))

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
        self.buttonBox.button(self.buttonBox.standardButtons().Save).clicked.connect(
            self.savePatientInformation
        )
        self.buttonBox.button(self.buttonBox.standardButtons().Ok).clicked.connect(
            self.showDashboardWindow
        )
        self.layout.addWidget(FormRow(self.errorLabel, self.buttonBox))
        self.setLayout(self.layout)

    def displayParameters(self):
        self.patientLineEdit.clear()
        self.weightEdit.clear()
        self.heightEdit.clear()
        self.dosageEdit.clear()
        self.ancMeasurementEdit.clear()
        self.dateEdit.setDate(QDate.currentDate())
        self.bodySurfaceAreaMeasurement.clear()

        if self.patient is not None:
            self.patientLineEdit.setText(self.patient.name)
            self.weightEdit.setText(str(self.patient.weight))
            self.heightEdit.setText(str(self.patient.height))
            self.dosageEdit.setText(str(self.patient.dosage))
            self.ancMeasurementEdit.setText(str(self.patient.ancMeasurement[-1][0]))
            self.dateEdit.setDate(self.patient.ancMeasurement[-1][1])
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
            self.bodySurfaceAreaMeasurement.setText("{:.2f}".format(bsa))

    def savePatientInformation(self):
        try:
            name = self.patientLineEdit.text()
            assert name != ""
            date = self.dateEdit.dateTime().toSecsSinceEpoch()
            weight = float(self.weightEdit.text())
            height = float(self.heightEdit.text())
            dosage = float(self.dosageEdit.text())
            bsa = float(self.bodySurfaceAreaMeasurement.text())
            ancMeasurement = float(self.ancMeasurementEdit.text())

            conn = self.parent().parent().getDatabaseConnection()
            patient_id = self.patient.id if self.patient else -1

            if self.patient is None:
                conn.execute(
                    """
                        INSERT INTO patients (name, weight, height, dosage, body_surface_area, oncologist_id)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        name,
                        weight,
                        height,
                        dosage,
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
                        SET name=?, weight=?, height=?, dosage=?, body_surface_area=? 
                        WHERE id=?
                    """,
                    (name, weight, height, dosage, bsa, self.patient.id),
                )

            conn.execute(
                """
                    INSERT INTO measurements (time, anc_measurement, patient_id)
                    VALUES (?, ?, ?)
                """,
                (date, ancMeasurement, patient_id),
            )
            conn.commit()

            self.parent().parent().updateSelectedPatient(patient_id)
            self.patient = self.parent().parent().selected_patient

        except sqlite3.Error as er:
            msg = "Existing entry in the database. Please check your inputs."
            self.errorLabel.setText(msg)
            self.errorLabel.setStyleSheet("color:red")
            logging.error(er)

        except:
            msg = "Input fields must not be empty"
            self.errorLabel.setText(msg)
            self.errorLabel.setStyleSheet("color:red")
            logging.error(msg)

        else:
            self.errorLabel.clear()
            self.patient.save(
                name,
                weight,
                height,
                dosage,
                bsa,
                (ancMeasurement, date),
                self.ancEdited,
            )
            msg = "Parameters saved successfully!"
            self.errorLabel.setText(msg)
            self.errorLabel.setStyleSheet("color:green")
            logging.info(msg)
            logging.info(vars(self.patient))
            self.ancEdited = False

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
            bsa = float(self.bodySurfaceAreaMeasurement.text())
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
