import math

from PyQt4 import QtCore, QtGui
import numpy as np

from hydrogen import Hydrogen
import output

class Contact(QtGui.QGraphicsItem):

    XSIZE = 3*Hydrogen.XSIZE
    YSIZE = 4*Hydrogen.YSIZE
    PATH = QtGui.QPainterPath()
    PATH.setFillRule(QtCore.Qt.WindingFill)
    tip_angle = math.degrees(math.atan(13.0/27 * YSIZE/XSIZE))
    PATH.moveTo(4*XSIZE/13 + 20, 0)
    PATH.arcTo(4*XSIZE/13 - 10, 0, 20, 20, 90, tip_angle)
    PATH.arcTo(0, YSIZE/3 - 10, 20, 20, 90 + 2*tip_angle, 90 - 2*tip_angle)
    PATH.arcTo(0, 2*YSIZE/3 - 10, 20, 20, 180, 90 - 2*tip_angle)
    PATH.arcTo(4*XSIZE/13 - 10, YSIZE - 20, 20, 20, 270 - tip_angle, tip_angle)
    PATH.arcTo(XSIZE - 20, YSIZE - 20, 20, 20, 270, 90)
    PATH.arcTo(XSIZE - 20, 0, 20, 20, 0, 90)
    PATH.closeSubpath()

    def __init__(self, x, y, parent=None):
        super(Contact, self).__init__(parent)
        self.setX(x)
        self.setY(y)
        self.xsize = self.XSIZE
        self.ysize = self.YSIZE
        self.dragged = False
        self.setZValue(1)
        self.translate(-25, -25)
        self.setTransformOriginPoint(50, 50)

    def getOutput(self, result):
        """Add the output data of the contact in to the results if it is
        on the surface."""
        if self.onSurface():
            pos = self.pos() - self.parentItem().corner
            out_pos = 1.0*pos.x()/Hydrogen.XSIZE * output.X_SCALE
            out_pos += 1.0*pos.y()/Hydrogen.YSIZE * output.Y_SCALE
            translation = 0.5*output.X_SCALE + output.Y_SCALE + output.HEIGHT
            rotation_m = output.getClockwiseRotationM(self.rotation())
            with open("../molecules/contact.xyz", "r") as f:
                count = 0
                f.seek(0)
                for line in f:
                    count += 1
                    if count > 2:
                        split = line.split()
                        atom_pos = np.array([float(x) for x in split[1:4]])
                        atom_pos = np.dot(rotation_m, atom_pos) + out_pos + translation
                        result.append("%-4s %-10f %-10f %-10f %d" %
                            ((split[0],) + tuple(atom_pos) + ((len(result) + 1),)))

    def getSaveState(self):
        """Return the state of the item without Qt bindings."""
        return SaveContact(self)

    def onSurface(self):
        """Check if the item is on the surface."""
        if self.parentItem().collidesWithItem(self):
            return True
        else:
            return False

    def reset(self):
        self.scene().removeItem(self)

    def addContextActions(self, menu):
        """Add item specific context actions to the menu."""
        pass

    def boundingRect(self):
        """Return the bounding rectangle of the item."""
        return QtCore.QRectF(0, 0, self.xsize, self.ysize)

    def paint(self, painter, options, widget):
        """Draw the item if it is on the surface."""
        if self.onSurface():
            painter.setBrush(QtGui.QColor(241, 231, 65))
            painter.setPen(QtGui.QColor(0, 0, 0))
            painter.drawPath(self.PATH)

    def mousePressEvent(self, event):
        """If left mouse button is pressed down start dragging
        the item. Rotate the item if middle button is pressed.
        """
        if event.button() == QtCore.Qt.LeftButton:
            self.dragged = True
        elif event.button() == QtCore.Qt.MidButton:
            self.setRotation(self.rotation() + 90)

    def mouseReleaseEvent(self, event):
        """End drag when mouse is released."""
        if event.button() == QtCore.Qt.LeftButton:
            self.dragged = False
            self.scene().painting_status = None
            self.scene().views()[0].scroll_dir = None
            self.ensureVisible()
            self.scene().updateSceneRect()

    def mouseMoveEvent(self, event):
        """If circuit is being dragged try to set the item position
        to the mouse position.
        """
        if self.dragged:
            old_pos = self.pos()
            pos = event.scenePos()
            pos.setX(pos.x() - pos.x() % 25)
            pos.setY(pos.y() - pos.y() % 25)
            self.setPos(pos)
            # Relay the movement to all other selected circuits
            if self.isSelected() and self.pos() != old_pos:
                self.setPos(old_pos)
                self.scene().moveSelected(pos - old_pos)
            # Update the connections since some of them might
            # have to be moved with the circuit.
            self.scene().updateMovingSceneRect()
            self.scene().views()[0].autoScroll(event.scenePos())
            self.scene().update()


class SaveContact(object):

    def __init__(self, contact):
        self.x = contact.x()
        self.y = contact.y()
        self.rotation = contact.rotation()

    def load(self, surface):
        contact = Contact(self.x, self.y, surface)
        contact.setRotation(self.rotation)
