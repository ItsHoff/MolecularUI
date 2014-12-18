
from PyQt4 import QtGui, QtCore

from ui_circuit import UICircuit

class Hydrogen(UICircuit):

    XSIZE = 50
    YSIZE = 25
    BORDER = 5
    LEFT_RECT = QtCore.QRectF(BORDER, (YSIZE - XSIZE/2 + BORDER)/2,
                              XSIZE/2 - BORDER, XSIZE/2 - BORDER)
    RIGHT_RECT = QtCore.QRectF(LEFT_RECT)
    RIGHT_RECT.moveTo(XSIZE/2, LEFT_RECT.y())
    NORMAL = 0
    VACANT = 1
    NORMAL_COLOR = QtGui.QColor(255, 0, 0)
    VACANT_COLOR = QtGui.QColor(43, 143, 141)

    def __init__(self, x, y):
        super(Hydrogen, self).__init__(x, y)
        self.xsize = self.XSIZE
        self.ysize = self.YSIZE
        self.right_status = self.NORMAL
        self.left_status = self.NORMAL

    def paint(self, painter, options, widget):
        """Paint the circuit. Called automatically by the scene."""
        if not self.scene().surface.contains(self.boundingRect().translated(self.pos())):
            return
        # painter.setBrush(QtGui.QColor(100, 100, 100))
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRect(0, 0, self.xsize, self.ysize)
        if self.left_status == self.VACANT:
            painter.setBrush(self.VACANT_COLOR)
            painter.drawEllipse(self.LEFT_RECT)
        else:
            painter.setBrush(self.NORMAL_COLOR)
            painter.drawEllipse(self.LEFT_RECT)
        if self.right_status == self.VACANT:
            painter.setBrush(self.VACANT_COLOR)
            painter.drawEllipse(self.RIGHT_RECT)
        else:
            painter.setBrush(self.NORMAL_COLOR)
            painter.drawEllipse(self.RIGHT_RECT)

    def mousePressEvent(self, event):
        """If left mouse button is pressed down start dragging
        the circuit. Toggle the circuit selection with control click.
        """
        if event.button() == QtCore.Qt.LeftButton:
            if event.pos().x() < self.xsize/2:
                if self.left_status == self.NORMAL:
                    self.left_status = self.VACANT
                    self.scene().painting_status = self.VACANT
                else:
                    self.left_status = self.NORMAL
                    self.scene().painting_status = self.NORMAL
            else:
                if self.right_status == self.NORMAL:
                    self.right_status = self.VACANT
                    self.scene().painting_status = self.VACANT
                else:
                    self.right_status = self.NORMAL
                    self.scene().painting_status = self.NORMAL
            self.update()

    def mouseReleaseEvent(self, event):
        """End drag when mouse is released."""
        if event.button() == QtCore.Qt.LeftButton:
            self.dragged = False
            self.scene().painting_status = None
            self.scene().views()[0].scroll_dir = None
            self.ensureVisible()
            self.scene().updateSceneRect()

    def mouseMoveEvent(self, event):
        """If circuit is being dragged try to set the circuits
        positions to the mouse position. Circuit will be
        snapping to 100x100 grid.
        """
        if self.scene().painting_status is not None:
            item_to_paint = self.scene().itemAt(event.scenePos())
            if item_to_paint is not None:
                pos = item_to_paint.mapFromScene(event.scenePos())
                if pos.x() < item_to_paint.xsize/2:
                    item_to_paint.left_status = item_to_paint.scene().painting_status
                else:
                    item_to_paint.right_status = item_to_paint.scene().painting_status
                item_to_paint.update()
