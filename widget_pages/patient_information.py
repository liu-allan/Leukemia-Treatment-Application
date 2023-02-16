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
    QPushButton,
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
        self.sideBar.setObjectName("SideBar")
        self.sideBar.setContentsMargins(0, 0, 0, 0)
        self.sideBar.setStyleSheet(
            """
            QWidget#SideBar{
                background-color: #bfd8d2;
                height: auto;
                border-radius: 20px;
            }
            """
        )
        self.sideBarLayout.addWidget(self.sideBar, 1)

        self.menuLayout = QVBoxLayout(self.sideBar)

        self.spacer = QSpacerItem(
            1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.menuLayout.addSpacerItem(self.spacer)
        self.backButton = QPushButton("Patient List")
        self.backButton.setContentsMargins(0, 0, 0, 0)
        self.backButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.backButton.setFont(QFont("Avenir", 18))
        self.backButton.setStyleSheet("background-color: #bfd8d2; border-radius: 20px")
        self.menuLayout.addWidget(self.backButton, alignment=Qt.AlignmentFlag.AlignCenter)

        self.patientInformationButton = QPushButton("Patient Information")
        self.patientInformationButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.patientInformationButton.setContentsMargins(0, 0, 0, 0)
        self.patientInformationButton.setFont(QFont("Avenir", 18))
        self.patientInformationButton.setStyleSheet("background-color: #bfd8d2; border-radius: 20px")
        self.menuLayout.addWidget(self.patientInformationButton, alignment=Qt.AlignmentFlag.AlignCenter)

        self.dashboardButton = QPushButton("Dashboard")
        self.dashboardButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.dashboardButton.setContentsMargins(0, 0, 0, 0)
        self.dashboardButton.setFont(QFont("Avenir", 18))
        self.dashboardButton.setStyleSheet("background-color: #bfd8d2; border-radius: 20px")
        self.menuLayout.addWidget(self.dashboardButton, alignment=Qt.AlignmentFlag.AlignCenter)
        self.menuLayout.addSpacerItem(self.spacer)

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
        
        # Add grid
        self.graphWidgetANC.showGrid(x=True, y=True)

        date_axis2 = pg.DateAxisItem(orientation='bottom')
        self.graphWidgetDosages = pg.PlotWidget(axisItems = {'bottom': date_axis2})
        self.graphLayout.addWidget(self.graphWidgetDosages, 7)

        self.graphWidgetDosages.setCursor(Qt.CursorShape.OpenHandCursor)
        # Temp data -> will connect to matlab in the future
        self.dosagePrescribedDate = []
        self.dosageAmount = []

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
        
        # Add grid
        self.graphWidgetDosages.showGrid(x=True, y=True)

        self.patientBottomLayout.addWidget(self.patientHistoricGraphs, 3)

        self.patientInputRight = QWidget()
        self.patientInputRight.setObjectName("PatientInputRight")
        self.patientInputRight.setContentsMargins(30, 0, 30, 0)
        self.patientInputRight.setStyleSheet(
            """
            QWidget#PatientInputRight
            {
                background-color: #ffffff;
                border-radius: 20px;
            }
            """
        )
        self.patientBottomLayout.addWidget(self.patientInputRight, 1)

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

        self.ancCountLabel = Label("ANC Measurement (g/L)")
        self.ancCountLabel.setContentsMargins(30, 0, 0, 0)
        self.ancMeasurementEdit = LineEdit("g/L")
        self.ancMeasurementEdit.setContentsMargins(0, 0, 30, 0)
        self.ancMeasurementEdit.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.ancMeasurementEdit.setStyleSheet(
            "background-color: #f5f5f5; height: 40px; border-radius: 20px; padding-left: 10px"
        )
        self.patientInputLayout.addWidget(FormRow(self.ancCountLabel, self.ancMeasurementEdit))

        self.dateLabel = Label("Date of ANC Measurement")
        self.dateLabel.setContentsMargins(30, 0, 0, 0)
        self.dateEdit = QDateEdit()
        self.dateEdit.setContentsMargins(0, 0, 30, 0)
        self.dateEdit.setFont(QFont("Avenir", 18))
        self.dateEdit.setFixedWidth(200)
        # self.dateEdit.setStyleSheet("""
        #         QDateEdit {
        #             border-radius: 20px;
        #             padding-left: 10px;
        #             background-color: #f5f5f5;
        #             height: 40px;
        #         }
        #         QDateEdit::down-arrow {
        #             border-image: url(down.png);
        #             border-radius: 20px;
        #             width: 20px;
        #             height: 20px;
        #         }
        #         QDateEdit::up-arrow {
        #             border-image: url(arrowhead-up.png);
        #             border-radius: 20px;
        #             width: 20px;
        #             height: 20px;
        #         }     
        # """)
  
        self.patientInputLayout.addWidget(FormRow(self.dateLabel, self.dateEdit))

        self.errorLabel = Label("")
        self.patient = None
        self.dosageEdit.setValidator(QDoubleValidator())
        self.ancMeasurementEdit.setValidator(QDoubleValidator())
        self.ancEdited = False
        self.dosageEdited = False

        self.ancMeasurementEdit.textEdited.connect(self.valueChanged)
        self.dateEdit.editingFinished.connect(self.valueChanged)
        self.dosageEdit.textEdited.connect(self.valueChangedDosage)

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(self.buttonBox.standardButtons().Cancel)
        self.buttonBox.addButton(self.buttonBox.standardButtons().Save)
        self.buttonBox.addButton(self.buttonBox.standardButtons().Ok)
        self.buttonBox.setFont(QFont("Avenir", 12))
        self.buttonBox.setFixedWidth(250)
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
        self.buttonBox.setContentsMargins(0, 0, 30, 0)
        self.patientInputLayout.addWidget(FormRow(self.errorLabel, self.buttonBox))

        self.patientBottomLayout.addWidget(self.patientInputRight, 2)
        self.setLayout(self.sideBarLayout)

    def displayParameters(self):
        self.dosageEdit.clear()
        self.ancMeasurementEdit.clear()
        self.dateEdit.setDate(QDate.currentDate())
        self.ancMeasurementDate.clear()
        self.ancMeasurement.clear()
        self.dosagePrescribedDate.clear()
        self.dosageAmount.clear()

        if self.patient is not None:
            self.ancMeasurementDate = [datetime.strptime(str(item[1]), '%Y%m%d') for item in self.patient.ancMeasurement]
            self.ancMeasurement = [item[0] for item in self.patient.ancMeasurement]
            self.ancMeasurementEdit.setText(str(self.ancMeasurement[-1]))
            self.dateEdit.setDate(
                QDate.fromString(str(self.ancMeasurementDate[-1].date()), "yyyy-MM-dd")
            )

            # Add legend
            self.ancLegend = self.graphWidgetANC.addLegend()
            if len(self.ancMeasurement) == 1:
                pen = None
                self.ancLine = self.graphWidgetANC.plot(
                    x=[self.ancMeasurementDate[0].timestamp(), self.ancMeasurementDate[0].timestamp() + 2628288 * 6], y=[self.ancMeasurement[0], self.ancMeasurement[0] + 1], name="ANC Measurement", pen=pen, symbol="o", symbolSize=7, symbolBrush=("#aaaaee")
                )
                self.graphWidgetANC.clear()
                self.ancLine = self.graphWidgetANC.plot(
                    x=[self.ancMeasurementDate[0].timestamp()], y=[self.ancMeasurement[0]], name="ANC Measurement", pen=pen, symbol="o", symbolSize=7, symbolBrush=("#aaaaee")
                )
            else:
                pen = pg.mkPen(color="#aaaaee", width=5) 
                self.ancLine = self.graphWidgetANC.plot(
                    x=[x.timestamp() for x in self.ancMeasurementDate], y=self.ancMeasurement, name="ANC Measurement", pen=pen, symbol="o", symbolSize=7, symbolBrush=("#aaaaee")
                )

            self.dosagePrescribedDate = [datetime.strptime(str(item[1]), '%Y%m%d') for item in self.patient.dosageMeasurement]
            self.dosageAmount = [item[0] for item in self.patient.dosageMeasurement]
            self.dosageEdit.setText(str(self.dosageAmount[-1]))

            # Add legend
            self.dosageLegend = self.graphWidgetDosages.addLegend()
            if len(self.ancMeasurement) == 1:
                pen = None
                self.dosageLine = self.graphWidgetDosages.plot(
                    x=[self.dosagePrescribedDate[0].timestamp(), self.dosagePrescribedDate[0].timestamp() + 2628288 * 6], y=[self.dosageAmount[0], self.dosageAmount[0] + 1], name="Dosage Amount Prescribed", pen=pen, symbol="o", symbolSize=7, symbolBrush=("#aaaaee")
                )
                self.graphWidgetDosages.clear()
                self.dosageLine = self.graphWidgetDosages.plot(
                    x=[x.timestamp() for x in self.dosagePrescribedDate], y=self.dosageAmount, name="Dosage Amount Prescribed", pen=pen, symbol="o", symbolSize=7, symbolBrush=("#aaaaee")
                )
            else:
                pen = pg.mkPen(color="#aaaaee", width=5)
                self.dosageLine = self.graphWidgetDosages.plot(
                    x=[x.timestamp() for x in self.dosagePrescribedDate], y=self.dosageAmount, name="Dosage Amount Prescribed", pen=pen, symbol="o", symbolSize=7, symbolBrush=("#aaaaee")
                )

    def savePatientInformation(self):
        try:
            name = self.patient.name
            assert name != ""
            date = self.dateEdit.date().toString("yyyyMMdd")
            print(name + " " + date)
            weight = self.patient.weight
            height = self.patient.height
            bsa = math.sqrt(height * weight / 3600)
            print(bsa)
            allType = self.patient.allType
            age = self.patient.age
            bloodType = self.patient.bloodType
            birthday = self.patient.birthday
            phoneNumber = self.patient.phoneNumber
            assignedDoctor = self.patient.assignedDoctor
            ancMeasurement = float(self.ancMeasurementEdit.text())
            dosageMeasurement = float(self.dosageEdit.text())
            print(ancMeasurement)
            print(dosageMeasurement)

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

    def showPatientListWindow(self):
        self.graphWidgetANC.clear()
        self.graphWidgetDosages.clear()
        self.errorLabel.clear()
        self.parent().parent().showPatientListWindow()

    def showDashboardWindow(self):
        try:
            name = self.patient.name
            assert name != ""
            date = self.dateEdit.date().toString("yyyyMMdd")
            weight = self.patient.weight
            height = self.patient.height
            bsa = math.sqrt(height * weight / 3600)
            allType = self.patient.allType
            age = self.patient.age
            bloodType = self.patient.bloodType
            birthday = self.patient.birthday
            phoneNumber = self.patient.phoneNumber
            assignedDoctor = self.patient.assignedDoctor
            ancMeasurement = float(self.ancMeasurementEdit.text())
            dosageMeasurement = float(self.dosageEdit.text())

        except:
            msg = "Input fields must not be empty"
            self.errorLabel.setText(msg)
            self.errorLabel.setStyleSheet("color:red")
            logging.error(msg)
        else:
            self.errorLabel.clear()
            self.parent().parent().showDashboardWindow()

    def showPatientFormWindow(self):
        self.errorLabel.clear()
        self.parent().parent().showPatientFormWindow()

    def valueChanged(self):
        self.ancEdited = True

    def valueChangedDosage(self):
        self.dosageEdited = True

    def updatePatientInfo(self):
        self.errorLabel.clear()
        self.patient = self.parent().parent().selected_patient
        self.displayParameters()
        self.patientCard.getPatientInfo(self.patient)

