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
    QComboBox,
    QMessageBox,
    QDialogButtonBox
)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QAbstractAnimation
from PyQt6.QtGui import QFont, QIcon, QPixmap

from datetime import datetime
from enum import Enum

logging.getLogger().setLevel(logging.INFO)

class SearchMode(Enum):
    DEFAULT = 0
    ADVANCED = 1

class PatientListItem(QPushButton):
    def __init__(self, patient_name, patient_id, user_id, birthday, is_admin=False):
        super(PatientListItem, self).__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("PatientListItem")
        self.setContentsMargins(15, 0, 0, 0)
        self.setStyleSheet(
            """
            QPushButton#PatientListItem
            {
                min-height: 100px;
                background-color: #ebebf2;
                border: 1px solid #aaaaaa;
                border-radius: 30px;
                padding: 5px
            }

            QPushButton#PatientListItem:hover
            {
                background-color: #e1e1f7;
            }
            """
        )
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        if (not is_admin):
            self.clicked.connect(self.showPatientInfo)

        self.patient_name = patient_name
        self.patient_id = patient_id
        self.user_id = user_id
        self.is_admin = is_admin
        self.birthday = datetime.strptime(birthday, '%Y%m%d').strftime('%Y-%m-%d') if birthday else ""

        self.avatar = QPushButton(self.patient_name[0])
        self.avatar.setObjectName("avatar")
        self.avatar.setFont(QFont("Avenir", 25))
        self.avatar.setFixedHeight(80)
        self.avatar.setFixedWidth(80)
        self.avatar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.avatar.setStyleSheet(
            """ 
            QPushButton#avatar
            {
                background-color: #aaaaee;
                border-radius: 40px;
                border-style: outset;
                border: 2px solid #aaaaee;
                padding: 10px;
            }
            """
        )

        self.name_label = QLabel(self.patient_name)
        patient_name_font = QFont("Avenir", 18)
        patient_name_font.setBold(True)
        self.name_label.setFont(patient_name_font)
        self.name_label.setFixedWidth(450)
        self.name_label.setContentsMargins(5, 10, 5, 0)

        if (is_admin):
            self.user_id_label = QLabel("Oncologist Username: " + self.user_id)
        else:
            self.user_id_label = QLabel("Patient ID: " + self.user_id)
        self.user_id_label.setFont(QFont("Avenir", 13, italic=True))
        self.user_id_label.setFixedWidth(450)
        self.user_id_label.setStyleSheet("color: #505050;")
        self.user_id_label.setContentsMargins(5, 0, 5, 10)

        if (not is_admin):
            self.birthday_label = QLabel("DOB: " + self.birthday)
            self.birthday_label.setFont(QFont("Avenir", 13))
            self.birthday_label.setFixedWidth(200)
            self.birthday_label.setStyleSheet("color: #505050;")
            self.birthday_label.setContentsMargins(0, 0, 5, 10)
        else:
            self.birthday_label = QLabel()

        self.delete_button = QPushButton()
        self.delete_button.setIcon(QIcon("icons/delete.png"))
        self.delete_button.setIconSize(QSize(40, 40))
        self.delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_button.setToolTip("Delete")
        self.delete_button.setContentsMargins(0, 0, 10, 10)
        self.delete_button.setStyleSheet(
            """
            QPushButton
            {
                background-color: rgba(255, 255, 255, 0);
                border-radius: 25px;
                padding: 20px
            }
            """
        )
        self.delete_button.enterEvent = self.onButtonHover
        self.delete_button.leaveEvent = self.onButtonUnhover
        self.delete_button.clicked.connect(self.deletePatient)

        avatar_spacer = QSpacerItem(
            10, 1, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum
        )
        name_spacer = QSpacerItem(
            20, 1, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum
        )
        main_spacer = QSpacerItem(
            1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.layout = QGridLayout()
        self.layout.addWidget(self.avatar, 0, 0, 2, 1)
        self.layout.addItem(avatar_spacer, 0, 1, 2, 1)
        self.layout.addWidget(self.name_label, 0, 2, 1, 1)
        self.layout.addWidget(self.user_id_label, 1, 2, 1, 1)
        self.layout.addItem(name_spacer, 0, 3, 2, 1)
        self.layout.addWidget(self.birthday_label, 1, 4, 1, 1)
        self.layout.addItem(main_spacer, 0, 5, 2, 1)
        self.layout.addWidget(self.delete_button, 0, 6, 2, 1)

        self.setLayout(self.layout)
    
    def onButtonHover(self, event):
        self.animation = QPropertyAnimation(self.delete_button, b"iconSize")
        self.animation.setDuration(200)
        self.animation.setStartValue(self.delete_button.iconSize())
        self.animation.setEndValue(QSize(46, 46))
        self.animation.start()
    
    def onButtonUnhover(self, event):
        self.animation = QPropertyAnimation(self.delete_button, b"iconSize")
        self.animation.setDuration(200)
        self.animation.setStartValue(self.delete_button.iconSize())
        self.animation.setEndValue(QSize(40, 40))
        self.animation.start()

    def show(self):
        self.setVisible(True)

    def hide(self):
        self.setVisible(False)

    def showPatientInfo(self):
        self.parent().parent().parent().parent().showPatientInformationWindow(
            self.patient_id
        )

    def deletePatient(self):

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Delete Patient")
        dlg.setText("Are you sure you want to delete " + self.patient_name +"?")
        dlg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        for button in dlg.findChild(QDialogButtonBox).findChildren(QPushButton):
            button.setCursor(Qt.CursorShape.PointingHandCursor)

        dlg.setFont(QFont("Avenir", 15))
        button = dlg.exec()

        if button == QMessageBox.StandardButton.No:
            return

        conn = self.parent().parent().parent().parent().getDatabaseConnection()

        try:
            conn.execute(
                "PRAGMA foreign_keys = ON"
            )  # enable foreign key cascade on delete for the measurements table
            
            if (self.is_admin):
                conn.execute(
                    """
                    DELETE FROM oncologists 
                    WHERE username=? 
                    """,
                    (self.user_id,),
                )
            else:
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

        # patient list window specific states
        self.search_mode = SearchMode.DEFAULT
        self.filter_name = ""
        self.filter_id = ""

        self.patients = []
        self.patient_widgets = []

        self.main_box_layout = QVBoxLayout()
        self.search_bar_layout = QHBoxLayout()

        search_bar_spacer1 = QWidget()
        search_bar_spacer1.setFixedWidth(15)
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

        self.name_search_bar = QLineEdit()
        self.name_search_bar.setPlaceholderText("Search Patients")
        self.name_search_bar.setStyleSheet(
            """
            QLineEdit {
                border: 1px solid #aaaaaa;
                border-radius: 5px;
                padding: 5px;
            }
            """
        )
        self.name_search_bar.textChanged.connect(self.filterByName)
        self.search_bar_layout.addWidget(self.name_search_bar)

        self.id_search_bar = QLineEdit()
        self.id_search_bar.setPlaceholderText("Patient ID")
        self.id_search_bar.setStyleSheet(
            """
            QLineEdit {
                border: 1px solid #aaaaaa;
                border-radius: 5px;
                padding: 5px;
            }
            """
        )
        self.id_search_bar.textChanged.connect(self.filterByID)
        self.id_search_bar.setVisible(False)
        self.search_bar_layout.addWidget(self.id_search_bar)

        search_bar_spacer3 = QWidget()
        search_bar_spacer3.setFixedWidth(10)
        self.search_bar_layout.addWidget(search_bar_spacer3)

        self.search_mode_button = QPushButton("Advanced Search")
        self.search_mode_button.setFont(QFont("Avenir", 13))
        self.search_mode_button.setCheckable(True)
        self.search_mode_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.search_mode_button.setStyleSheet(
            """
            QPushButton
            {
                background-color: #fafafa;
                border: 1px solid #aaaaaa;
                border-radius: 5px;
                padding: 10px
            }

            QPushButton:hover
            {
                background-color: #f0f0f0;
            }
            """
        )
        self.search_mode_button.clicked.connect(self.setSearchMode)
        self.search_bar_layout.addWidget(self.search_mode_button)

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
    
    def setSearchMode(self):
        if self.search_mode_button.isChecked():
            self.search_mode = SearchMode(1)
            self.showAdvancedOptions(True)
        else:
            self.search_mode = SearchMode(0)
            self.showAdvancedOptions(False)
    
    def showAdvancedOptions(self, display):
        if display:
            self.search_mode_button.setText("Default Search")
            self.name_search_bar.setPlaceholderText("Patient Name")
            self.name_search_bar.clear()
            self.id_search_bar.clear()
            self.id_search_bar.setVisible(True)
        else:
            self.search_mode_button.setText("Advanced Search")
            self.name_search_bar.setPlaceholderText("Search Patient")
            self.name_search_bar.clear()
            self.id_search_bar.clear()
            self.id_search_bar.setVisible(False)
    
    def filterByName(self, input):
        self.filter_name = input
        self.filterPatients()
    
    def filterByID(self, input):
        self.filter_id = input
        self.filterPatients()

    def filterPatients(self):
        for widget in self.patient_widgets:
            widget.show()
        for widget in self.patient_widgets:
            if self.filter_name and self.filter_name.lower() not in widget.patient_name.lower():
                widget.hide()
            if self.filter_id and self.filter_id.lower() not in widget.user_id.lower():
                widget.hide()

    def showPatientFormWindow(self):
        # whenever you press "Add Patient", should clear state so the fields aren't pre-populated
        self.parent().parent().selected_patient = None
        if (self.parent().parent().is_admin_user):
            self.parent().parent().showOncologistFormWindow()
        else:
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

        if (self.parent().parent().is_admin_user):
            for username, full_name in self.patients:
                widget = PatientListItem(full_name, "", username, "", True)
                self.patient_widgets.append(widget)
                self.list_layout.addWidget(widget)
        else:
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

        if (self.parent().parent().is_admin_user):
            res = conn.execute(
                """SELECT username, full_name
                FROM oncologists o
                WHERE o.is_admin='FALSE'
                """
            ) 
        else:
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
