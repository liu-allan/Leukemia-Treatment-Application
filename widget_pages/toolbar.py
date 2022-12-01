from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QHBoxLayout,
    QWidget,
    QToolBar,
    QSizePolicy,
)
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt


class ToolBar(QWidget):
    def __init__(self, page_name, username):
        super().__init__()

        # Top tool bar that shows page name + user account
        toolBar = QToolBar("tool bar")
        toolBar.setStyleSheet(
            "background-color: #a9c7c5; height : 50; border-radius: 10px"
        )

        dashboard_label = QLabel(page_name)
        dashboard_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        dashboard_label.setFont(QFont("Avenir", 25))
        dashboard_label.setMargin(10)
        toolBar.addWidget(dashboard_label)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        toolBar.addWidget(spacer)

        avatar = QPushButton(username[0].upper(), self)
        avatar.setCursor(Qt.CursorShape.PointingHandCursor)
        avatar.clicked.connect(self.userProfileClick)
        avatar.setFont(QFont("Avenir", 15))
        avatar.setFixedHeight(40)
        avatar.setFixedWidth(40)

        # https://stackoverflow.com/questions/12734319/change-rectangular-qt-button-to-round
        avatar.setStyleSheet(
            """ QPushButton {
                                        background-color: #bfd8d2;
                                        border-radius: 20px;
                                        border-style: outset;
                                        background: qradialgradient(
                                            cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,
                                            radius: 1.35, stop: 0 #bfd8d2, stop: 1 #bfd8d2
                                        );
                                        border: 2px solid #bfd8d2;
                                        padding: 5px;
                                    }

                                    QPushButton:hover {
                                        background: qradialgradient(
                                            cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,
                                            radius: 1.35, stop: 0 #bfd8d2, stop: 1 #82a3ac
                                        );
                                    }"""
        )

        # setting radius and border
        toolBar.addWidget(avatar)

        name_label = QLabel("Dr. " + username)
        name_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        name_label.setFont(QFont("Avenir", 20))
        name_label.setMargin(15)
        toolBar.addWidget(name_label)

        self.layout = QHBoxLayout()
        self.layout.addWidget(toolBar)
        self.setLayout(self.layout)
    
    def userProfileClick(self, s):
        print("click", s)