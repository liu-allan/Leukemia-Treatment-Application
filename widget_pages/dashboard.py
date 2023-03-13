from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
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
from matlab_script import runModel


class TabShowGraph(QMainWindow):
    def __init__(self):
        super().__init__()

        widget = QWidget()
        self.graphLayout = QVBoxLayout()

        self.graphWidget = pg.PlotWidget()
        self.graphLayout.addWidget(self.graphWidget)

        self.graphWidget.setCursor(Qt.CursorShape.OpenHandCursor)
        # Temp data -> will connect to matlab in the future
        # day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # anticipatory_neutraphil_count = [-10, 1, 10, -4, 15, -12, 20, 8, -17, 3]
        # reactive_neutraphil_count = [-25, 5, 15, -15, 4, -22, -7, 25, 13, 0]
        self.boundary_positive = []
        self.boundary_negative = []
        self.day = []
        self.anticipatory_anc = []
        self.reactive_anc = []
        self.anticipatory_dosage = []
        self.reactive_dosage = []
        
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
        self.graphWidget.setYRange(0, 6, padding=0)

        # Creating tables for dosages
        # ant_dosages = [50, 30, 100, 25, 30, 80, 50]
        # self.anticipatory_dosage_title = QLabel("Anticipatory dosages")
        # self.anticipatory_dosage_title.setFont(QFont("Avenir", 15))
        # self.anticipatory_dosage_title.setMargin(5)
        # self.anticipatory_dosage_table = self.createTable(2, 8, ant_dosages)
        # self.graphLayout.addWidget(self.anticipatory_dosage_title)
        # self.graphLayout.addWidget(self.anticipatory_dosage_table)

        # reac_dosages = [10, 30, 40, 20, 79, 84, 24]
        # self.reactive_dosage_title = QLabel("Reactive dosages")
        # self.reactive_dosage_title.setFont(QFont("Avenir", 15))
        # self.reactive_dosage_title.setMargin(5)
        # self.reactive_dosage_table = self.createTable(2, 8, reac_dosages)
        # self.graphLayout.addWidget(self.reactive_dosage_title)
        # self.graphLayout.addWidget(self.reactive_dosage_table)

        widget.setLayout(self.graphLayout)
        self.setCentralWidget(widget)

    def plotANCGraph(self):
        self.plot(self.day, self.anticipatory_anc, "Anticipatory", "r")
        self.plot(self.day, self.reactive_anc, "Reactive", "b")

        self.plot_straight(self.day, self.boundary_positive, "Neutraphil Top Boundary", "#4a707a")
        self.plot_straight(self.day, self.boundary_negative, "Neutraphil Bottom Boundary", "#4a707a")
    
    def createDosageTable(self):
        # ant_dosages = [50, 30, 100, 25, 30, 80, 50]
        self.anticipatory_dosage_title = QLabel("Anticipatory dosages")
        self.anticipatory_dosage_title.setFont(QFont("Avenir", 15))
        self.anticipatory_dosage_title.setMargin(5)
        self.anticipatory_dosage_table = self.createTable(2, len(self.anticipatory_dosage) + 1, self.anticipatory_dosage)
        self.graphLayout.addWidget(self.anticipatory_dosage_title)
        self.graphLayout.addWidget(self.anticipatory_dosage_table)

        self.reactive_dosage_title = QLabel("Reactive dosages")
        self.reactive_dosage_title.setFont(QFont("Avenir", 15))
        self.reactive_dosage_title.setMargin(5)
        self.reactive_dosage_table = self.createTable(2, len(self.reactive_dosage) + 1, self.reactive_dosage)
        self.graphLayout.addWidget(self.reactive_dosage_title)
        self.graphLayout.addWidget(self.reactive_dosage_table)

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

        # Row count
        self.tableWidget.setRowCount(row)

        # Column count
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
                    item = QTableWidgetItem("{:.2f}".format(dosages_list[j - 1]))
                    item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.tableWidget.setItem(i, j, item)

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)

        # Table will fit the screen horizontally
        self.tableWidget.verticalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        return self.tableWidget

    def setGraphTableData(self, reactive_anc, anticipatory_anc, reactive_dosage, anticipatory_dosage):
        # set graph and table parameters
        self.day = [i + 1 for i in range(len(reactive_anc))]
        self.boundary_positive = [2 for _ in range(len(self.day))]
        self.boundary_negative = [1 for _ in range(len(self.day))]
        self.anticipatory_anc = anticipatory_anc
        self.reactive_anc = reactive_anc
        self.anticipatory_dosage = anticipatory_dosage
        self.reactive_dosage = reactive_dosage

        # plot anc graph
        self.plotANCGraph()

        # create dosage table
        self.createDosageTable()

class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.patient = None

        layout = QVBoxLayout()

        # Side tabs
        self.tabs = QTabWidget()

        self.tabs.tabBar().setCursor(Qt.CursorShape.PointingHandCursor)

        # TODO horizontal text tabBar

        self.graph = TabShowGraph()
        self.tabs.addTab(self.graph, "Model Output")
        self.tabs.addTab(QWidget(), "Patient List")
        self.tabs.addTab(QWidget(), "Change Parameter")

        self.tabs.currentChanged.connect(self.tabBarClicked)

        self.tabs.setTabPosition(QTabWidget.TabPosition.West)

        layout.addWidget(self.tabs)

        self.setLayout(layout)

    # Setting currentIndex to 0 so that whenever the user navigates back to the dashboard
    # it will always show the graph tab
    def tabBarClicked(self, tabIndex):
        if tabIndex == 1:
            self.tabs.setCurrentIndex(0)
            self.showPatientListWindow()
        elif tabIndex == 2:
            self.tabs.setCurrentIndex(0)
            self.showPatientInformationWindow()

    def updateUsername(self, username):
        self.parent().parent().updateUsername(username)

    def showLoginWindow(self):
        self.parent().parent().showLoginWindow()

    def showPatientListWindow(self):
        self.parent().parent().showPatientListWindow()

    def showPatientInformationWindow(self):
        self.parent().parent().showPatientInformationWindow()

    def updatePatientInfo(self, calculation_info):
        self.patient = self.parent().parent().selected_patient
        if calculation_info[0]:
            self.runMatLabModel(self.patient, calculation_info[1])

    def runMatLabModel(self, patient, num_cycles):
        # currently, run 1 cycle into the future, we can make this an option later
        bsa = float(patient.bsa)
        num_cycles = float(num_cycles + 1)
        dosage = [float(patient.dosageMeasurement[-1][0])]
        anc = [float(patient.ancMeasurement[-1][0])]
        print(bsa, num_cycles, dosage, anc)
        print("running model for {} cycles...".format(num_cycles))
        _, _, _, reactive_anc, anticipatory_anc, reactive_dosage, anticipatory_dosage = runModel(bsa, num_cycles, dosage, anc)
        print("finished running model")
        self.graph.setGraphTableData(reactive_anc, anticipatory_anc, reactive_dosage, anticipatory_dosage)