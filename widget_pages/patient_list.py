import sys
import logging
from PyQt6.QtWidgets import (
    QLabel, 
    QPushButton, 
    QVBoxLayout, 
    QHBoxLayout, 
    QWidget, 
    QSpacerItem, 
    QSizePolicy, 
    QScrollArea,
    QLineEdit,
    QFrame
)
from PyQt6.QtCore import Qt
from PyQt6 import uic

logging.getLogger().setLevel(logging.INFO)


class PatientListItem(QWidget):
    def __init__(self, patient_name):
        super(PatientListItem, self).__init__()

        self.patient_name = patient_name
        self.label = QLabel(self.patient_name)
        self.select_button = QPushButton("Patient Information")
        self.middle_spacer = QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addItem(self.middle_spacer)
        self.layout.addWidget(self.select_button)

        self.setLayout(self.layout)

        self.select_button.clicked.connect(self.showPatientInfo)
    
    def show(self):
        for item in [self, self.label, self.select_button]:
            item.setVisible(True)

    def hide(self):
        for item in [self, self.label, self.select_button]:
            item.setVisible(False)
    
    def showPatientInfo(self):
        # lol
        self.parent().parent().parent().parent().showPatientInformationWindow()

class PatientListWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # uic.loadUi("ui/patientlist.ui", self)

        self.patients = [
            "Bill Anderson",
            "Big Wu",
            "Bigger Wu",
            "Jack Ma",
            "Jacked Ma",
            "Ripped Ma",
            "Frodo Baggins",
            "Allan Liu"
        ]

        self.patients.sort()
        self.patient_widgets = []

        self.main_box_layout = QVBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search patients")
        self.search_bar.textChanged.connect(self.filterSearchItems)

        self.list = QWidget()
        self.list_layout = QVBoxLayout()

        for patient in self.patients:
            widget = PatientListItem(patient)
            self.patient_widgets.append(widget)
            self.list_layout.addWidget(widget)
        
        bottom_spacer = QSpacerItem(1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.list_layout.addItem(bottom_spacer)

        self.list.setLayout(self.list_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(self.list)
        self.scroll_area.setWidgetResizable(True)

        self.main_box_layout.addWidget(self.search_bar)
        self.main_box_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_box_layout)

        # layout = QVBoxLayout()
        # button = QPushButton("Show Patient Information")
        # button.clicked.connect(self.showPatientInformationWindow)

        # layout.addWidget(QLabel("Patient List Window"))
        # layout.addWidget(button)

        # self.setLayout(layout)
    def filterSearchItems(self, input):
        for widget in self.patient_widgets:
            if input.lower() in widget.patient_name.lower():
                widget.show()
            else:
                widget.hide()

    def showPatientInformationWindow(self):
        self.parent().parent().showPatientInformationWindow()
