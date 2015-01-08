from PyQt4 import QtGui, QtCore
import numpy as np

from hydrogen import Hydrogen
from contact import Contact
import output

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
        self.size = QtCore.QSizeF(20 * Hydrogen.XSIZE, 40 * Hydrogen.YSIZE)
        super(Surface, self).__init__(scene=scene)
        self.corner = QtCore.QPointF(-10 * Hydrogen.XSIZE, -20 * Hydrogen.YSIZE)
        self.populate()

    def addHydrogen(self, x, y):
        """Add a hydrogen pair on to the surface at (x,y)."""
        if not isinstance(self.scene().itemAt(x, y), Hydrogen):
            Hydrogen(x-x%Hydrogen.XSIZE, y-y%Hydrogen.YSIZE, self)

    def addDroppedItem(self, pos):
        """Add a item dropped in to the scene on to the surface."""
        Contact(pos.x(), pos.y(), self)

    def boundingRect(self):
        """Return the bounding rectangle of the surface."""
        return QtCore.QRectF(self.corner, self.size)

    def populate(self):
        """Fill the surface with hydrogen."""
        y = self.top()
        while y < self.bottom():
            x = self.left()
            while x < self.right():
                self.addHydrogen(x, y)
                x += Hydrogen.XSIZE
            y += Hydrogen.YSIZE

    def populateVerticalLines(self, xmin, xmax):
        """Fill the vertical lines between xmin and xmax with hydrogen."""
        for x in range(int(xmin), int(xmax) + Hydrogen.XSIZE, Hydrogen.XSIZE):
            y = self.top()
            items_at_line = self.scene().items(x, y, Hydrogen.XSIZE, self.bottom() - y)
            if len(items_at_line) < (self.bottom() - y)/Hydrogen.YSIZE:
                while y < self.bottom():
                    self.addHydrogen(x, y)
                    y += Hydrogen.YSIZE

    def populateHorizontalLines(self, ymin, ymax):
        """Fill the horizontal lines between ymin and ymax with hydrogen."""
        for y in range(int(ymin), int(ymax) + Hydrogen.YSIZE, Hydrogen.YSIZE):
            x = self.left()
            items_at_line = self.scene().items(x, y, self.right() - x, Hydrogen.YSIZE)
            if len(items_at_line) < (self.right() - x)/Hydrogen.XSIZE:
                while x < self.right():
                    self.addHydrogen(x, y)
                    x += Hydrogen.XSIZE

    def resize(self, pos, border):
        """Resize the surface by moving given border to the given position."""
        old_rect = QtCore.QRectF(self.boundingRect())
        if border == LEFTB or border == BOTTOMLB or border == TOPLB:
            if pos.x() < self.right():
                if pos.x() < self.left() - Hydrogen.XSIZE:
                    self.setLeft(pos.x() - pos.x() % Hydrogen.XSIZE + Hydrogen.XSIZE)
                    self.populateVerticalLines(self.left(), old_rect.left())
                elif pos.x() > self.left() + Hydrogen.XSIZE:
                    self.setLeft(pos.x() - pos.x() % Hydrogen.XSIZE)
        if border == RIGHTB or border == BOTTOMRB or border == TOPRB:
            if pos.x() > self.left():
                if pos.x() < self.right() - Hydrogen.XSIZE:
                    self.setRight(pos.x() - pos.x() % Hydrogen.XSIZE + Hydrogen.XSIZE)
                elif pos.x() > self.right() + Hydrogen.XSIZE:
                    self.setRight(pos.x() - pos.x() % Hydrogen.XSIZE)
                    self.populateVerticalLines(old_rect.right(), self.right())
        if border == TOPB or border == TOPLB or border == TOPRB:
            if pos.y() < self.bottom():
                if pos.y() < self.top() - Hydrogen.YSIZE:
                    self.setTop(pos.y() - pos.y() % Hydrogen.YSIZE + Hydrogen.YSIZE)
                    self.populateHorizontalLines(self.top(), old_rect.top())
                elif pos.y() > self.top() + Hydrogen.YSIZE:
                    self.setTop(pos.y() - pos.y() % Hydrogen.YSIZE)
        if border == BOTTOMB or border == BOTTOMLB or border == BOTTOMRB:
            if pos.y() > self.top():
                if pos.y() < self.bottom() - Hydrogen.YSIZE:
                    self.setBottom(pos.y() - pos.y() % Hydrogen.YSIZE + Hydrogen.YSIZE)
                elif pos.y() > self.bottom() + Hydrogen.YSIZE:
                    self.setBottom(pos.y() - pos.y() % Hydrogen.YSIZE)
                    self.populateHorizontalLines(old_rect.bottom(), self.bottom())

    def getOutput(self):
        """Get the output information of the surface and its child items."""
        result = []
        base_translation = output.LEFT_H_POS * output.TOTAL_SCALE
        with open("../molecules/base.xyz", "r") as f:
            for i in range(int(self.width()/Hydrogen.XSIZE)):
                x_offset = i*output.X_SCALE
                for j in range(int(self.height()/Hydrogen.YSIZE)):
                    y_offset = j*output.Y_SCALE
                    count = 0
                    f.seek(0)
                    for line in f:
                        count += 1
                        if count > 2:
                            split = line.split()
                            pos = np.array([float(x) for x in split[1:4]])
                            pos = pos + x_offset + y_offset + base_translation
                            result.append("%-4s %-10f %-10f %-10f %d" %
                                ((split[0],) + tuple(pos) + ((len(result) + 1),)))
        for item in self.childItems():
            item.getOutput(result)
        return result

    def addContextActions(self, menu):
        """Add item specific context actions in to the menu."""
        pass

    def paint(self, painter, options, widget):
        """Draw the surface."""
        painter.setPen(QtGui.QColor(0, 0, 0))
        painter.setBrush(QtGui.QColor(48, 48, 122))
        painter.drawRect(self.boundingRect())

    def left(self):
        """Return the x value of the left border."""
        return self.sceneBoundingRect().left()

    def right(self):
        """Return the x value of the right border."""
        return self.sceneBoundingRect().right()

    def top(self):
        """Return the y value of the top border."""
        return self.sceneBoundingRect().top()

    def bottom(self):
        """Return the y value of the bottom border."""
        return self.sceneBoundingRect().bottom()

    def setLeft(self, value):
        """Set the x value of the left border."""
        rect = self.sceneBoundingRect()
        rect.setLeft(value)
        self.corner = rect.topLeft()
        self.size = rect.size()

    def setRight(self, value):
        """Set the x value of the right border."""
        rect = self.sceneBoundingRect()
        rect.setRight(value)
        self.corner = rect.topLeft()
        self.size = rect.size()

    def setTop(self, value):
        """Set the y value of the top border."""
        rect = self.sceneBoundingRect()
        rect.setTop(value)
        self.corner = rect.topLeft()
        self.size = rect.size()

    def setBottom(self, value):
        """Set the y value of the bottom border."""
        rect = self.sceneBoundingRect()
        rect.setBottom(value)
        self.corner = rect.topLeft()
        self.size = rect.size()
