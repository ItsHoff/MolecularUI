'''
Created on Jun 6, 2014

@author: keisano1
'''

from PyQt4 import QtGui, QtCore
import numpy as np

from surface import Surface
from hydrogen import Hydrogen
from contact import Contact
# from selection_box import SelectionBox
import output

TOPB = 1
TOPRB = 2
RIGHTB = 3
BOTTOMRB = 4
BOTTOMB = 5
BOTTOMLB = 6
LEFTB = 7
TOPLB = 8


class MachineWidget(QtGui.QGraphicsScene):
    """Scene displaying the current state of the machine."""

    def __init__(self, tree_widget, parent=None):
        super(MachineWidget, self).__init__(parent)
        self.tree_widget = tree_widget
        self.surface = Surface(self)
        self.molecules = []
        self.selection_box = None
        self.drag_border = None
        self.painting_status = None
        self.saved_selections = [None]*10
        self.initWidget()

    def initWidget(self):
        """Initialise the UI of the widget."""
        self.updateSceneRect()
        self.update()

    def getNewSceneRect(self):
        """Return a new scene rectangle based on the bounding rectangle
        of all scene items.
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
        """Update the scene rectangle but don't make it smaller. Used while
        moving circuits to avoid unwanted movement.
        """
        old_rect = self.sceneRect()
        new_rect = self.getNewSceneRect()
        new_rect = new_rect.united(old_rect)
        self.setSceneRect(new_rect)

    def addCircuit(self, x, y):
        """Add a circuit with corresponding name to the scene
        and update the scene.
        """
        if not isinstance(self.itemAt(x, y), Hydrogen):
            circuit = Hydrogen(x-x%Hydrogen.XSIZE, y-y%Hydrogen.YSIZE)
            self.circuits.append(circuit)
            self.addItem(circuit)
            # self.updateSceneRect()
            # self.update()

    def addContact(self, x, y):
        contact = Contact(x, y)
        self.addItem(contact)

    def addDroppedCircuit(self, pos):
        """Add the dropped circuit to the scene after a dropEvent."""
        self.addContact(pos.x(), pos.y())

    def addClickedCircuit(self, pos):
        """Add circuit selected from the main_window tree_widget
        to the scene. If nothing is selected do nothing.
        """
        item = self.tree_widget.currentItem()
        if item is None:
            return
        if item.parent():
            self.addToRecentlyUsed(item)
            self.addCircuit(pos.x(), pos.y())

    def addLoadedCircuit(self, save_state):
        """Add circuit loaded from save_state into the scene."""
        circuit = UICircuit(0, 0)
        self.circuits.append(circuit)
        self.addItem(circuit)
        circuit.loadSaveState(save_state)
        circuit.setSelected(True)

    def findMatchingCircuit(self, save_state):
        """Return the circuit with the matching save_state."""
        for circuit in self.circuits:
            if circuit.save_state == save_state:
                return circuit

    def getOutput(self):
        result = []
        base_translation = output.LEFT_H_POS * output.TOTAL_SCALE
        with open("../molecules/base.xyz", "r") as f:
            for i in range(int(self.surface.width()/Hydrogen.XSIZE)):
                x_offset = i*output.X_SCALE
                for j in range(int(self.surface.height()/Hydrogen.YSIZE)):
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
        for item in self.items():
            item.getOutput(result)
        return result

    def addContextActions(self, menu):
        """Add widget specific context actions to the
        context menu given as parameter.
        """
        clear_all = QtGui.QAction("Reset", menu)
        self.connect(clear_all, QtCore.SIGNAL("triggered()"), self.reset)

        save_selected = QtGui.QAction("Save Selected", menu)
        self.connect(save_selected, QtCore.SIGNAL("triggered()"),
                     self.views()[0].window().saveSelected)

        delete_selected = QtGui.QAction("Delete Selected", menu)
        self.connect(delete_selected, QtCore.SIGNAL("triggered()"),
                     self.deleteSelected)

        if self.selectedItems():
            menu.addAction(save_selected)
            menu.addAction(delete_selected)
        menu.addAction(clear_all)

    def showMessageBox(self, title, text):
        """Show a message box with a title and text. Return the value of
        the dialog.
        """
        message_box = QtGui.QMessageBox()
        message_box.setWindowTitle(title)
        message_box.setText(text)
        message_box.setStandardButtons(message_box.Yes | message_box.No)
        message_box.setDefaultButton(message_box.Yes)
        return message_box.exec_()

    def reset(self):
        """Clear everything from the scene after confirmation."""
        value = self.showMessageBox("Reset",
                                    "Do you want to reset?")
        if value == QtGui.QMessageBox.Yes:
            self.clearAll()

    def clearAll(self):
        """Clear everything from the scene."""
        status_bar = self.parent().window().statusBar()
        for circuit in self.circuits[:]:
            circuit.left_status = Hydrogen.NORMAL
            circuit.right_status = Hydrogen.NORMAL
            status_bar.showMessage("Reset", 3000)
        self.update()

    def removeCircuit(self, circuit):
        """Remove the specified circuit from the scene.
        Also remove all the circuits inputs, outputs and connections
        from the scene.
        """
        status_bar = self.parent().window().statusBar()
        self.circuits.remove(circuit)
        self.removeItem(circuit)
        # status_bar.showMessage("Removed circuit", 3000)
        # self.updateSceneRect()
        # self.update()

    def moveSelected(self, amount):
        """Move all the selected items by amount."""
        selected = self.selectedItems()
        for circuit in selected:
            circuit.moveBy(amount)

    def deleteSelected(self):
        """Delete all currently selected circuits."""
        value = self.showMessageBox("Delete Selected",
                                    "Do you want to delete selected circuits?")
        if value == QtGui.QMessageBox.Yes:
            for circuit in self.selectedItems():
                self.removeCircuit(circuit)

    def saveSelection(self, key):
        """Save current selection under key."""
        self.saved_selections[key] = self.selectedItems()

    def appendSelection(self, key):
        """Add current selection to the selection under key."""
        if self.saved_selections[key] is not None:
            self.saved_selections[key].append(self.selectedItems())
        else:
            self.saveSelection(key)

    def highlightOutputs(self):
        """Highlight the outputs of the scene and try to make them all
        visible.
        """
        output_rect = QtCore.QRectF()
        for circuit in self.circuits:
            if circuit.circuit_info.circuit_type == "output":
                rect = circuit.boundingRect()
                rect.moveTo(circuit.pos())
                output_rect = output_rect.united(rect)
                circuit.highlighted = True
        self.views()[0].ensureVisible(output_rect)

    def clearHighlight(self):
        """Clear highlight from all circuits."""
        for circuit in self.circuits:
            circuit.highlighted = False

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
        """Accept event and add the dropped circuit
        to the scene.
        """
        if event.source() is self.tree_widget:
            event.accept()
            dropped_item = event.source().currentItem()
            self.addDroppedCircuit(event.scenePos())
            self.addToRecentlyUsed(dropped_item)

    def addToRecentlyUsed(self, tree_item):
        """Add tree item under the recently used tab if it's not allready
        there.
        """
        recently = self.tree_widget.findItems("Recently Used",
                                              QtCore.Qt.MatchExactly)[0]
        for i in range(recently.childCount()):
            if recently.child(i).text(0) == tree_item.text(0):
                return
        clone = tree_item.clone()
        recently.addChild(clone)

    def mousePressEvent(self, event):
        """If user is holding down shift try to add circuit to the scene.
        Regular left clicks will start a rubberband selection.
        Otherwise call the super function to send signal forward.
        """
        if (event.modifiers() & QtCore.Qt.ShiftModifier and
                event.button() == QtCore.Qt.LeftButton):
            event.accept()
            self.addClickedCircuit(event.scenePos())
        elif (event.button() == QtCore.Qt.LeftButton and
              not self.surface.contains(event.scenePos()) and
              not event.modifiers() & QtCore.Qt.ControlModifier):
            self.drag_border = self.checkBorder(event.scenePos())
            # self.clearSelection()
            # self.selection_box = SelectionBox(event.scenePos(), None, self)
            # self.update()
        elif self.itemAt(event.scenePos()) is not None:
            super(MachineWidget, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """If user is trying to create a connection update connections
        end point when mouse is moved. With rubberband selection
        update the selection.
        """
        super(MachineWidget, self).mouseMoveEvent(event)
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
        """Set the cursor to the right style defined by border."""
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
        """Check if cursor is close to the surface edge."""
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
        """Remove the selection box and save the most recent valid
        selection on 0.
        """
        super(MachineWidget, self).mouseReleaseEvent(event)
        self.views()[0].scroll_dir = None
        self.drag_border = None
        self.updateSceneRect()
        if self.selection_box is not None:
            if self.selection_box.boundingRect().isValid():
                self.saveSelection(0)
            self.removeItem(self.selection_box)
            self.selection_box = None
            self.update()

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

    def keyPressEvent(self, event):
        """Save the current selection with control + number and load the
        selection with the corresponding number.
        """
        zero = QtCore.Qt.Key_0
        key = event.key()
        if key >= zero and key <= zero + 9:
            if event.modifiers() & QtCore.Qt.ControlModifier:
                self.saveSelection(key-zero)
            else:
                self.clearSelection()
                if self.saved_selections[key-zero] is not None:
                    bounding_rect = QtCore.QRectF()
                    for item in self.saved_selections[key-zero]:
                        rect = item.boundingRect()
                        rect.moveTo(item.pos())
                        bounding_rect = bounding_rect.united(rect)
                        item.setSelected(True)
                    self.views()[0].ensureVisible(bounding_rect, 0, 0)
