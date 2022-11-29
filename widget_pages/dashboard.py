from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QToolBar, QTabWidget, QSizePolicy, QTabBar, QGridLayout, QMainWindow
from PyQt6.QtGui import QAction, QIcon, QPalette, QColor, QFont
from PyQt6.QtCore import Qt
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

# class Color(QWidget):

#     def __init__(self, color):
#         super(Color, self).__init__()
#         self.setAutoFillBackground(True)

#         palette = self.palette()
#         palette.setColor(QPalette.ColorRole.Window, QColor(color))
#         self.setPalette(palette)

class TabShowGraph(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        day = [1,2,3,4,5,6,7,8,9,10]
        anticipatory_neutraphil_count = [-10,1,10,-4,15,-12,20,8,-17,3]
        reactive_neutraphil_count = [-25,5,15,-15,4,-22,-7,25,13,0]
        boundary_positive = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20]
        boundary_negative = [-20, -20, -20, -20, -20, -20, -20, -20, -20, -20]

        #Add Background colour to white
        self.graphWidget.setBackground('w')
        # Add Title
        self.graphWidget.setTitle("Neutraphil Count (Anticipatory vs. Reactive)", color="#000000", size="25pt", font="Avenir")
        # Add Axis Labels
        styles = {"color": "#000000", "font-size": "20px", "font":"Avenir"}
        self.graphWidget.setLabel("left", "Neutraphil Count ()", **styles)
        self.graphWidget.setLabel("bottom", "Day (days)", **styles)
        #Add legend
        self.graphWidget.addLegend()
        #Add grid
        self.graphWidget.showGrid(x=True, y=True)
        #Set Range
        self.graphWidget.setXRange(0, 11, padding=0)
        self.graphWidget.setYRange(-35, 35, padding=0)

        self.plot(day, anticipatory_neutraphil_count, "Anticipatory", 'r')
        self.plot(day, reactive_neutraphil_count, "Reactive", 'b')

        self.plot_straight(day, boundary_positive, "Neutraphil Top Boundary", '#4a707a')
        self.plot_straight(day, boundary_negative, "Neutraphil Bottom Boundary", '#4a707a')

    def plot(self, x, y, plotname, color):
        pen = pg.mkPen(color=color, width=5)
        self.graphWidget.plot(x, y, name=plotname, pen=pen, symbol='o', symbolSize=7, symbolBrush=(color))
    
    def plot_straight(self, x, y, plotname, color):
        pen = pg.mkPen(color=color, width=7, style=Qt.PenStyle.DashLine)
        self.graphWidget.plot(x, y, name=plotname, pen=pen, symbolBrush=(color))
    
    def main():
        main = TabShowGraph()
        main.show()

class TabPatientList(QWidget):
    def __init__(self):
        super().__init__()

        print("inside patient list")

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
        toolBar.setStyleSheet("background-color: #a9c7c5; height : 50; border-radius: 10px")
        layout.addWidget(toolBar)

        dashboard_label = QLabel("Dashboard")
        dashboard_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        dashboard_label.setFont(QFont('Avenir', 25))
        dashboard_label.setMargin(10)
        toolBar.addWidget(dashboard_label)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        toolBar.addWidget(spacer)
        
        user_name = QPushButton("AX", self)
        user_name.setCursor(Qt.CursorShape.PointingHandCursor)
        user_name.clicked.connect(self.userProfileClick)
        user_name.setFont(QFont('Avenir', 15))
        user_name.setFixedHeight(40)
        user_name.setFixedWidth(40)
        
        # https://stackoverflow.com/questions/12734319/change-rectangular-qt-button-to-round
        user_name.setStyleSheet(""" QPushButton {
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
                                    }""")
  
        # setting radius and border
        toolBar.addWidget(user_name)

        name_label = QLabel("Dr. Anne Xie")
        name_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        name_label.setFont(QFont('Avenir', 20))
        name_label.setMargin(15)
        toolBar.addWidget(name_label)

        # Side tabs
        tabs = QTabWidget()

        tabs.setCursor(Qt.CursorShape.PointingHandCursor)

        # tabBars = QTabBar()
        # tabs.setTabBar(tabBars)

        # tabShowGraph = QLabel("Model Output2")
        # tabBars.setTabButton(0, QTabBar.ButtonPosition.LeftSide, tabShowGraph)
        # tabBars.setTabData(0, TabShowGraph())

        # tabPatientList = QLabel("Patient List2")
        # tabBars.setTabButton(1, QTabBar.ButtonPosition.LeftSide, tabPatientList)
        # tabBars.setTabData(1, TabPatientList())

        # tabs.setTabBar(tabBars)

        tabs.addTab(TabShowGraph(), "Model Output")
        tabs.addTab(TabPatientList(), "Patient List")
        tabs.addTab(TabChangeParameter(), "Change Parameter")
        tabs.addTab(TabLogOff(), "Log Off")

        tabs.setTabPosition(QTabWidget.TabPosition.West)
                
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


