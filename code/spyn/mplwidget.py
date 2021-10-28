from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

class MplWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())
        self.toolbarr = NavigationToolbar(self.canvas, self)
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.canvas)
        vlayout.addWidget(self.toolbarr)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vlayout)