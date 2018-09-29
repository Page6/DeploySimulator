# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets

from .mainwindow import MainWindow

class DeploySimulator(QtWidgets.QApplication):

    def __init__(self):
        super(DeploySimulator, self).__init__(sys.argv)
        self.setOrganizationName('DeploySimulator')
        self.setApplicationName('DeploySimulator')
        self.window = MainWindow()

    def run(self):
        self.window.show()
        print('DeploySimulator run......')
        sys.exit(self.exec_())
