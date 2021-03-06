import math

from PyQt4 import QtCore, QtGui
import numpy as np

from atom_pair import AtomPair
import output
import molecular_scene
import settings

class Molecule(QtGui.QGraphicsItem):

    def __init__(self, x, y, variables, parent=None):
        super(Molecule, self).__init__(parent)
        self.variables = variables
        self.setX(x - x % self.variables.snap[0])
        self.setY(y - y % self.variables.snap[1])
        self.xsize = self.variables.size[0]
        self.ysize = self.variables.size[1]
        if self.variables.shape is not None:
            self.shape = settings.getShape(self.variables.shape, self.xsize, self.ysize)
        else:
            self.shape = None
        self.dragged = False
        self.setZValue(3)
        self.translate(*self.variables.scene_translation)
        self.setTransformOriginPoint(*self.variables.rotation_axis)

    def getOutput(self, result, options):
        """Add the output data of the contact in to the results if it is
        on the surface.
        """
        if self.onSurface():
            pos = self.pos() - self.parentItem().corner
            out_pos = np.array((1.0*pos.x()/AtomPair.XSIZE * output.X_SCALE,
                                1.0*pos.y()/AtomPair.YSIZE * output.Y_SCALE, 0))
            scene_translation = self.variables.scene_translation
            translation = (np.array(self.variables.output_translation)
                + np.array((1.0*scene_translation[0]/AtomPair.XSIZE*output.X_SCALE,
                            1.0*scene_translation[1]/AtomPair.YSIZE*output.Y_SCALE, 0)))
            rotation_axis = (-np.array(self.variables.output_translation) +
                np.array((1.0*self.variables.rotation_axis[0]/AtomPair.XSIZE*output.X_SCALE,
                1.0*self.variables.rotation_axis[1]/AtomPair.YSIZE*output.Y_SCALE, 0)))
            rotation_m = output.getCounterClockwiseRotationM(self.rotation())
            try:
                with open("../molecules/" + self.variables.output_file, "r") as f:
                    count = 0
                    f.seek(0)
                    for line in f:
                        count += 1
                        if count > 2:
                            split = line.split()
                            atom_pos = np.array([float(x) for x in split[1:4]])
                            atom_pos -= rotation_axis
                            atom_pos = np.dot(rotation_m, atom_pos)
                            atom_pos += rotation_axis
                            atom_pos += out_pos + translation
                            result.append("%-4s %-10f %-10f %-10f %d" %
                                ((split[0],) + tuple(atom_pos) + ((len(result) + 1),)))
            except IOError as e:
                print "IOError: Structure file '%s' not found for molecule '%s'." % \
                        (self.variables.output_file, self.variables.name)
                raise e

    def getSaveState(self):
        """Return the state of the item without Qt bindings."""
        return SaveMolecule(self)

    def onSurface(self):
        """Check if the item is on the surface."""
        if self.collidesWithItem(self.parentItem(), QtCore.Qt.ContainsItemShape):
            return True
        else:
            return False

    def collidesWithMolecules(self):
        """Check if the contact collides with other contacts."""
        for item in self.collidingItems():
            if isinstance(item, Molecule):
                return True
        return False

    def resolveCollisions(self):
        """Tries to resolve collisions by moving the item."""
        pos = self.pos()
        for i in range(10):
            self.setPos(pos.x(), pos.y() + i*self.variables.snap[1])
            if self.onSurface() and not self.collidesWithMolecules():
                return True
            self.setPos(pos.x(), pos.y() - i*self.variables.snap[1])
            if self.onSurface() and not self.collidesWithMolecules():
                return True
            self.setPos(pos.x() + i*self.variables.snap[0], pos.y())
            if self.onSurface() and not self.collidesWithMolecules():
                return True
            self.setPos(pos.x() - i*self.variables.snap[0], pos.y())
            if self.onSurface() and not self.collidesWithMolecules():
                return True
        self.setPos(pos)
        return False

    def reset(self):
        """Reset the item state to scene defaults."""
        self.scene().removeItem(self)

    def contextRotate(self):
        """Rotate the contact by 90 degrees."""
        self.setRotation(self.rotation() + 90)

    def addContextActions(self, menu):
        """Add item specific context actions to the menu."""
        if self.variables.rotating:
            rotate = QtGui.QAction("Rotate " + self.variables.name, menu)
            QtCore.QObject.connect(rotate, QtCore.SIGNAL("triggered()"), self.contextRotate)
            menu.addAction(rotate)

        remove = QtGui.QAction("Remove " + self.variables.name, menu)
        QtCore.QObject.connect(remove, QtCore.SIGNAL("triggered()"), self.reset)
        menu.addAction(remove)

    def boundingRect(self):
        """Return the bounding rectangle of the item."""
        return QtCore.QRectF(0, 0, self.xsize, self.ysize)

    def shape(self):
        """Return the shape of the item."""
        if self.shape is not None:
            return self.shape
        else:
            return super(Molecule, self).shape()

    def paint(self, painter, options, widget):
        """Draw the item if it is on the surface."""
        if self.scene().draw_mode == molecular_scene.DRAW_SURFACE_ONLY:
            painter.setOpacity(0.5)
        if self.onSurface():
            painter.setBrush(QtGui.QColor(*self.variables.color))
            painter.setPen(QtGui.QColor(0, 0, 0))
            if self.shape is not None:
                painter.drawPath(self.shape)
            else:
                painter.drawRect(self.boundingRect())

    def mousePressEvent(self, event):
        """If left mouse button is pressed down start dragging
        the item. Rotate the item if middle button is pressed.
        """
        if (event.button() == QtCore.Qt.LeftButton and
           event.modifiers() == QtCore.Qt.ShiftModifier and
           self.scene().draw_mode != molecular_scene.DRAW_SURFACE_ONLY):
            self.dragged = True
        elif (event.button() == QtCore.Qt.LeftButton and
              self.scene().draw_mode != molecular_scene.DRAW_SURFACE_ONLY):
            pass
        else:
            super(Molecule, self).mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        """Rotate the item on double click."""
        if (event.button() == QtCore.Qt.LeftButton and self.variables.rotating and
           not self.scene().draw_mode != molecular_scene.DRAW_SURFACE_ONLY):
            self.setRotation(self.rotation() + 90)
            if not self.resolveCollisions():
                status_bar = self.scene().views()[0].window().statusBar()
                status_bar.showMessage("Item couldn't be rotated.", 3000)
                self.setRotation(self.rotation() - 90)

    def mouseReleaseEvent(self, event):
        """End drag when mouse is released."""
        if event.button() == QtCore.Qt.LeftButton:
            self.dragged = False
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
            new_pos.setX(new_pos.x() - new_pos.x() % self.variables.snap[0])
            new_pos.setY(new_pos.y() - new_pos.y() % self.variables.snap[1])
            self.setPos(new_pos)
            if not self.onSurface() or self.collidesWithMolecules():
                self.setPos(new_pos.x(), old_pos.y())
                if not self.onSurface() or self.collidesWithMolecules():
                    self.setPos(old_pos.x(), new_pos.y())
                    if not self.onSurface() or self.collidesWithMolecules():
                        self.setPos(old_pos)
            self.scene().updateMovingSceneRect()
            self.scene().views()[0].autoScroll(event.scenePos())
            self.scene().update()


class SaveMolecule(object):

    def __init__(self, molecule):
        self.x = molecule.x()
        self.y = molecule.y()
        self.variables = molecule.variables
        self.rotation = molecule.rotation()

    def load(self, surface):
        molecule = Molecule(self.x, self.y, self.variables, surface)
        molecule.setRotation(self.rotation)
