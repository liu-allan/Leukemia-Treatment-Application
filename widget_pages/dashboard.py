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
from PyQt6.QtGui import QColor, QFont, QMovie
from PyQt6.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot
from pyqtgraph import plot
import pyqtgraph as pg

from widget_pages.toolbar import ToolBar
from matlab_script import runModel
from util.util import clearLayout
from widget_pages.sidebar import SideBar


class TabShowGraph(QWidget):
    def __init__(self):
        super().__init__()

        self.graphLayout = QVBoxLayout()

        self.noResultsWidget = QLabel("No Results", self)
        self.noResultsWidget.setFont(QFont("Avenir", 24))
        self.noResultsWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.noResultsWidget.setAlignment(Qt.AlignCenter)
        self.noResultsWidget.setVisible(False)

        self.loadingWidget = QWidget(self)
        self.loadingLayout = QVBoxLayout()

        self.loadingTextWidget = QLabel("Performing Simulations...", self)
        self.loadingTextWidget.setFont(QFont("Avenir", 24))
        self.loadingTextWidget.setAlignment(Qt.AlignCenter)
        self.loadingTextWidget.setVisible(False)

        self.loadingMovieWidget = QLabel(self)
        movie = QMovie("icons/loading.gif")
        self.loadingMovieWidget.setMovie(movie)
        self.loadingMovieWidget.setMinimumWidth(100)
        self.loadingMovieWidget.setAlignment(Qt.AlignCenter)
        self.loadingMovieWidget.setVisible(False)
        movie.start()

        self.loadingLayout.addWidget(self.loadingTextWidget)
        self.loadingLayout.setAlignment(self.loadingTextWidget, Qt.AlignCenter)
        self.loadingLayout.addWidget(self.loadingMovieWidget)
        self.loadingLayout.setAlignment(self.loadingMovieWidget, Qt.AlignCenter)
        self.loadingWidget.setLayout(self.loadingLayout)
        self.loadingWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.loadingWidget.setVisible(False)

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
            "Neutrophil Count (Anticipatory vs. Reactive)",
            color="#000",
            font=QFont("Avenir", 20),
            size="20pt",
        )
        # Add Axis Labels
        styles = {"color": "#000000", "font": QFont("Avenir", 25), "font-size": "25px"}
        self.graphWidget.setLabel(
            "left", "Neutrophil Count (# Cells/L) x 1e9", **styles
        )
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

        self.graphLayout.addWidget(self.loadingWidget)
        self.graphLayout.addWidget(self.noResultsWidget)
        self.graphLayout.addWidget(self.graphContainer)
        self.graphLayout.addWidget(self.dosageTableWidget)

        self.setGraphTableData(None, None, None, None)

        self.anticipatory_dosage_title.setVisible(False)
        self.anticipatory_dosage_table.setVisible(False)
        self.reactive_dosage_title.setVisible(False)
        self.reactive_dosage_table.setVisible(False)

        self.setLayout(self.graphLayout)

    def plotANCGraph(self):
        pen = pg.mkPen(color="r", width=5)
        self.ant_plot = self.graphWidget.plot(
            self.day,
            self.anticipatory_anc,
            name="Anticipatory",
            pen=pen,
            symbol="o",
            symbolSize=7,
            symbolBrush=("r"),
        )
        pen = pg.mkPen(color="b", width=5)
        self.rea_plot = self.graphWidget.plot(
            self.day,
            self.reactive_anc,
            name="Reactive",
            pen=pen,
            symbol="o",
            symbolSize=7,
            symbolBrush=("b"),
        )

        pen = pg.mkPen(color="#4a707a", width=5, style=Qt.PenStyle.DashLine)
        self.pos_plot = self.graphWidget.plot(
            self.day,
            self.boundary_positive,
            name="Neutrophil Top Boundary",
            pen=pen,
            symbolBrush=("#4a707a"),
        )
        pen = pg.mkPen(color="#4a707a", width=5, style=Qt.PenStyle.DashLine)
        self.neg_plot = self.graphWidget.plot(
            self.day,
            self.boundary_negative,
            name="Neutrophil Bottom Boundary",
            pen=pen,
            symbolBrush=("#4a707a"),
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
        if self.day:
            self.graphWidget.setXRange(0, len(self.day), padding=0)

    def updateDosageTable(self):
        clearLayout(self.dosageTableLayout)

        self.anticipatory_dosage_title = QLabel("Anticipatory dosages")
        self.anticipatory_dosage_title.setFont(QFont("Avenir", 15))
        self.anticipatory_dosage_title.setMargin(5)
        self.anticipatory_dosage_table = self.createTable(
            2, len(self.anticipatory_dosage) + 1, self.anticipatory_dosage
        )

        self.reactive_dosage_title = QLabel("Reactive dosages")
        self.reactive_dosage_title.setFont(QFont("Avenir", 15))
        self.reactive_dosage_title.setMargin(5)
        self.reactive_dosage_table = self.createTable(
            2, len(self.reactive_dosage) + 1, self.reactive_dosage
        )

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

        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(column)

        item = QTableWidgetItem("Day")
        item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        item.setFont(QFont("Avenir", 18))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setBackground(QColor("#bfd8d2"))
        self.tableWidget.setItem(0, 0, item)

        item = QTableWidgetItem("Dosages (mg)")
        item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        item.setFont(QFont("Avenir", 18))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setBackground(QColor("#bfd8d2"))
        self.tableWidget.setItem(1, 0, item)

        self.tableWidget.setColumnWidth(0, 125)

        for i in range(row):
            for j in range(1, column):
                self.tableWidget.setColumnWidth(j, 125)

                if i == 0:
                    item = QTableWidgetItem(str(j))
                    item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                    item.setFont(QFont("Avenir", 18))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    item.setBackground(QColor("#bfd8d2"))
                    self.tableWidget.setItem(i, j, item)
                elif i == 1:
                    item = QTableWidgetItem("{:.2f}".format(dosages_list[j - 1]))
                    item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                    item.setFont(QFont("Avenir", 18))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.tableWidget.setItem(i, j, item)

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)

        self.tableWidget.verticalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Fixed
        )
        return self.tableWidget

    def setGraphTableData(
        self, reactive_anc, anticipatory_anc, reactive_dosage, anticipatory_dosage
    ):
        # set graph and table parameters
        if (
            reactive_anc
            and anticipatory_anc
            and reactive_dosage
            and anticipatory_dosage
        ):
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

    def showLoadingScreen(self, show):
        self.noResultsWidget.setVisible(False)

        if show:
            self.graphWidget.setVisible(not show)
            self.anticipatory_dosage_title.setVisible(not show)
            self.anticipatory_dosage_table.setVisible(not show)
            self.reactive_dosage_title.setVisible(not show)
            self.reactive_dosage_table.setVisible(not show)
            self.loadingWidget.setVisible(show)
            self.loadingMovieWidget.setVisible(show)
            self.loadingTextWidget.setVisible(show)
        else:
            self.loadingWidget.setVisible(show)
            self.loadingMovieWidget.setVisible(show)
            self.loadingTextWidget.setVisible(show)
            self.graphWidget.setVisible(not show)
            self.anticipatory_dosage_title.setVisible(not show)
            self.anticipatory_dosage_table.setVisible(not show)
            self.reactive_dosage_title.setVisible(not show)
            self.reactive_dosage_table.setVisible(not show)


class ModelTask(QObject):
    returned = pyqtSignal(list)
    finished = pyqtSignal()

    def __init__(self, bsa, num_cycles, dosage, anc):
        super().__init__()
        self.bsa = bsa
        self.num_cycles = num_cycles
        self.dosage = dosage
        self.anc = anc

    def run(self):
        print("running model for {} cycles...".format(self.num_cycles))
        _, _, ra, aa, rd, ad = runModel(
            self.bsa, self.num_cycles, self.dosage, self.anc
        )
        print("finished running model")
        self.returned.emit([ra, aa, rd, ad])
        self.finished.emit()


class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.patient = None
        self.displayed_patient = None

        self.model_thread = None
        self.model_task = None
        self.simulating_patient = None

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

    def updatePatientInfo(self, calculation_info):
        self.patient = self.parent().parent().selected_patient

        if (
            self.simulating_patient
            and self.simulating_patient.user_id == self.patient.user_id
        ):
            self.graphs.showLoadingScreen(True)
        else:
            self.graphs.showLoadingScreen(False)
            if calculation_info[0]:
                self.graphs.toggleResults(True)
                self.runMatLabModel(calculation_info[1])
                self.displayed_patient = self.patient
            elif (
                self.displayed_patient
                and self.displayed_patient.user_id == self.patient.user_id
                and self.simulating_patient == None
            ):
                self.graphs.toggleResults(True)
            else:
                self.graphs.toggleResults(False)

    @pyqtSlot(list)
    def displayGraphTable(self, info_list):
        self.simulating_patient = None
        self.graphs.setGraphTableData(
            info_list[0], info_list[1], info_list[2], info_list[3]
        )
        self.graphs.showLoadingScreen(False)
        self.sideBar.lockButtons(False)
        self.parent().parent().toolBar.lockLogoutButton(False)

    def runMatLabModel(self, num_cycles):
        bsa = float(self.patient.bsa)
        num_cycles = float(num_cycles + 1)
        dosage = [float(self.patient.dosageMeasurement[-1][0])]
        anc = [float(self.patient.ancMeasurement[-1][0])]

        print(bsa, num_cycles, dosage, anc)

        self.model_thread = QThread()
        self.model_task = ModelTask(bsa, num_cycles, dosage, anc)
        self.model_task.moveToThread(self.model_thread)

        self.model_thread.started.connect(self.model_task.run)
        self.model_task.returned.connect(self.displayGraphTable)
        self.model_task.finished.connect(self.model_thread.quit)
        self.model_task.finished.connect(self.model_task.deleteLater)
        self.model_thread.finished.connect(self.model_thread.deleteLater)

        self.model_thread.start()

        self.simulating_patient = self.patient

        self.graphs.showLoadingScreen(True)
        self.sideBar.lockButtons(True)
        self.parent().parent().toolBar.lockLogoutButton(True)

    def backButtonClicked(self):
        self.showPatientListWindow()

    def dashboardButtonClicked(self):
        return

    def patientInformationButtonClicked(self):
        self.showPatientInformationWindow()
