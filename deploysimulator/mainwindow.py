#!/usr/bin/env python3

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QAction, QApplication, QDockWidget,
                              QMainWindow, QMessageBox, QListWidget)
                              
from .sensors import Sensors
from .console import Console
from .simulation import Simulation

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.createActions()
        self.createMenus()
        self.createStatusBar()
        self.createDockWindows()

        self.setWindowTitle("Deploy Simulator")

    def about(self):
        QMessageBox.about(self, "About DeploySimulator",
                "The <b>DeploySimulator</b> uses to simulate the environment "
                "of wireless sendor networks, with numberous sensors.")

    def changeEnvironment(self, environment):
        if not environment:
            return
        environmentList = environment.split(', ')
        for i in environmentList[:]:
            print("changeEnvironment-->"+i)

    def createActions(self):
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                statusTip="Exit the application", triggered=self.close)

        self.aboutAct = QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QApplication.instance().aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addSeparator();
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = self.menuBar().addMenu("&View")

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createDockWindows(self):
        dock = QDockWidget("Sensors", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.sensors= Sensors(dock)
        dock.setWidget(self.sensors)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())

        dock = QDockWidget("Environment", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.environmentList = QListWidget(dock)
        self.environmentList.addItems((
            "Omnidirectional Sensor Networks",
            "Directional Sensor Networks",
            "Directional Path Tracking",
            "Big Target Coverage"))
        dock.setWidget(self.environmentList)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())

        dock = QDockWidget("Simulation", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.simulation= Simulation(dock)
        dock.setWidget(self.simulation)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())

        dock = QDockWidget("Console", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.console= Console(dock)
        dock.setWidget(self.console)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())
        self.console.applyButton.clicked.connect(self.applyButtonState)
        self.console.playButton.clicked.connect(self.playButtonState)
        self.console.pauseButton.clicked.connect(self.pauseButtonState)

        self.environmentList.currentTextChanged.connect(self.changeEnvironment)
        
    def applyButtonState(self):
        
        if self.console.applyButton.isChecked():
            pass
        else:
            self.simulation.initialization(float(self.sensors.radDownText1.text()), 
                                           float(self.sensors.radUpText1.text()), 
                                           int(self.sensors.angDownText.text()), 
                                           int(self.sensors.angUpText.text()), 
                                           int(self.sensors.numText1.text()), 
                                           float(self.sensors.radDownText2.text()), 
                                           float(self.sensors.radUpText2.text()), 
                                           int(self.sensors.numText2.text()))
    
    def playButtonState(self):
        
        if self.console.playButton.isChecked():     
            pass
        else:
            self.simulation.setAnimating(True)
            print('play button clicked')
            
    def pauseButtonState(self):
        
        if self.console.pauseButton.isChecked():
            pass
        else:
            self.simulation.setAnimating(False)
            print('pause button clicked')
    
    def adjustButtonState(self):
        
        if self.console.adjustButton.isChecked():
            pass
        else:
            self.simulation.setTime(float(self.console.speedSpin.text()))
