import sys

import numpy as np
import pyqtgraph as pg
from PySide6 import QtWidgets
from PySide6.QtCore import Slot

from OceanOptics.controller import OceanOpticsController

# PyQtGraph global options
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")


class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        vbox = QtWidgets.QVBoxLayout(central_widget)
        self.plot_widget = pg.PlotWidget()
        vbox.addWidget(self.plot_widget)
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)

        self.controller = OceanOpticsController()
        self.controller.plot()

    # @Slot()
    # def plot(self):
    #    ...


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
