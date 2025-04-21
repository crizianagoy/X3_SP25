# dieselController.py

from dieselModel import DieselCycleModel
from dieselView import DieselCycleView
import numpy as np

class DieselCycleController:
    """
    Controller class for the Diesel Cycle Simulator.
    Handles interaction between the DieselCycleView (GUI) and the DieselCycleModel (calculations).
    """

    def __init__(self, view):
        """
        Initialize the controller, bind the model and view, and connect GUI signals.

        Args:
            view (DieselCycleView): The GUI view object containing widgets.
        """
        self.view = view
        self.model = DieselCycleModel()

        # Connect the 'Calculate' button click to the calculate() function
        self.view.calcButton.clicked.connect(self.calculate)

    def calculate(self):
        """
        Reads input values from the GUI, runs the Diesel cycle model calculations,
        updates the GUI with results, and triggers plotting of the P-v diagram.
        """
        try:
            # Read and convert user inputs from text fields
            self.model.r = float(self.view.r_input.text())    # Compression ratio
            self.model.rc = float(self.view.rc_input.text())  # Cutoff ratio
            self.model.T1 = float(self.view.T1_input.text())  # Initial temperature
            self.model.P1 = float(self.view.P1_input.text())  # Initial pressure
        except ValueError:
            # If conversion fails, display an error message
            self.view.efficiency_output.setText('Invalid Input!')
            return

        # Solve the Diesel cycle using the model
        results = self.model.solve()

        # Update GUI output fields with calculated results
        self.view.T2_output.setText(f'{results["T2"]:.2f}')
        self.view.P2_output.setText(f'{results["P2"]:.2f}')
        self.view.T3_output.setText(f'{results["T3"]:.2f}')
        self.view.P3_output.setText(f'{results["P3"]:.2f}')
        self.view.T4_output.setText(f'{results["T4"]:.2f}')
        self.view.P4_output.setText(f'{results["P4"]:.2f}')
        self.view.efficiency_output.setText(f'{results["efficiency"]*100:.2f}')

        # Plot the Diesel cycle on a P-v diagram
        self.plot_cycle(results)

    def plot_cycle(self, results):
        """
        Plot the Diesel cycle as a simplified P-v diagram based on calculated results.

        Args:
            results (dict): Dictionary of computed state points (T2, P2, T3, P3, T4, P4, efficiency).
        """
        self.view.figure.clf()  # Clear any previous plot
        ax = self.view.figure.add_subplot(111)

        # Assume V1 = 1 (arbitrary unit volume)
        V1 = 1
        V2 = V1 / self.model.r        # Compressed volume after compression
        V3 = self.model.rc * V2        # Expanded volume after heat addition
        V4 = V1                        # Final volume after expansion back to initial

        # Pressures at each state point
        P1 = self.model.P1
        P2 = results['P2']
        P3 = results['P3']
        P4 = results['P4']

        # Define lists of volumes and pressures for the plot
        V = [V1, V2, V3, V4, V1]  # Cycle returns to starting point
        P = [P1, P2, P3, P4, P1]

        # Create the P-v diagram
        ax.plot(V, P, marker='o')
        ax.set_xlabel('Volume (arbitrary units)')
        ax.set_ylabel('Pressure (MPa)')
        ax.set_title('Diesel Cycle P-v Diagram')
        ax.grid(True)

        # Draw the updated canvas
        self.view.canvas.draw()
