# dieselController.py
from dieselModel import DieselCycleModel
from dieselView import DieselCycleView
import numpy as np

class DieselCycleController:
    def __init__(self, view):
        self.view = view
        self.model = DieselCycleModel()

        self.view.calcButton.clicked.connect(self.calculate)

    def calculate(self):
        # Read inputs from GUI
        try:
            self.model.r = float(self.view.r_input.text())
            self.model.rc = float(self.view.rc_input.text())
            self.model.T1 = float(self.view.T1_input.text())
            self.model.P1 = float(self.view.P1_input.text())
        except ValueError:
            # Simple error handling if input is bad
            self.view.efficiency_output.setText('Invalid Input!')
            return

        # Solve using model
        results = self.model.solve()

        # Update GUI output fields
        self.view.T2_output.setText(f'{results["T2"]:.2f}')
        self.view.P2_output.setText(f'{results["P2"]:.2f}')
        self.view.T3_output.setText(f'{results["T3"]:.2f}')
        self.view.P3_output.setText(f'{results["P3"]:.2f}')
        self.view.T4_output.setText(f'{results["T4"]:.2f}')
        self.view.P4_output.setText(f'{results["P4"]:.2f}')
        self.view.efficiency_output.setText(f'{results["efficiency"]*100:.2f}')

        # Plot P-v diagram (simplified schematic)
        self.plot_cycle(results)

    def plot_cycle(self, results):
        self.view.figure.clf()
        ax = self.view.figure.add_subplot(111)

        # Sketch volumes for each point
        V1 = 1
        V2 = V1 / self.model.r
        V3 = self.model.rc * V2
        V4 = V1

        # Sketch pressures from results
        P1 = self.model.P1
        P2 = results['P2']
        P3 = results['P3']
        P4 = results['P4']

        V = [V1, V2, V3, V4, V1]
        P = [P1, P2, P3, P4, P1]

        ax.plot(V, P, marker='o')
        ax.set_xlabel('Volume (arbitrary units)')
        ax.set_ylabel('Pressure (MPa)')
        ax.set_title('Diesel Cycle P-v Diagram')
        ax.grid(True)

        self.view.canvas.draw()
