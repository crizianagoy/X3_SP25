# draw_circuit.py

import sys
import os

# macOS-specific settings to fix rendering and OpenGL issues
os.environ["QT_MAC_WANTS_LAYER"] = "1"
os.environ["QT_OPENGL"] = "software"

# PyQt5 modules for GUI components
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsTextItem
from PyQt5.QtGui import QPen, QFont
from PyQt5.QtCore import Qt

# Custom parser to load circuit elements from a file
from circuit_parser import parse_circuit_file


class CircuitWindow(QMainWindow):
    """
    Main window for displaying a circuit diagram using PyQt5's Graphics View Framework.

    Attributes:
        title (str): Title of the window parsed from the file.
        nodes (dict): Dictionary of Node objects keyed by their IDs.
        elements (list): List of CircuitElement objects (resistors, capacitors, etc.).
        wires (list): List of Wire objects connecting nodes.
        scene (QGraphicsScene): Graphics scene to hold all drawn items.
        view (QGraphicsView): View to visualize the scene.
    """

    def __init__(self):
        """
        Initializes the CircuitWindow by parsing the circuit file,
        setting up the main window, graphics scene, and drawing the circuit.
        """
        super().__init__()
        print("Starting CircuitWindow initialization...")

        try:
            # --- Parse the circuit description file ---
            print("Parsing circuit file...")
            self.title, self.nodes, self.elements, self.wires = parse_circuit_file("circuit.txt")
            print(
                f"Parsed: Title={self.title}, Nodes={len(self.nodes)}, Elements={len(self.elements)}, Wires={len(self.wires)}")

            # --- Set up the main window ---
            self.setWindowTitle(self.title)
            self.setGeometry(100, 100, 800, 600)
            print("Window setup complete.")

            # --- Set up the graphics scene and view ---
            self.scene = QGraphicsScene()
            self.view = QGraphicsView(self.scene, self)
            self.setCentralWidget(self.view)
            print("Graphics View and Scene setup complete.")

            # --- Draw the parsed circuit ---
            self.draw_circuit()

            # --- Adjust scene rect to fit all items with padding ---
            bounding_rect = self.scene.itemsBoundingRect()
            print(
                f"Items bounding rect: x={bounding_rect.x()}, y={bounding_rect.y()}, width={bounding_rect.width()}, height={bounding_rect.height()}")

            padding = 30  # Add padding around the scene
            self.scene.setSceneRect(
                bounding_rect.x() - padding,
                bounding_rect.y() - padding,
                bounding_rect.width() + 2 * padding,
                bounding_rect.height() + 2 * padding
            )

            # --- Fit the view and zoom in for better visibility ---
            self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
            self.view.scale(12.0, 12.0)
            print("Scene rect and view adjusted.")

        except Exception as e:
            print(f"Error during initialization: {e}")
            sys.exit(1)

    def draw_circuit(self):
        """
        Draws all elements, wires, and nodes onto the scene.
        Adds graphical items for each object and labels nodes.
        """
        try:
            # --- Draw all circuit elements (resistors, capacitors, etc.) ---
            print("Drawing elements...")
            for element in self.elements:
                print(f"Adding element: {type(element).__name__}")
                self.scene.addItem(element)

            # --- Draw all connecting wires ---
            print("Drawing wires...")
            for wire in self.wires:
                print(f"Adding wire between nodes {wire.node1.id} and {wire.node2.id}")
                self.scene.addItem(wire)

            # --- Draw nodes as dots and label them ---
            print("Drawing nodes...")
            for node in self.nodes.values():
                print(f"Adding node {node.id} at ({node.x}, {node.y})")
                # Draw a small ellipse for the node
                self.scene.addEllipse(int(node.x) - 3, int(node.y) - 3, 6, 6, QPen(Qt.black), Qt.black)

                # Create a text label for the node
                label = QGraphicsTextItem(f"N{node.id}")
                label.setFont(QFont("Arial", 10))  # Set label font size

                # Adjust label position based on node ID for better placement
                if node.id == "1":
                    label.setPos(int(node.x) - 25, int(node.y) - 15)  # Top-left
                elif node.id == "2":
                    label.setPos(int(node.x) + 10, int(node.y) - 15)  # Top-right
                elif node.id == "3":
                    label.setPos(int(node.x) + 10, int(node.y) + 5)  # Bottom-right
                elif node.id == "4":
                    label.setPos(int(node.x) - 25, int(node.y) + 5)  # Bottom-left
                else:
                    label.setPos(int(node.x) + 5, int(node.y) + 5)  # Default placement
                self.scene.addItem(label)

            print("Circuit drawing complete.")
        except Exception as e:
            print(f"Error during drawing: {e}")
            sys.exit(1)


if __name__ == "__main__":
    """
    Entry point for the application.
    Sets up the QApplication, creates the main window, and starts the event loop.
    """
    print("Starting application...")
    app = QApplication(sys.argv)
    window = CircuitWindow()
    print("Showing window...")
    window.show()
    print("Entering event loop...")
    window.repaint()
    sys.exit(app.exec_())
