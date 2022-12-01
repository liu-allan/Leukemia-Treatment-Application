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
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

logging.getLogger().setLevel(logging.INFO)


class PatientListItem(QWidget):
    def __init__(self, patient_name):
        super(PatientListItem, self).__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(
            "background-color: #ccccff; border-radius: 5px; padding: 10px"
        )

        self.patient_name = patient_name
        self.label = QLabel(self.patient_name)
        self.label.setFont(QFont("Avenir", 12))
        self.select_button = QPushButton("Select")
        self.select_button.setFont(QFont("Avenir", 12))
        self.select_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.select_button.setStyleSheet(
            "background-color: #aaaaee; border-radius: 5px; padding: 10px"
        )
        self.middle_spacer = QSpacerItem(
            1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

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
        self.parent().parent().parent().parent().showPatientInformationWindow()


class PatientListWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.patients = [
            "Bill Anderson",
            "Mario Luigi",
            "Jack Lantern",
            "Frodo Baggins",
            "Samwise Gamgee",
            "Harry Potter",
            "Patient Zero",
            "Giant Gnome",
            "Patient One",
            "Patient Two",
            "Gandalf Grey",
            "Bilbo Baggins",
            "Sting Ray",
            "Captain America",
            "Rice Cake",
            "Robert Smith",
            "Rick Smith",
            "Adam Smith",
            "Sophie Smith",
            "Emily Smith",
            "Zoe Smith",
            "Kat Smith",
            "Teresa Smith",
            "Mike Smith"
        ]

        self.patients.sort()
        self.patient_widgets = []

        self.main_box_layout = QVBoxLayout()
        self.search_bar_layout = QHBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search patients")
        self.search_bar.textChanged.connect(self.filterSearchItems)
        self.search_bar_layout.addWidget(self.search_bar)

        search_bar_spacer = QWidget()
        search_bar_spacer.setFixedWidth(20)
        self.search_bar_layout.addWidget(search_bar_spacer)

        self.new_patient_button = QPushButton("Add Patient")
        self.new_patient_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.new_patient_button.clicked.connect(self.showPatientInformationWindow)
        self.search_bar_layout.addWidget(self.new_patient_button)

        self.list = QWidget()
        self.list_layout = QVBoxLayout()

        for patient in self.patients:
            widget = PatientListItem(patient)
            self.patient_widgets.append(widget)
            self.list_layout.addWidget(widget)

        bottom_spacer = QSpacerItem(
            1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.list_layout.addItem(bottom_spacer)

        self.list.setLayout(self.list_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setWidget(self.list)
        self.scroll_area.setWidgetResizable(True)

        self.main_box_layout.addLayout(self.search_bar_layout)
        self.main_box_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_box_layout)

    def filterSearchItems(self, input):
        for widget in self.patient_widgets:
            if input.lower() in widget.patient_name.lower():
                widget.show()
            else:
                widget.hide()

    def showPatientInformationWindow(self):
        self.parent().parent().showPatientInformationWindow()
