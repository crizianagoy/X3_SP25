# dieselModel.py
import math

class DieselCycleModel:
    def __init__(self):
        self.r = 18          # Compression ratio
        self.rc = 2          # Cutoff ratio
        self.T1 = 300        # Initial Temperature in K
        self.P1 = 0.1        # Initial Pressure in MPa
        self.k = 1.4         # Specific heat ratio for air

    def solve(self):
        # Step 1: Isentropic compression 1->2
        T2 = self.T1 * self.r ** (self.k - 1)
        P2 = self.P1 * self.r ** self.k

        # Step 2: Constant pressure heat addition 2->3
        V2 = 1  # Assume V2=1 for simplicity
        V3 = self.rc * V2
        T3 = T2 * self.rc
        P3 = P2

        # Step 3: Isentropic expansion 3->4
        T4 = T3 * (V2/V3) ** (self.k - 1)
        P4 = P3 * (V2/V3) ** self.k

        # Efficiency for diesel cycle
        efficiency = 1 - (1 / self.r ** (self.k - 1)) * ((self.rc ** self.k - 1) / (self.k * (self.rc - 1)))

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
