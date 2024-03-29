import math

from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QWidget,
)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from datetime import datetime


class Label(QLabel):
    def __init__(self, text, textSize, margins, color):
        super().__init__()
        self.setText(text)
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.setFont(QFont("Avenir", textSize))
        self.setContentsMargins(margins[0], margins[1], margins[2], margins[3])
        self.setStyleSheet("color: {}".format(color))


class LabelBolded(QLabel):
    def __init__(self, text, textSize, margins):
        super().__init__()
        self.setText(text)
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.setFont(QFont("Avenir", textSize))
        self.setContentsMargins(margins[0], margins[1], margins[2], margins[3])
        self.setStyleSheet("font-weight: bold;")


class PatientCard(QWidget):
    def __init__(self):
        super().__init__()

        self.patient = None
        self.patientSex = ""

        self.layout_box = QHBoxLayout()
        self.layout_box.setContentsMargins(0, 0, 0, 0)

        self.patient_card = QWidget()
        self.patient_card.setContentsMargins(0, 0, 0, 0)
        self.patient_card.setStyleSheet(
            "background-color: #ffffff; height: 250; border-radius: 20px;"
        )

        self.layout_box.addWidget(self.patient_card)

        self.inside_layout = QHBoxLayout(self.patient_card)
        self.inside_layout.setContentsMargins(0, 0, 0, 0)

        self.patient_card_left = QWidget()
        self.patient_card_left.setContentsMargins(0, 0, 0, 0)
        self.patient_card_left.setStyleSheet(
            "background-color: #ccccff; height: 250; border-radius: 20px;"
        )

        self.left_layout = QVBoxLayout(self.patient_card_left)

        self.avatarWidget = QWidget()
        self.avatar_layout = QHBoxLayout(self.avatarWidget)
        self.patientAvatar = QPushButton("")
        self.patientAvatar.setCursor(Qt.CursorShape.PointingHandCursor)
        # patientAvatar.clicked.connect(self.userProfileClick)
        self.patientAvatar.setFont(QFont("Avenir", 25))
        self.patientAvatar.setFixedHeight(80)
        self.patientAvatar.setFixedWidth(80)

        self.patientAvatar.setStyleSheet(
            """ QPushButton {
                                        background-color: #aaaaee;
                                        border-radius: 20px;
                                        border-style: outset;
                                        border: 2px solid #aaaaee;
                                        padding: 5px;
                                    }"""
        )
        self.avatar_layout.addWidget(self.patientAvatar, 1)

        self.nameWidget = QWidget()
        self.name_layout = QVBoxLayout(self.nameWidget)

        # set patient name
        self.patientName = LabelBolded("", 25, [10, 0, 0, 0])
        self.name_layout.addWidget(self.patientName)

        self.ageWidget = QWidget()
        self.ageWidget.setContentsMargins(0, 0, 0, 0)
        self.age_layout = QGridLayout(self.ageWidget)

        self.maleIcon = QIcon("icons/male.png")
        self.femaleIcon = QIcon("icons/female.png")

        self.sexLabel = QLabel()
        self.sexLabel.setPixmap(self.maleIcon.pixmap(40, 40))
        self.age_layout.addWidget(self.sexLabel, 0, 0, 2, 1)

        # set patient age
        self.patientAge = Label("Age", 18, [0, 0, 0, 0], "black")
        self.age_layout.addWidget(self.patientAge, 0, 1, 1, 1)

        self.patientAgeV = LabelBolded("", 18, [0, 0, 0, 0])
        self.age_layout.addWidget(self.patientAgeV, 1, 1, 1, 1)

        self.name_layout.addWidget(self.ageWidget)
        self.avatar_layout.addWidget(self.nameWidget, 3)
        self.left_layout.addWidget(self.avatarWidget)

        # patient detail layout
        self.patient_detail = QWidget()
        self.patient_detail.setContentsMargins(0, 0, 0, 0)
        self.patient_detail.setStyleSheet(
            "background-color: #ccccff; height: 250; border-radius: 20px"
        )
        self.patient_detail_layout = QGridLayout(self.patient_detail)

        # set patient height label
        self.patientHeight = Label("Height(cm)", 18, [0, 0, 0, 1], "#000")
        self.patient_detail_layout.addWidget(self.patientHeight, 0, 0)

        # set patient weight label
        self.patientWeight = Label("Weight(kg)", 18, [0, 0, 0, 1], "#000")
        self.patient_detail_layout.addWidget(self.patientWeight, 0, 1)

        # set patient blood type label
        self.patientBlood = Label("Blood Type", 18, [0, 0, 0, 1], "#000")
        self.patient_detail_layout.addWidget(self.patientBlood, 0, 2)

        # set patient height
        self.patientHeightV = LabelBolded("", 18, [0, 0, 0, 1])
        self.patient_detail_layout.addWidget(self.patientHeightV, 1, 0)

        # set patient weight
        self.patientWeightV = LabelBolded("", 18, [0, 0, 0, 1])
        self.patient_detail_layout.addWidget(self.patientWeightV, 1, 1)

        # set patient blood type
        self.patientBloodV = LabelBolded("", 18, [0, 0, 0, 1])
        self.patient_detail_layout.addWidget(self.patientBloodV, 1, 2)

        self.left_layout.addWidget(self.patient_detail)
        self.inside_layout.addWidget(self.patient_card_left, 1)

        # Birthday, phone number, patient ID, ALL type, Assigned Doctor, Body Surface Area (m^2)
        self.patient_card_right = QWidget()
        self.patient_card_right.setStyleSheet(
            "background-color: #ffffff; height: 250; border-radius: 20px;"
        )
        self.patient_card_right.setContentsMargins(10, 15, 0, 7)

        self.right_layout = QGridLayout(self.patient_card_right)

        # set patient ID label
        self.patientID = Label("Patient ID", 18, [0, 0, 0, 0], "#71797E")
        self.right_layout.addWidget(self.patientID, 0, 0)

        # set patient birthday label
        self.birthday = Label("Birthday", 18, [0, 0, 0, 0], "#71797E")
        self.right_layout.addWidget(self.birthday, 0, 1)

        # set patient phone number label
        self.phoneNumber = Label("Phone Number", 18, [0, 0, 0, 0], "#71797E")
        self.right_layout.addWidget(self.phoneNumber, 0, 2)

        # set patient ID
        self.patientIDV = LabelBolded("", 18, [0, 0, 0, 10])
        self.right_layout.addWidget(self.patientIDV, 1, 0)

        # set patient birthday
        self.birthdayV = LabelBolded("", 18, [0, 0, 0, 10])
        self.right_layout.addWidget(self.birthdayV, 1, 1)

        # set phone number
        self.phoneNumberV = LabelBolded("", 18, [0, 0, 0, 10])
        self.right_layout.addWidget(self.phoneNumberV, 1, 2)

        # set ALL type label
        self.allType = Label("ALL Type", 18, [0, 0, 0, 0], "#71797E")
        self.right_layout.addWidget(self.allType, 2, 0)

        # set assigned doctor label
        self.assignedDoctor = Label("Assigned Doctor", 18, [0, 0, 0, 0], "#71797E")
        self.right_layout.addWidget(self.assignedDoctor, 2, 1)

        # set body surface area label
        self.bodySurfaceArea = Label(
            "Body Surface Area(m^2)", 18, [0, 0, 0, 0], "#71797E"
        )
        self.right_layout.addWidget(self.bodySurfaceArea, 2, 2)

        # set ALL type
        self.allTypeV = LabelBolded("", 18, [0, 0, 0, 0])
        self.right_layout.addWidget(self.allTypeV, 3, 0)

        # set assigned doctor
        self.assignedDoctorV = LabelBolded("", 18, [0, 0, 0, 0])
        self.right_layout.addWidget(self.assignedDoctorV, 3, 1)

        # set body surface area
        self.buttons = QWidget()
        self.buttons.setContentsMargins(0, 0, 0, 0)
        self.buttons.setStyleSheet(
            "background-color: #ffffff; height: 250; border-radius: 20px;"
        )
        self.buttonLayout = QHBoxLayout(self.buttons)
        self.buttonLayout.setContentsMargins(0, 0, 20, 0)

        self.bodySurfaceAreaV = LabelBolded("", 18, [0, 0, 0, 0])
        self.buttonLayout.addWidget(self.bodySurfaceAreaV)

        self.editButton = QPushButton("Edit")
        self.editButton.clicked.connect(self.editClicked)
        self.editButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.editButton.setMinimumWidth(60)
        self.editButton.setMinimumHeight(40)
        self.editButton.setMaximumHeight(45)
        self.editButton.setFont(QFont("Avenir", 18))
        self.editButton.setStyleSheet(
            "background-color: #aaaaee; border-radius: 10px; padding: 10px 15px;"
        )
        self.buttonLayout.addWidget(
            self.editButton, alignment=Qt.AlignmentFlag.AlignRight
        )

        self.right_layout.addWidget(self.buttons, 3, 2)
        self.inside_layout.addWidget(self.patient_card_right, 3)
        self.setLayout(self.layout_box)

    def setSexIcon(self):
        if self.patientSex == "Male":
            self.sexLabel.setPixmap(self.maleIcon.pixmap(40, 40))
        else:
            self.sexLabel.setPixmap(self.femaleIcon.pixmap(40, 40))

    def editClicked(self):
        self.parent().parent().parent().parent().adding_new_patient = False
        self.parent().parent().showPatientFormWindow()

    def getPatientInfo(self, patient):
        self.patient = patient
        self.displayPatientInfo()

    def displayPatientInfo(self):
        self.patientName.clear()

        if self.patient is not None:
            self.patientName.setText(self.patient.name)
            self.patientAvatar.setText(self.patient.name[0])
            self.patientAgeV.setText(str(self.patient.age))
            self.patientSex = str(self.patient.sex)
            self.patientHeightV.setText(str(self.patient.height))
            self.patientWeightV.setText(str(self.patient.weight))
            self.patientBloodV.setText(self.patient.bloodType)
            self.patientIDV.setText(str(self.patient.user_id))
            self.phoneNumberFormatter()
            self.allTypeV.setText(self.patient.allType)
            self.assignedDoctorV.setText(
                self.getAssignedDoctorFullName(self.patient.assignedDoctor)
            )
            self.bodySurfaceAreaV.setText(str(self.patient.bsa))
            self.birthdayV.setText(
                datetime.strptime(self.patient.birthday, "%Y%m%d").strftime("%Y-%m-%d")
            )

            self.setSexIcon()

    def getAssignedDoctorFullName(self, doctorID):
        conn = self.parent().parent().parent().parent().db_conn

        res = conn.execute(
            """SELECT full_name
            FROM oncologists o
            WHERE o.username=?
            """,
            (doctorID,),
        )

        row = res.fetchone()
        if row:
            return row[0]
        else:
            return doctorID

    def calculateBodySurfaceArea(self):
        weight = self.patientWeightV.text()
        height = self.patientHeightV.text()
        try:
            weight = float(weight)
            height = float(height)
        except:
            return
        else:
            bsa = math.sqrt(height * weight / 3600)
            self.bodySurfaceAreaV.setText("{:.2f}".format(bsa))

    def phoneNumberFormatter(self):
        self.phoneNumberV.setText(
            format(int(self.patient.phoneNumber[:-1]), ",").replace(",", "-")
            + self.patient.phoneNumber[-1]
        )
