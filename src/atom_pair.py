from PyQt4 import QtGui, QtCore
import numpy as np

import output
import molecular_scene

class AtomPair(QtGui.QGraphicsItem):

    XSIZE = 50
    YSIZE = 25
    RADIUS = 0.4 * YSIZE
    LEFT_RECT = QtCore.QRectF(output.LEFT_H_POS[0]*XSIZE - RADIUS,
                              output.LEFT_H_POS[1]*YSIZE - RADIUS,
                              2*RADIUS, 2*RADIUS)
    RIGHT_RECT = QtCore.QRectF(output.RIGHT_H_POS[0]*XSIZE - RADIUS,
                               output.RIGHT_H_POS[1]*YSIZE - RADIUS,
                               2*RADIUS, 2*RADIUS)
    VACANT = "VACANT"
    CURRENT_ATOM = "CURRENT_ATOM"
    NORMAL_BRUSH = QtGui.QBrush(QtGui.QColor(255, 0, 0))
    VACANT_BRUSH = QtGui.QBrush(QtGui.QColor(43, 143, 141))
    PEN = QtGui.QPen(QtGui.QColor(0, 0, 0))
    PEN.setWidth(1)

    def __init__(self, x, y, surface, parent=None):
        if parent is None:
            parent = surface
        self.xsize = AtomPair.XSIZE
        self.ysize = AtomPair.YSIZE
        super(AtomPair, self).__init__(parent)
        self.setX(x)
        self.setY(y)
        self.right_status = 0
        self.left_status = 0
        self.surface = surface

    def getOutput(self, result):
        """Add the output information of the item in to the result."""
        if not self.onSurface() or self.overwritten():
            return
        pos = self.scenePos() - self.surface.corner
        out_pos = np.array((pos.x()/self.XSIZE * output.X_SCALE,
                  pos.y()/self.YSIZE * output.Y_SCALE, 0))
        if self.left_status != self.VACANT:
            left_pos = out_pos + output.LEFT_H_POS * output.TOTAL_SCALE
            result.append("%-4s %-10f %-10f %-10f %d" %
                    ((self.surface.atom_types[self.left_status],) +
                     tuple(left_pos) + ((len(result) + 1),)))
        if self.right_status != self.VACANT:
            right_pos = out_pos + output.RIGHT_H_POS * output.TOTAL_SCALE
            result.append("%-4s %-10f %-10f %-10f %d" %
                    ((self.surface.atom_types[self.right_status],) +
                     tuple(right_pos) + ((len(result) + 1),)))

    def getSaveState(self):
        """Return the state of the item without Qt bindings."""
        return SaveAtom(self)

    def onSurface(self):
        """Check if the item is on the surface."""
        if self.collidesWithItem(self.parentItem(), QtCore.Qt.ContainsItemShape):
            return True
        else:
            return False

    def overwritten(self):
        """Check if hydrogen is overwritten by selection box."""
        if (self.surface is self.parentItem() and
           self.getStackedAtom() is not None and
           self.getStackedAtom().scenePos() == self.scenePos()):
            return True
        else:
            return False

    def getStackedAtom(self):
        """Return the other hydrogen possibly stacked with this one."""
        if self.surface is self.parentItem():
            return self.surface.selection_atoms.get((self.x(), self.y()))
        else:
            pos = self.scenePos()
            return self.surface.surface_atoms.get((pos.x(), pos.y()))

    def copyFromSurface(self):
        """Copy the state of surface hydrogen to selected hydrogen."""
        surface_atom = self.getStackedAtom()
        self.left_status = surface_atom.left_status
        self.right_status = surface_atom.right_status
        surface_atom.reset()

    def copyToSurface(self):
        """Copy the status of selected hydrogen to surface hydrogen
        under it."""
        surface_atom = self.getStackedAtom()
        surface_atom.left_status = self.left_status
        surface_atom.right_status = self.right_status

    def reset(self):
        self.left_status = 0
        self.right_status = 0

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
        if not self.onSurface() or self.overwritten():
            return
        painter.setPen(self.PEN)
        if self.scene().current_layer != 0:
            painter.setOpacity(0.5)
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
                if self.left_status != self.VACANT:
                    self.left_status = self.VACANT
                    self.surface.painting_status = self.VACANT
                else:
                    self.left_status = self.surface.current_atom
                    self.surface.painting_status = self.CURRENT_ATOM
            else:
                if self.right_status != self.VACANT:
                    self.right_status = self.VACANT
                    self.surface.painting_status = self.VACANT
                else:
                    self.right_status = self.surface.current_atom
                    self.surface.painting_status = self.CURRENT_ATOM
            self.update()
        else:
            super(AtomPair, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Reset all the flags possibly set by other mouse events."""
        self.surface.painting_status = None

    def mouseMoveEvent(self, event):
        """If were painting the hydrogen, try to set the state of the hydrogen
        under the mouse to the one given by the scene painting_status.
        """
        if self.surface.painting_status is not None:
            line = QtGui.QGraphicsLineItem(QtCore.QLineF(event.scenePos(), event.lastScenePos()),
                                           self.scene().surface)
            for item in line.collidingItems():
                if isinstance(item, AtomPair) and not item.overwritten():
                    l_rect = QtCore.QRectF(-0.1, -0.1, AtomPair.XSIZE/2 + 0.2, AtomPair.YSIZE + 0.2)
                    r_rect = QtCore.QRectF(AtomPair.XSIZE/2 - 0.1, -0.1, AtomPair.XSIZE/2 + 0.2,
                                           AtomPair.YSIZE + 0.2)
                    left_rect = QtGui.QGraphicsRectItem(l_rect.translated(item.scenePos()))
                    right_rect = QtGui.QGraphicsRectItem(r_rect.translated(item.scenePos()))
                    if line.collidesWithItem(left_rect):
                        if self.surface.painting_status == self.CURRENT_ATOM:
                            item.left_status = self.surface.current_atom
                        else:
                            item.left_status = self.VACANT
                    if line.collidesWithItem(right_rect):
                        if self.surface.painting_status == self.CURRENT_ATOM:
                            item.right_status = self.surface.current_atom
                        else:
                            item.right_status = self.VACANT
                    item.update()
            self.scene().removeItem(line)


class SaveAtom(object):

    def __init__(self, atom):
        self.x = atom.x()
        self.y = atom.y()
        self.left_status = atom.left_status
        self.right_status = atom.right_status

    def load(self, surface, parent=None):
        atom = AtomPair(self.x, self.y, surface, parent)
        atom.left_status = self.left_status
        atom.right_status = self.right_status
