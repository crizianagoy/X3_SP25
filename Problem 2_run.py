import sys
from typing import Optional
from PyQt5 import QtWidgets, QtGui, QtCore

class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.x = float(x)
        self.y = float(y)

class CircuitElement(QtWidgets.QGraphicsItem):
    def __init__(self, start, end, name, parent: QtWidgets.QGraphicsItem = None):
        super().__init__(parent=parent)
        self.start = start
        self.end = end
        self.name = name
        self.setPos(self.start.x, self.start.y)
        self.width = self.end.x - self.start.x
        self.height = self.end.y - self.start.y

    def boundingRect(self) -> QtCore.QRectF:
        x = min(0, self.width)
        y = min(0, self.height)
        w = abs(self.width)
        h = abs(self.height)
        return QtCore.QRectF(x, y, w, h)

    def draw_label(self, painter: QtGui.QPainter) -> None:
        painter.setPen(QtCore.Qt.black)
        painter.setFont(QtGui.QFont("Arial", 10))
        painter.drawText(abs(self.width)/2, abs(self.height)/2, self.name)

class ResistorItem(CircuitElement):
    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionGraphicsItem, widget: QtWidgets.QWidget = None) -> None:
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        if abs(self.height) < abs(self.width):  # Horizontal
            step = abs(self.width) / 6
            if self.width >= 0:
                points = [QtCore.QPointF(0, 0),
                          QtCore.QPointF(step, 10),
                          QtCore.QPointF(2*step, -10),
                          QtCore.QPointF(3*step, 10),
                          QtCore.QPointF(4*step, -10),
                          QtCore.QPointF(5*step, 10),
                          QtCore.QPointF(abs(self.width), 0)]
            else:
                points = [QtCore.QPointF(0, 0),
                          QtCore.QPointF(-step, 10),
                          QtCore.QPointF(-2*step, -10),
                          QtCore.QPointF(-3*step, 10),
                          QtCore.QPointF(-4*step, -10),
                          QtCore.QPointF(-5*step, 10),
                          QtCore.QPointF(-abs(self.width), 0)]
        else:  # Vertical
            step = abs(self.height) / 6
            if self.height >= 0:
                points = [QtCore.QPointF(0, 0),
                          QtCore.QPointF(10, step),
                          QtCore.QPointF(-10, 2*step),
                          QtCore.QPointF(10, 3*step),
                          QtCore.QPointF(-10, 4*step),
                          QtCore.QPointF(10, 5*step),
                          QtCore.QPointF(0, abs(self.height))]
            else:
                points = [QtCore.QPointF(0, 0),
                          QtCore.QPointF(10, -step),
                          QtCore.QPointF(-10, -2*step),
                          QtCore.QPointF(10, -3*step),
                          QtCore.QPointF(-10, -4*step),
                          QtCore.QPointF(10, -5*step),
                          QtCore.QPointF(0, -abs(self.height))]
        painter.drawPolyline(QtGui.QPolygonF(points))
        self.draw_label(painter)

class CapacitorItem(CircuitElement):
    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionGraphicsItem, widget: QtWidgets.QWidget = None) -> None:
        painter.setPen(QtGui.QPen(QtCore.Qt.blue, 2))
        if abs(self.height) < abs(self.width):  # Horizontal
            mid = abs(self.width) / 2
            if self.width >= 0:
                painter.drawLine(0, 0, mid - 10, 0)
                painter.drawLine(mid + 10, 0, abs(self.width), 0)
                painter.drawLine(mid - 10, -20, mid - 10, 20)
                painter.drawLine(mid + 10, -20, mid + 10, 20)
            else:
                painter.drawLine(0, 0, -mid + 10, 0)
                painter.drawLine(-mid - 10, 0, -abs(self.width), 0)
                painter.drawLine(-mid + 10, -20, -mid + 10, 20)
                painter.drawLine(-mid - 10, -20, -mid - 10, 20)
        else:  # Vertical
            mid = abs(self.height) / 2
            if self.height >= 0:
                painter.drawLine(0, 0, 0, mid - 10)
                painter.drawLine(0, mid + 10, 0, abs(self.height))
                painter.drawLine(-20, mid - 10, 20, mid - 10)
                painter.drawLine(-20, mid + 10, 20, mid + 10)
            else:
                painter.drawLine(0, 0, 0, -mid + 10)
                painter.drawLine(0, -mid - 10, 0, -abs(self.height))
                painter.drawLine(-20, -mid + 10, 20, -mid + 10)
                painter.drawLine(-20, -mid - 10, 20, -mid - 10)
        self.draw_label(painter)

class InductorItem(CircuitElement):
    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionGraphicsItem, widget: QtWidgets.QWidget = None) -> None:
        painter.setPen(QtGui.QPen(QtCore.Qt.darkGreen, 2))
        if abs(self.height) < abs(self.width):  # Horizontal
            step = abs(self.width) / 4
            for i in range(4):
                if self.width >= 0:
                    rect = QtCore.QRectF(i*step, -10, step, 20)
                    painter.drawArc(rect, 0, 180 * 16)
                else:
                    rect = QtCore.QRectF(-i*step - step, -10, step, 20)
                    painter.drawArc(rect, 0, 180 * 16)
        else:  # Vertical
            step = abs(self.height) / 4
            for i in range(4):
                if self.height >= 0:
                    rect = QtCore.QRectF(-10, i*step, 20, step)
                    painter.drawArc(rect, 90 * 16, 180 * 16)
                else:
                    rect = QtCore.QRectF(-10, -i*step - step, 20, step)
                    painter.drawArc(rect, 90 * 16, 180 * 16)
        self.draw_label(painter)

class VoltageSourceItem(CircuitElement):
    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionGraphicsItem, widget: QtWidgets.QWidget = None) -> None:
        painter.setPen(QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.DashLine))
        if abs(self.height) < abs(self.width):  # Horizontal
            mid = abs(self.width) / 2
            if self.width >= 0:
                painter.drawLine(0, 0, mid - 20, 0)
                painter.drawEllipse(mid - 20, -20, 40, 40)
                painter.drawLine(mid + 20, 0, abs(self.width), 0)
            else:
                painter.drawLine(0, 0, -mid + 20, 0)
                painter.drawEllipse(-mid - 20, -20, 40, 40)
                painter.drawLine(-mid - 20, 0, -abs(self.width), 0)
        else:  # Vertical
            mid = abs(self.height) / 2
            if self.height >= 0:
                painter.drawLine(0, 0, 0, mid - 20)
                painter.drawEllipse(-20, mid - 20, 40, 40)
                painter.drawLine(0, mid + 20, 0, abs(self.height))
            else:
                painter.drawLine(0, 0, 0, -mid + 20)
                painter.drawEllipse(-20, -mid - 20, 40, 40)
                painter.drawLine(0, -mid - 20, 0, -abs(self.height))
        self.draw_label(painter)

class CircuitScene(QtWidgets.QGraphicsScene):
    def __init__(self, filename):
        super().__init__()
        self.nodes = {}
        self.load_file(filename)

    def load_file(self, filename):
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
            return

        for line in lines:
            if '<node' in line:
                name = self.get_attr(line, 'name')
                x = self.get_attr(line, 'x')
                y = self.get_attr(line, 'y')
                self.nodes[name] = Node(name, x, y)
                ellipse = QtWidgets.QGraphicsEllipseItem(self.nodes[name].x-3, self.nodes[name].y-3, 6, 6)
                ellipse.setBrush(QtCore.Qt.black)
                self.addItem(ellipse)
            elif '<resistor' in line:
                name = self.get_attr(line, 'name')
                n1 = self.get_attr(line, 'n1')
                n2 = self.get_attr(line, 'n2')
                item = ResistorItem(self.nodes[n1], self.nodes[n2], name, parent=None)
                self.addItem(item)
            elif '<capacitor' in line:
                name = self.get_attr(line, 'name')
                n1 = self.get_attr(line, 'n1')
                n2 = self.get_attr(line, 'n2')
                item = CapacitorItem(self.nodes[n1], self.nodes[n2], name, parent=None)
                self.addItem(item)
            elif '<inductor' in line:
                name = self.get_attr(line, 'name')
                n1 = self.get_attr(line, 'n1')
                n2 = self.get_attr(line, 'n2')
                item = InductorItem(self.nodes[n1], self.nodes[n2], name, parent=None)
                self.addItem(item)
            elif '<voltage_source' in line:
                name = self.get_attr(line, 'name')
                n1 = self.get_attr(line, 'n1')
                n2 = self.get_attr(line, 'n2')
                item = VoltageSourceItem(self.nodes[n1], self.nodes[n2], name, parent=None)
                self.addItem(item)

    @staticmethod
    def get_attr(line: str, key: str) -> str:
        start = line.find(key + '="') + len(key) + 2
        end = line.find('"', start)
        return line[start:end]

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Circuit Diagram Drawer")
        self.setGeometry(100, 100, 800, 600)

        self.scene = CircuitScene('circuit.txt')
        self.scene.setSceneRect(-50, -50, 300, 300)
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        self.setCentralWidget(self.view)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())