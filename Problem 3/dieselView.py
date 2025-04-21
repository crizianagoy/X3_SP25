# dieselView.py

from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class DieselCycleView(QtWidgets.QWidget):
    """
    View class for the Diesel Cycle Simulator GUI.

    Manages the layout, input fields, output fields, calculation button,
    and embeds a Matplotlib canvas for plotting the P-v diagram.
    """

    def __init__(self):
        """
        Initialize the DieselCycleView widget by setting up the user interface.
        """
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Creates and organizes all UI components including inputs, outputs,
        buttons, and plot area inside layouts.
        """
        # --- Window Settings ---
        self.setWindowTitle('Diesel Cycle Simulator')
        self.setGeometry(100, 100, 1000, 700)

        # --- Layouts ---
        mainLayout = QtWidgets.QVBoxLayout(self)     # Main vertical layout
        inputLayout = QtWidgets.QFormLayout()         # Form layout for input fields
        buttonLayout = QtWidgets.QHBoxLayout()        # Horizontal layout for buttons
        outputLayout = QtWidgets.QFormLayout()        # Form layout for output fields

        # --- Input Fields ---
        self.r_input = QtWidgets.QLineEdit('18')      # Compression ratio input
        self.rc_input = QtWidgets.QLineEdit('2')      # Cutoff ratio input
        self.T1_input = QtWidgets.QLineEdit('300')    # Initial temperature input (K)
        self.P1_input = QtWidgets.QLineEdit('0.1')    # Initial pressure input (MPa)

        self.unitToggle = QtWidgets.QComboBox()       # Unit system toggle dropdown
        self.unitToggle.addItems(['SI', 'English'])   # Default units options

        # Add input fields to the input layout
        inputLayout.addRow('Compression Ratio (r):', self.r_input)
        inputLayout.addRow('Cutoff Ratio (rc):', self.rc_input)
        inputLayout.addRow('T1 (K):', self.T1_input)
        inputLayout.addRow('P1 (MPa):', self.P1_input)
        inputLayout.addRow('Units:', self.unitToggle)

        # --- Calculate Button ---
        self.calcButton = QtWidgets.QPushButton('Calculate')
        buttonLayout.addWidget(self.calcButton)

        # --- Output Fields ---
        self.T2_output = QtWidgets.QLineEdit()  # Temperature after compression
        self.P2_output = QtWidgets.QLineEdit()  # Pressure after compression
        self.T3_output = QtWidgets.QLineEdit()  # Temperature after heat addition
        self.P3_output = QtWidgets.QLineEdit()  # Pressure after heat addition
        self.T4_output = QtWidgets.QLineEdit()  # Temperature after expansion
        self.P4_output = QtWidgets.QLineEdit()  # Pressure after expansion
        self.efficiency_output = QtWidgets.QLineEdit()  # Cycle thermal efficiency

        # Set output fields as read-only (user cannot edit results manually)
        for widget in [self.T2_output, self.P2_output, self.T3_output,
                       self.P3_output, self.T4_output, self.P4_output, self.efficiency_output]:
            widget.setReadOnly(True)

        # Add output fields to the output layout
        outputLayout.addRow('T2 (K):', self.T2_output)
        outputLayout.addRow('P2 (MPa):', self.P2_output)
        outputLayout.addRow('T3 (K):', self.T3_output)
        outputLayout.addRow('P3 (MPa):', self.P3_output)
        outputLayout.addRow('T4 (K):', self.T4_output)
        outputLayout.addRow('P4 (MPa):', self.P4_output)
        outputLayout.addRow('Efficiency (%):', self.efficiency_output)

        # --- Plotting Area ---
        self.figure, self.ax = plt.subplots()        # Create a Matplotlib figure and axis
        self.canvas = FigureCanvas(self.figure)      # Embed the Matplotlib figure into Qt

        # --- Assemble the Layouts ---
        mainLayout.addLayout(inputLayout)             # Add input layout
        mainLayout.addLayout(buttonLayout)            # Add button layout
        mainLayout.addLayout(outputLayout)            # Add output layout
        mainLayout.addWidget(self.canvas)             # Add plotting canvas at the bottom
