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

        self.sideBarLayout = QHBoxLayout()
        self.sideBarLayout.setContentsMargins(10, 0, 10, 0)

        self.sideBar = QWidget()
        self.sideBar.setContentsMargins(0, 0, 0, 0)
        self.sideBar.setStyleSheet(
            "background-color: #bfd8d2; height: 750; border-radius: 20px;"
        )
        self.sideBarLayout.addWidget(self.sideBar, 1)

        self.patientInfo = QWidget()
        self.patientInfo.setContentsMargins(0, 0, 0, 0)
        self.sideBarLayout.addWidget(self.patientInfo, 9)

        self.layout = QVBoxLayout(self.patientInfo)
        self.layout.setContentsMargins(10, 0, 0, 0)
        
        self.patientCard = PatientCard()
        self.layout.addWidget(self.patientCard, 1)

        self.patientInput = QWidget()
        self.patientInput.setContentsMargins(0, 10, 0, 0)
        self.layout.addWidget(self.patientInput, 3)

        self.patientBottomLayout = QHBoxLayout(self.patientInput)
        self.patientBottomLayout.setContentsMargins(0, 0, 0, 0)

        # HISTORIC GRAPHS
        self.patientHistoricGraphs = QWidget()
        self.patientHistoricGraphs.setContentsMargins(0, 0, 0, 0)
        self.patientHistoricGraphs.setStyleSheet(
            "background-color: #aaaaee; border-radius: 20px;"
        )

        self.graphLayout = QVBoxLayout(self.patientHistoricGraphs)

        self.graphLabel = LabelBolded("Patient Historic Data", 20, [0, 0, 0, 10])
        self.graphLayout.addWidget(self.graphLabel, 1)

        date_axis = pg.DateAxisItem(orientation='bottom')
        self.graphWidgetANC = pg.PlotWidget(axisItems = {'bottom': date_axis})
    
        self.graphLayout.addWidget(self.graphWidgetANC, 7)

        self.graphWidgetANC.setCursor(Qt.CursorShape.OpenHandCursor)
        # Temp data -> will connect to matlab in the future
        self.ancMeasurementDate = []
        self.ancMeasurement = []
        # Add Background colour to white
        self.graphWidgetANC.setBackground("w")
        # Add Title
        self.graphWidgetANC.setTitle(
            "Historic ANC Measurement",
            color="#000",
            font=QFont("Avenir", 15)
        )
        # Add Axis Labels
        styles = {"color": "#000000", "font": QFont("Avenir", 15)}
        self.graphWidgetANC.setLabel("left", "ANC Measurement (g/L)", **styles)
        self.graphWidgetANC.setLabel("bottom", "ANC Measurement Date", **styles)
        # Add legend
        self.graphWidgetANC.addLegend()
        # Add grid
        self.graphWidgetANC.showGrid(x=True, y=True)

        date_axis2 = pg.DateAxisItem(orientation='bottom')
        self.graphWidgetDosages = pg.PlotWidget(axisItems = {'bottom': date_axis2})
        self.graphLayout.addWidget(self.graphWidgetDosages, 7)

        self.graphWidgetDosages.setCursor(Qt.CursorShape.OpenHandCursor)
        # Temp data -> will connect to matlab in the future
        self.dosagePrescribedDate = [datetime(2022, 8, 21), datetime(2022, 9, 21), datetime(2022, 11, 30), datetime(2023, 1, 10)]
        self.dosageAmount = [60, 30, 40, 20]

        # Add Background colour to white
        self.graphWidgetDosages.setBackground("w")
        # Add Title
        self.graphWidgetDosages.setTitle(
            "Historic Dosage Amount Prescribed",
            color="#000",
            font=QFont("Avenir", 15)
        )
        # Add Axis Labels
        styles = {"color": "#000000", "font": QFont("Avenir", 15)}
        self.graphWidgetDosages.setLabel("left", "Dosage Amount Prescribed", **styles)
        self.graphWidgetDosages.setLabel("bottom", "Dosage Prescription Date", **styles)
        # Add legend
        self.graphWidgetDosages.addLegend()
        # Add grid
        self.graphWidgetDosages.showGrid(x=True, y=True)

        pen = pg.mkPen(color="#aaaaee", width=5)
        self.graphWidgetDosages.plot(
            x=[x.timestamp() for x in self.dosagePrescribedDate], y=self.dosageAmount, name="Dosage Amount Prescribed", pen=pen, symbol="o", symbolSize=7, symbolBrush=("#aaaaee")
        )

        self.patientBottomLayout.addWidget(self.patientHistoricGraphs, 1)

        self.patientInputRight = QWidget()
        self.patientInputRight.setContentsMargins(0, 0, 0, 0)
        self.patientInputRight.setStyleSheet(
            "background-color: #ffffff; border-radius: 20px;"
        )
        self.patientBottomLayout.addWidget(self.patientInputRight, 2)

        self.patientInputLayout = QVBoxLayout(self.patientInputRight)
        self.patientInputLayout.setContentsMargins(0, 0, 0, 0)

        # self.patientLabel = Label("Patient Name")
        # self.patientLineEdit = LineEdit("Patient")
        # self.patientInputLayout.addWidget(FormRow(self.patientLabel, self.patientLineEdit))

        # self.weightLabel = Label("Weight (kg)")
        # self.weightEdit = LineEdit("kg")
        # self.patientInputLayout.addWidget(FormRow(self.weightLabel, self.weightEdit))

        # self.heightLabel = Label("Height (cm)")
        # self.heightEdit = LineEdit("cm")
        # self.patientInputLayout.addWidget(FormRow(self.heightLabel, self.heightEdit))

        # self.bodySurfaceAreaLabel = Label("Body Surface Area (m^2)")
        # self.bodySurfaceAreaMeasurement = Label("m^2")
        # self.bodySurfaceAreaMeasurement.setFixedWidth(200)
        # self.patientInputLayout.addWidget(FormRow(self.bodySurfaceAreaLabel, self.bodySurfaceAreaMeasurement))

        self.dosageLabel = Label("6-MP Dosage (mg)")
        self.dosageEdit = LineEdit("mg")
        self.patientInputLayout.addWidget(FormRow(self.dosageLabel, self.dosageEdit))

        self.ancCountLabel = Label("ANC Measurement (g/L)")
        self.ancMeasurementEdit = LineEdit("g/L")
        self.patientInputLayout.addWidget(FormRow(self.ancCountLabel, self.ancMeasurementEdit))

        self.dateLabel = Label("Date of ANC Measurement")
        self.dateEdit = QDateEdit()
        self.dateEdit.setFixedWidth(200)
        self.patientInputLayout.addWidget(FormRow(self.dateLabel, self.dateEdit))

        self.errorLabel = Label("")
        self.patient = None
        # self.weightEdit.setValidator(QDoubleValidator())
        # self.heightEdit.setValidator(QDoubleValidator())
        self.dosageEdit.setValidator(QDoubleValidator())
        self.ancMeasurementEdit.setValidator(QDoubleValidator())
        self.ancEdited = False

        self.ancMeasurementEdit.textEdited.connect(self.valueChanged)
        self.dateEdit.editingFinished.connect(self.valueChanged)
        # self.weightEdit.textEdited.connect(self.calculateBodySurfaceArea)
        # self.heightEdit.textEdited.connect(self.calculateBodySurfaceArea)

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
        self.buttonBox.setCursor(Qt.CursorShape.PointingHandCursor)
        self.patientInputLayout.addWidget(FormRow(self.errorLabel, self.buttonBox))

        self.patientBottomLayout.addWidget(self.patientInputRight, 2)
        self.setLayout(self.sideBarLayout)

    def displayParameters(self):
        # self.patientLineEdit.clear()
        # self.weightEdit.clear()
        # self.heightEdit.clear()
        self.dosageEdit.clear()
        self.ancMeasurementEdit.clear()
        self.dateEdit.setDate(QDate.currentDate())
        # self.bodySurfaceAreaMeasurement.clear()

        if self.patient is not None:
            # self.patientLineEdit.setText(self.patient.name)
            # self.weightEdit.setText(str(self.patient.weight))
            # self.heightEdit.setText(str(self.patient.height))
            self.dosageEdit.setText(str(self.patient.dosage))

            # self.calculateBodySurfaceArea()
            self.ancMeasurementDate = [datetime.strptime(str(item[1]), '%Y%m%d') for item in self.patient.ancMeasurement]
            self.ancMeasurement = [item[0] for item in self.patient.ancMeasurement]
            self.ancMeasurementEdit.setText(str(self.ancMeasurement[-1]))
            self.dateEdit.setDate(
                QDate.fromString(str(self.ancMeasurementDate[-1].date()), "yyyy-MM-dd")
            )

            pen = pg.mkPen(color="#aaaaee", width=5)
            self.graphWidgetANC.plot(
                x=[x.timestamp() for x in self.ancMeasurementDate], y=self.ancMeasurement, name="ANC Measurement", pen=pen, symbol="o", symbolSize=7, symbolBrush=("#aaaaee")
            )

    # def calculateBodySurfaceArea(self):
    #     weight = self.weightEdit.text()
    #     height = self.heightEdit.text()
    #     try:
    #         weight = float(weight)
    #         height = float(height)
    #     except:
    #         return
    #     else:
    #         bsa = math.sqrt(height * weight / 3600)
    #         self.bodySurfaceAreaMeasurement.setText("{:.2f}".format(bsa))

    def savePatientInformation(self):
        try:
            # name = self.patientLineEdit.text()
            name = self.patient.name
            assert name != ""
            date = self.dateEdit.date().toString("yyyyMMdd")
            print(name + " " + date)
            # weight = float(self.weightEdit.text())
            # height = float(self.heightEdit.text())
            weight = self.patient.weight
            print(weight)
            height = self.patient.height
            print(height)
            dosage = float(self.dosageEdit.text())
            print(dosage)
            # bsa = float(self.bodySurfaceAreaMeasurement.text())
            bsa = math.sqrt(height * weight / 3600)
            print(bsa)
            ancMeasurement = float(self.ancMeasurementEdit.text())

            print(ancMeasurement)

            conn = self.parent().parent().getDatabaseConnection()
            patient_id = self.patient.id if self.patient else -1

            # if self.patient is None:
            #     conn.execute(
            #         """
            #             INSERT INTO patients (name, weight, height, dosage, body_surface_area, oncologist_id)
            #             VALUES (?, ?, ?, ?, ?, ?)
            #         """,
            #         (
            #             name,
            #             weight,
            #             height,
            #             dosage,
            #             bsa,
            #             self.parent().parent().username,
            #         ),
            #     )

            #     res = conn.execute("SELECT last_insert_rowid()")
            #     patient_id = res.fetchone()[0]

            # else:
            #     conn.execute(
            #         """
            #             UPDATE patients 
            #             SET name=?, weight=?, height=?, dosage=?, body_surface_area=? 
            #             WHERE id=?
            #         """,
            #         (name, weight, height, dosage, bsa, self.patient.id),
            #     )

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

    def showPatientFormWindow(self):
        self.errorLabel.clear()
        self.parent().parent().showPatientFormWindow()
        self.displayParameters()

    def valueChanged(self):
        self.ancEdited = True

    def updatePatientInfo(self):
        self.errorLabel.clear()
        self.patient = self.parent().parent().selected_patient
        self.displayParameters()
        self.patientCard.getPatientInfo(self.patient)

