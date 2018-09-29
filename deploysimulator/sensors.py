#!/usr/bin/env python3

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFrame, QPushButton,  QHBoxLayout, 
        QLabel, QGridLayout, QLineEdit)

class Sensors(QFrame):
    def __init__(self, parent=None):
        super(Sensors, self).__init__(parent)
        
        self.sensorLabel = QLabel("Sensor:")
        self.radLabel1 = QLabel("Radius Range:")
        self.angabel = QLabel("Angle Range:")
        self.numLabel1 = QLabel("Number of Sensors:")
        self.wavLabel1 = QLabel("~")
        self.wavLabel2 = QLabel("~")
        
        self.radDownText1 = QLineEdit("0.01")
        self.radUpText1 = QLineEdit("0.25")
        self.angDownText = QLineEdit("30")
        self.angUpText = QLineEdit("90")
        self.numText1 = QLineEdit("20")
        
        self.targetLabel = QLabel("Target:")
        self.radLabel2 = QLabel("Radius Range:")
        self.numLabel2 = QLabel("Number of Targets:")
        self.wavLabel3 = QLabel("~")
        
        self.radDownText2 = QLineEdit("0.5")
        self.radUpText2 = QLineEdit("1.0")
        self.numText2 = QLineEdit("1")
        
        layout = QGridLayout()
        
        layout.setRowStretch(1,5)
        layout.setRowStretch(2,20)
        layout.setRowStretch(3,20)
        layout.setRowStretch(4,5)
        layout.setRowStretch(5,20)
        layout.setRowStretch(6,20)
        layout.setRowStretch(7,20)
        
        layout.setColumnStretch(1,20)
        layout.setColumnStretch(1,20)
        layout.setColumnStretch(1,3)
        layout.setColumnStretch(1,20)
        
        layout.addWidget(self.sensorLabel, 0, 0)
        
        layout.addWidget(self.radLabel1, 1, 0)
        layout.addWidget(self.radDownText1, 1, 1)
        layout.addWidget(self.wavLabel1, 1, 2)
        layout.addWidget(self.radUpText1, 1, 3)
        
        layout.addWidget(self.angabel, 2, 0)
        layout.addWidget(self.angDownText, 2, 1)
        layout.addWidget(self.wavLabel2, 2, 2)
        layout.addWidget(self.angUpText, 2, 3)
        
        layout.addWidget(self.numLabel1, 3, 0)
        layout.addWidget(self.numText1, 3, 1)
        
        layout.addWidget(self.targetLabel, 4, 0)
        
        layout.addWidget(self.radLabel2, 5, 0)
        layout.addWidget(self.radDownText2, 5, 1)
        layout.addWidget(self.wavLabel3, 5, 2)
        layout.addWidget(self.radUpText2, 5, 3)
        
        layout.addWidget(self.numLabel2, 6, 0)
        layout.addWidget(self.numText2, 6, 1)
        
        self.setLayout(layout)
        