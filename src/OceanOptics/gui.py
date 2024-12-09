import sys
import threading
import time

import matplotlib.pyplot as plt
import numpy as np
import pyqtgraph as pg
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Slot

from OceanOptics.Experiment import OceanOpticsController

# PyQtGraph global options
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")


class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        self.controller = OceanOpticsController()

        vbox = QtWidgets.QVBoxLayout(central_widget)
        self.plot_widget = pg.PlotWidget()
        vbox.addWidget(self.plot_widget)
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)

        self.initial_plot()

        start_button = QtWidgets.QPushButton("Start measurement")
        hbox.addWidget(start_button)

        stop_button = QtWidgets.QPushButton("Stop measurement")
        hbox.addWidget(stop_button)

        start_button.clicked.connect(self.run)
        stop_button.clicked.connect(self.pause)

        self.int_time_spinbox = QtWidgets.QDoubleSpinBox()
        self.int_time_spinbox.setPrefix("Integration time (s): ")
        self.int_time_spinbox.setMaximum(10)
        self.int_time_spinbox.setMinimum(0.01)
        self.int_time_spinbox.setSingleStep(0.01)
        self.int_time_spinbox.setValue(0.1)
        hbox.addWidget(self.int_time_spinbox)

        start_button.clicked.connect(self.run)
        stop_button.clicked.connect(self.pause)

        # self.controller.start_scan()

        # # Plot timer
        # self.plot_timer = QtCore.QTimer()
        # # Roep iedere 1 ms de plotfunctie aan
        # self.plot_timer.timeout.connect(self.plot)
        # self.plot_timer.start(1)

        self.show()

    def plot(self):
        """This method clears the plot widget and displays the experimental data."""
        self.plot_widget.clear()

        self.controller._scan_thread.join()

        values = self.controller.data(self.int_time_spinbox.value() * 1000000)

        pixels = []
        a = 187.047120
        b = 0.462711
        c = -2.483961e-005
        d = -3.224254e-010
        pixels = []
        for i in range(len(values)):
            y = a + b * i + c * (i) ** 2 + d * (i) ** 3
            pixels.append(y)
        for i in range(32):
            del pixels[0]
            del values[0]
        for i in range(6):
            del pixels[-1]
            del values[-1]

        self.plot_widget.plot(pixels, values, symbol="o", symbolSize=4, pen=None)

        self.plot_widget.setLabel("left", "Intensity")
        self.plot_widget.setLabel("bottom", "Wavelength (nm)")
        self.plot_widget.setTitle("Spectrum")

    def initial_plot(self):
        """This method shows an initial empty plot window. An empty measurement is created as a default."""
        pixels, values = [[], []]

        self.plot_widget.plot(pixels, values, symbol="o", symbolSize=4, pen=None)

        self.plot_widget.setLabel("left", "Intensity")
        self.plot_widget.setLabel("bottom", "pixels")
        self.plot_widget.setTitle("Spectrum")

    def run(self):
        self.controller.start_scan()

        # Plot timer
        self.plot_timer = QtCore.QTimer()
        # Roep iedere 1 ms de plotfunctie aan
        self.plot_timer.timeout.connect(self.plot)
        self.plot_timer.start(1)

    def pause(self):
        if self.controller.running:
            self.controller.stop_scan()

            self.plot_timer.stop()

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
