# circuit_elements.py
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtCore import Qt, QRectF


class Node:
    """
    A class to represent a circuit node (connection point).

    Attributes:
        id (str): Identifier of the node.
        x (float): X-coordinate of the node.
        y (float): Y-coordinate of the node.
    """

    def __init__(self, id, x, y):
        """
        Initialize a Node with its ID and coordinates.

        Args:
            id (str): Unique identifier for the node.
            x (float): X-coordinate.
            y (float): Y-coordinate.
        """
        self.id = id
        self.x = float(x)
        self.y = float(y)


class CircuitElement(QGraphicsItem):
    """
    Abstract base class for all circuit elements (e.g., Resistor, Capacitor, Inductor).
    Handles basic properties like orientation and bounding box.
    """

    def __init__(self, node1, node2):
        """
        Initialize a CircuitElement between two nodes.

        Args:
            node1 (Node): First connected node.
            node2 (Node): Second connected node.
        """
        super().__init__()
        self.node1 = node1
        self.node2 = node2
        # Determine orientation based on greater axis distance
        self.is_horizontal = abs(node1.x - node2.x) > abs(node1.y - node2.y)
        self.length = 50 if self.is_horizontal else 30
        self.width = 40

    def boundingRect(self):
        """
        Define the bounding rectangle for drawing, including padding.

        Returns:
            QRectF: Bounding box of the element.
        """
        if self.is_horizontal:
            x = min(self.node1.x, self.node2.x)
            y = min(self.node1.y, self.node2.y) - self.width / 2
            w = abs(self.node1.x - self.node2.x)
            h = self.width
        else:
            x = min(self.node1.x, self.node2.x) - self.width / 2
            y = min(self.node1.y, self.node2.y)
            w = self.width
            h = abs(self.node1.y - self.node2.y)
        padding = 15  # Add extra margin to avoid clipping
        return QRectF(x - padding, y - padding, w + 2 * padding, h + 2 * padding)


class VoltageSource(CircuitElement):
    """
    Represents a voltage source, drawn as a circle with '+' and '-' signs.
    """

    def paint(self, painter, option, widget):
        """
        Paint the voltage source between two nodes.
        """
        try:
            painter.setPen(QPen(Qt.black, 2))
            mid_x = int((self.node1.x + self.node2.x) / 2)
            mid_y = int((self.node1.y + self.node2.y) / 2)

            if self.is_horizontal:
                # Draw voltage source horizontally
                painter.drawEllipse(mid_x - 10, mid_y - 10, 20, 20)
                painter.drawLine(mid_x - 5, mid_y, mid_x + 5, mid_y)  # '+'
                painter.drawLine(mid_x, mid_y - 5, mid_x, mid_y + 5)
                painter.drawLine(mid_x + 15, mid_y, mid_x + 25, mid_y)  # '-'
                painter.drawLine(int(self.node1.x), int(self.node1.y), mid_x - 10, mid_y)
                painter.drawLine(mid_x + 25, mid_y, int(self.node2.x), int(self.node2.y))
                painter.setFont(QFont("Arial", 12))
                painter.drawText(mid_x - 5, mid_y - 25, "V")
            else:
                # Draw voltage source vertically
                painter.drawEllipse(mid_x - 10, mid_y - 10, 20, 20)
                painter.drawLine(mid_x - 5, mid_y, mid_x + 5, mid_y)  # '+'
                painter.drawLine(mid_x, mid_y - 5, mid_x, mid_y + 5)
                painter.drawLine(mid_x, mid_y + 15, mid_x, mid_y + 25)  # '-'
                painter.drawLine(int(self.node1.x), int(self.node1.y), mid_x, mid_y - 10)
                painter.drawLine(mid_x, mid_y + 25, int(self.node2.x), int(self.node2.y))
                painter.setFont(QFont("Arial", 12))
                painter.drawText(mid_x - 25, mid_y - 5, "V")
        except Exception as e:
            print(f"Error drawing VoltageSource: {e}")
            raise


class Inductor(CircuitElement):
    """
    Represents an inductor, drawn as a series of arcs.
    """

    def paint(self, painter, option, widget):
        """
        Paint the inductor between two nodes.
        """
        try:
            painter.setPen(QPen(Qt.black, 2))
            mid_x = int((self.node1.x + self.node2.x) / 2)
            mid_y = int((self.node1.y + self.node2.y) / 2)

            if self.is_horizontal:
                # Draw horizontal coils
                for i in range(3):
                    x = mid_x - 15 + i * 10
                    painter.drawArc(x, mid_y - 7, 14, 14, 0, 180 * 16)
                painter.drawLine(int(self.node1.x), int(self.node1.y), mid_x - 15, mid_y)
                painter.drawLine(mid_x + 15, mid_y, int(self.node2.x), int(self.node2.y))
                painter.setFont(QFont("Arial", 12))
                painter.drawText(mid_x - 5, mid_y - 25, "L")
            else:
                # Draw vertical coils
                for i in range(3):
                    y = mid_y - 15 + i * 10
                    painter.drawArc(mid_x - 7, y, 14, 14, 90 * 16, 180 * 16)
                painter.drawLine(int(self.node1.x), int(self.node1.y), mid_x, mid_y - 15)
                painter.drawLine(mid_x, mid_y + 15, int(self.node2.x), int(self.node2.y))
                painter.setFont(QFont("Arial", 12))
                painter.drawText(mid_x + 25, mid_y - 5, "L")
        except Exception as e:
            print(f"Error drawing Inductor: {e}")
            raise


class Resistor(CircuitElement):
    """
    Represents a resistor, drawn as a rectangle.
    """

    def paint(self, painter, option, widget):
        """
        Paint the resistor between two nodes.
        """
        try:
            painter.setPen(QPen(Qt.black, 2))
            mid_x = int((self.node1.x + self.node2.x) / 2)
            mid_y = int((self.node1.y + self.node2.y) / 2)

            if self.is_horizontal:
                painter.drawRect(mid_x - 15, mid_y - 5, 30, 10)
                painter.drawLine(int(self.node1.x), int(self.node1.y), mid_x - 15, mid_y)
                painter.drawLine(mid_x + 15, mid_y, int(self.node2.x), int(self.node2.y))
                painter.setFont(QFont("Arial", 12))
                painter.drawText(mid_x - 5, mid_y + 25, "R")
            else:
                painter.drawRect(mid_x - 5, mid_y - 15, 10, 30)
                painter.drawLine(int(self.node1.x), int(self.node1.y), mid_x, mid_y - 15)
                painter.drawLine(mid_x, mid_y + 15, int(self.node2.x), int(self.node2.y))
                painter.setFont(QFont("Arial", 12))
                painter.drawText(mid_x + 25, mid_y - 5, "R")
        except Exception as e:
            print(f"Error drawing Resistor: {e}")
            raise


class Capacitor(CircuitElement):
    """
    Represents a capacitor, drawn as two parallel lines.
    """

    def paint(self, painter, option, widget):
        """
        Paint the capacitor between two nodes.
        """
        try:
            painter.setPen(QPen(Qt.black, 2))
            mid_x = int((self.node1.x + self.node2.x) / 2)
            mid_y = int((self.node1.y + self.node2.y) / 2)

            if self.is_horizontal:
                painter.drawLine(mid_x - 15, mid_y - 25, mid_x - 15, mid_y - 5)
                painter.drawLine(mid_x + 15, mid_y - 25, mid_x + 15, mid_y - 5)
                painter.drawLine(int(self.node1.x), int(self.node1.y), mid_x - 15, mid_y - 15)
                painter.drawLine(mid_x + 15, mid_y - 15, int(self.node2.x), int(self.node2.y))
                painter.setFont(QFont("Arial", 12))
                painter.drawText(mid_x - 5, mid_y - 40, "C")
            else:
                painter.drawLine(mid_x - 25, mid_y - 15, mid_x - 5, mid_y - 15)
                painter.drawLine(mid_x - 25, mid_y + 15, mid_x - 5, mid_y + 15)
                painter.drawLine(int(self.node1.x), int(self.node1.y), mid_x - 15, mid_y - 15)
                painter.drawLine(mid_x - 15, mid_y + 15, int(self.node2.x), int(self.node2.y))
                painter.setFont(QFont("Arial", 12))
                painter.drawText(mid_x - 40, mid_y - 5, "C")
        except Exception as e:
            print(f"Error drawing Capacitor: {e}")
            raise


class Wire(QGraphicsItem):
    """
    Represents a simple wire connection between two nodes.
    """

    def __init__(self, node1, node2):
        """
        Initialize a Wire between two nodes.

        Args:
            node1 (Node): Starting node.
            node2 (Node): Ending node.
        """
        super().__init__()
        self.node1 = node1
        self.node2 = node2

    def boundingRect(self):
        """
        Define the bounding rectangle around the wire.

        Returns:
            QRectF: Bounding box of the wire.
        """
        x = min(self.node1.x, self.node2.x)
        y = min(self.node1.y, self.node2.y)
        w = abs(self.node1.x - self.node2.x)
        h = abs(self.node1.y - self.node2.y)
        padding = 5
        return QRectF(x - padding, y - padding, w + 2 * padding, h + 2 * padding)

    def paint(self, painter, option, widget):
        """
        Paint the wire as a straight line between two nodes.
        """
        try:
            painter.setPen(QPen(Qt.black, 2))
            painter.drawLine(int(self.node1.x), int(self.node1.y), int(self.node2.x), int(self.node2.y))
        except Exception as e:
            print(f"Error drawing Wire: {e}")
            raise
