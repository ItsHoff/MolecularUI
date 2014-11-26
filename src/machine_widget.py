'''
Created on Jun 6, 2014

@author: keisano1
'''

from PyQt4 import QtGui, QtCore

from ui_circuit import UICircuit
from ui_IO import UIIO
from ui_connection import UIConnection
from selection_box import SelectionBox
import circuits


class MachineWidget(QtGui.QGraphicsScene):
    """Scene displaying the current state of the machine."""

    def __init__(self, tree_widget, parent=None):
        super(MachineWidget, self).__init__(parent)
        self.tree_widget = tree_widget
        self.circuits = []
        self.connections = []
        self.new_connection = None
        self.selection_box = None
        self.saved_selections = [None]*10
        self.initWidget()

    def initWidget(self):
        """Initialise the UI of the widget."""
        self.addCircuits()
        self.updateSceneRect()
        self.update()

    def getNewSceneRect(self):
        """Return a new scene rectangle based on the bounding rectangle
        of all scene items.
        """
        rect = self.itemsBoundingRect()
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

    def addCircuits(self):
        """Add some circuits to the scene on startup."""
        pass

    def addCircuit(self, name, x, y):
        """Add a circuit with corresponding name to the scene
        and update the scene.
        """
        circuit = UICircuit(x-x%100, y-y%100, circuits.circuits[name])
        circuit.addIO()
        self.circuits.append(circuit)
        self.addItem(circuit)
        self.resolveNameConflicts(circuit)
        self.updateSceneRect()
        self.update()

    def addDroppedCircuit(self, dropped, pos):
        """Add the dropped circuit to the scene after a dropEvent."""
        name = str(dropped.text(0))
        self.addCircuit(name, pos.x(), pos.y())

    def addClickedCircuit(self, pos):
        """Add circuit selected from the main_window tree_widget
        to the scene. If nothing is selected do nothing.
        """
        item = self.tree_widget.currentItem()
        if item is None:
            return
        name = str(item.text(0))
        if item.parent():
            self.addToRecentlyUsed(item)
            self.addCircuit(name, pos.x(), pos.y())

    def addLoadedCircuit(self, save_state):
        """Add circuit loaded from save_state into the scene."""
        circuit = UICircuit(0, 0, save_state.circuit_info)
        self.circuits.append(circuit)
        self.addItem(circuit)
        circuit.loadSaveState(save_state)
        circuit.setSelected(True)
        self.resolveNameConflicts(circuit)

    def resolveNameConflicts(self, check_circuit):
        """Make sure that the name of the circuit doesn't conflict
        with any other circuit."""
        conflict_found = True
        name = check_circuit.name
        number = 0
        while conflict_found:
            if number != 0:
                name = check_circuit.name + str(number)
            conflict_found = False
            for circuit in self.circuits:
                if circuit.name == name and circuit is not check_circuit:
                    conflict_found = True
                    number += 1
                    continue
        check_circuit.setName(name)

    def createNewConnection(self, origin, mouse_pos):
        """Try to create a new connection starting from mouse_pos.
        Throw a ValueError if input under mouse is allready connected.
        Should be called by the input or output at the start of the
        connection.
        """
        status_bar = self.parent().window().statusBar()
        try:
            self.new_connection = UIConnection(origin, mouse_pos)
        except ValueError as e:
            status_bar.showMessage(e.message, 3000)
            return
        self.views()[0].setMouseTracking(True)
        self.addItem(self.new_connection)

    def addConnection(self):
        """Add a new valid connection. Should be called
        by the input or output at the end of connection.
        """
        status_bar = self.parent().window().statusBar()
        input_ = self.new_connection.input_
        output = self.new_connection.output
        message = "Connected %s.%s and %s.%s" % (output.circuit.name,
                  output.name, input_.circuit.name, input_.name)
        self.connections.append(self.new_connection)
        self.new_connection = None
        self.views()[0].setMouseTracking(False)
        status_bar.showMessage(message, 4000)

    def addLoadedConnection(self, save_state):
        """Add connection loaded from save_state into the scene."""
        output = save_state.output
        connection = UIConnection(output.loaded_item, output.loaded_item.pos())
        connection.loadSaveState(save_state)
        self.connections.append(connection)
        self.addItem(connection)

    def deleteNewConnection(self):
        """Delete unconnected new_connextion."""
        if self.new_connection is not None:
            status_bar = self.parent().window().statusBar()
            self.removeItem(self.new_connection)
            self.new_connection = None
            self.views()[0].setMouseTracking(False)
            status_bar.showMessage("Destroyed connection", 2000)

    def updateConnections(self):
        """Update paths for all required connections.
        Needed after some move events."""
        for connection in self.connections:
            connection.updatePath()

    def hasIOatPos(self, pos):
        """Check if there's input or output at position pos
        and return True if there is and False otherwise.
        """
        items = self.items(pos)
        for item in items:
            if isinstance(item, UIIO):
                return True
        return False

    def findMatchingCircuit(self, save_state):
        """Return the circuit with the matching save_state."""
        for circuit in self.circuits:
            if circuit.save_state == save_state:
                return circuit

    def addContextActions(self, menu):
        """Add widget specific context actions to the
        context menu given as parameter.
        """
        clear_all = QtGui.QAction("Delete All", menu)
        self.connect(clear_all, QtCore.SIGNAL("triggered()"), self.deleteAll)

        clear_connections = QtGui.QAction("Delete All Connections", menu)
        self.connect(clear_connections, QtCore.SIGNAL("triggered()"),
                     self.removeConnections)

        save_selected = QtGui.QAction("Save Selected", menu)
        self.connect(save_selected, QtCore.SIGNAL("triggered()"),
                     self.views()[0].window().saveSelected)

        delete_selected = QtGui.QAction("Delete Selected", menu)
        self.connect(delete_selected, QtCore.SIGNAL("triggered()"),
                     self.deleteSelected)

        if self.selectedItems():
            menu.addAction(save_selected)
            menu.addAction(delete_selected)
        menu.addAction(clear_connections)
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

    def deleteAll(self):
        """Clear everything from the scene after confirmation."""
        value = self.showMessageBox("Delete All",
                                    "Do you want to delete everything?")
        if value == QtGui.QMessageBox.Yes:
            self.clearAll()

    def clearAll(self):
        """Clear everything from the scene."""
        status_bar = self.parent().window().statusBar()
        for circuit in self.circuits[:]:
            self.removeCircuit(circuit)
            # self.updateSceneRect()
            status_bar.showMessage("Cleared all", 3000)
        self.update()

    def removeConnections(self):
        """Clear all connections from the scene."""
        value = self.showMessageBox("Delete All Connections",
                                    "Do you want to delete all connections?")
        if value == QtGui.QMessageBox.Yes:
            status_bar = self.parent().window().statusBar()
            for connection in self.connections:
                self.removeItem(connection)
            self.connections = []
            status_bar.showMessage("Removed all connections", 3000)
            self.update()

    def removeConnectionsFrom(self, IO):
        """Remove all connections from input or output
        given as parameter.
        """
        status_bar = self.parent().window().statusBar()
        for connection in self.connections[:]:
            if connection.input_ == IO or connection.output == IO:
                self.connections.remove(connection)
                self.removeItem(connection)
        status_bar.showMessage("Removed all connections from %s.%s"%
                (IO.circuit.name, IO.name), 3000)
        self.update()

    def removeConnection(self, connection):
        """Remove the specified connection from the scene."""
        status_bar = self.parent().window().statusBar()
        input_ = connection.input_
        output = connection.output
        message = "Removed connection from %s.%s to %s.%s" % (input_.circuit.name,
                input_.name, output.circuit.name, output.name)
        self.connections.remove(connection)
        self.removeItem(connection)
        status_bar.showMessage(message, 3000)

    def removeCircuit(self, circuit):
        """Remove the specified circuit from the scene.
        Also remove all the circuits inputs, outputs and connections
        from the scene.
        """
        status_bar = self.parent().window().statusBar()
        for io in circuit.ios:
            self.removeConnectionsFrom(io)
        self.circuits.remove(circuit)
        self.removeItem(circuit)
        status_bar.showMessage("Removed %s"%circuit.name, 3000)
        self.updateSceneRect()
        self.update()

    def selectedConnections(self):
        """Return list of connections whose both ends are selected."""
        selected_items = self.selectedItems()
        selected_connections = []
        for connection in self.connections:
            if (connection.input_.circuit in selected_items and
                    connection.output.circuit in selected_items):
                selected_connections.append(connection)
        return selected_connections

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
        for x in range(int(tl.x() - tl.x() % 100),
                       int(br.x()), 100):
            for y in range(int(tl.y() - tl.y() % 100),
                           int(br.y()), 100):
                qp.drawLine(int(tl.x()), int(y), int(br.x()), int(y))
                qp.drawLine(int(x), int(tl.y()), int(x), int(br.y()))
        # Draw thicklines to the middle of the scene
        qp.setPen(solid_pen)
        qp.drawLine(0, int(tl.y()),
                    0, int(br.y()))
        qp.drawLine(int(tl.x()), 0,
                    int(br.x()), 0)

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
            self.addDroppedCircuit(dropped_item, event.scenePos())
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
              self.itemAt(event.scenePos()) is None  and
              not event.modifiers() & QtCore.Qt.ControlModifier):
            self.clearSelection()
            self.selection_box = SelectionBox(event.scenePos(), None, self)
            self.update()
        # If user was trying to create a new connection
        # and clicked something other than input or output
        # destroy the connection. Also non left clicks
        # destroy the connection.
        elif (self.new_connection is not None and
             (not self.hasIOatPos(event.scenePos()) or
              event.button() != QtCore.Qt.LeftButton)):
            self.deleteNewConnection()
        elif self.itemAt(event.scenePos()) is not None:
            super(MachineWidget, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """If user is trying to create a connection update connections
        end point when mouse is moved. With rubberband selection
        update the selection.
        """
        super(MachineWidget, self).mouseMoveEvent(event)
        if self.new_connection is not None:
            self.new_connection.updateMousePos(event.scenePos())
            self.update()
        elif self.selection_box is not None:
            self.views()[0].autoScroll(event.scenePos())
            self.selection_box.setCorner(event.scenePos())
            selection_area = self.selection_box.selectionArea()
            area = QtGui.QPainterPath()
            area.addPolygon(selection_area)
            self.setSelectionArea(area)
            self.update()

    def mouseReleaseEvent(self, event):
        """Remove the selection box and save the most recent valid
        selection on 0.
        """
        super(MachineWidget, self).mouseReleaseEvent(event)
        self.views()[0].scroll_dir = None
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
