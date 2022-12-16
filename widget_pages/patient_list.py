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
    def __init__(self, patient_name, patient_id):
        super(PatientListItem, self).__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(
            "background-color: #ccccff; border-radius: 5px; padding: 10px"
        )

        self.patient_name = patient_name
        self.patient_id = patient_id
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
        self.parent().parent().parent().parent().showPatientInformationWindow(
            self.patient_id
        )


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
        self.new_patient_button.clicked.connect(self.showPatientInformationWindow)
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

    def showPatientInformationWindow(self, patient_id=-1):
        self.parent().parent().updateSelectedPatient(patient_id)
        self.parent().parent().showPatientInformationWindow()

    def displayPatientList(self):
        self.list = QWidget()
        self.list_layout = QVBoxLayout()

        for patient_name, patient_id in self.patients:
            widget = PatientListItem(patient_name, patient_id)
            self.patient_widgets.append(widget)
            self.list_layout.addWidget(widget)

        bottom_spacer = QSpacerItem(
            1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.list_layout.addItem(bottom_spacer)

        self.list.setLayout(self.list_layout)
        self.scroll_area.setWidget(self.list)
        self.scroll_area.setWidgetResizable(True)

    def updatePatientList(self, conn, username):
        res = conn.execute(
            """SELECT name, id 
               FROM patients p 
               INNER JOIN oncologists o ON p.oncologist_id=o.username
                    AND o.username=?
            """,
            (username,),
        )

        rows = res.fetchall()
        if rows:
            self.patients = rows
        self.displayPatientList()
