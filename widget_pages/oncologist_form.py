import bcrypt
import logging
import sqlite3

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QDialogButtonBox,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtGui import QFont

logging.getLogger().setLevel(logging.INFO)


class Label(QLabel):
    def __init__(self, text, width=400):
        super().__init__()
        self.setText(text)
        self.setFont(QFont("Avenir", 15))
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

        self.oncologistFormLayout = QVBoxLayout()
        self.oncologistFormLayout.setContentsMargins(0, 0, 0, 0)

        self.usernameLabel = Label("Oncologist Username")
        self.usernameLineEdit = LineEdit("Username")
        self.oncologistFormLayout.addWidget(FormRow(self.usernameLabel, self.usernameLineEdit))

        self.passwordLabel = Label("Password")
        self.passwordEdit = LineEdit("Password")
        self.oncologistFormLayout.addWidget(FormRow(self.passwordLabel, self.passwordEdit))

        self.fullNameLabel = Label("Full Name")
        self.fullNameEdit = LineEdit("Name")
        self.oncologistFormLayout.addWidget(FormRow(self.fullNameLabel, self.fullNameEdit))

        self.errorLabel = Label("")
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(self.buttonBox.standardButtons().Cancel)
        self.buttonBox.addButton(self.buttonBox.standardButtons().Save)
        self.buttonBox.setFont(QFont("Avenir", 12))
        self.buttonBox.setFixedWidth(200)
        self.buttonBox.setStyleSheet(
            "background-color: #aaaaee; border-radius: 5px; padding: 10px"
        )

        self.buttonBox.button(self.buttonBox.standardButtons().Cancel).clicked.connect(
            self.showPatientListWindow
        )
        self.buttonBox.button(self.buttonBox.standardButtons().Save).clicked.connect(
            self.savePatientInformation
        )

        self.buttonBox.setCursor(Qt.CursorShape.PointingHandCursor)
        self.oncologistFormLayout.addWidget(FormRow(self.errorLabel, self.buttonBox))

        self.setLayout(self.oncologistFormLayout)

    def savePatientInformation(self):
        try:
            username = self.usernameLineEdit.text()
            assert username != ""
            password = self.encryptPassword(self.passwordEdit.text())
            fullName = self.fullNameEdit.text()
            
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
        self.fullNameEdit.clear() 