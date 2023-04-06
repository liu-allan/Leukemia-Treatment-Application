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
from util.util import clearLayout


class TabShowGraph(QMainWindow):
    def __init__(self):
        super().__init__()

        widget = QWidget()
        self.graphLayout = QVBoxLayout()

        self.noResultsWidget = QLabel("No Results", self)
        self.noResultsWidget.setFont(QFont("Avenir", 24))
        self.noResultsWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.noResultsWidget.setAlignment(Qt.AlignCenter)
        self.noResultsWidget.setVisible(False)

        self.dosageTableWidget = QWidget()
        self.dosageTableLayout = QVBoxLayout()
        self.dosageTableWidget.setLayout(self.dosageTableLayout)

        self.boundary_positive = []
        self.boundary_negative = []
        self.day = []
        self.anticipatory_anc = []
        self.reactive_anc = []
        self.anticipatory_dosage = []
        self.reactive_dosage = []
        self.ant_plot = None
        self.rea_plot = None
        self.pos_plot = None
        self.neg_plot = None

        self.graphContainer = QWidget()
        self.graphContainer.setMinimumHeight(300)
        self.graphContainerLayout = QVBoxLayout(self.graphContainer)

        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setCursor(Qt.CursorShape.OpenHandCursor)
        
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
        self.graphWidget.setLabel("left", "Neutrophil Count (# Cells/L) x 1e9", **styles)
        self.graphWidget.setLabel("bottom", "Day (days)", **styles)
        # Add legend
        self.graphWidget.addLegend()
        # Add grid
        self.graphWidget.showGrid(x=True, y=True)
        # Set Range
        self.graphWidget.setXRange(0, 11, padding=0)
        self.graphWidget.setYRange(0, 6, padding=0)

        self.plotANCGraph()

        self.graphContainerLayout.addWidget(self.graphWidget)

        self.graphLayout.addWidget(self.noResultsWidget)
        self.graphLayout.addWidget(self.graphContainer)
        self.graphLayout.addWidget(self.dosageTableWidget)

        self.setGraphTableData(None, None, None, None)

        self.anticipatory_dosage_title.setVisible(False)
        self.anticipatory_dosage_table.setVisible(False)
        self.reactive_dosage_title.setVisible(False)
        self.reactive_dosage_table.setVisible(False)

        widget.setLayout(self.graphLayout)
        self.setCentralWidget(widget)

    def plotANCGraph(self):
        pen = pg.mkPen(color='r', width=5)
        self.ant_plot = self.graphWidget.plot(
            self.day, self.anticipatory_anc, name="Anticipatory", pen=pen, symbol="o", symbolSize=7, symbolBrush=('r')
        )
        pen = pg.mkPen(color='b', width=5)
        self.rea_plot = self.graphWidget.plot(
            self.day, self.reactive_anc, name="Reactive", pen=pen, symbol="o", symbolSize=7, symbolBrush=('b')
        )

        pen = pg.mkPen(color="#4a707a", width=5, style=Qt.PenStyle.DashLine)
        self.pos_plot = self.graphWidget.plot(
            self.day, self.boundary_positive, name="Neutraphil Top Boundary", pen=pen, symbolBrush=("#4a707a")
        )
        pen = pg.mkPen(color="#4a707a", width=5, style=Qt.PenStyle.DashLine)
        self.neg_plot = self.graphWidget.plot(
            self.day, self.boundary_negative, name="Neutraphil Bottom Boundary", pen=pen, symbolBrush=("#4a707a")
        )

    def updateANCGraph(self):
        if self.ant_plot:
            self.ant_plot.setData(self.day, self.anticipatory_anc)
        if self.rea_plot:
            self.rea_plot.setData(self.day, self.reactive_anc)
        if self.pos_plot:
            self.pos_plot.setData(self.day, self.boundary_positive)
        if self.neg_plot:
            self.neg_plot.setData(self.day, self.boundary_negative)

    def updateDosageTable(self):
        clearLayout(self.dosageTableLayout)

        self.anticipatory_dosage_title = QLabel("Anticipatory dosages")
        self.anticipatory_dosage_title.setFont(QFont("Avenir", 15))
        self.anticipatory_dosage_title.setMargin(5)
        self.anticipatory_dosage_table = self.createTable(2, len(self.anticipatory_dosage) + 1, self.anticipatory_dosage)

        self.reactive_dosage_title = QLabel("Reactive dosages")
        self.reactive_dosage_title.setFont(QFont("Avenir", 15))
        self.reactive_dosage_title.setMargin(5)
        self.reactive_dosage_table = self.createTable(2, len(self.reactive_dosage) + 1, self.reactive_dosage)

        self.dosageTableLayout.addWidget(self.anticipatory_dosage_title)
        self.dosageTableLayout.addWidget(self.anticipatory_dosage_table)
        self.dosageTableLayout.addWidget(self.reactive_dosage_title)
        self.dosageTableLayout.addWidget(self.reactive_dosage_table)

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
        if reactive_anc and anticipatory_anc and reactive_dosage and anticipatory_dosage:
            self.day = [i + 1 for i in range(len(reactive_anc))]
            self.boundary_positive = [2 for _ in range(len(self.day))]
            self.boundary_negative = [1 for _ in range(len(self.day))]
            self.anticipatory_anc = anticipatory_anc
            self.reactive_anc = reactive_anc
            self.anticipatory_dosage = anticipatory_dosage
            self.reactive_dosage = reactive_dosage
        else:
            self.day = []
            self.boundary_positive = []
            self.boundary_negative = []
            self.anticipatory_anc = []
            self.reactive_anc = []
            self.anticipatory_dosage = []
            self.reactive_dosage = []

        self.updateANCGraph()
        self.updateDosageTable()
    
    def toggleResults(self, show):
        self.noResultsWidget.setVisible(not show)
        self.graphWidget.setVisible(show)
        self.anticipatory_dosage_title.setVisible(show)
        self.anticipatory_dosage_table.setVisible(show)
        self.reactive_dosage_title.setVisible(show)
        self.reactive_dosage_table.setVisible(show)

class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.patient = None
        self.displayed_patient = None

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
            self.graph.toggleResults(True)
            self.runMatLabModel(calculation_info[1])
            self.displayed_patient = self.patient
        elif self.displayed_patient and self.displayed_patient.user_id == self.patient.user_id:
            self.graph.toggleResults(True)
        else:
            self.graph.toggleResults(False)

    def runMatLabModel(self, num_cycles):
        bsa = float(self.patient.bsa)
        num_cycles = float(num_cycles + 1)
        dosage = [float(self.patient.dosageMeasurement[-1][0])]
        anc = [float(self.patient.ancMeasurement[-1][0])]
        print(bsa, num_cycles, dosage, anc)
        print("running model for {} cycles...".format(num_cycles))
        _, _, _, reactive_anc, anticipatory_anc, reactive_dosage, anticipatory_dosage = runModel(bsa, num_cycles, dosage, anc)
        print("finished running model")
        self.graph.setGraphTableData(reactive_anc, anticipatory_anc, reactive_dosage, anticipatory_dosage)