# main.py
import sys
from PyQt5 import QtWidgets
from dieselView import DieselCycleView
from dieselController import DieselCycleController

def main():
    app = QtWidgets.QApplication(sys.argv)
    view = DieselCycleView()
    controller = DieselCycleController(view)
    view.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
