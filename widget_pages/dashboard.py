from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        button1 = QPushButton("Back to Patient List")
        button2 = QPushButton("Back to Patient Information")
        button1.clicked.connect(self.showPatientListWindow)
        button2.clicked.connect(self.showPatientInformationWindow)

        layout.addWidget(QLabel("Dashboard Window"))
        layout.addWidget(button1)
        layout.addWidget(button2)

        self.setLayout(layout)

    def showPatientListWindow(self):
        self.parent().parent().showPatientListWindow()

    def showPatientInformationWindow(self):
        self.parent().parent().showPatientInformationWindow()
