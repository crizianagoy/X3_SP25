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
        self.setPos(self.start.x, self.start.y)  # move the item to the starting node
        self.width = self.end.x - self.start.x
        self.height = self.end.y - self.start.y

    def boundingRect(self):
        return QtCore.QRectF(
            0, 0,
            abs(self.width),
            abs(self.height)
        )


# local coordinates inside item

class ResistorItem(CircuitElement):
    def paint(self, painter, option, widget=None):
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        painter.drawLine(0, 0, self.width, self.height)  # local drawing inside the item

class CapacitorItem(CircuitElement):
    def paint(self, painter, option, widget=None):
        painter.setPen(QtGui.QPen(QtCore.Qt.blue, 2))
        mid_x = self.width / 2
        mid_y = self.height / 2
        if abs(self.width) > abs(self.height):  # Horizontal
            painter.drawLine(0, 0, mid_x - 10, 0)
            painter.drawLine(mid_x + 10, 0, self.width, 0)
            painter.drawLine(mid_x - 10, -20, mid_x - 10, 20)
            painter.drawLine(mid_x + 10, -20, mid_x + 10, 20)
        else:  # Vertical
            painter.drawLine(0, 0, 0, mid_y - 10)
            painter.drawLine(0, mid_y + 10, 0, self.height)
            painter.drawLine(-20, mid_y - 10, 20, mid_y - 10)
            painter.drawLine(-20, mid_y + 10, 20, mid_y + 10)

class InductorItem(CircuitElement):
    def paint(self, painter, option, widget=None):
        painter.setPen(QtGui.QPen(QtCore.Qt.darkGreen, 2))
        painter.drawLine(0, 0, self.width, self.height)  # simple straight line for now

class VoltageSourceItem(CircuitElement):
    def paint(self, painter, option, widget=None):
        painter.setPen(QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.DashLine))
        mid_x = self.width / 2
        mid_y = self.height / 2
        if abs(self.width) > abs(self.height):  # Horizontal
            painter.drawLine(0, 0, mid_x - 20, 0)
            painter.drawEllipse(mid_x - 20, -20, 40, 40)
            painter.drawLine(mid_x + 20, 0, self.width, 0)
        else:  # Vertical
            painter.drawLine(0, 0, 0, mid_y - 20)
            painter.drawEllipse(-20, mid_y - 20, 40, 40)
            painter.drawLine(0, mid_y + 20, 0, self.height)

class CircuitScene(QtWidgets.QGraphicsScene):
    def __init__(self, filename):
        super().__init__()
        self.nodes = {}
        self.load_file(filename)

    def load_file(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue
            if '<node' in line:
                name = self.get_attr(line, 'name')
                x = self.get_attr(line, 'x')
                y = self.get_attr(line, 'y')
                self.nodes[name] = Node(name, x, y)
                # draw a small dot for node
                ellipse = QtWidgets.QGraphicsEllipseItem(self.nodes[name].x-3, self.nodes[name].y-3, 6, 6)
                ellipse.setBrush(QtCore.Qt.black)
                self.addItem(ellipse)
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

        self.scene = CircuitScene('../Problem 2/circuit.txt')
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setSceneRect(self.scene.itemsBoundingRect())
        self.setCentralWidget(self.view)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
