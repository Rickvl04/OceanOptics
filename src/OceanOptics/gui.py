import sys

import matplotlib.pyplot as plt
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

        self.plot()

    def plot(self):
        """This method clears the plot widget and displays the experimental data."""
        self.plot_widget.clear()

        self.controller = OceanOpticsController()
        values = self.controller.data()

        pixels = []
        for i in range(len(values)):
            pixels.append(i)

        self.plot_widget.plot(pixels, values, symbol="o", symbolSize=5, pen=None)

        self.plot_widget.setLabel("left", "??")
        self.plot_widget.setLabel("bottom", "??")
        self.plot_widget.setTitle("Spectrum")

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
