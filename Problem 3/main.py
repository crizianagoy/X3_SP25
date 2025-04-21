# main.py

import sys
from PyQt5 import QtWidgets
from dieselView import DieselCycleView
from dieselController import DieselCycleController

def main():
    """
    Main function to start the Diesel Cycle Simulator application.

    - Creates a QApplication instance (required for any PyQt app).
    - Instantiates the DieselCycleView (GUI layout).
    - Instantiates the DieselCycleController (handles logic between view and model).
    - Displays the GUI window.
    - Starts the application's event loop.
    """
    # Create the Qt application object
    app = QtWidgets.QApplication(sys.argv)

    # Create the GUI view
    view = DieselCycleView()

    # Create the controller and connect it to the view
    controller = DieselCycleController(view)

    # Show the main window
    view.show()

    # Start the event loop and exit cleanly on close
    sys.exit(app.exec_())

if __name__ == '__main__':
    """
    Program entry point.
    Calls the main() function to start the simulator.
    """
    main()
