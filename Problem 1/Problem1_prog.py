import sys
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class RLC_GUI(QtWidgets.QWidget):
    """
    Main GUI class for simulating the transient response of a series RLC circuit.
    Allows user to input parameters, view a circuit diagram, and display the simulation results.
    """

    def __init__(self):
        """
        Initialize the RLC_GUI window with title, dimensions, and UI setup.
        """
        super().__init__()
        self.setWindowTitle('RLC Circuit Transient Simulator')
        self.setGeometry(100, 100, 1200, 700)
        self.initUI()

    def initUI(self):
        """
        Create and arrange all GUI components including input fields, circuit diagram, and plotting area.
        """
        # Create main vertical layout
        mainLayout = QtWidgets.QVBoxLayout(self)

        # Create top layout: user inputs and circuit diagram side-by-side
        topLayout = QtWidgets.QHBoxLayout()

        # Left Side: Input form for circuit parameters
        inputGroup = QtWidgets.QGroupBox("Circuit Parameters")
        inputLayout = QtWidgets.QFormLayout()

        # Input fields with default values
        self.R_edit = QtWidgets.QLineEdit('10')    # Resistance input
        self.L_edit = QtWidgets.QLineEdit('20')    # Inductance input
        self.C_edit = QtWidgets.QLineEdit('0.05')  # Capacitance input
        self.V0_edit = QtWidgets.QLineEdit('20')   # Voltage amplitude input
        self.freq_edit = QtWidgets.QLineEdit('20') # Angular frequency input
        self.phase_edit = QtWidgets.QLineEdit('0') # Phase input

        # Add labeled input fields to the layout
        inputLayout.addRow("Resistance R (Ω):", self.R_edit)
        inputLayout.addRow("Inductance L (H):", self.L_edit)
        inputLayout.addRow("Capacitance C (F):", self.C_edit)
        inputLayout.addRow("Voltage Amplitude V0 (V):", self.V0_edit)
        inputLayout.addRow("Frequency (rad/s):", self.freq_edit)
        inputLayout.addRow("Phase (rad):", self.phase_edit)

        # Simulate button to run the simulation
        self.simulateButton = QtWidgets.QPushButton('Simulate')
        self.simulateButton.clicked.connect(self.simulate)
        inputLayout.addRow(self.simulateButton)

        inputGroup.setLayout(inputLayout)

        # Right Side: Circuit Diagram display
        imageGroup = QtWidgets.QGroupBox("Circuit Diagram")
        imageLayout = QtWidgets.QVBoxLayout()
        self.circuitImage = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap('circuit.png')  # Load image
        pixmap = pixmap.scaledToWidth(300, QtCore.Qt.SmoothTransformation)  # Resize image
        self.circuitImage.setPixmap(pixmap)
        imageLayout.addWidget(self.circuitImage)
        imageGroup.setLayout(imageLayout)

        # Add both input and image groups to the top layout
        topLayout.addWidget(inputGroup)
        topLayout.addWidget(imageGroup)

        # Bottom layout: Matplotlib canvas and toolbar
        self.figure = plt.figure()                # Create matplotlib figure
        self.canvas = FigureCanvas(self.figure)    # Embed figure into Qt
        self.toolbar = NavigationToolbar(self.canvas, self)  # Navigation toolbar

        # Assemble the complete GUI layout
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.toolbar)
        mainLayout.addWidget(self.canvas)

    def simulate(self):
        """
        Perform the transient simulation based on user input parameters.
        Solves the ODEs for the RLC circuit and plots the results.
        """
        try:
            # Retrieve user inputs and convert to float
            R = float(self.R_edit.text())
            L = float(self.L_edit.text())
            C = float(self.C_edit.text())
            V0 = float(self.V0_edit.text())
            omega = float(self.freq_edit.text())
            phase = float(self.phase_edit.text())

            # Define input voltage v(t) = V0 * sin(omega*t + phase)
            def v_in(t):
                return V0 * np.sin(omega * t + phase)

            # Define system of ODEs for series RLC circuit
            def rlc_odes(t, X):
                i1, vC = X
                di1_dt = (v_in(t) - R*i1 - vC) / L  # KVL: sum of voltages around loop
                dvC_dt = i1 / C                     # Capacitor current-voltage relation
                return [di1_dt, dvC_dt]

            # Set time span and evaluation points
            t_span = (0, 5)  # From 0 to 5 seconds
            t_eval = np.linspace(t_span[0], t_span[1], 1000)  # 1000 time points

            # Initial conditions: current and voltage both zero at t=0
            X0 = [0, 0]

            # Solve the ODE system using solve_ivp
            sol = solve_ivp(rlc_odes, t_span, X0, t_eval=t_eval)

            # Extract solutions
            t = sol.t
            i1 = sol.y[0]  # Inductor current
            i2 = i1        # In series RLC, inductor and resistor currents are identical
            vC = sol.y[1]  # Capacitor voltage

            # Clear previous plot and create new one
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(t, i1, label='$i_1(t)$ - Inductor Current')
            ax.plot(t, i2, label='$i_2(t)$ - Resistor Current', linestyle='--')
            ax.plot(t, vC, label='$v_C(t)$ - Capacitor Voltage', linestyle='-.')

            # Set plot labels and title
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Current (A) / Voltage (V)')
            ax.set_title('Transient Response of RLC Circuit')
            ax.legend()
            ax.grid(True)

            # Update the canvas to display the plot
            self.canvas.draw()

        except Exception as e:
            # Display error message box if simulation fails
            QtWidgets.QMessageBox.critical(self, "Input Error", str(e))

if __name__ == '__main__':
    # Main entry point of the program
    app = QtWidgets.QApplication(sys.argv)
    window = RLC_GUI()
    window.show()
    sys.exit(app.exec_())
