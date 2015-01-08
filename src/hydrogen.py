
from PyQt4 import QtGui, QtCore

import output

class Hydrogen(QtGui.QGraphicsItem):

    XSIZE = 50
    YSIZE = 25
    RADIUS = 0.4 * YSIZE
    LEFT_RECT = QtCore.QRectF(output.LEFT_H_POS[0]*XSIZE - RADIUS,
                              output.LEFT_H_POS[2]*YSIZE - RADIUS,
                              2*RADIUS, 2*RADIUS)
    RIGHT_RECT = QtCore.QRectF(output.RIGHT_H_POS[0]*XSIZE - RADIUS,
                               output.RIGHT_H_POS[2]*YSIZE - RADIUS,
                               2*RADIUS, 2*RADIUS)
    NORMAL = 0
    VACANT = 1
    NORMAL_COLOR = QtGui.QColor(255, 0, 0)
    VACANT_COLOR = QtGui.QColor(43, 143, 141)

    def __init__(self, x, y, parent):
        self.xsize = Hydrogen.XSIZE
        self.ysize = Hydrogen.YSIZE
        super(Hydrogen, self).__init__(parent)
        self.setX(x)
        self.setY(y)
        self.right_status = self.NORMAL
        self.left_status = self.NORMAL

    def getOutput(self, result):
        """Add the output information of the item in to the result."""
        if not self.onSurface():
            return
        pos = self.pos()
        out_pos = (pos.x()/self.XSIZE * output.X_SCALE +
                  pos.y()/self.YSIZE * output.Y_SCALE)
        if self.left_status == self.NORMAL:
            left_pos = out_pos + output.LEFT_H_POS * output.TOTAL_SCALE
            result.append("%-4s %-10f %-10f %-10f %d" %
                    (("HE",) + tuple(left_pos) + ((len(result) + 1),)))
        if self.right_status == self.NORMAL:
            right_pos = out_pos + output.RIGHT_H_POS * output.TOTAL_SCALE
            result.append("%-4s %-10f %-10f %-10f %d" %
                    (("HE",) + tuple(right_pos) + ((len(result) + 1),)))

    def onSurface(self):
        """Check if the item is on the surface."""
        if self.parentItem().collidesWithItem(self):
            return True
        else:
            return False

    def addContextActions(self, menu):
        """Add item specific context actions to the menu."""
        pass

    def boundingRect(self):
        """Return the bounding rectangle of the item."""
        return QtCore.QRectF(0, 0, self.xsize, self.ysize)

    def paint(self, painter, options, widget):
        """Paint the item if its on the surface."""
        if not self.onSurface():
            return
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
        """Toggle the state of the hydrogen when clicked."""
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
        """Reset all the flags possibly set by other mouse events."""
        self.scene().painting_status = None

    def mouseMoveEvent(self, event):
        """If were painting the hydrogen, try to set the state of the hydrogen
        under the mouse to the one given by the scene painting_status.
        """
        if self.scene().painting_status is not None:
            item_to_paint = self.scene().itemAt(event.scenePos())
            if item_to_paint is not None:
                pos = item_to_paint.mapFromScene(event.scenePos())
                if pos.x() < item_to_paint.xsize/2:
                    item_to_paint.left_status = self.scene().painting_status
                else:
                    item_to_paint.right_status = self.scene().painting_status
                item_to_paint.update()