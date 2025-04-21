import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class Node:
    """
    Class to represent a node in the circuit with a name and (x, y) position.
    """
    def __init__(self, name, x, y):
        """
        Initialize a node with a name and coordinates.
        :param name: str, name of the node
        :param x: float, x-coordinate
        :param y: float, y-coordinate
        """
        self.name = name
        self.x = float(x)
        self.y = float(y)

class CircuitElement(QtWidgets.QGraphicsItem):
    """
    Base class for all circuit elements (resistor, capacitor, inductor, voltage source).
    Inherits from QGraphicsItem for graphical representation.
    """
    def __init__(self, start, end):
        """
        Initialize a circuit element between two nodes.
        :param start: Node, starting node
        :param end: Node, ending node
        """
        super().__init__()
        self.start = start
        self.end = end
        self.setPos(self.start.x, self.start.y)  # move item to starting node
        self.width = self.end.x - self.start.x
        self.height = self.end.y - self.start.y

    def boundingRect(self):
        """
        Defines the local coordinate bounding rectangle for the item.
        :return: QRectF, bounding box
        """
        return QtCore.QRectF(0, 0, abs(self.width), abs(self.height))

class ResistorItem(CircuitElement):
    """
    Graphics item to represent a resistor between two nodes.
    """
    def paint(self, painter, option, widget=None):
        """
        Paint a simple straight line for a resistor.
        """
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        painter.drawLine(0, 0, self.width, self.height)

class CapacitorItem(CircuitElement):
    """
    Graphics item to represent a capacitor between two nodes.
    """
    def paint(self, painter, option, widget=None):
        """
        Paint a symbolic representation of a capacitor depending on orientation.
        """
        painter.setPen(QtGui.QPen(QtCore.Qt.blue, 2))
        mid_x = self.width / 2
        mid_y = self.height / 2
        if abs(self.width) > abs(self.height):  # Horizontal capacitor
            painter.drawLine(0, 0, mid_x - 10, 0)
            painter.drawLine(mid_x + 10, 0, self.width, 0)
            painter.drawLine(mid_x - 10, -20, mid_x - 10, 20)
            painter.drawLine(mid_x + 10, -20, mid_x + 10, 20)
        else:  # Vertical capacitor
            painter.drawLine(0, 0, 0, mid_y - 10)
            painter.drawLine(0, mid_y + 10, 0, self.height)
            painter.drawLine(-20, mid_y - 10, 20, mid_y - 10)
            painter.drawLine(-20, mid_y + 10, 20, mid_y + 10)

class InductorItem(CircuitElement):
    """
    Graphics item to represent an inductor between two nodes.
    """
    def paint(self, painter, option, widget=None):
        """
        Paint a simple straight line as placeholder for an inductor.
        """
        painter.setPen(QtGui.QPen(QtCore.Qt.darkGreen, 2))
        painter.drawLine(0, 0, self.width, self.height)

class VoltageSourceItem(CircuitElement):
    """
    Graphics item to represent a voltage source between two nodes.
    """
    def paint(self, painter, option, widget=None):
        """
        Paint a dashed line with a circle symbolizing a voltage source.
        """
        painter.setPen(QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.DashLine))
        mid_x = self.width / 2
        mid_y = self.height / 2
        if abs(self.width) > abs(self.height):  # Horizontal voltage source
            painter.drawLine(0, 0, mid_x - 20, 0)
            painter.drawEllipse(mid_x - 20, -20, 40, 40)
            painter.drawLine(mid_x + 20, 0, self.width, 0)
        else:  # Vertical voltage source
            painter.drawLine(0, 0, 0, mid_y - 20)
            painter.drawEllipse(-20, mid_y - 20, 40, 40)
            painter.drawLine(0, mid_y + 20, 0, self.height)

class CircuitScene(QtWidgets.QGraphicsScene):
    """
    Custom QGraphicsScene to manage and display circuit components.
    """
    def __init__(self, filename):
        """
        Initialize the scene and load circuit elements from file.
        :param filename: str, path to circuit description file
        """
        super().__init__()
        self.nodes = {}
        self.load_file(filename)

    def load_file(self, filename):
        """
        Read the circuit file and populate the scene.
        :param filename: str, path to circuit description file
        """
        with open(filename, 'r') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Handle different types of elements
            if '<node' in line:
                name = self.get_attr(line, 'name')
                x = self.get_attr(line, 'x')
                y = self.get_attr(line, 'y')
                self.nodes[name] = Node(name, x, y)
                # Draw a small dot for each node
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
        """
        Helper function to extract attribute values from an XML-like line.
        :param line: str, the text line
        :param key: str, the attribute name
        :return: str, attribute value
        """
        start = line.find(key+'="') + len(key) + 2
        end = line.find('"', start)
        return line[start:end]

class MainWindow(QtWidgets.QMainWindow):
    """
    Main application window that contains the QGraphicsView.
    """
    def __init__(self):
        """
        Initialize the main window and setup the scene.
        """
        super().__init__()
        self.setWindowTitle("Circuit Diagram Drawer")
        self.setGeometry(100, 100, 800, 600)

        self.scene = CircuitScene('../Problem 2/circuit.txt')  # Change path if needed
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setSceneRect(self.scene.itemsBoundingRect())  # Auto-adjust view
        self.setCentralWidget(self.view)

if __name__ == '__main__':
    # Entry point for the application
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())