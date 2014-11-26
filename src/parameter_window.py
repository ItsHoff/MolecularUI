'''
Created on Jun 19, 2014

@author: keisano1
'''

from PyQt4 import QtGui, QtCore

import ui_circuit
import widget_creator
from custom_line_edit import CustomLineEdit


class ParameterWindow(QtGui.QDialog):
    """Widget for editing parameters of the circuits.
    Normally opens a separate window, but can also be embedded
    by adding it to a layout.
    """

    def __init__(self, circuit):
        """Construct the window based on the circuit parameters.
        Circuit can also be the main machine in addition to regular
        circuits.
        """
        self.circuit = circuit
        if isinstance(self.circuit, ui_circuit.UICircuit):
            super(ParameterWindow, self).__init__(circuit.scene().parent().window())
            self.setWindowTitle(self.circuit.name + " parameters")
            self.addWidgets(self.circuit.circuit_info.param_window_style)
        else:
            super(ParameterWindow, self).__init__(circuit.window())
            self.setWindowTitle("Machine parameters")
            self.addWidgets(self.circuit.param_window_style)

    def showWindow(self):
        """Update the widgets to show the current parameter values and
        show the window and make sure it's activated and on top."""
        self.setValues()
        self.show()
        self.raise_()
        self.activateWindow()

    def addWidgets(self, param_window_style):
        """Add widgets specified in the param_window_style to the window."""
        grid = QtGui.QGridLayout()
        self.setLayout(grid)
        widgets = []
        # Create all the necessary widgets and add them to the temporary
        # widgets container.
        for name, widget_type in param_window_style.iteritems():
            if widget_type.endswith("LineEdit"):
                widgets.append(widget_creator.createLineEdit(name, widget_type))
            elif widget_type == "CheckBox":
                widgets.append(widget_creator.createCheckBox(name))
            elif widget_type == "FileDialog":
                widgets.append(widget_creator.createFileDialog(name))
            elif widget_type == "DirDialog":
                widgets.append(widget_creator.createDirDialog(name))
            elif widget_type == "RegisterDialog":
                widgets.append(widget_creator.createRegisterDialog(name,
                                self.parent().centralWidget(), self))
            elif widget_type == "ModeSetup":
                widgets.append(widget_creator.createModeSetup(name, self))
            elif widget_type == "RecorderSelect":
                widgets.append(widget_creator.createRecorderSelect(name))
            else:
                print "Incorrect widget type on circuit " + self.circuit.name
        # Add the widgets from the container into the window layout.
        row = 0
        for widget_row in widgets:
            col = 0
            for widget in widget_row:
                grid.addWidget(widget, row, col)
                col += 1
            row += 1
        # Create the buttons for the window and connect them.
        ok_button = QtGui.QPushButton("Done")
        QtCore.QObject.connect(ok_button, QtCore.SIGNAL("clicked()"),
                               self.setParameters)
        # cancel_button = QtGui.QPushButton("Cancel")
        # QtCore.QObject.connect(cancel_button, QtCore.SIGNAL("clicked()"),
        #                        self.cancel)
        grid.addWidget(ok_button, row, 0, 1, 2)
        # grid.addWidget(cancel_button, row, 1)
        self.setValues()

    def setParameters(self):
        """Collect all the parameters given and call the circuits
        setParameters to save them. Finally close the window.
        """
        rows = self.layout().rowCount()
        parameters = {}
        for row in range(0, rows - 1):
            label = self.layout().itemAtPosition(row, 0).widget()
            edit = self.layout().itemAtPosition(row, 1).widget()
            parameters[label.text()] = edit.getValue()
        self.circuit.setParameters(parameters)
        self.close()

    def setValues(self):
        """Iterate through all the window widgets and set the widget value
        to match the current parameter value."""
        rows = self.layout().rowCount()
        for row in range(0, rows - 1):
            label_text = self.layout().itemAtPosition(row, 0).widget().text()
            edit = self.layout().itemAtPosition(row, 1).widget()
            if label_text in self.circuit.parameters:
                edit.setValue(self.circuit.parameters[str(label_text)])
            else:
                edit.clearValue()

    def getValue(self, label):
        """Return the value of the item with matching label."""
        rows = self.layout().rowCount()
        for row in range(0, rows - 1):
            label_text = self.layout().itemAtPosition(row, 0).widget().text()
            if label == label_text:
                edit = self.layout().itemAtPosition(row, 1).widget()
                return edit.getValue()

    def cancel(self):
        """Close the window without action when cancel is pressed."""
        self.close()


class InputValueWindow(QtGui.QDialog):
    """Small dialog window for manually setting input values."""

    def __init__(self, input_):
        self.input_ = input_
        self.circuit = self.input_.parentItem()
        super(InputValueWindow, self).__init__(input_.scene().parent().window())
        self.setWindowTitle(self.circuit.name + "." + self.input_.name)
        self.initUI()

    def initUI(self):
        """Initialise the UI elements of the window."""
        layout = QtGui.QGridLayout()
        label = QtGui.QLabel("Value")
        self.edit = CustomLineEdit("FloatLineEdit")
        if "INPUT:"+self.input_.name in self.circuit.parameters:
            self.edit.setText(self.circuit.parameters["INPUT:"+self.input_.name])
        done_button = QtGui.QPushButton("Done")
        QtCore.QObject.connect(done_button, QtCore.SIGNAL("clicked()"),
                               self.setParameters)

        layout.addWidget(label, 0, 0)
        layout.addWidget(self.edit, 0, 1)
        layout.addWidget(done_button, 1, 0, 1, 2)
        self.setLayout(layout)

    def showWindow(self):
        """Show the window and make sure it's activated and on top."""
        self.setWindowTitle(self.circuit.name + "." + self.input_.name)
        self.show()
        self.raise_()
        self.activateWindow()

    def setParameters(self):
        """Set the input value in circuit parameters."""
        parameters = {"INPUT:"+self.input_.name: self.edit.text()}
        self.circuit.setParameters(parameters)
        self.close()
