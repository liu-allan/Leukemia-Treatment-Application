from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class PatientListWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        button = QPushButton("Show Patient Information")
        button.clicked.connect(self.showPatientInformationWindow)

        layout.addWidget(QLabel("Patient List Window"))
        layout.addWidget(button)

        self.setLayout(layout)

    def showPatientInformationWindow(self):
        self.parent().parent().showPatientInformationWindow()
