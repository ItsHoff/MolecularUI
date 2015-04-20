from PyQt4 import QtGui, QtCore
import numpy as np

from atom_pair import AtomPair
from molecule import Molecule
import output
import molecular_scene
import settings

TOPB = 1
TOPRB = 2
RIGHTB = 3
BOTTOMRB = 4
BOTTOMB = 5
BOTTOMLB = 6
LEFTB = 7
TOPLB = 8


class Surface(QtGui.QGraphicsItem):

    def __init__(self, scene):
        super(Surface, self).__init__(scene=scene)
        self.size = None
        self.corner = None
        self.atom_types = None
        self.surface_atoms = {}
        self.selection_atoms = {}
        self.painting_status = None
        self.current_atom = 0
        self.currently_painting = False

    @classmethod
    def create(cls, scene):
        surface = cls(scene)
        surface.size = QtCore.QSizeF(20 * AtomPair.XSIZE, 40 * AtomPair.YSIZE)
        surface.corner = QtCore.QPointF(-surface.size.width()/2, -surface.size.height()/2)
        surface.populate()
        return surface

    def matchSize(self, other):
        """Match the size of other surface."""
        self.size = other.size
        self.corner = other.corner
        self.populate()

    def addAtom(self, x, y):
        """Add a hydrogen pair on to the surface at (x,y)."""
        if (x, y) not in self.surface_atoms:
            atom = AtomPair(x, y, self)
            self.surface_atoms[(x, y)] = atom

    def addDroppedItem(self, pos, dropped_item):
        """Add a item dropped in to the scene on to the surface."""
        status_bar = self.scene().views()[0].window().statusBar()
        data_type = dropped_item.data(0, QtCore.Qt.UserRole)
        data = dropped_item.data(0, QtCore.Qt.UserRole + 1)
        if data_type == "BLOCK":
            new_item = data.insert(self)
            new_item.setPos(pos.x() - pos.x()%AtomPair.XSIZE,
                            pos.y() - pos.y()%AtomPair.YSIZE)
        elif data_type == "MOLECULE":
            if self.scene().surface is self:
                new_item = Molecule(pos.x(), pos.y(), data, self)
            else:
                status_bar.showMessage("Molecules can only be added to the surface.", 3000)
                return
        if not new_item.resolveCollisions():
            self.scene().removeItem(new_item)
            status_bar.showMessage("Item couldn't be added there.", 3000)
        elif data_type == "BLOCK":
            new_item.updateIndexing()

    def indexAtoms(self):
        """Add unindexed surface atoms to the index."""
        for item in self.childItems():
            if isinstance(item, AtomPair):
                if not (item.x(), item.y()) in self.surface_atoms:
                    self.surface_atoms[item.x(), item.y()] = item

    def findAtomAt(self, pos):
        """Return the hydrogen at the given position."""
        key = (pos.x() - pos.x()%AtomPair.XSIZE, pos.y() - pos.y()%AtomPair.YSIZE)
        if key in self.selection_atoms:
            return self.selection_atoms[key]
        elif key in self.surface_atoms:
            return self.surface_atoms[key]
        else:
            return None

    def removeFromIndex(self, rect):
        """Remove items inside the given rectangle from the selection index."""
        xmin = rect.left() + AtomPair.XSIZE - rect.left() % AtomPair.XSIZE
        xmax = rect.right() - AtomPair.XSIZE
        ymin = rect.top() + AtomPair.YSIZE - rect.top() % AtomPair.YSIZE
        ymax = rect.bottom() - AtomPair.YSIZE
        for x in range(int(xmin), int(xmax), AtomPair.XSIZE):
            for y in range(int(ymin), int(ymax), AtomPair.YSIZE):
                del self.selection_atoms[(x, y)]

    def addToIndex(self, selection):
        """Add child items of selection to the index."""
        for item in selection.childItems():
            pos = item.scenePos()
            self.selection_atoms[(pos.x(), pos.y())] = item

    def boundingRect(self):
        """Return the bounding rectangle of the surface."""
        return QtCore.QRectF(self.corner - QtCore.QPointF(2, 2),
                             self.size + QtCore.QSizeF(4, 4))

    def populate(self):
        """Fill the surface with hydrogen."""
        y = self.top()
        while y < self.bottom():
            x = self.left()
            while x < self.right():
                self.addAtom(x, y)
                x += AtomPair.XSIZE
            y += AtomPair.YSIZE

    def populateVerticalLines(self, xmin, xmax):
        """Fill the vertical lines between xmin and xmax with hydrogen."""
        for x in range(int(xmin), int(xmax) + AtomPair.XSIZE, AtomPair.XSIZE):
            y = self.top()
            while y < self.bottom():
                self.addAtom(x, y)
                y += AtomPair.YSIZE

    def populateHorizontalLines(self, ymin, ymax):
        """Fill the horizontal lines between ymin and ymax with hydrogen."""
        for y in range(int(ymin), int(ymax) + AtomPair.YSIZE, AtomPair.YSIZE):
            x = self.left()
            while x < self.right():
                self.addAtom(x, y)
                x += AtomPair.XSIZE

    def resize(self, pos, border):
        """Resize the surface by moving given border to the given position."""
        self.prepareGeometryChange()
        old_rect = QtCore.QRectF(self.corner, self.size)
        if border == LEFTB or border == BOTTOMLB or border == TOPLB:
            if pos.x() < self.right():
                if pos.x() < self.left() - AtomPair.XSIZE:
                    self.setLeft(pos.x() - pos.x() % AtomPair.XSIZE + AtomPair.XSIZE)
                    self.populateVerticalLines(self.left(), old_rect.left())
                elif pos.x() > self.left() + AtomPair.XSIZE:
                    self.setLeft(pos.x() - pos.x() % AtomPair.XSIZE)
        if border == RIGHTB or border == BOTTOMRB or border == TOPRB:
            if pos.x() > self.left():
                if pos.x() < self.right() - AtomPair.XSIZE:
                    self.setRight(pos.x() - pos.x() % AtomPair.XSIZE + AtomPair.XSIZE)
                elif pos.x() > self.right() + AtomPair.XSIZE:
                    self.setRight(pos.x() - pos.x() % AtomPair.XSIZE)
                    self.populateVerticalLines(old_rect.right(), self.right())
        if border == TOPB or border == TOPLB or border == TOPRB:
            if pos.y() < self.bottom():
                if pos.y() < self.top() - AtomPair.YSIZE:
                    self.setTop(pos.y() - pos.y() % AtomPair.YSIZE + AtomPair.YSIZE)
                    self.populateHorizontalLines(self.top(), old_rect.top())
                elif pos.y() > self.top() + AtomPair.YSIZE:
                    self.setTop(pos.y() - pos.y() % AtomPair.YSIZE)
        if border == BOTTOMB or border == BOTTOMLB or border == BOTTOMRB:
            if pos.y() > self.top():
                if pos.y() < self.bottom() - AtomPair.YSIZE:
                    self.setBottom(pos.y() - pos.y() % AtomPair.YSIZE + AtomPair.YSIZE)
                elif pos.y() > self.bottom() + AtomPair.YSIZE:
                    self.setBottom(pos.y() - pos.y() % AtomPair.YSIZE)
                    self.populateHorizontalLines(old_rect.bottom(), self.bottom())
        # Ignore the changes if contacts are outside of the new surface
        for item in self.childItems():
            if not isinstance(item, AtomPair):
                if not item.onSurface():
                    self.size = old_rect.size()
                    self.corner = old_rect.topLeft()
                    return False

    def getOutput(self, result, options):
        """Get the output information of the surface and its child items."""
        for item in self.childItems():
            item.getOutput(result, options)
        return result

    def getSaveState(self):
        return SaveSurface(self)

    def reset(self):
        pass

    def addContextActions(self, menu):
        """Add item specific context actions in to the menu."""
        pass

    def paint(self, painter, options, widget):
        """Draw the surface."""
        painter.setPen(QtGui.QColor(0, 0, 0))
        painter.setBrush(QtGui.QColor(48, 48, 122))
        painter.drawRect(QtCore.QRectF(self.corner, self.size))

    def width(self):
        """Return the width of the surface."""
        return self.size.width()

    def height(self):
        """Return the height of the surface."""
        return self.size.height()

    def left(self):
        """Return the x value of the left border."""
        return self.corner.x()

    def right(self):
        """Return the x value of the right border."""
        return self.corner.x() + self.size.width()

    def top(self):
        """Return the y value of the top border."""
        return self.corner.y()

    def bottom(self):
        """Return the y value of the bottom border."""
        return self.corner.y() + self.size.height()

    def setLeft(self, value):
        """Set the x value of the left border."""
        old_left = self.left()
        self.corner.setX(value)
        self.size.setWidth(self.width() - value + old_left)

    def setRight(self, value):
        """Set the x value of the right border."""
        old_right = self.right()
        self.size.setWidth(self.width() + value - old_right)

    def setTop(self, value):
        """Set the y value of the top border."""
        old_top = self.top()
        self.corner.setY(value)
        self.size.setHeight(self.height() - value + old_top)

    def setBottom(self, value):
        """Set the y value of the bottom border."""
        old_bottom = self.bottom()
        self.size.setHeight(self.height() + value - old_bottom)


class SaveSurface(object):

    def __init__(self, surface):
        self.x = surface.corner.x()
        self.y = surface.corner.y()
        self.width = surface.width()
        self.height = surface.height()
        self.atom_types = surface.atom_types
        self.child_items = []
        for child in surface.childItems():
            self.child_items.append(child.getSaveState())

    def load(self, scene):
        surface = Surface(scene)
        surface.corner = QtCore.QPointF(self.x, self.y)
        surface.size = QtCore.QSizeF(self.width, self.height)
        surface.atom_types = self.atom_types
        scene.surface = surface
        for child in self.child_items:
            child.load(surface)
        surface.indexAtoms()
        return surface
