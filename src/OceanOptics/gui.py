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

        # self.controller = OceanOpticsController()
        # pixels = self.controller.data()

        # plt.clf()
        # plt.plot(pixels[20:])
        # print(pixels)
        # plt.show()

    def plot(self):
        """This method clears the plot widget and displays the experimental data."""
        self.plot_widget.clear()

        self.controller = OceanOpticsController()
        pixels = self.controller.data()

        self.plot_widget.plot(pixels[0], pixels[1], symbol="o", symbolSize=5, pen=None)

        self.plot_widget.setLabel("left", "I [Ampere]")
        self.plot_widget.setLabel("bottom", "U [Voltage]")
        self.plot_widget.setTitle("U-I")

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
