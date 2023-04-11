import bcrypt
import logging
import sqlite3

from PyQt6.QtCore import Qt, QRect
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QRadioButton,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QScrollArea
)
from PyQt6.QtGui import QFont
from util.animation_manager import AnimationManager

logging.getLogger().setLevel(logging.INFO)


class Label(QLabel):
    def __init__(self, text, width=400):
        super().__init__()
        self.setText(text)
        self.setFont(QFont("Avenir", 18))
        self.setFixedWidth(width)

class LineEdit(QLineEdit):
    def __init__(self, placeholderText, width=200):
        super().__init__()
        self.setPlaceholderText(placeholderText)
        self.setFont(QFont("Avenir", 15))
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

class OncologistFormWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.oncologistFormBigLayout = QVBoxLayout()
        self.oncologistFormBigLayout.setContentsMargins(0, 0, 0, 0)

        self.oncologistFormWidget = QWidget()
        self.oncologistFormWidget.setContentsMargins(0, 0, 0, 0)
        self.oncologistFormWidget.setFixedWidth(640)
        self.oncologistFormWidget.setFixedHeight(820)
        self.oncologistFormWidget.setObjectName("OncologistFormOverall")
        self.oncologistFormWidget.setStyleSheet(
            """
            QWidget#OncologistFormOverall
            {
                border: 1px solid #aaaaaa;
                background-color: #ffffff;
                border-radius: 20px;
                padding: 5px;
            }
            """
        )
        self.oncologistFormBigLayout.addWidget(self.oncologistFormWidget, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.oncologistFormLayout = QVBoxLayout(self.oncologistFormWidget)
        self.oncologistFormLayout.setContentsMargins(0, 30, 0, 10)

        self.typeOfOncologistForm = Label("New Oncologist Enrollment")
        self.typeOfOncologistForm.setContentsMargins(30, 10, 0, 10)
        self.typeOfOncologistForm.setFont(QFont("Avenir", 30))
        self.typeOfOncologistForm.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.typeOfOncologistForm.setFixedWidth(self.oncologistFormWidget.width() - 60)
        self.typeOfOncologistForm.setStyleSheet("background-color: rgba(170, 170, 238, 100); height: 60px; border-radius: 20px;")
        self.oncologistFormLayout.addWidget(self.typeOfOncologistForm, alignment=Qt.AlignmentFlag.AlignCenter)

        self.fullNameLabel = Label("Full Name")
        self.fullNameLabel.setContentsMargins(30, 20, 0, 0)
        self.oncologistFormLayout.addWidget(self.fullNameLabel, alignment=Qt.AlignmentFlag.AlignBottom)

        self.oncologistNameLayout = QHBoxLayout()
        self.oncologistNameLayout.setContentsMargins(0, 0, 0, 0)

        self.oncologistFirstNameLineEdit = QLineEdit()
        self.oncologistFirstNameLineEdit.setContentsMargins(30, 0, 0, 0)
        self.oncologistFirstNameLineEdit.setPlaceholderText("First Name")
        self.oncologistFirstNameLineEdit.setFont(QFont("Avenir", 18))
        self.oncologistFirstNameLineEdit.setStyleSheet(
            "background-color: #f5f5f5; height: 40px; border-radius: 10px; padding: 0px 10px"
        )
        self.oncologistNameLayout.addWidget(self.oncologistFirstNameLineEdit)

        self.oncologistLastNameLineEdit = QLineEdit()
        self.oncologistLastNameLineEdit.setContentsMargins(10, 0, 30, 0)
        self.oncologistLastNameLineEdit.setPlaceholderText("Last Name")
        self.oncologistLastNameLineEdit.setFont(QFont("Avenir", 18))
        self.oncologistLastNameLineEdit.setStyleSheet(
            "background-color: #f5f5f5; height: 40px; border-radius: 10px; padding: 0px 10px"
        )
        self.oncologistNameLayout.addWidget(self.oncologistLastNameLineEdit)
        self.oncologistFormLayout.addLayout(self.oncologistNameLayout)
        
        self.genderLabel = Label("Gender/Sex")
        self.genderLabel.setContentsMargins(30, 20, 0, 0)
        self.oncologistFormLayout.addWidget(self.genderLabel, alignment=Qt.AlignmentFlag.AlignBottom)

        self.genderLayout = QHBoxLayout()
        self.genderLayout.setContentsMargins(30, 0, 0, 0)

        self.radioButton = QRadioButton("Male")
        self.radioButton.setContentsMargins(0, 0, 0, 0)
        self.radioButton.setChecked(True)
        self.radioButton.gender = "Male"
        self.radioButton.setFont(QFont("Avenir", 18))
        self.radioButton.toggled.connect(self.selectedGenderType)
        self.genderLayout.addWidget(self.radioButton)

        self.radioButton = QRadioButton("Female")
        self.radioButton.setContentsMargins(10, 0, 0, 0)
        self.radioButton.setFont(QFont("Avenir", 18))
        self.radioButton.gender = "Female"
        self.radioButton.toggled.connect(self.selectedGenderType)
        self.genderLayout.addWidget(self.radioButton)

        self.oncologistFormLayout.addLayout(self.genderLayout)

        self.usernameLabel = Label("Oncologist Username")
        self.usernameLabel.setContentsMargins(30, 20, 30, 0)
        self.oncologistFormLayout.addWidget(self.usernameLabel, alignment=Qt.AlignmentFlag.AlignBottom)

        self.usernameLineEdit = QLineEdit()
        self.usernameLineEdit.setContentsMargins(30, 0, 30, 0)
        self.usernameLineEdit.setPlaceholderText("Username")
        self.usernameLineEdit.setFont(QFont("Avenir", 18))
        self.usernameLineEdit.setStyleSheet(
            "background-color: #f5f5f5; height: 40px; border-radius: 10px; padding: 0px 10px"
        )
        self.oncologistFormLayout.addWidget(self.usernameLineEdit)

        self.passwordLabel = Label("Password")
        self.passwordLabel.setContentsMargins(30, 20, 30, 0)
        self.oncologistFormLayout.addWidget(self.passwordLabel, alignment=Qt.AlignmentFlag.AlignBottom)

        self.passwordEdit = QLineEdit()
        self.passwordEdit.setContentsMargins(30, 0, 30, 0)
        self.passwordEdit.setPlaceholderText("Password")
        self.passwordEdit.setFont(QFont("Avenir", 18))
        self.passwordEdit.setStyleSheet(
            "background-color: #f5f5f5; height: 40px; border-radius: 10px; padding: 0px 10px"
        )
        self.passwordEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.oncologistFormLayout.addWidget(self.passwordEdit)

        self.confirmPasswordLabel = Label("Confirm Password")
        self.confirmPasswordLabel.setContentsMargins(30, 20, 30, 0)
        self.oncologistFormLayout.addWidget(self.confirmPasswordLabel, alignment=Qt.AlignmentFlag.AlignBottom)

        self.confirmPasswordEdit = QLineEdit()
        self.confirmPasswordEdit.setContentsMargins(30, 0, 30, 0)
        self.confirmPasswordEdit.setPlaceholderText("Confirm Password")
        self.confirmPasswordEdit.setFont(QFont("Avenir", 18))
        self.confirmPasswordEdit.setStyleSheet(
            "background-color: #f5f5f5; height: 40px; border-radius: 10px; padding: 0px 10px"
        )
        self.confirmPasswordEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.oncologistFormLayout.addWidget(self.confirmPasswordEdit)
        self.confirmPasswordEdit.textEdited.connect(self.checkPasswordMatch)

        self.spacer = QSpacerItem(
            1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.oncologistFormLayout.addSpacerItem(self.spacer)

        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.setContentsMargins(30, 0, 30, 10)

        self.errorLabel = Label("")
        self.errorLabel.setContentsMargins(0, 0, 0, 0)
        self.bottomLayout.addWidget(self.errorLabel, 8, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.showPatientListWindow)
        self.cancelButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancelButton.setMinimumWidth(100)
        self.cancelButton.setMinimumHeight(40)
        self.cancelButton.setMaximumHeight(50)
        self.cancelButton.setFont(QFont("Avenir", 18))
        self.cancelButton.setStyleSheet(
            "background-color: #aaaaee; border-radius: 10px; padding: 10px 15px;"
        )
        self.bottomLayout.addWidget(self.cancelButton, 1, alignment=Qt.AlignmentFlag.AlignRight)

        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.savePatientInformation)
        self.saveButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.saveButton.setMinimumWidth(100)
        self.saveButton.setMinimumHeight(40)
        self.saveButton.setMaximumHeight(50)
        self.saveButton.setFont(QFont("Avenir", 18))
        self.saveButton.setStyleSheet(
            "background-color: #aaaaee; border-radius: 10px; padding: 10px 15px;"
        )
        self.bottomLayout.addWidget(self.saveButton, 1, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.cancelAnimationManager = AnimationManager(widget=self.cancelButton)
        self.saveAnimationManager = AnimationManager(widget=self.saveButton)

        self.oncologistFormLayout.addLayout(self.bottomLayout)

        self.setLayout(self.oncologistFormBigLayout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.cancelAnimationManager.reset()
        self.saveAnimationManager.reset()

    def selectedGenderType(self):
        self.radioButton = self.sender()
        if self.radioButton.isChecked():
            print(self.radioButton.gender)

    def checkPasswordMatch(self):
        if(self.confirmPasswordEdit.text() != self.passwordEdit.text()):
            msg = "Password does not match!"
            self.errorLabel.setText(msg)
            self.errorLabel.setStyleSheet("color:red")
            logging.error(msg)
        else:
            msg = "Password matches!"
            self.errorLabel.setText(msg)
            self.errorLabel.setStyleSheet("color:green")
            logging.info(msg)
    
    def savePatientInformation(self):
        try:
            username = self.usernameLineEdit.text()
            assert username != ""
            password = self.encryptPassword(self.passwordEdit.text())
            fullName = self.oncologistFirstNameLineEdit.text() + " " + self.oncologistLastNameLineEdit.text()
            
            conn = self.parent().parent().getDatabaseConnection()
            conn.execute(
                '''
                INSERT INTO oncologists (username, password, full_name, is_admin)
                VALUES (?, ?, ?, 'FALSE')
                ''',
                (username, password, fullName),
            )
            conn.commit()

        except sqlite3.Error as er:
            msg = "Username is taken!"
            self.errorLabel.setText(msg)
            self.errorLabel.setStyleSheet("color:red")
            logging.error(er)

        except:
            msg = "Input fields must not be empty!"
            self.errorLabel.setText(msg)
            self.errorLabel.setStyleSheet("color:red")
            logging.error(msg)

        else:
            self.errorLabel.clear()
            msg = "Parameters saved successfully!"
            self.errorLabel.setText(msg)
            self.errorLabel.setStyleSheet("color:green")
            logging.info(msg)
            self.showPatientListWindow()

    def encryptPassword(self, password):
        bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(bytes, salt)

    def showPatientListWindow(self):
        self.errorLabel.clear()
        self.clearForm()
        self.parent().parent().showPatientListWindow()

    def clearForm(self):
        self.usernameLineEdit.clear()
        self.passwordEdit.clear()
        self.oncologistFirstNameLineEdit.clear() 
        self.oncologistLastNameLineEdit.clear()
        self.confirmPasswordEdit.clear()
