"""Module containing the RecorderSelect widget."""

from PyQt4 import QtGui, QtCore

import ui_circuit


class RecorderSelect(QtGui.QWidget):
    """Widget for selecting the recorder output of the scanner."""

    def __init__(self):
        super(RecorderSelect, self).__init__()
        self.recorder = None
        self.button = QtGui.QToolButton(self)
        self.button.setIcon(self.style().standardIcon(QtGui.QStyle.SP_ArrowRight))
        self.label = QtGui.QLabel("No recorder selected", self)
        self.layout = QtGui.QHBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        self.connect(self.button, QtCore.SIGNAL("clicked()"), self.startSelection)

    def startSelection(self):
        """Setup the window to take a selection."""
        self.parent().circuit.scene().highlightOutputs()
        self.grabMouse()
        self.window().hide()

    def setValue(self, value):
        """Set the value of the widget."""
        # Update the name
        recorder = self.parent().circuit.scene().findMatchingCircuit(value)
        if recorder is not None:
            recorder.getSaveState()
        else:
            self.clearValue()
            return
        self.recorder = value
        self.label.setText(self.recorder.name)

    def getValue(self):
        """Return the value of the circuit."""
        # Find the circuit linked to the save state
        recorder = self.parent().circuit.scene().findMatchingCircuit(self.recorder)
        if recorder is not None:
            return self.recorder

    def clearValue(self):
        """Clear the value of the widget."""
        self.recorder = None
        self.label.setText("No recorder selected")

    def findRecorder(self, items):
        """Check the list of items for outputs and set the selected
        recorder if output is found.
        """
        for item in items:
            if isinstance(item, ui_circuit.UICircuit):
                if item.circuit_info.circuit_type == "output":
                    self.setValue(item.getSaveState())

    def mapToScene(self, local_point):
        """Map the point from local coordinates to scene coordinates."""
        view = self.parent().circuit.scene().views()[0]
        global_point = self.mapToGlobal(local_point)
        view_point = view.mapFromGlobal(global_point)
        scene_point = view.mapToScene(view_point)
        return scene_point

    def mousePressEvent(self, event):
        """Check for selection on left click otherwise call the graphics view
        to allow movement while selecting.
        """
        if event.button() == QtCore.Qt.LeftButton:
            scene_pos = self.mapToScene(event.pos())
            items  = self.parent().circuit.scene().items(scene_pos)
            self.findRecorder(items)
            self.parent().circuit.scene().clearHighlight()
            self.parent().circuit.ensureVisible()
            self.window().show()
            self.releaseMouse()
        else:
            self.parent().circuit.scene().views()[0].mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Call the graphics view to allow movement while selecting."""
        self.parent().circuit.scene().views()[0].mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        """Call the graphics view to allow movement while selecting."""
        self.parent().circuit.scene().views()[0].mouseMoveEvent(event)
