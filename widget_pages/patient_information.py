from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class PatientInformationWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        button1 = QPushButton("Back to Patient List")
        button2 = QPushButton("Show Dashboard")
        button1.clicked.connect(self.showPatientListWindow)
        button2.clicked.connect(self.showDashboardWindow)

        layout.addWidget(QLabel("Patient Information Window"))
        layout.addWidget(button1)
        layout.addWidget(button2)

        self.setLayout(layout)

    def showPatientListWindow(self):
        self.parent().parent().showPatientListWindow()

    def showDashboardWindow(self):
        self.parent().parent().showDashboardWindow()
