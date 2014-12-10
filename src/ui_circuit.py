'''
Created on Jun 12, 2014

@author: keisano1
'''

from PyQt4 import QtGui, QtCore

XSIZE = 25
YSIZE = 25
LEFT_RECT = QtCore.QRectF(0, (YSIZE - XSIZE/2)/2,
                               XSIZE/2, XSIZE/2)
RIGHT_RECT = QtCore.QRectF(LEFT_RECT)
RIGHT_RECT.moveTo(LEFT_RECT.x() + XSIZE/2, LEFT_RECT.y())

class UICircuit(QtGui.QGraphicsItem):
    """Graphics item that represents the circuits of the machine."""

    def __init__(self, x, y):
        """Create a circuit defined by the circuit_info and
        place it into the at (x, y)
        """
        super(UICircuit, self).__init__()
        self.setX(x)
        self.setY(y)
        self.setFlag(self.ItemIsSelectable, True)
        # self.setFlag(self.ItemIsMovable, True)
        # self.setFlag(self.ItemSendsScenePositionChanges, True)
        self.xsize = XSIZE
        self.ysize = YSIZE
        self.left_rect = LEFT_RECT
        self.right_rect = RIGHT_RECT
        self.circuit_info = {}
        self.dragged = False
        self.highlighted = False
        self.save_state = SaveCircuit(self)

    def addContextActions(self, menu):
        """Add circuit specific context actions into the menu."""
        pass
        # remove = QtGui.QAction("Remove "+self.name, menu)
        # QtCore.QObject.connect(remove, QtCore.SIGNAL("triggered()"),
                               # self.remove)
        # menu.addAction(remove)

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
        self.circuit_info = save_state.circuit_info

    def boundingRect(self):
        """Return the bounding rectangle of the circuit.
        Required by the scene.
        """
        return QtCore.QRectF(0, 0, self.xsize, self.ysize)

    def paint(self, painter, options, widget):
        """Paint the circuit. Called automatically by the scene."""
        if not self.scene().surface.contains(self.boundingRect().translated(self.pos())):
            self.scene().removeCircuit(self)
            return
        # if self.highlighted:
            # self.setZValue(2)
            # painter.setBrush(QtGui.QColor(188, 244, 184))
        # elif self.isSelected():
            # self.setZValue(1)
            # painter.setBrush(QtGui.QColor(165, 198, 255))
        # else:
        self.setZValue(0)
        painter.setBrush(QtGui.QColor(100, 100, 100))
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRect(0, 0, self.xsize, self.ysize)
        painter.setBrush(QtGui.QColor(255, 0, 0))
        painter.drawEllipse(self.left_rect)
        painter.drawEllipse(self.right_rect)

    def mousePressEvent(self, event):
        """If left mouse button is pressed down start dragging
        the circuit. Toggle the circuit selection with control click.
        """
        if (event.button() == QtCore.Qt.LeftButton and
                event.modifiers() & QtCore.Qt.ControlModifier):
            self.toggleSelection()
            self.scene().saveSelection(0)
        elif event.button() == QtCore.Qt.LeftButton:
            self.dragged = True
        # super(UICircuit, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """End drag when mouse is released."""
        if event.button() == QtCore.Qt.LeftButton:
            self.dragged = False
            self.scene().views()[0].scroll_dir = None
            self.ensureVisible()
            self.scene().updateSceneRect()
        # super(UICircuit, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        """If circuit is being dragged try to set the circuits
        positions to the mouse position. Circuit will be
        snapping to 100x100 grid.
        """
        if self.dragged:
            old_pos = self.pos()
            pos = event.scenePos()
            pos.setX(pos.x() - pos.x() % self.xsize)
            pos.setY(pos.y() - pos.y() % self.ysize)
            self.setPos(pos)
            # If new position collides with other circuit
            # return to old position.
            for circuit in self.scene().circuits:
                if (self.collidesWithItem(circuit) and circuit != self and
                        (not self.isSelected() or not circuit.isSelected())):
                    self.setPos(old_pos)
                    break
            # Relay the movement to all other selected circuits
            if self.isSelected() and self.pos() != old_pos:
                self.setPos(old_pos)
                self.scene().moveSelected(pos - old_pos)
            # Update the connections since some of them might
            # have to be moved with the circuit.
            self.scene().updateMovingSceneRect()
            self.scene().views()[0].autoScroll(event.scenePos())
            self.scene().update()
        # super(UICircuit, self).mouseMoveEvent(event)

    def moveBy(self, amount):
        """Move the circuit by amount."""
        self.setPos(self.pos() +  amount)


class SaveCircuit(object):
    """Container for UICircuit state without Qt bindings. Used for saving."""

    def __init__(self, circuit):
        pos = circuit.pos()
        self.x = pos.x()
        self.y = pos.y()
        self.circuit_info = circuit.circuit_info
        self.loaded_item = None                 # Clear this before saving

    def update(self, circuit):
        """Update the save state to match the current state."""
        self.__init__(circuit)

    def clean(self):
        """Remove the reference to the circuit."""
        self.loaded_item = None
