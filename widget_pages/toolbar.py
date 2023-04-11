from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QHBoxLayout,
    QWidget,
    QToolBar,
    QSizePolicy,
    QMessageBox,
    QDialogButtonBox,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from util.util import getLastNameFromFullName

class ToolBar(QWidget):
    def __init__(self, page_name, user_full_name):
        super().__init__()

        # Top tool bar that shows page name + user account
        self.toolBar = QToolBar("tool bar")
        self.toolBar.setContentsMargins(0, 0, 0, 0)
        self.toolBar.setStyleSheet(
            "background-color: #a9c7c5; height: 100; border-radius: 10px;"
        )
        
        self.dashboard_label = QLabel(page_name)
        self.dashboard_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.dashboard_label.setFont(QFont("Avenir", 25))
        self.dashboard_label.setMargin(10)
        self.toolBar.addWidget(self.dashboard_label)

        spacer1 = QWidget()
        spacer1.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.toolBar.addWidget(spacer1)

        self.avatar = QPushButton(
            getLastNameFromFullName(user_full_name)[0].upper()
            if user_full_name
            else "",
            self,
        )
        self.avatar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.avatar.clicked.connect(self.userProfileClick)
        self.avatar.setFont(QFont("Avenir", 19))
        self.avatar.setFixedHeight(40)
        self.avatar.setFixedWidth(40)

        # https://stackoverflow.com/questions/12734319/change-rectangular-qt-button-to-round
        self.avatar.setStyleSheet(
            """
            QPushButton 
            {
                background-color: #bfd8d2;
                border-radius: 20px;
                border-style: outset;
                border: 2px solid #bfd8d2;
                padding: 5px;
            }

            QPushButton:hover 
            {
                background: qradialgradient(
                    cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,
                    radius: 1.35, stop: 0 #bfd8d2, stop: 1 #82a3ac
                );
            }
            """
        )

        # setting radius and border
        self.toolBar.addWidget(self.avatar)

        self.name_label = QLabel(
            "Dr. " + getLastNameFromFullName(user_full_name) if user_full_name else ""
        )
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.name_label.setFont(QFont("Avenir", 20))
        self.name_label.setMargin(15)
        self.toolBar.addWidget(self.name_label)

        self.logout_button = QPushButton("Log Off")
        self.logout_button.setMinimumHeight(35)
        self.logout_button.setMaximumHeight(40)
        self.logout_button.setStyleSheet(
            "background-color: #e5e5e5; border-radius: 10px; padding: 5px"
        )
        self.logout_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.logout_button.clicked.connect(self.logoffClicked)
        self.logout_button.setFont(QFont("Avenir", 18))
        self.toolBar.addWidget(self.logout_button)

        spacer2 = QWidget()
        spacer2.setFixedWidth(20)
        self.toolBar.addWidget(spacer2)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.toolBar)
        self.setLayout(self.layout)

    def updateToolBar(self, page_name, user_full_name):
        if page_name == "Login":
            for item in [
                self,
                self.dashboard_label,
                self.avatar,
                self.name_label,
                self.logout_button,
            ]:
                item.setVisible(False)
            return
        else:
            for item in [
                self,
                self.dashboard_label,
                self.avatar,
                self.name_label,
                self.logout_button,
            ]:
                item.setVisible(True)
        self.dashboard_label.setText(page_name)
        self.avatar.setText(
            getLastNameFromFullName(user_full_name)[0].upper() if user_full_name else ""
        )
        self.name_label.setText(
            "Dr. " + getLastNameFromFullName(user_full_name) if user_full_name else ""
        )

    def logoffClicked(self):
        dlg = QMessageBox()
        dlg.setWindowTitle("Log Off")
        dlg.setText("Are you sure you want to log off?")
        dlg.addButton("Yes", QMessageBox.ButtonRole.YesRole)
        dlg.addButton("No", QMessageBox.ButtonRole.NoRole)
        for button in dlg.findChild(QDialogButtonBox).findChildren(QPushButton):
            button.setCursor(Qt.CursorShape.PointingHandCursor)

        dlg.setStyleSheet(
            """
                QMessageBox {
                    background-color: #ffffff; border-radius: 20px
                }
            """
        )

        dlg.setFont(QFont("Avenir", 15))
        button = dlg.exec()

        # Yes button is pressed
        if button == 0:
            # link to login page
            self.updateUsername("")
            self.showLoginWindow()

    def updateUsername(self, username):
        self.parent().parent().updateUsername(username)

    def showLoginWindow(self):
        self.parent().parent().showLoginWindow()

    def userProfileClick(self, s):
        return

    