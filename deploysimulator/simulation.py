#!/usr/bin/env python3

from PyQt5.QtWidgets import QFrame, QLabel, QGridLayout
from .painting import PWidgetGL

class Simulation(QFrame):
    def __init__(self, parent=None):
        super(Simulation, self).__init__(parent)
        
        frameStyle = QFrame.Sunken | QFrame.Panel
        
        self.integerLabel = QLabel()
        self.integerLabel.setFrameStyle(frameStyle)
        self.paint = PWidgetGL(self)
        
        layout = QGridLayout()
        layout.setColumnStretch(1, 1)
        layout.addWidget(self.paint, 0, 0)
        self.setLayout(layout)
        
        #self.paint.setAnimating(True)
        
    def setAnimating(self, animating):
        
        self.paint.setAnimating(animating)
        
    def initialization(self, radDown, radUp, angDown, angUp, num, TradDown, TradUp, Tnum):
        
        self.paint.initialization(radDown, radUp, angDown, angUp, num, TradDown, TradUp, Tnum)
    
    def setTime(self, time):
        
        self.paint.setTime(time)