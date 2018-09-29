#!/usr/bin/env python3

from PyQt5.QtWidgets import (QFrame, QLabel, QPushButton,  QGridLayout,
        QSpinBox)
from PyQt5.QtCore import Qt

class Console(QFrame):
    def __init__(self, parent=None):
        super(Console, self).__init__(parent)
        
        self.applyButton = QPushButton("Apply")
        self.playButton = QPushButton("Play")
        self.pauseButton = QPushButton("Pause")
        
        self.speedLabel = QLabel("Speed:")
        self.speedLabel.setAlignment(Qt.AlignCenter|Qt.AlignRight)
        self.speedSpin = QSpinBox()
        self.speedSpin.setValue(10)
        self.adjustButton = QPushButton("Adjust")
        
        layout = QGridLayout()
        for i in range (6):
            layout.setColumnStretch(i, 10)
        
        layout.addWidget(self.applyButton, 0, 0)
        layout.addWidget(self.playButton, 0, 1)
        layout.addWidget(self.pauseButton, 0, 2)
        
        layout.addWidget(self.speedLabel, 0, 3)
        layout.addWidget(self.speedSpin, 0, 4)
        layout.addWidget(self.adjustButton, 0, 5)
        
        self.setLayout(layout)
