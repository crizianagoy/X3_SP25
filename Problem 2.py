import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.x = float(x)
        self.y = float(y)

class CircuitElement(QtWidgets.QGraphicsItem):
    def __init__(self, start, end):
        super().__init__()
        self.start = start
        self.end = end

    def boundingRect(self):
        return QtCore.QRectF(min(self.start.x, self.end.x), min(self.start.y, self.end.y),
                             abs(self.start.x - self.end.x), abs(self.start.y - self.end.y))

class ResistorItem(CircuitElement):
    def paint(self, painter, option, widget=None):
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        painter.drawLine(self.start.x, self.start.y, self.end.x, self.end.y)
        # Simple zigzag could be added here

class CapacitorItem(CircuitElement):
    def paint(self, painter, option, widget=None):
        painter.setPen(QtGui.QPen(QtCore.Qt.blue, 2))
        mid_x = (self.start.x + self.end.x) / 2
        mid_y = (self.start.y + self.end.y) / 2
        painter.drawLine(self.start.x, self.start.y, mid_x - 10, mid_y - 10)
        painter.drawLine(mid_x + 10, mid_y + 10, self.end.x, self.end.y)
        painter.drawLine(mid_x - 10, mid_y - 10, mid_x - 10, mid_y + 10)
        painter.drawLine(mid_x + 10, mid_y - 10, mid_x + 10, mid_y + 10)

class InductorItem(CircuitElement):
    def paint(self, painter, option, widget=None):
        painter.setPen(QtGui.QPen(QtCore.Qt.darkGreen, 2))
        painter.drawLine(self.start.x, self.start.y, self.end.x, self.end.y)
        # You could add arcs for coils

class VoltageSourceItem(CircuitElement):
    def paint(self, painter, option, widget=None):
        painter.setPen(QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.DashLine))
        painter.drawLine(self.start.x, self.start.y, self.end.x, self.end.y)

class CircuitScene(QtWidgets.QGraphicsScene):
    def __init__(self, filename):
        super().__init__()
        self.nodes = {}
        self.load_file(filename)

    def load_file(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        for line in lines:
            if '<node' in line:
                name = self.get_attr(line, 'name')
                x = self.get_attr(line, 'x')
                y = self.get_attr(line, 'y')
                self.nodes[name] = Node(name, x, y)
            elif '<resistor' in line:
                n1 = self.get_attr(line, 'n1')
                n2 = self.get_attr(line, 'n2')
                item = ResistorItem(self.nodes[n1], self.nodes[n2])
                self.addItem(item)
            elif '<capacitor' in line:
                n1 = self.get_attr(line, 'n1')
                n2 = self.get_attr(line, 'n2')
                item = CapacitorItem(self.nodes[n1], self.nodes[n2])
                self.addItem(item)
            elif '<inductor' in line:
                n1 = self.get_attr(line, 'n1')
                n2 = self.get_attr(line, 'n2')
                item = InductorItem(self.nodes[n1], self.nodes[n2])
                self.addItem(item)
            elif '<voltage_source' in line:
                n1 = self.get_attr(line, 'n1')
                n2 = self.get_attr(line, 'n2')
                item = VoltageSourceItem(self.nodes[n1], self.nodes[n2])
                self.addItem(item)

    def get_attr(self, line, key):
        start = line.find(key+'="') + len(key) + 2
        end = line.find('"', start)
        return line[start:end]

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Circuit Diagram Drawer")
        self.setGeometry(100, 100, 800, 600)

        self.scene = CircuitScene('circuit.txt')
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())