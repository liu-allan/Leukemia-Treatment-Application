from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QToolBar,
    QTabWidget,
    QSizePolicy,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QDialogButtonBox,
    QHeaderView,
    QMainWindow,
)
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt
from pyqtgraph import plot
import pyqtgraph as pg

from widget_pages.toolbar import ToolBar
from widget_pages.sidebar import SideBar


class TabShowGraph(QWidget):
    def __init__(self):
        super().__init__()
        
        self.graphLayout = QVBoxLayout()

        self.graphWidget = pg.PlotWidget()
        self.graphLayout.addWidget(self.graphWidget)

        self.graphWidget.setCursor(Qt.CursorShape.OpenHandCursor)
        day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        anticipatory_neutraphil_count = [-10, 1, 10, -4, 15, -12, 20, 8, -17, 3]
        reactive_neutraphil_count = [-25, 5, 15, -15, 4, -22, -7, 25, 13, 0]
        boundary_positive = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20]
        boundary_negative = [-20, -20, -20, -20, -20, -20, -20, -20, -20, -20]

        # Add Background colour to white
        self.graphWidget.setBackground("w")
        # Add Title
        self.graphWidget.setTitle(
            "Neutraphil Count (Anticipatory vs. Reactive)",
            color="#000",
            font=QFont("Avenir", 20),
            size="20pt",
        )
        # Add Axis Labels
        styles = {"color": "#000000", "font": QFont("Avenir", 25), "font-size": "25px"}
        self.graphWidget.setLabel("left", "Neutraphil Count", **styles)
        self.graphWidget.setLabel("bottom", "Day (days)", **styles)
        # Add legend
        self.graphWidget.addLegend()
        # Add grid
        self.graphWidget.showGrid(x=True, y=True)
        # Set Range
        self.graphWidget.setXRange(0, 11, padding=0)
        self.graphWidget.setYRange(-35, 35, padding=0)

        self.plot(day, anticipatory_neutraphil_count, "Anticipatory", "r")
        self.plot(day, reactive_neutraphil_count, "Reactive", "b")

        self.plot_straight(day, boundary_positive, "Neutraphil Top Boundary", "#4a707a")
        self.plot_straight(
            day, boundary_negative, "Neutraphil Bottom Boundary", "#4a707a"
        )

        # Creating tables for dosages
        ant_dosages = [50, 30, 100, 25, 30, 80, 50]
        self.anticipatory_dosage_title = QLabel("Anticipatory dosages")
        self.anticipatory_dosage_title.setFont(QFont("Avenir", 15))
        self.anticipatory_dosage_title.setMargin(5)
        self.anticipatory_dosage = self.createTable(2, 8, ant_dosages)
        self.graphLayout.addWidget(self.anticipatory_dosage_title)
        self.graphLayout.addWidget(self.anticipatory_dosage)

        reac_dosages = [10, 30, 40, 20, 79, 84, 24]
        self.reactive_dosage_title = QLabel("Reactive dosages")
        self.reactive_dosage_title.setFont(QFont("Avenir", 15))
        self.reactive_dosage_title.setMargin(5)
        self.reactive_dosage = self.createTable(2, 8, reac_dosages)
        self.graphLayout.addWidget(self.reactive_dosage_title)
        self.graphLayout.addWidget(self.reactive_dosage)

        self.setLayout(self.graphLayout)

    def plot(self, x, y, plotname, color):
        pen = pg.mkPen(color=color, width=5)
        self.graphWidget.plot(
            x, y, name=plotname, pen=pen, symbol="o", symbolSize=7, symbolBrush=(color)
        )

    def plot_straight(self, x, y, plotname, color):
        pen = pg.mkPen(color=color, width=5, style=Qt.PenStyle.DashLine)
        self.graphWidget.plot(x, y, name=plotname, pen=pen, symbolBrush=(color))
    
    def createTable(self, row, column, dosages_list):
        self.tableWidget = QTableWidget()

        self.tableWidget.setStyleSheet(
            """ QTableWidget {
                border: 1px solid #000;
                gridline-color: 1px solid #000;
            }"""
        )

        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(column)

        item = QTableWidgetItem("Day")
        item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setBackground(QColor("#bfd8d2"))
        self.tableWidget.setItem(0, 0, item)

        item = QTableWidgetItem("Dosages (mg)")
        item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setBackground(QColor("#bfd8d2"))
        self.tableWidget.setItem(1, 0, item)

        for i in range(row):
            for j in range(1, column):

                if i == 0:
                    item = QTableWidgetItem(str(j))
                    item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    item.setBackground(QColor("#bfd8d2"))
                    self.tableWidget.setItem(i, j, item)
                elif i == 1:
                    item = QTableWidgetItem(str(dosages_list[j - 1]))
                    item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.tableWidget.setItem(i, j, item)

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)

        self.tableWidget.verticalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        return self.tableWidget

class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.patient = None

        self.sideBarLayout = QHBoxLayout()
        self.sideBarLayout.setContentsMargins(10, 0, 10, 0)

        self.sideBar = SideBar("Dashboard")
        self.sideBarLayout.addWidget(self.sideBar, 1)

        self.graphs = TabShowGraph()
        self.sideBarLayout.addWidget(self.graphs, 19)

        self.setLayout(self.sideBarLayout)

    def updateUsername(self, username):
        self.parent().parent().updateUsername(username)

    def showLoginWindow(self):
        self.parent().parent().showLoginWindow()

    def showPatientListWindow(self):
        self.parent().parent().showPatientListWindow()

    def showPatientInformationWindow(self):
        self.parent().parent().showPatientInformationWindow()

    def updatePatientInfo(self):
        self.patient = self.parent().parent().selected_patient
    
    def backButtonClicked(self):
        self.showPatientListWindow()
    
    def dashboardButtonClicked(self):
        return
    
    def patientInformationButtonClicked(self):
        self.showPatientInformationWindow()

    def logoffButtonClicked(self):
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
            self.dosageEdit.clear()
            self.ancMeasurementEdit.clear()
            # link to login page
            self.updateUsername("")
            self.showLoginWindow()
