import logging
import sqlite3
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
    def __init__(self, patient_name, patient_id, user_id):
        super(PatientListItem, self).__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(
            "background-color: #ccccff; border-radius: 5px; padding: 10px"
        )

        self.patient_name = patient_name
        self.patient_id = patient_id
        self.user_id = user_id
        self.label = QLabel(self.patient_name)
        self.label.setFont(QFont("Avenir", 12))
        self.user_id_label = QLabel(self.user_id)
        self.user_id_label.setFont(QFont("Avenir", 10))
        self.select_button = QPushButton("Select")
        self.select_button.setFont(QFont("Avenir", 12))
        self.select_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.select_button.setStyleSheet(
            "background-color: #aaaaee; border-radius: 5px; padding: 10px"
        )
        self.delete_button = QPushButton("Delete")
        self.delete_button.setFont(QFont("Avenir", 12))
        self.delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_button.setStyleSheet(
            "background-color: #e3735e; border-radius: 5px; padding: 10px"
        )
        self.middle_spacer = QSpacerItem(
            1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addItem(self.middle_spacer)
        self.layout.addWidget(self.user_id_label)
        self.layout.addWidget(self.select_button)
        self.layout.addWidget(self.delete_button)

        self.setLayout(self.layout)

        self.select_button.clicked.connect(self.showPatientInfo)
        self.delete_button.clicked.connect(self.deletePatient)

    def show(self):
        for item in [self, self.label, self.select_button]:
            item.setVisible(True)

    def hide(self):
        for item in [self, self.label, self.select_button]:
            item.setVisible(False)

    def showPatientInfo(self):
        self.parent().parent().parent().parent().showPatientInformationWindow(
            self.patient_id
        )

    def deletePatient(self):
        conn = self.parent().parent().parent().parent().getDatabaseConnection()

        try:
            conn.execute(
                "PRAGMA foreign_keys = ON"
            )  # enable foreign key cascade on delete for the measurements table
            
            conn.execute(
                """
                DELETE FROM patients 
                WHERE id=? 
                """,
                (self.patient_id,),
            )
            conn.commit()

        except sqlite3.Error as er:
            logging.error("Something went wrong while deleting the patient", er)

        self.parent().parent().parent().parent().updatePatientList()


class PatientListWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.patients = []
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
        self.new_patient_button.clicked.connect(self.showPatientFormWindow)
        self.search_bar_layout.addWidget(self.new_patient_button)

        self.scroll_area = QScrollArea()
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.main_box_layout.addLayout(self.search_bar_layout)
        self.main_box_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_box_layout)

    def filterSearchItems(self, input):
        for widget in self.patient_widgets:
            if input.lower() in widget.patient_name.lower():
                widget.show()
            else:
                widget.hide()

    def showPatientFormWindow(self):
        # whenever you press "Add Patient", should clear state so the fields aren't pre-populated
        self.parent().parent().selected_patient = None
        self.parent().parent().showPatientFormWindow()

    def showPatientInformationWindow(self, patient_id=-1):
        self.parent().parent().updateSelectedPatient(patient_id)
        self.parent().parent().showPatientInformationWindow()

    def getDatabaseConnection(self):
        return self.parent().parent().getDatabaseConnection()

    def displayPatientList(self):
        self.list = QWidget()
        self.list_layout = QVBoxLayout()

        for patient_name, patient_id, user_id in self.patients:
            widget = PatientListItem(patient_name, patient_id, user_id)
            self.patient_widgets.append(widget)
            self.list_layout.addWidget(widget)

        bottom_spacer = QSpacerItem(
            1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.list_layout.addItem(bottom_spacer)

        self.list.setLayout(self.list_layout)
        self.scroll_area.setWidget(self.list)
        self.scroll_area.setWidgetResizable(True)

    def updatePatientList(self):
        conn = self.getDatabaseConnection()
        username = self.parent().parent().username
        res = conn.execute(
            """SELECT name, id, user_id 
               FROM patients p 
               INNER JOIN oncologists o ON p.oncologist_id=o.username
                    AND o.username=?
            """,
            (username,),
        )

        rows = res.fetchall()
        self.patients.clear()
        self.patient_widgets.clear()
        if rows:
            self.patients = rows
        self.displayPatientList()
