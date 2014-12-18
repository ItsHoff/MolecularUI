'''
Created on Jun 12, 2014

@author: keisano1
'''

from PyQt4 import QtGui, QtCore

class UICircuit(QtGui.QGraphicsItem):
    """Graphics item that represents the circuits of the machine."""

    def __init__(self, x, y):
        """Create a circuit defined by the circuit_info and
        place it into the at (x, y)
        """
        super(UICircuit, self).__init__()
        self.setX(x)
        self.setY(y)
        self.xsize = 0
        self.ysize = 0
        self.save_state = SaveCircuit(self)

    def addContextActions(self, menu):
        """Add circuit specific context actions into the menu."""
        pass

    def remove(self):
        """Call the scene to remove the circuit."""
        value = self.scene().showMessageBox("Remove "+self.name,
                                    "Do you want to remove %s?" % self.name)
        if value == QtGui.QMessageBox.Yes:
            self.scene().removeCircuit(self)

    def toggleSelection(self):
        """Toggle the selection state."""
        if self.isSelected():
            self.setSelected(False)
        else:
            self.setSelected(True)

    def getSaveState(self):
        """Return the current state of the circuit without the Qt bindings
        for saving.
        """
        self.save_state.update(self)
        return self.save_state

    def getCleanSaveState(self):
        """Return the current state of the circuit without the Qt bindings
        for saving.
        """
        self.save_state.update(self)
        self.save_state.clean()
        return self.save_state

    def loadSaveState(self, save_state):
        """Load the state given in save_state."""
        save_state.loaded_item = self
        self.save_state = save_state
        self.setX(save_state.x)
        self.setY(save_state.y)

    def boundingRect(self):
        """Return the bounding rectangle of the circuit.
        Required by the scene.
        """
        bounding_rect = QtCore.QRectF(0, 0, self.xsize, self.ysize)
        return bounding_rect

    def paint(self, painter, options, widget):
        """Paint the circuit. Called automatically by the scene."""
        pass

    def mousePressEvent(self, event):
        """If left mouse button is pressed down start dragging
        the circuit. Toggle the circuit selection with control click.
        """
        pass

    def mouseReleaseEvent(self, event):
        """End drag when mouse is released."""
        pass

    def mouseMoveEvent(self, event):
        """If circuit is being dragged try to set the circuits
        positions to the mouse position. Circuit will be
        snapping to 100x100 grid.
        """
        pass

    def moveBy(self, amount):
        """Move the circuit by amount."""
        self.setPos(self.pos() +  amount)


class SaveCircuit(object):
    """Container for UICircuit state without Qt bindings. Used for saving."""

    def __init__(self, circuit):
        pos = circuit.pos()
        self.x = pos.x()
        self.y = pos.y()
        self.loaded_item = None                 # Clear this before saving

    def update(self, circuit):
        """Update the save state to match the current state."""
        self.__init__(circuit)

    def clean(self):
        """Remove the reference to the circuit."""
        self.loaded_item = None
