from PyQt4 import QtGui, QtCore
import numpy as np

from surface import Surface
from hydrogen import Hydrogen

TOPB = 1
TOPRB = 2
RIGHTB = 3
BOTTOMRB = 4
BOTTOMB = 5
BOTTOMLB = 6
LEFTB = 7
TOPLB = 8


class MolecularScene(QtGui.QGraphicsScene):
    """Scene displaying the current state of the circuit."""

    def __init__(self, tree_widget, parent=None):
        super(MolecularScene, self).__init__(parent)
        self.tree_widget = tree_widget
        self.surface = Surface(self)
        self.molecules = []
        self.selection_box = None
        self.drag_border = None
        self.painting_status = None
        self.saved_selections = [None]*10
        self.updateSceneRect()
        self.update()

    def getNewSceneRect(self):
        """Return a new scene rectangle based on the bounding rectangle
        of the surface.
        """
        rect = self.surface.sceneBoundingRect()
        center = rect.center()
        rect.setHeight(rect.height() + 500)
        rect.setWidth(rect.width() + 500)
        rect.moveCenter(center)
        return rect

    def updateSceneRect(self):
        """Update the scene rect to the one given by getNewSceneRect."""
        rect = self.getNewSceneRect()
        self.setSceneRect(rect)

    def updateMovingSceneRect(self):
        """Update the scene rectangle but don't make it smaller. Used when
        moving items around the scene to avoid movement blow ups.
        """
        old_rect = self.sceneRect()
        new_rect = self.getNewSceneRect()
        new_rect = new_rect.united(old_rect)
        self.setSceneRect(new_rect)

    def getOutput(self):
        """Get the output information from the scene."""
        return self.surface.getOutput()

    def addContextActions(self, menu):
        """Add widget specific context actions to the
        context menu given as parameter.
        """
        reset = QtGui.QAction("Reset", menu)
        self.connect(reset, QtCore.SIGNAL("triggered()"), self.reset)
        menu.addAction(reset)

    def showMessageBox(self, title, text):
        """Show a message box with given title and text.
        Forward the return value of the dialog.
        """
        message_box = QtGui.QMessageBox()
        message_box.setWindowTitle(title)
        message_box.setText(text)
        message_box.setStandardButtons(message_box.Yes | message_box.No)
        message_box.setDefaultButton(message_box.Yes)
        return message_box.exec_()

    def reset(self):
        """Ask user for confirmation and reset the scene if accepted."""
        value = self.showMessageBox("Reset",
                                    "Do you want to reset?")
        if value == QtGui.QMessageBox.Yes:
            status_bar = self.parent().window().statusBar()
            for item in self.items():
                item.reset()
            status_bar.showMessage("Reset", 3000)
            self.update()

    def drawBackground(self, qp, rect):
        """Draw the background white and call a grid draw"""
        qp.setPen(QtGui.QColor(255, 255, 255))
        qp.setBrush(QtGui.QColor(255, 255, 255))
        qp.drawRect(rect)
        self.drawGrid(qp, rect)

    def drawGrid(self, qp, rect):
        """Draw a grid with a spacing of 100 to the background."""
        tl = rect.topLeft()
        br = rect.bottomRight()
        solid_pen = QtGui.QPen(QtGui.QColor(0, 0, 0), 4, QtCore.Qt.SolidLine)
        faint_pen = QtGui.QPen(QtGui.QColor(150, 150, 150), 1, QtCore.Qt.SolidLine)
        qp.setPen(faint_pen)
        for x in range(int(tl.x() - tl.x() % 100), int(br.x()), 100):
            for y in range(int(tl.y() - tl.y() % 100), int(br.y()), 100):
                qp.drawLine(int(tl.x()), int(y), int(br.x()), int(y))
                qp.drawLine(int(x), int(tl.y()), int(x), int(br.y()))
        # Draw thicklines to the middle of the scene
        qp.setPen(solid_pen)
        qp.drawLine(0, int(tl.y()), 0, int(br.y()))
        qp.drawLine(int(tl.x()), 0, int(br.x()), 0)

    def dragEnterEvent(self, event):
        """Accept event for drag & drop to work."""
        event.accept()

    def dragMoveEvent(self, event):
        """Accept event for drag & drop to work."""
        event.accept()

    def dragLeaveEvent(self, event):
        """Accept event for drag & drop to work."""
        event.accept()

    def dropEvent(self, event):
        """Accept event and try to add the dropped item to the scene."""
        if event.source() is self.tree_widget:
            event.accept()
            dropped_item = event.source().currentItem()
            self.surface.addDroppedItem(event.scenePos())
            self.addToRecentlyUsed(dropped_item)

    def addToRecentlyUsed(self, tree_item):
        """Add tree_item to the recently used tab if it's not allready
        added.
        """
        recently = self.tree_widget.findItems("Recently Used",
                                              QtCore.Qt.MatchExactly)[0]
        for i in range(recently.childCount()):
            if recently.child(i).text(0) == tree_item.text(0):
                return
        clone = tree_item.clone()
        recently.addChild(clone)

    def mousePressEvent(self, event):
        """Handle all the possible mouse presses for the scene and pass
        the event forward if its not handled by the scene.
        """
        if (event.modifiers() & QtCore.Qt.ShiftModifier and
                event.button() == QtCore.Qt.LeftButton):
            event.accept()
            self.addClickedCircuit(event.scenePos())
        elif (event.button() == QtCore.Qt.LeftButton and
              not self.surface.contains(event.scenePos()) and
              not event.modifiers() & QtCore.Qt.ControlModifier):
            self.drag_border = self.checkBorder(event.scenePos())
        else:
            super(MolecularScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handle all the mouse movement for the scene and pass the event
        forward if its not handled by the scene.
        """
        super(MolecularScene, self).mouseMoveEvent(event)
        if self.selection_box is not None:
            self.views()[0].autoScroll(event.scenePos())
            self.selection_box.setCorner(event.scenePos())
            selection_area = self.selection_box.selectionArea()
            area = QtGui.QPainterPath()
            area.addPolygon(selection_area)
            self.setSelectionArea(area)
            self.update()
        elif self.drag_border is not None:
            self.views()[0].autoScroll(event.scenePos())
            self.surface.resize(event.scenePos(), self.drag_border)
            self.updateMovingSceneRect()
            self.update()
        else:
            border = self.checkBorder(event.scenePos())
            self.setCursor(border)

    def setCursor(self, border=None):
        """Set the cursor to the right style depending on the border."""
        if border is None:
            border = self.drag_border
        if border == LEFTB or border == RIGHTB:
            self.views()[0].setCursor(QtCore.Qt.SizeHorCursor)
        elif border == TOPB or border == BOTTOMB:
            self.views()[0].setCursor(QtCore.Qt.SizeVerCursor)
        elif border == BOTTOMLB or border == TOPRB:
            self.views()[0].setCursor(QtCore.Qt.SizeBDiagCursor)
        elif border == TOPLB or border == BOTTOMRB:
            self.views()[0].setCursor(QtCore.Qt.SizeFDiagCursor)
        else:
            self.views()[0].setCursor(QtCore.Qt.ArrowCursor)

    def checkBorder(self, pos):
        """Check if cursor is close to one of the surface edges."""
        distance = 20
        surface_rect = self.surface.sceneBoundingRect()
        top = surface_rect.top()
        bottom = surface_rect.bottom()
        left = surface_rect.left()
        right = surface_rect.right()
        if not surface_rect.contains(pos):
            if abs(left - pos.x()) < distance and top < pos.y() < bottom:
                return LEFTB
            elif abs(right - pos.x()) < distance and top < pos.y() < bottom:
                return RIGHTB
            elif abs(top - pos.y()) < distance and left < pos.x() < right:
                return TOPB
            elif abs(bottom - pos.y()) < distance and left < pos.x() < right:
                return BOTTOMB
            elif (surface_rect.topLeft()- pos).manhattanLength() < distance:
                return TOPLB
            elif (surface_rect.topRight()- pos).manhattanLength() < distance:
                return TOPRB
            elif (surface_rect.bottomLeft()- pos).manhattanLength() < distance:
                return BOTTOMLB
            elif (surface_rect.bottomRight()- pos).manhattanLength() < distance:
                return BOTTOMRB
        return None

    def mouseReleaseEvent(self, event):
        """Reset all the flags possibly set by mouse press events."""
        super(MolecularScene, self).mouseReleaseEvent(event)
        self.views()[0].scroll_dir = None
        self.drag_border = None
        self.updateSceneRect()

    def contextMenuEvent(self, event):
        """Create a new context menu and open it under mouse"""
        self.views()[0].scroll_dir = None
        menu = QtGui.QMenu()
        # Insert actions to the menu from all the items under the mouse
        for item in self.items(event.scenePos()):
            item.addContextActions(menu)
        self.addContextActions(menu)
        # Show the menu under mouse
        menu.exec_(event.screenPos())