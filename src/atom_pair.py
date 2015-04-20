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
    SMALL_RADIUS = 0.25 * YSIZE
    SMALL_LEFT_RECT = QtCore.QRectF(output.LEFT_H_POS[0]*XSIZE - SMALL_RADIUS,
                              output.LEFT_H_POS[1]*YSIZE - SMALL_RADIUS,
                              2*SMALL_RADIUS, 2*SMALL_RADIUS)
    SMALL_RIGHT_RECT = QtCore.QRectF(output.RIGHT_H_POS[0]*XSIZE - SMALL_RADIUS,
                               output.RIGHT_H_POS[1]*YSIZE - SMALL_RADIUS,
                               2*SMALL_RADIUS, 2*SMALL_RADIUS)
    VACANT = "VACANT"
    CURRENT_ATOM = "CURRENT_ATOM"
    BRUSHES = [QtGui.QBrush(QtGui.QColor(255, 0, 0)),
               QtGui.QBrush(QtGui.QColor(255, 255, 0)),
               QtGui.QBrush(QtGui.QColor(0, 255, 0)),
               QtGui.QBrush(QtGui.QColor(0, 255, 255)),
               QtGui.QBrush(QtGui.QColor(0, 0, 255))]
    VACANT_BRUSH = QtGui.QBrush(QtGui.QColor(43, 143, 141))
    PEN = QtGui.QPen(QtGui.QColor(0, 0, 0))
    PEN.setWidth(1)

    def __init__(self, x, y, layer, parent=None):
        if parent is None:
            parent = layer
        self.xsize = AtomPair.XSIZE
        self.ysize = AtomPair.YSIZE
        super(AtomPair, self).__init__(parent)
        self.setX(x)
        self.setY(y)
        self.right_status = 0
        self.left_status = 0
        self.layer = layer

    def getOutput(self, result, options):
        """Add the output information of the item in to the result."""
        if not self.onSurface() or self.overwritten():
            return
        layer_n = self.scene().layers.index(self.layer)

        if layer_n == 0:
            atom_types = options["surface_atom_types"]
        else:
            atom_types = options["substrate_atom_types"]

        if layer_n == 0:
            z_offset = np.array([0, 0, 0])
            left_offset = output.LEFT_H_POS * output.TOTAL_SCALE
            right_offset = output.RIGHT_H_POS * output.TOTAL_SCALE
        elif layer_n == 1:
            z_offset = output.SURFACE_Z
            left_offset = output.SURFACE_LEFT
            right_offset = output.SURFACE_RIGHT
        elif layer_n == 2:
            z_offset = output.INITIAL_Z
            left_offset = output.LAYER_LEFT[(layer_n+2) % 4]
            right_offset = output.LAYER_RIGHT[(layer_n+2) % 4]
        else:
            z_offset = (max((layer_n+2)/4 - 1, 0) * output.Z_OFFSET + output.INITIAL_Z
                        + output.LAYER_Z[(layer_n+2) % 4])
            left_offset = output.LAYER_LEFT[(layer_n+2) % 4]
            right_offset = output.LAYER_RIGHT[(layer_n+2) % 4]

        pos = self.scenePos() - self.layer.corner
        out_pos = np.array((pos.x()/self.XSIZE * output.X_SCALE,
                  pos.y()/self.YSIZE * output.Y_SCALE, 0))
        if self.left_status != self.VACANT:
            left_pos = out_pos + z_offset + left_offset
            result.append("%-4s %-10f %-10f %-10f %d" %
                    ((atom_types[self.left_status],) +
                     tuple(left_pos) + ((len(result) + 1),)))
            if layer_n == options["layers_to_draw"]:
                result.append("%-4s %-10f %-10f %-10f %d" %
                    (("H",) + tuple(left_pos + output.LEFT_BOTTOM_H[layer_n%2])
                    + ((len(result) + 1),)))
                result.append("%-4s %-10f %-10f %-10f %d" %
                    (("H",) + tuple(left_pos + output.RIGHT_BOTTOM_H[layer_n%2])
                    + ((len(result) + 1),)))
        if self.right_status != self.VACANT:
            right_pos = out_pos + z_offset + right_offset
            result.append("%-4s %-10f %-10f %-10f %d" %
                    ((atom_types[self.right_status],) +
                     tuple(right_pos) + ((len(result) + 1),)))
            if layer_n == options["layers_to_draw"]:
                result.append("%-4s %-10f %-10f %-10f %d" %
                    (("H",) + tuple(right_pos + output.LEFT_BOTTOM_H[layer_n%2])
                        + ((len(result) + 1),)))
                result.append("%-4s %-10f %-10f %-10f %d" %
                    (("H",) + tuple(right_pos + output.RIGHT_BOTTOM_H[layer_n%2])
                        + ((len(result) + 1),)))

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
        if (self.layer is self.parentItem() and
           self.getStackedAtom() is not None and
           self.getStackedAtom().scenePos() == self.scenePos()):
            return True
        else:
            return False

    def getStackedAtom(self):
        """Return the other hydrogen possibly stacked with this one."""
        if self.layer is self.parentItem():
            return self.layer.selection_atoms.get((self.x(), self.y()))
        else:
            pos = self.scenePos()
            return self.layer.surface_atoms.get((pos.x(), pos.y()))

    def copyFromSurface(self):
        """Copy the state of surface hydrogen to selected hydrogen."""
        surface_atom = self.getStackedAtom()
        self.left_status = surface_atom.left_status
        self.right_status = surface_atom.right_status
        surface_atom.reset()

    def copyToSurface(self):
        """Copy the status of selected atom to atom under it."""
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
        """Paint the item if its on the layer."""
        if (not self.onSurface() or self.overwritten() or
           self.scene().current_layer != self.layer):
            return
        painter.setPen(self.PEN)
        painter.drawRect(0, 0, self.xsize, self.ysize)
        if self.left_status == self.VACANT:
            painter.setBrush(self.VACANT_BRUSH)
            painter.drawEllipse(self.LEFT_RECT)
        else:
            painter.setBrush(self.BRUSHES[self.left_status])
            painter.drawEllipse(self.LEFT_RECT)
        if self.right_status == self.VACANT:
            painter.setBrush(self.VACANT_BRUSH)
            painter.drawEllipse(self.RIGHT_RECT)
        else:
            painter.setBrush(self.BRUSHES[self.right_status])
            painter.drawEllipse(self.RIGHT_RECT)

    def mousePressEvent(self, event):
        """Toggle the state of the hydrogen when clicked."""
        if self.layer != self.scene().current_layer:
            event.ignore()
            return
        if (event.button() == QtCore.Qt.LeftButton and
           event.modifiers() == QtCore.Qt.NoModifier):
            if event.pos().x() < self.xsize/2:
                if self.left_status != self.layer.current_atom:
                    self.left_status = self.layer.current_atom
                    self.layer.painting_status = self.CURRENT_ATOM
                else:
                    self.left_status = self.VACANT
                    self.layer.painting_status = self.VACANT
            else:
                if self.right_status != self.layer.current_atom:
                    self.right_status = self.layer.current_atom
                    self.layer.painting_status = self.CURRENT_ATOM
                else:
                    self.right_status = self.VACANT
                    self.layer.painting_status = self.VACANT
            self.update()
        else:
            super(AtomPair, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Reset all the flags possibly set by other mouse events."""
        self.layer.painting_status = None

    def mouseMoveEvent(self, event):
        """If were painting the hydrogen, try to set the state of the hydrogen
        under the mouse to the one given by the scene painting_status.
        """
        if self.layer != self.scene().current_layer:
            event.ignore()
            return
        if self.layer.painting_status is not None:
            line = QtGui.QGraphicsLineItem(QtCore.QLineF(event.scenePos(), event.lastScenePos()),
                                           self.scene().current_layer)
            for item in line.collidingItems():
                if (isinstance(item, AtomPair) and not item.overwritten() and
                   item.layer == self.layer and item.onSurface()):
                    l_rect = QtCore.QRectF(-0.1, -0.1, AtomPair.XSIZE/2 + 0.2, AtomPair.YSIZE + 0.2)
                    r_rect = QtCore.QRectF(AtomPair.XSIZE/2 - 0.1, -0.1, AtomPair.XSIZE/2 + 0.2,
                                           AtomPair.YSIZE + 0.2)
                    left_rect = QtGui.QGraphicsRectItem(l_rect.translated(item.scenePos()))
                    right_rect = QtGui.QGraphicsRectItem(r_rect.translated(item.scenePos()))
                    if line.collidesWithItem(left_rect):
                        if self.layer.painting_status == self.CURRENT_ATOM:
                            item.left_status = self.layer.current_atom
                        else:
                            item.left_status = self.VACANT
                    if line.collidesWithItem(right_rect):
                        if self.layer.painting_status == self.CURRENT_ATOM:
                            item.right_status = self.layer.current_atom
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

    def load(self, layer, parent=None):
        atom = AtomPair(self.x, self.y, layer, parent)
        atom.left_status = self.left_status
        atom.right_status = self.right_status
