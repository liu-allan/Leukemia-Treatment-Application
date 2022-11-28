from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QToolBar, QTabWidget, QSizePolicy
from PyQt6.QtGui import QAction, QIcon, QPalette, QColor, QFont
from PyQt6.QtCore import Qt
# import json
# import logging

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class TabPatientList(QWidget):
    def __init__(self):
        super().__init__()

class TabChangeParameter(QWidget):
    def __init__(self):
        super().__init__()

class TabLogOff(QWidget):
    def __init__(self):
        super().__init__()

class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Top tool bar that shows page name + user account 
        toolBar = QToolBar("Dashboard top bar")
        toolBar.setStyleSheet("height : 50")
        layout.addWidget(toolBar)

        dashboard_label = QLabel("Dashboard")
        dashboard_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        dashboard_label.setFont(QFont('Sans Serif', 25))
        dashboard_label.setMargin(10)
        toolBar.addWidget(dashboard_label)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        toolBar.addWidget(spacer)
        
        user_name = QPushButton("IC", self)
        user_name.clicked.connect(self.userProfileClick)
        user_name.setFont(QFont('Sans Serif', 15))
        user_name.setFixedHeight(40)
        user_name.setFixedWidth(40)
        
        # https://stackoverflow.com/questions/12734319/change-rectangular-qt-button-to-round
        user_name.setStyleSheet(""" QPushButton {
                                        color: #333;
                                        border: 2px solid #555;
                                        border-radius: 20px;
                                        border-style: outset;
                                        background: qradialgradient(
                                            cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,
                                            radius: 1.35, stop: 0 #fff, stop: 1 #888
                                        );
                                        padding: 5px;
                                    }

                                    QPushButton:hover {
                                        background: qradialgradient(
                                            cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,
                                            radius: 1.35, stop: 0 #fff, stop: 1 #bbb
                                        );
                                    }""")
  
        # setting radius and border
        toolBar.addWidget(user_name)

        spacer2 = QWidget()
        toolBar.addWidget(spacer2)

        # Side tabs
        tabs = QTabWidget()

        tabs.addTab(TabPatientList(), "Patient List")
        tabs.addTab(TabChangeParameter(), "Change Parameter")
        tabs.addTab(TabLogOff(), "Log off")

        # West position, QTabWidget.West doesn't work
        # tabs.setTabPosition(QTabWidget.TabPosition.West)
        tabs.setMovable(True)
        
        layout.addWidget(tabs)

        button1 = QPushButton("Back to Patient List")
        button2 = QPushButton("Back to Patient Information")
        button1.clicked.connect(self.showPatientListWindow)
        button2.clicked.connect(self.showPatientInformationWindow)

        layout.addWidget(button1)
        layout.addWidget(button2)

        self.setLayout(layout)

    def userProfileClick(self, s):
        print("click", s)

    def showPatientListWindow(self):
        self.parent().parent().showPatientListWindow()

    def showPatientInformationWindow(self):
        self.parent().parent().showPatientInformationWindow()


