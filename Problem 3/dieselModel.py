# dieselModel.py

import math

class DieselCycleModel:
    """
    Model class for solving an ideal Diesel engine thermodynamic cycle.

    Attributes:
        r (float): Compression ratio (V1/V2).
        rc (float): Cutoff ratio (V3/V2).
        T1 (float): Initial temperature at state 1 (K).
        P1 (float): Initial pressure at state 1 (MPa).
        k (float): Specific heat ratio (Cp/Cv) for air (typically around 1.4).
    """

    def __init__(self):
        """
        Initialize the DieselCycleModel with default parameters for the cycle.
        """
        self.r = 18          # Compression ratio (default: 18)
        self.rc = 2          # Cutoff ratio (default: 2)
        self.T1 = 300        # Initial temperature in Kelvin (default: 300K)
        self.P1 = 0.1        # Initial pressure in MPa (default: 0.1MPa)
        self.k = 1.4         # Specific heat ratio for air (default: 1.4)

    def solve(self):
        """
        Solve the Diesel cycle for all key thermodynamic states and efficiency.

        Returns:
            dict: A dictionary containing temperatures, pressures, and efficiency:
                - 'T2', 'P2': After isentropic compression
                - 'T3', 'P3': After constant pressure heat addition
                - 'T4', 'P4': After isentropic expansion
                - 'efficiency': Thermal efficiency of the cycle
        """
        # --- Step 1: Isentropic compression from state 1 -> state 2 ---
        T2 = self.T1 * self.r ** (self.k - 1)  # Temperature after compression
        P2 = self.P1 * self.r ** self.k        # Pressure after compression

        # --- Step 2: Constant pressure heat addition from state 2 -> state 3 ---
        V2 = 1  # Assume V2 = 1 (arbitrary reference volume)
        V3 = self.rc * V2  # V3 is rc times V2
        T3 = T2 * self.rc  # Temperature increases with volume during heat addition
        P3 = P2            # Pressure remains constant during heat addition

        # --- Step 3: Isentropic expansion from state 3 -> state 4 ---
        T4 = T3 * (V2 / V3) ** (self.k - 1)  # Temperature after expansion
        P4 = P3 * (V2 / V3) ** self.k        # Pressure after expansion

        # --- Diesel cycle thermal efficiency calculation ---
        # Efficiency derived from Diesel cycle equations
        efficiency = 1 - (1 / self.r ** (self.k - 1)) * ((self.rc ** self.k - 1) / (self.k * (self.rc - 1)))

        # --- Bundle results into a dictionary and return ---
        results = {
            'T2': T2,
            'P2': P2,
            'T3': T3,
            'P3': P3,
            'T4': T4,
            'P4': P4,
            'efficiency': efficiency
        }
        return results
