import logging
import math
import sqlite3
import numpy as np

from PyQt6 import uic
from PyQt6.QtCore import QDate, Qt, QSize
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QDateEdit,
    QDialogButtonBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QMessageBox,
)
from PyQt6.QtGui import QDoubleValidator, QIntValidator, QFont, QIcon
from widget_pages.patient_card import PatientCard
from pyqtgraph import plot
import pyqtgraph as pg
from datetime import datetime
from widget_pages.sidebar import SideBar

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

        self.sideBar = SideBar("Patient Information")
        self.sideBarLayout.addWidget(self.sideBar, 1)

        self.patientInfo = QWidget()
        self.patientInfo.setContentsMargins(0, 0, 0, 0)
        self.sideBarLayout.addWidget(self.patientInfo, 19)

        self.layout = QVBoxLayout(self.patientInfo)
        self.layout.setContentsMargins(10, 0, 0, 0)

        self.patientCard = PatientCard()
        self.layout.addWidget(self.patientCard, 1)

        self.patientInput = QWidget()
        self.patientInput.setContentsMargins(0, 10, 0, 0)
        self.layout.addWidget(self.patientInput, 3)

        self.patientBottomLayout = QGridLayout(self.patientInput)
        self.patientBottomLayout.setContentsMargins(0, 0, 0, 0)
        self.patientBottomLayout.setRowStretch(0, 4)
        self.patientBottomLayout.setRowStretch(1, 1)

        # HISTORIC GRAPHS
        self.patientHistoricGraphs = QWidget()
        self.patientHistoricGraphs.setContentsMargins(0, 0, 0, 0)
        self.patientHistoricGraphs.setStyleSheet(
            "background-color: #aaaaee; border-radius: 20px;"
        )

        self.graphLayout = QVBoxLayout(self.patientHistoricGraphs)

        self.graphLabel = LabelBolded("Patient Historic Data", 20, [0, 0, 0, 10])
        self.graphLayout.addWidget(self.graphLabel, 1)

        date_axis = pg.DateAxisItem(orientation="bottom")
        self.graphWidgetANC = pg.PlotWidget(axisItems={"bottom": date_axis})

        self.graphLayout.addWidget(self.graphWidgetANC, 7)

        self.graphWidgetANC.setCursor(Qt.CursorShape.OpenHandCursor)
        # Temp data -> will connect to matlab in the future
        self.ancMeasurementDate = []
        self.ancMeasurement = []
        # Add Background colour to white
        self.graphWidgetANC.setBackground("w")
        # Add Title
        self.graphWidgetANC.setTitle(
            "Historic ANC Measurement", color="#000", font=QFont("Avenir", 15)
        )
        # Add Axis Labels
        styles = {"color": "#000000", "font": QFont("Avenir", 15)}
        self.graphWidgetANC.setLabel(
            "left", "ANC Measurement (# Cells/L) x 1e9", **styles
        )
        self.graphWidgetANC.setLabel("bottom", "ANC Measurement Date", **styles)

        # Add grid
        self.graphWidgetANC.showGrid(x=True, y=True)

        date_axis2 = pg.DateAxisItem(orientation="bottom")
        self.graphWidgetDosages = pg.PlotWidget(axisItems={"bottom": date_axis2})
        self.graphLayout.addWidget(self.graphWidgetDosages, 7)

        self.graphWidgetDosages.setCursor(Qt.CursorShape.OpenHandCursor)
        # Temp data -> will connect to matlab in the future
        self.dosagePrescribedDate = []
        self.dosageAmount = []

        # Add Background colour to white
        self.graphWidgetDosages.setBackground("w")
        # Add Title
        self.graphWidgetDosages.setTitle(
            "Historic Dosage Amount Prescribed", color="#000", font=QFont("Avenir", 15)
        )
        # Add Axis Labels
        styles = {"color": "#000000", "font": QFont("Avenir", 15)}
        self.graphWidgetDosages.setLabel("left", "Dosage Amount Prescribed", **styles)
        self.graphWidgetDosages.setLabel("bottom", "Dosage Prescription Date", **styles)

        # Add grid
        self.graphWidgetDosages.showGrid(x=True, y=True)

        self.patientBottomLayout.addWidget(self.patientHistoricGraphs, 0, 0, 2, 1)

        # Add legends
        self.ancLegend = self.graphWidgetANC.addLegend()
        self.dosageLegend = self.graphWidgetDosages.addLegend()

        self.patientInputRight = QWidget()
        self.patientInputRight.setObjectName("PatientInputRight")
        self.patientInputRight.setContentsMargins(30, 20, 30, 0)
        self.patientInputRight.setStyleSheet(
            """
            QWidget#PatientInputRight
            {
                background-color: #ffffff;
                border-radius: 20px;
            }
            """
        )

        self.patientInputLayout = QVBoxLayout(self.patientInputRight)
        self.patientInputLayout.setContentsMargins(0, 0, 0, 0)

        self.dosageLabel = Label("6-MP Dosage (mg)")
        self.dosageLabel.setContentsMargins(30, 0, 0, 0)
        self.dosageEdit = LineEdit("mg")
        self.dosageEdit.setContentsMargins(0, 0, 30, 0)
        self.dosageEdit.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.dosageEdit.setStyleSheet(
            "background-color: #f5f5f5; height: 40px; border-radius: 20px; padding-left: 10px"
        )
        self.patientInputLayout.addWidget(FormRow(self.dosageLabel, self.dosageEdit))

        self.ancCountLabel = Label("ANC Measurement (# Cells/L) x 1e9")
        self.ancCountLabel.setContentsMargins(30, 0, 0, 0)
        self.ancMeasurementEdit = LineEdit("# Cells/L x 1e9")
        self.ancMeasurementEdit.setContentsMargins(0, 0, 30, 0)
        self.ancMeasurementEdit.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.ancMeasurementEdit.setStyleSheet(
            "background-color: #f5f5f5; height: 40px; border-radius: 20px; padding-left: 10px"
        )
        self.patientInputLayout.addWidget(
            FormRow(self.ancCountLabel, self.ancMeasurementEdit)
        )

        self.dateLabel = Label("Date of ANC Measurement")
        self.dateLabel.setContentsMargins(30, 0, 0, 0)
        self.dateEdit = QDateEdit()
        self.dateEdit.setContentsMargins(0, 0, 30, 0)
        self.dateEdit.setFont(QFont("Avenir", 18))
        self.dateEdit.setFixedWidth(200)

        self.patientInputLayout.addWidget(FormRow(self.dateLabel, self.dateEdit))

        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.setContentsMargins(50, 0, 50, 20)

        self.errorLabel = Label("")
        self.errorLabel.setContentsMargins(0, 0, 0, 0)
        self.bottomLayout.addWidget(
            self.errorLabel, 9, alignment=Qt.AlignmentFlag.AlignLeft
        )

        self.patient = None
        self.dosageEdit.setValidator(QDoubleValidator())
        self.ancMeasurementEdit.setValidator(QDoubleValidator())
        self.ancEdited = False
        self.dosageEdited = False

        self.ancMeasurementEdit.textEdited.connect(self.valueChanged)
        self.dateEdit.editingFinished.connect(self.valueChanged)
        self.dosageEdit.textEdited.connect(self.valueChangedDosage)

        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.savePatientInformation)
        self.saveButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.saveButton.setMinimumWidth(70)
        self.saveButton.setMinimumHeight(40)
        self.saveButton.setMaximumHeight(50)
        self.saveButton.setFont(QFont("Avenir", 18))
        self.saveButton.setStyleSheet(
            "background-color: #aaaaee; border-radius: 10px; padding: 10px"
        )
        self.bottomLayout.addWidget(
            self.saveButton, 1, alignment=Qt.AlignmentFlag.AlignRight
        )
        self.patientInputLayout.addLayout(self.bottomLayout)

        self.patientBottomLayout.addWidget(self.patientInputRight, 0, 1, 1, 1)

        # create modelInput panel in bottom right
        self.modelInput = QWidget()
        self.modelInput.setObjectName("modelInput")
        self.modelInput.setContentsMargins(30, 0, 30, 0)
        self.modelInput.setStyleSheet(
            """
            QWidget#modelInput
            {
                background-color: #ffffff;
                border-radius: 20px;
            }
            """
        )

        self.modelInputLayout = QHBoxLayout(self.modelInput)
        self.modelInputLayout.setContentsMargins(0, 0, 0, 0)

        self.numCyclesEdit = LineEdit("# calculation cycles")
        self.numCyclesEdit.setContentsMargins(30, 0, 30, 0)
        self.numCyclesEdit.setFixedWidth(500)
        self.numCyclesEdit.setStyleSheet(
            "background-color: #f5f5f5; height: 40px; border-radius: 20px; padding-left: 10px"
        )
        self.numCyclesEdit.setValidator(QIntValidator())
        self.numCyclesEdit.textChanged.connect(self.toggleCalculateButton)

        self.calculateButton = QPushButton("Calculate")
        self.calculateButton.setFont(QFont("Avenir", 15))
        self.calculateButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.calculateButton.setStyleSheet(
            "background-color: #aaaaee; border-radius: 5px; padding: 10px"
        )
        self.calculateButton.setEnabled(False)

        self.calculateButton.clicked.connect(
            lambda: self.showDashboardWindow(do_calculation=True)
        )

        self.modelInputLayout.addWidget(self.numCyclesEdit)
        self.modelInputLayout.addWidget(self.calculateButton)

        self.patientBottomLayout.addWidget(self.modelInput, 1, 1, 1, 1)

        self.setLayout(self.sideBarLayout)

    def toggleCalculateButton(self, input):
        if input and int(input) > 0 and int(input) < 100:
            self.calculateButton.setEnabled(True)
        else:
            self.calculateButton.setEnabled(False)

    def backButtonClicked(self):
        self.showPatientListWindow()

    def patientInformationButtonClicked(self):
        return

    def dashboardButtonClicked(self):
        self.showDashboardWindow(do_calculation=False)

    def updateUsername(self, username):
        self.parent().parent().updateUsername(username)

    def showLoginWindow(self):
        self.parent().parent().showLoginWindow()

    def displayParameters(self):
        self.dateEdit.setDate(QDate.currentDate())
        self.dosageEdit.clear()
        self.ancMeasurementEdit.clear()
        self.ancMeasurementDate.clear()
        self.ancMeasurement.clear()
        self.dosagePrescribedDate.clear()
        self.dosageAmount.clear()
        self.dosageLegend.clear()
        self.ancLegend.clear()

        if self.patient is not None:
            self.ancMeasurementDate = [
                datetime.strptime(str(item[1]), "%Y%m%d")
                for item in self.patient.ancMeasurement
            ]
            self.ancMeasurement = [item[0] for item in self.patient.ancMeasurement]

            # Add legend
            if len(self.ancMeasurement) == 1:
                pen = None
                self.ancLine = self.graphWidgetANC.plot(
                    x=[
                        self.ancMeasurementDate[0].timestamp(),
                        self.ancMeasurementDate[0].timestamp() + 2628288 * 6,
                    ],
                    y=[self.ancMeasurement[0], self.ancMeasurement[0] + 1],
                    name="ANC Measurement",
                    pen=pen,
                    symbol="o",
                    symbolSize=7,
                    symbolBrush=("#aaaaee"),
                )
                self.graphWidgetANC.clear()
                self.ancLine = self.graphWidgetANC.plot(
                    x=[self.ancMeasurementDate[0].timestamp()],
                    y=[self.ancMeasurement[0]],
                    name="ANC Measurement",
                    pen=pen,
                    symbol="o",
                    symbolSize=7,
                    symbolBrush=("#aaaaee"),
                )
            else:
                pen = pg.mkPen(color="#aaaaee", width=5)
                self.ancLine = self.graphWidgetANC.plot(
                    x=[x.timestamp() for x in self.ancMeasurementDate],
                    y=self.ancMeasurement,
                    name="ANC Measurement",
                    pen=pen,
                    symbol="o",
                    symbolSize=7,
                    symbolBrush=("#aaaaee"),
                )

            self.dosagePrescribedDate = [
                datetime.strptime(str(item[1]), "%Y%m%d")
                for item in self.patient.dosageMeasurement
            ]
            self.dosageAmount = [item[0] for item in self.patient.dosageMeasurement]

            # Add legend
            if len(self.ancMeasurement) == 1:
                pen = None
                self.dosageLine = self.graphWidgetDosages.plot(
                    x=[
                        self.dosagePrescribedDate[0].timestamp(),
                        self.dosagePrescribedDate[0].timestamp() + 2628288 * 6,
                    ],
                    y=[self.dosageAmount[0], self.dosageAmount[0] + 1],
                    name="Dosage Amount Prescribed",
                    pen=pen,
                    symbol="o",
                    symbolSize=7,
                    symbolBrush=("#aaaaee"),
                )
                self.graphWidgetDosages.clear()
                self.dosageLine = self.graphWidgetDosages.plot(
                    x=[x.timestamp() for x in self.dosagePrescribedDate],
                    y=self.dosageAmount,
                    name="Dosage Amount Prescribed",
                    pen=pen,
                    symbol="o",
                    symbolSize=7,
                    symbolBrush=("#aaaaee"),
                )
            else:
                pen = pg.mkPen(color="#aaaaee", width=5)
                self.dosageLine = self.graphWidgetDosages.plot(
                    x=[x.timestamp() for x in self.dosagePrescribedDate],
                    y=self.dosageAmount,
                    name="Dosage Amount Prescribed",
                    pen=pen,
                    symbol="o",
                    symbolSize=7,
                    symbolBrush=("#aaaaee"),
                )

    def savePatientInformation(self):
        try:
            name = self.patient.name
            assert name != ""
            date = self.dateEdit.date().toString("yyyyMMdd")
            ancMeasurement = float(self.ancMeasurementEdit.text())
            dosageMeasurement = float(self.dosageEdit.text())

            conn = self.parent().parent().getDatabaseConnection()
            patient_id = self.patient.id if self.patient else -1

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
            self.displayParameters()

        except sqlite3.Error as er:
            msg = "Existing entry in the database. Please check your inputs."
            self.errorLabel.setText(msg)
            self.errorLabel.setWordWrap(True)
            self.errorLabel.setStyleSheet("color:red")
            logging.error(er)

        except Exception as e:
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

    def showPatientListWindow(self):
        self.numCyclesEdit.clear()
        self.errorLabel.clear()
        self.parent().parent().showPatientListWindow()

    def showDashboardWindow(self, do_calculation):
        if do_calculation:
            try:
                name = self.patient.name
                assert name != ""
                numCalculationCycles = int(self.numCyclesEdit.text())
            except Exception as e:
                msg = "Input fields must not be empty"
                self.errorLabel.setText(msg)
                self.errorLabel.setStyleSheet("color:red")
                logging.error(e)
            else:
                self.errorLabel.clear()
                self.parent().parent().showDashboardWindow(
                    calculation_info=(True, numCalculationCycles)
                )
        else:
            self.errorLabel.clear()
            self.parent().parent().showDashboardWindow(calculation_info=(False, 0))

    def showPatientFormWindow(self):
        self.errorLabel.clear()
        self.parent().parent().showPatientFormWindow()

    def valueChanged(self):
        self.ancEdited = True

    def valueChangedDosage(self):
        self.dosageEdited = True

    def updatePatientInfo(self):
        self.graphWidgetANC.clear()
        self.graphWidgetDosages.clear()
        self.errorLabel.clear()
        self.patient = self.parent().parent().selected_patient
        self.displayParameters()
        self.patientCard.getPatientInfo(self.patient)
