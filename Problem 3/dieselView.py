# dieselView.py
from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class DieselCycleView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Diesel Cycle Simulator')
        self.setGeometry(100, 100, 1000, 700)

        # Layouts
        mainLayout = QtWidgets.QVBoxLayout(self)
        inputLayout = QtWidgets.QFormLayout()
        buttonLayout = QtWidgets.QHBoxLayout()
        outputLayout = QtWidgets.QFormLayout()

        # Inputs
        self.r_input = QtWidgets.QLineEdit('18')
        self.rc_input = QtWidgets.QLineEdit('2')
        self.T1_input = QtWidgets.QLineEdit('300')
        self.P1_input = QtWidgets.QLineEdit('0.1')

        self.unitToggle = QtWidgets.QComboBox()
        self.unitToggle.addItems(['SI', 'English'])

        inputLayout.addRow('Compression Ratio (r):', self.r_input)
        inputLayout.addRow('Cutoff Ratio (rc):', self.rc_input)
        inputLayout.addRow('T1 (K):', self.T1_input)
        inputLayout.addRow('P1 (MPa):', self.P1_input)
        inputLayout.addRow('Units:', self.unitToggle)

        # Calculate Button
        self.calcButton = QtWidgets.QPushButton('Calculate')
        buttonLayout.addWidget(self.calcButton)

        # Outputs
        self.T2_output = QtWidgets.QLineEdit()
        self.P2_output = QtWidgets.QLineEdit()
        self.T3_output = QtWidgets.QLineEdit()
        self.P3_output = QtWidgets.QLineEdit()
        self.T4_output = QtWidgets.QLineEdit()
        self.P4_output = QtWidgets.QLineEdit()
        self.efficiency_output = QtWidgets.QLineEdit()

        for widget in [self.T2_output, self.P2_output, self.T3_output,
                       self.P3_output, self.T4_output, self.P4_output, self.efficiency_output]:
            widget.setReadOnly(True)

        outputLayout.addRow('T2 (K):', self.T2_output)
        outputLayout.addRow('P2 (MPa):', self.P2_output)
        outputLayout.addRow('T3 (K):', self.T3_output)
        outputLayout.addRow('P3 (MPa):', self.P3_output)
        outputLayout.addRow('T4 (K):', self.T4_output)
        outputLayout.addRow('P4 (MPa):', self.P4_output)
        outputLayout.addRow('Efficiency (%):', self.efficiency_output)

        # Plot
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        # Assemble
        mainLayout.addLayout(inputLayout)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addLayout(outputLayout)
        mainLayout.addWidget(self.canvas)
