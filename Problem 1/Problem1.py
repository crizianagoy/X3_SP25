# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Problem1.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    """
    Ui_Form class represents the auto-generated GUI layout.
    It defines and arranges the widgets inside the main form.
    """

    def setupUi(self, Form):
        """
        Set up the user interface layout and widget properties for the form.

        :param Form: The main QWidget to set up
        """
        Form.setObjectName("Form")  # Set the object name for the main form
        Form.resize(400, 300)  # Set initial size of the form

        # Create a vertical layout to arrange all top-level widgets
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")

        # Create a group box to contain the input fields
        self.gb_Input = QtWidgets.QGroupBox(Form)
        self.gb_Input.setObjectName("gb_Input")

        # Create a nested vertical layout inside the group box
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.gb_Input)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # Create a grid layout to neatly organize multiple input widgets
        self.layout_GridInput = QtWidgets.QGridLayout()
        self.layout_GridInput.setObjectName("layout_GridInput")

        # Add the grid layout into the group box's vertical layout
        self.verticalLayout_2.addLayout(self.layout_GridInput)

        # Add the group box into the main form's vertical layout
        self.verticalLayout.addWidget(self.gb_Input)

        # Setup static text and titles
        self.retranslateUi(Form)

        # Connect signal-slot mechanisms automatically
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        """
        Set the static text for widgets and window title.
        Useful for localization and translation support.

        :param Form: The main QWidget where texts are set
        """
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))  # Set window title
        self.gb_Input.setTitle(_translate("Form", "Input"))  # Set group box title
