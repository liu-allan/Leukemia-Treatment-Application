from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        button = QPushButton("Show Patient List")
        button.clicked.connect(self.showPatientListWindow)

        layout.addWidget(QLabel("Login Window"))
        layout.addWidget(button)

        self.setLayout(layout)

    def showPatientListWindow(self):
        self.parent().parent().showPatientListWindow()
