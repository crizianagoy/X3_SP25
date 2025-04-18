import sys
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class RLC_GUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('RLC Circuit Transient Simulator')
        self.setGeometry(100, 100, 1200, 700)
        self.initUI()

    def initUI(self):
        # Main layout
        mainLayout = QtWidgets.QVBoxLayout(self)

        # Top layout (Inputs + Circuit Picture)
        topLayout = QtWidgets.QHBoxLayout()

        # Left Side: Inputs
        inputGroup = QtWidgets.QGroupBox("Circuit Parameters")
        inputLayout = QtWidgets.QFormLayout()

        self.R_edit = QtWidgets.QLineEdit('10')
        self.L_edit = QtWidgets.QLineEdit('20')
        self.C_edit = QtWidgets.QLineEdit('0.05')
        self.V0_edit = QtWidgets.QLineEdit('20')
        self.freq_edit = QtWidgets.QLineEdit('20')
        self.phase_edit = QtWidgets.QLineEdit('0')

        inputLayout.addRow("Resistance R (Ω):", self.R_edit)
        inputLayout.addRow("Inductance L (H):", self.L_edit)
        inputLayout.addRow("Capacitance C (F):", self.C_edit)
        inputLayout.addRow("Voltage Amplitude V0 (V):", self.V0_edit)
        inputLayout.addRow("Frequency (rad/s):", self.freq_edit)
        inputLayout.addRow("Phase (rad):", self.phase_edit)

        self.simulateButton = QtWidgets.QPushButton('Simulate')
        self.simulateButton.clicked.connect(self.simulate)
        inputLayout.addRow(self.simulateButton)

        inputGroup.setLayout(inputLayout)

        # Right Side: Circuit Image
        imageGroup = QtWidgets.QGroupBox("Circuit Diagram")
        imageLayout = QtWidgets.QVBoxLayout()
        self.circuitImage = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap('circuit.png')
        pixmap = pixmap.scaledToWidth(300, QtCore.Qt.SmoothTransformation)
        self.circuitImage.setPixmap(pixmap)
        imageLayout.addWidget(self.circuitImage)
        imageGroup.setLayout(imageLayout)

        # Add to topLayout
        topLayout.addWidget(inputGroup)
        topLayout.addWidget(imageGroup)

        # Bottom layout: Matplotlib Figure
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Add layouts to mainLayout
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.toolbar)
        mainLayout.addWidget(self.canvas)

    def simulate(self):
        try:
            # Get user inputs
            R = float(self.R_edit.text())
            L = float(self.L_edit.text())
            C = float(self.C_edit.text())
            V0 = float(self.V0_edit.text())
            omega = float(self.freq_edit.text())
            phase = float(self.phase_edit.text())

            # Define v(t)
            def v_in(t):
                return V0 * np.sin(omega * t + phase)

            # Define system of ODEs
            def rlc_odes(t, X):
                i1, vC = X
                di1_dt = (v_in(t) - R*i1 - vC) / L
                dvC_dt = i1 / C
                return [di1_dt, dvC_dt]

            # Time span for simulation
            t_span = (0, 5)
            t_eval = np.linspace(t_span[0], t_span[1], 1000)

            # Initial conditions (assume zero)
            X0 = [0, 0]

            # Solve ODE
            sol = solve_ivp(rlc_odes, t_span, X0, t_eval=t_eval)

            t = sol.t
            i1 = sol.y[0]
            i2 = i1  # because same in this series connection
            vC = sol.y[1]

            # Plot results
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(t, i1, label='$i_1(t)$ - Inductor Current')
            ax.plot(t, i2, label='$i_2(t)$ - Resistor Current', linestyle='--')
            ax.plot(t, vC, label='$v_C(t)$ - Capacitor Voltage', linestyle='-.')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Current (A) / Voltage (V)')
            ax.set_title('Transient Response of RLC Circuit')
            ax.legend()
            ax.grid(True)
            self.canvas.draw()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Input Error", str(e))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = RLC_GUI()
    window.show()
    sys.exit(app.exec_())
