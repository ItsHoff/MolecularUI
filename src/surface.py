from PyQt4 import QtGui, QtCore

from hydrogen import Hydrogen

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
        if not isinstance(self.scene().itemAt(x, y), Hydrogen):
            hydrogen = Hydrogen(x-x%Hydrogen.XSIZE, y-y%Hydrogen.YSIZE, self)
            # self.circuits.append(circuit)

    def boundingRect(self):
        return QtCore.QRectF(self.corner, self.size)

    def populate(self):
        y = self.top()
        while y < self.bottom():
            x = self.left()
            while x < self.right():
                self.addHydrogen(x, y)
                x += Hydrogen.XSIZE
            y += Hydrogen.YSIZE

    def populateVerticalLines(self, xmin, xmax):
        for x in range(int(xmin), int(xmax) + Hydrogen.XSIZE, Hydrogen.XSIZE):
            y = self.top()
            items_at_line = self.scene().items(x, y, Hydrogen.XSIZE, self.bottom() - y)
            if len(items_at_line) < (self.bottom() - y)/Hydrogen.YSIZE:
                while y < self.bottom():
                    self.addHydrogen(x, y)
                    y += Hydrogen.YSIZE

    def populateHorizontalLines(self, ymin, ymax):
        for y in range(int(ymin), int(ymax) + Hydrogen.YSIZE, Hydrogen.YSIZE):
            x = self.left()
            items_at_line = self.scene().items(x, y, self.right() - x, Hydrogen.YSIZE)
            if len(items_at_line) < (self.right() - x)/Hydrogen.XSIZE:
                while x < self.right():
                    self.addHydrogen(x, y)
                    x += Hydrogen.XSIZE

    def resize(self, pos, border):
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

    def paint(self, painter, options, widget):
        painter.setPen(QtGui.QColor(0, 0, 0))
        painter.setBrush(QtGui.QColor(48, 48, 122))
        painter.drawRect(self.boundingRect())

    def left(self):
        return self.sceneBoundingRect().left()

    def right(self):
        return self.sceneBoundingRect().right()

    def top(self):
        return self.sceneBoundingRect().top()

    def bottom(self):
        return self.sceneBoundingRect().bottom()

    def setLeft(self, value):
        rect = self.sceneBoundingRect()
        rect.setLeft(value)
        self.corner = rect.topLeft()
        self.size = rect.size()

    def setRight(self, value):
        rect = self.sceneBoundingRect()
        rect.setRight(value)
        self.corner = rect.topLeft()
        self.size = rect.size()

    def setTop(self, value):
        rect = self.sceneBoundingRect()
        rect.setTop(value)
        self.corner = rect.topLeft()
        self.size = rect.size()

    def setBottom(self, value):
        rect = self.sceneBoundingRect()
        rect.setBottom(value)
        self.corner = rect.topLeft()
        self.size = rect.size()
