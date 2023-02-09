import logging
import sqlite3
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QWidget,
    QSpacerItem,
    QSizePolicy,
    QScrollArea,
    QLineEdit,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QPixmap

from datetime import datetime

logging.getLogger().setLevel(logging.INFO)


class PatientListItem(QPushButton):
    def __init__(self, patient_name, patient_id, user_id, birthday):
        super(PatientListItem, self).__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("PatientListItem")
        self.setStyleSheet(
            """
            QPushButton#PatientListItem
            {
                min-height: 40px;
                background-color: #ccccff;
                border: 1px solid #aaaaaa;
                border-radius: 5px;
                padding: 10px
            }

            QPushButton#PatientListItem:hover
            {
                background-color: #b6b6fa;
            }
            """
        )
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self.showPatientInfo)

        self.patient_name = patient_name
        self.patient_id = patient_id
        self.user_id = user_id
        self.birthday = birthday

        self.name_label = QLabel(self.patient_name)
        self.name_label.setFont(QFont("Avenir", 13))
        self.name_label.setFixedWidth(300)

        self.user_id_label = QLabel("Patient ID: " + self.user_id)
        self.user_id_label.setFont(QFont("Avenir", 10, italic=True))
        self.user_id_label.setFixedWidth(300)
        self.user_id_label.setStyleSheet("color: #505050;")

        self.birthday_label = QLabel("DOB: " + datetime.strptime(self.birthday, '%Y%m%d').strftime('%Y-%m-%d'))
        self.birthday_label.setFont(QFont("Avenir", 10))
        self.birthday_label.setFixedWidth(200)
        self.birthday_label.setStyleSheet("color: #505050;")

        self.delete_button = QPushButton("Delete")
        self.delete_button.setFont(QFont("Avenir", 12))
        self.delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_button.setStyleSheet(
            """
            QPushButton
            {
                background-color: #e35e5e;
                border-radius: 5px;
                padding: 10px
            }

            QPushButton:hover
            {
                background-color: #de3333;
            }
            """
        )
        name_spacer = QSpacerItem(
            20, 1, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum
        )
        main_spacer = QSpacerItem(
            1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.layout = QGridLayout()
        self.layout.addWidget(self.name_label, 0, 0, 1, 1)
        self.layout.addWidget(self.user_id_label, 1, 0, 1, 1)
        self.layout.addItem(name_spacer, 0, 1, 2, 1)
        self.layout.addWidget(self.birthday_label, 0, 2, 2, 1)
        self.layout.addItem(main_spacer, 0, 3, 2, 1)
        self.layout.addWidget(self.delete_button, 0, 4, 2, 1)

        self.setLayout(self.layout)

        self.delete_button.clicked.connect(self.deletePatient)

    def show(self):
        self.setVisible(True)

    def hide(self):
        self.setVisible(False)

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

        search_bar_spacer1 = QWidget()
        search_bar_spacer1.setFixedWidth(5)
        self.search_bar_layout.addWidget(search_bar_spacer1)

        self.new_patient_button = QPushButton("+")
        self.new_patient_button.setFont(QFont("Avenir", 15))
        self.new_patient_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.new_patient_button.setToolTip('Add Patient')
        self.new_patient_button.setFixedHeight(40)
        self.new_patient_button.setFixedWidth(40)
        self.new_patient_button.setStyleSheet(
            """
            QPushButton
            {
                background-color: #aaaaee;
                border-radius: 20px;
                padding: 5px;
            }

            QPushButton:hover
            {
                background-color: #9898ed;
            }
            """
        )
        self.new_patient_button.clicked.connect(self.showPatientFormWindow)
        self.search_bar_layout.addWidget(self.new_patient_button)

        search_bar_spacer2 = QWidget()
        search_bar_spacer2.setFixedWidth(10)
        self.search_bar_layout.addWidget(search_bar_spacer2)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search patients")
        self.search_bar.setStyleSheet(
            """
            QLineEdit {
                border: 1px solid #aaaaaa;
                border-radius: 5px;
                padding: 5px;
            }
            """
        )
        self.search_bar.textChanged.connect(self.filterSearchItems)
        self.search_bar_layout.addWidget(self.search_bar)

        self.scroll_area = QScrollArea()
        self.scroll_area.setStyleSheet(
            """
            QScrollArea
            {
                background-color: #ffffff;
                border: 1px solid #aaaaaa;
                border-radius: 5px;
                padding: 5px
            }
            """
        )
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
        self.list.setObjectName("PatientList")
        self.list.setStyleSheet(
            "QWidget#PatientList { background-color: #ffffff; }"
        )
        self.list_layout = QVBoxLayout()

        for patient_name, patient_id, user_id, birthday in self.patients:
            widget = PatientListItem(patient_name, patient_id, user_id, birthday)
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
            """SELECT name, id, user_id, birthday 
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
