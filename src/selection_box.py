from PyQt4 import QtGui, QtCore

from atom_pair import AtomPair


class SelectionBox(QtGui.QGraphicsItem):
    """Rubberband selection box."""

    def __init__(self, origin, parent=None, scene=None):
        super(SelectionBox, self).__init__(parent, scene)
        self.setX(origin.x() - origin.x() % AtomPair.XSIZE)
        self.setY(origin.y() - origin.y() % AtomPair.YSIZE)
        self.size = QtCore.QSizeF(origin.x() - self.pos().x(),
                                  origin.y() - self.pos().y())
        self.indexed_rect = None
        self.setZValue(2)

    def setCorner(self, corner):
        """Set the corner to the new value. Signal the geometry change."""
        self.prepareGeometryChange()
        if self.parentItem().contains(corner):
            old_size = self.size
            self.size = QtCore.QSizeF(corner.x() - self.pos().x(),
                                      corner.y() - self.pos().y())
            if self.collidesWithSelections():
                self.size = old_size

    def selectionArea(self):
        """Return the area under the box in scene coordinates."""
        return self.mapToScene(self.boundingRect())

    def finalize(self):
        """Finalize the selection."""
        self.prepareGeometryChange()
        if self.width() < 0:
            self.size.setWidth(abs(self.width()) + AtomPair.XSIZE - abs(self.width()) % AtomPair.XSIZE)
            self.moveBy(-self.width(), 0)
        else:
            self.size.setWidth(self.width() - self.width() % AtomPair.XSIZE + AtomPair.XSIZE)
        if self.height() < 0:
            self.size.setHeight(abs(self.height()) + AtomPair.YSIZE - abs(self.height()) % AtomPair.YSIZE)
            self.moveBy(0, -self.height())
        else:
            self.size.setHeight(self.height() - self.height() % AtomPair.YSIZE + AtomPair.YSIZE)
        if self.height() == 0 or self.width() == 0:
            self.scene().removeItem(self)
            return
        self.populate()
        self.updateIndexing()

    def populate(self):
        """Fill the selection area with hydrogen and
        copy their state from the surface.
        """
        y = 0
        while y < self.height() - 2:
            x = 0
            while x < self.width() - 2:
                atom = AtomPair(x-x%AtomPair.XSIZE, y-y%AtomPair.YSIZE,
                                self.parentItem(), self)
                atom.copyFromSurface()
                x += AtomPair.XSIZE
            y += AtomPair.YSIZE

    def updateIndexing(self):
        """Update the atom index of the surface."""
        new_rect = self.mapRectToScene(self.boundingRect())
        if new_rect != self.indexed_rect:
            if self.indexed_rect is not None:
                self.parentItem().removeFromIndex(self.indexed_rect)
            self.parentItem().addToIndex(self)
            self.indexed_rect = new_rect

    def findAtomAt(self, pos):
        """Return the hydrogen at the given position."""
        return self.parentItem().findAtomAt(pos)

    def addContextActions(self, menu):
        """Add widget specific context actions to the
        context menu given as parameter.
        """
        save = QtGui.QAction("Save block", menu)
        QtCore.QObject.connect(save, QtCore.SIGNAL("triggered()"), self.save)
        menu.addAction(save)

        fill_hydrogen = QtGui.QAction("Fill selected atoms", menu)
        QtCore.QObject.connect(fill_hydrogen, QtCore.SIGNAL("triggered()"), self.fillAtoms)
        menu.addAction(fill_hydrogen)

        remove_hydrogen = QtGui.QAction("Vacate selected atoms", menu)
        QtCore.QObject.connect(remove_hydrogen, QtCore.SIGNAL("triggered()"), self.vacateAtoms)
        menu.addAction(remove_hydrogen)

        remove = QtGui.QAction("Deselect", menu)
        QtCore.QObject.connect(remove, QtCore.SIGNAL("triggered()"), self.deselect)
        menu.addAction(remove)

    def deselect(self):
        """Remove the item from the scene and copy the atoms
        back to the surface.
        """
        for item in self.childItems():
            item.copyToSurface()
        self.reset()

    def save(self):
        """Save the item."""
        self.scene().views()[0].window().saveBlock(self)
        self.scene().views()[0].parent().updateBlocks()

    def vacateAtoms(self):
        for item in self.childItems():
            item.left_status = item.VACANT
            item.right_status = item.VACANT
        self.update()

    def fillAtoms(self):
        for item in self.childItems():
            item.left_status = self.parentItem().current_atom
            item.right_status = self.parentItem().current_atom
        self.update()

    def reset(self):
        self.parentItem().removeFromIndex(self.sceneBoundingRect())
        self.scene().removeItem(self)

    def getOutput(self, result, options):
        for item in self.childItems():
            item.getOutput(result, options)

    def onSurface(self):
        """Check if the item is on the surface."""
        if self.collidesWithItem(self.parentItem(), QtCore.Qt.ContainsItemShape):
            return True
        else:
            return False

    def collidesWithSelections(self):
        """Check if the contact collides with other contacts."""
        for item in self.collidingItems():
            if isinstance(item, SelectionBox):
                return True
        return False

    def resolveCollisions(self):
        """Tries to resolve collisions by moving the item."""
        pos = self.pos()
        for i in range(10):
            self.setPos(pos.x(), pos.y() + i*25)
            if self.onSurface() and not self.collidesWithSelections():
                return True
            self.setPos(pos.x(), pos.y() - i*25)
            if self.onSurface() and not self.collidesWithSelections():
                return True
            self.setPos(pos.x() + i*25, pos.y())
            if self.onSurface() and not self.collidesWithSelections():
                return True
            self.setPos(pos.x() - i*25, pos.y())
            if self.onSurface() and not self.collidesWithSelections():
                return True
        self.setPos(pos)
        return False

    def getSaveState(self):
        """Return the save state of the item."""
        return SaveSelection(self)

    def boundingRect(self):
        """Return the bounding rectangle of the box in item coordinates.
        Make sure that width and height are positive."""
        w = self.size.width() + 2
        h = self.size.height() + 2
        x = min(0, w) - 1
        y = min(0, h) - 1
        return QtCore.QRectF(x, y, abs(w), abs(h))

    def shape(self):
        """Return the shape of the box in item coordinates.
        Make sure that width and height are positive."""
        w = self.size.width() - 0.2
        h = self.size.height() - 0.2
        x = min(0, w) + 0.1
        y = min(0, h) + 0.1
        path = QtGui.QPainterPath()
        path.addRect(QtCore.QRectF(x, y, abs(w), abs(h)))
        return path

    def paint(self, painter, options, widget):
        """Paint the box."""
        pen = QtGui.QPen(QtGui.QColor(255, 255, 0))
        pen.setWidth(2)
        painter.setPen(pen)
        if self.childItems():
            painter.setBrush(QtGui.QColor(80, 80, 122))
        painter.drawRect(0, 0, self.width(), self.height())

    def mousePressEvent(self, event):
        """If left mouse button is pressed down start dragging
        the item. Rotate the item if middle button is pressed.
        """
        if (event.button() == QtCore.Qt.LeftButton and
           event.modifiers() == QtCore.Qt.ShiftModifier):
            self.dragged = True
        else:
            super(SelectionBox, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """End drag when mouse is released."""
        if event.button() == QtCore.Qt.LeftButton:
            self.dragged = False
            self.updateIndexing()
            self.scene().painting_status = None
            self.scene().views()[0].endScroll()
            self.ensureVisible()
            self.scene().updateSceneRect()

    def mouseMoveEvent(self, event):
        """If circuit is being dragged try to set the item position
        to the mouse position.
        """
        if self.dragged:
            old_pos = self.pos()
            new_pos = event.scenePos()
            new_pos.setX(new_pos.x() - new_pos.x() % AtomPair.XSIZE)
            new_pos.setY(new_pos.y() - new_pos.y() % AtomPair.YSIZE)
            self.setPos(new_pos)
            if not self.onSurface() or self.collidesWithSelections():
                self.setPos(new_pos.x(), old_pos.y())
                if not self.onSurface() or self.collidesWithSelections():
                    self.setPos(old_pos.x(), new_pos.y())
                    if not self.onSurface() or self.collidesWithSelections():
                        self.setPos(old_pos)
            self.scene().updateMovingSceneRect()
            self.scene().views()[0].autoScroll(event.scenePos())
            self.update()

    def width(self):
        """Return the width of the surface."""
        return self.size.width()

    def height(self):
        """Return the height of the surface."""
        return self.size.height()

    def left(self):
        """Return the x value of the left border."""
        return self.pos().x()

    def right(self):
        """Return the x value of the right border."""
        return self.pos().x() + self.width()

    def top(self):
        """Return the y value of the top border."""
        return self.pos().y()

    def bottom(self):
        """Return the y value of the bottom border."""
        return self.pos().y() +  self.height()


class SaveSelection(object):

    def __init__(self, selection):
        self.x = selection.pos().x()
        self.y = selection.pos().y()
        self.size = selection.size
        self.width = selection.width()
        self.height = selection.height()
        self.child_items = []
        for child in selection.childItems():
            self.child_items.append(child.getSaveState())

    def load(self, surface):
        selection = SelectionBox(QtCore.QPointF(self.x, self.y), surface)
        selection.size = QtCore.QSizeF(self.width, self.height)
        for child in self.child_items:
            child.load(surface, selection)
        selection.updateIndexing()
        return selection
