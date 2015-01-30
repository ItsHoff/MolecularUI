from PyQt4 import QtGui, QtCore
import numpy as np

import output
import molecular_scene

class Hydrogen(QtGui.QGraphicsItem):

    XSIZE = 50
    YSIZE = 25
    RADIUS = 0.4 * YSIZE
    LEFT_RECT = QtCore.QRectF(output.LEFT_H_POS[0]*XSIZE - RADIUS,
                              output.LEFT_H_POS[1]*YSIZE - RADIUS,
                              2*RADIUS, 2*RADIUS)
    RIGHT_RECT = QtCore.QRectF(output.RIGHT_H_POS[0]*XSIZE - RADIUS,
                               output.RIGHT_H_POS[1]*YSIZE - RADIUS,
                               2*RADIUS, 2*RADIUS)
    NORMAL = 0
    VACANT = 1
    NORMAL_BRUSH = QtGui.QBrush(QtGui.QColor(255, 0, 0))
    VACANT_BRUSH = QtGui.QBrush(QtGui.QColor(43, 143, 141))
    PEN = QtGui.QPen(QtGui.QColor(0, 0, 0))
    PEN.setWidth(1)

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
        if not self.onSurface() or self.overwritten():
            return
        if self.parentItem().parentItem() is not None:
            pos = self.scenePos() - self.parentItem().parentItem().corner
        else:
            pos = self.pos() - self.parentItem().corner
        out_pos = np.array((pos.x()/self.XSIZE * output.X_SCALE,
                  pos.y()/self.YSIZE * output.Y_SCALE, 0))
        if self.left_status == self.NORMAL:
            left_pos = out_pos + output.LEFT_H_POS * output.TOTAL_SCALE
            result.append("%-4s %-10f %-10f %-10f %d" %
                    (("HE",) + tuple(left_pos) + ((len(result) + 1),)))
        if self.right_status == self.NORMAL:
            right_pos = out_pos + output.RIGHT_H_POS * output.TOTAL_SCALE
            result.append("%-4s %-10f %-10f %-10f %d" %
                    (("HE",) + tuple(right_pos) + ((len(result) + 1),)))

    def getSaveState(self):
        """Return the state of the item without Qt bindings."""
        return SaveHydrogen(self)

    def onSurface(self):
        """Check if the item is on the surface."""
        if self.collidesWithItem(self.parentItem(), QtCore.Qt.ContainsItemShape):
            return True
        else:
            return False

    def overwritten(self):
        """Check if hydrogen is overwritten by selection box."""
        if (self.parentItem().parentItem() is None and
           self.getStackedHydrogen() is not None):
            return True
        else:
            return False

    def getStackedHydrogen(self):
        """Return the other hydrogen possibly stacked with this one."""
        for item in self.collidingItems():
            if isinstance(item, Hydrogen):
                return item
        return None

    def copyFromSurface(self):
        """Copy the state of surface hydrogen to selected hydrogen."""
        if self.parentItem().parentItem() is not None:
            surface_hydrogen = self.getStackedHydrogen()
            self.left_status = surface_hydrogen.left_status
            self.right_status = surface_hydrogen.right_status
            surface_hydrogen.reset()

    def copyToSurface(self):
        """Copy the status of selected hydrogen to surface hydrogen
        under it."""
        if self.parentItem().parentItem() is not None:
            surface_hydrogen = self.getStackedHydrogen()
            surface_hydrogen.left_status = self.left_status
            surface_hydrogen.right_status = self.right_status

    def reset(self):
        self.left_status = Hydrogen.NORMAL
        self.right_status = Hydrogen.NORMAL

    def addContextActions(self, menu):
        """Add item specific context actions to the menu."""
        pass

    def boundingRect(self):
        """Return the bounding rectangle of the item."""
        return QtCore.QRectF(0, 0, self.xsize, self.ysize)

    def shape(self):
        """Return the shape of the item."""
        path = QtGui.QPainterPath()
        path.addRect(QtCore.QRectF(0.2, 0.2, self.xsize - 0.4, self.ysize - 0.4))
        return path

    def paint(self, painter, options, widget):
        """Paint the item if its on the surface."""
        if not self.onSurface():
            return
        painter.setPen(self.PEN)
        painter.drawRect(0, 0, self.xsize, self.ysize)
        if self.left_status == self.VACANT:
            painter.setBrush(self.VACANT_BRUSH)
            painter.drawEllipse(self.LEFT_RECT)
        else:
            painter.setBrush(self.NORMAL_BRUSH)
            painter.drawEllipse(self.LEFT_RECT)
        if self.right_status == self.VACANT:
            painter.setBrush(self.VACANT_BRUSH)
            painter.drawEllipse(self.RIGHT_RECT)
        else:
            painter.setBrush(self.NORMAL_BRUSH)
            painter.drawEllipse(self.RIGHT_RECT)

    def mousePressEvent(self, event):
        """Toggle the state of the hydrogen when clicked."""
        if (event.button() == QtCore.Qt.LeftButton and
           event.modifiers() == QtCore.Qt.NoModifier):
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
        else:
            super(Hydrogen, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Reset all the flags possibly set by other mouse events."""
        self.scene().painting_status = None

    def mouseMoveEvent(self, event):
        """If were painting the hydrogen, try to set the state of the hydrogen
        under the mouse to the one given by the scene painting_status.
        """
        if self.scene().painting_status is not None:
            if self.scene().paint_mode == molecular_scene.PAINT_SURFACE_ONLY:
                item_to_paint = None
                for item in self.scene().items(event.scenePos()):
                    if isinstance(item, Hydrogen):
                        item_to_paint = item
                        break
            else:
                item_to_paint = self.scene().itemAt(event.scenePos())
            if isinstance(item_to_paint, Hydrogen):
                pos = item_to_paint.mapFromScene(event.scenePos())
                if pos.x() < item_to_paint.xsize/2:
                    item_to_paint.left_status = self.scene().painting_status
                else:
                    item_to_paint.right_status = self.scene().painting_status
                item_to_paint.update()


class SaveHydrogen(object):

    def __init__(self, hydrogen):
        self.x = hydrogen.x()
        self.y = hydrogen.y()
        self.left_status = hydrogen.left_status
        self.right_status = hydrogen.right_status

    def load(self, surface):
        hydrogen = Hydrogen(self.x, self.y, surface)
        hydrogen.left_status = self.left_status
        hydrogen.right_status = self.right_status
