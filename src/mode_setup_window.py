"""Module containing all the parts for the ModeSetupWindow."""

from PyQt4 import QtGui, QtCore

from custom_line_edit import CustomLineEdit
import drag_selection_window


class ModeSetupButton(QtGui.QPushButton):
    """Button wrapper for the window. Its purpose is to give a common interface
    for all parameter window widgets."""

    def __init__(self, parent):
        super(ModeSetupButton, self).__init__("Setup Modes")
        self.window = ModeSetupWindow(parent)
        QtCore.QObject.connect(self, QtCore.SIGNAL("clicked()"),
                               self.window.showWindow)

    def getValue(self):
        """Return the save state of the window."""
        return self.window.getSaveState()

    def setValue(self, value):
        """Load the save state of the window."""
        self.window.loadSaveState(value)

    def clearValue(self):
        """Clear the value of the widget."""
        self.window.clearSelections()


class ModeSetupWindow(drag_selection_window.DragSelectionWindow):
    """Window for condiguring the modes for the advanced cantilever circuit."""

    def __init__(self, parent=None):
        super(ModeSetupWindow, self).__init__(parent)

    def initUI(self):
        self.setWindowTitle("Setup Modes")
        self.resize(600, 400)
        grid = QtGui.QGridLayout()
        self.selection_tree = ModeSetupTree()
        self.selection_tree.setHeaderLabel("Current Modes")

        done_button = QtGui.QPushButton("Done")
        QtCore.QObject.connect(done_button, QtCore.SIGNAL("clicked()"),
                               self.hide)

        grid.addWidget(self.selection_tree, 0, 0)
        grid.addWidget(done_button, 1, 0)
        self.setLayout(grid)

    def updateNames(self):
        n_vertical = self.parent().getValue("NumberOfModesV")
        if n_vertical == "":
            n_vertical = self.parent().circuit.parameters["NumberOfModesV"]
        n_lateral = self.parent().getValue("NumberOfModesL")
        if n_lateral == "":
            n_lateral = self.parent().circuit.parameters["NumberOfModesL"]
        modes_vertical = self.selection_tree.nAddedModes(True)
        modes_lateral = self.selection_tree.nAddedModes(False)
        self.selection_tree.changeNofModes(True, int(n_vertical)-modes_vertical)
        self.selection_tree.changeNofModes(False, int(n_lateral)-modes_lateral)

    def dragEnterEvent(self, event):
        """Ignore the event to disallow deletion."""
        event.ignore()


class ModeSetupTree(drag_selection_window.SelectionTree):
    """Selection tree containing all the current modes."""

    def __init__(self):
        super(ModeSetupTree, self).__init__()

    def createNewItem(self, vertical):
        """Create a new empty tree item."""
        new_item = QtGui.QTreeWidgetItem()
        item_widget = ModeSetupTreeItem(self.window().parent().circuit, vertical)
        # Set the tree item size hint to match the widget size hint.
        size_hint = item_widget.sizeHint()
        new_item.setSizeHint(0, size_hint)
        return new_item, item_widget

    def createLoadedItem(self, save_state):
        """Create a new item matching the save state."""
        machine = self.window().parent().circuit.scene()
        new_item = QtGui.QTreeWidgetItem()
        circuit = machine.findMatchingCircuit(save_state.circuit)
        # No match is found so remove the item
        if circuit is None:
            return None, None
        item_widget = ModeSetupTreeItem(circuit, save_state.vertical)
        size_hint = item_widget.sizeHint()
        new_item.setSizeHint(0, size_hint)
        item_widget.setText(save_state.edit_text)
        return new_item, item_widget

    def addVerticalMode(self):
        """Add a vertical mode to the tree."""
        new_item, widget = self.createNewItem(True)
        # widget.setText("Vertical=True, k= , Q= , M= , f0= ")
        self.addTopLevelItem(new_item)
        self.setItemWidget(new_item, 0, widget)
        self.setCurrentItem(new_item)

    def addMode(self, vertical):
        """Add a lateral mode to the tree."""
        new_item, widget = self.createNewItem(vertical)
        # widget.setText("Vertical=False, k= , Q= , M= , f0= ")
        self.addTopLevelItem(new_item)
        self.setItemWidget(new_item, 0, widget)
        self.setCurrentItem(new_item)

    def removeMode(self, vertical):
        """Remove the bottom most mode with matching vertical."""
        item_count = self.topLevelItemCount()
        for i in range(item_count):
            index = item_count-1 - i
            top_item = self.topLevelItem(index)
            item_widget = self.itemWidget(top_item, 0)
            if item_widget.vertical == vertical:
                self.takeTopLevelItem(index)
                return

    def getSaveState(self):
        """Return the save state of the tree."""
        save_state = ModeSetupSaveList()
        for i in range(self.topLevelItemCount()):
            top_item = self.topLevelItem(i)
            item_widget = self.itemWidget(top_item, 0)
            save_item = ModeSetupSaveItem(item_widget)
            save_state.append(save_item)
        return save_state

    def nAddedModes(self, vertical):
        """Return the number of modes matching vertical state."""
        number = 0
        for i in range(self.topLevelItemCount()):
            top_item = self.topLevelItem(i)
            item_widget = self.itemWidget(top_item, 0)
            if item_widget.vertical == vertical:
                number += 1
        return number

    def changeNofModes(self, vertical, amount):
        """Change the number of modes matching vertical by amount."""
        if amount < 0:
            for i in range(abs(amount)):
                self.removeMode(vertical)
        else:
            for i in range(amount):
                self.addMode(vertical)

    def keyPressEvent(self, event):
        """Overwrite the event to not delete items."""
        if event.key() == QtCore.Qt.Key_Delete:
            pass
        else:
            super(ModeSetupTree, self).keyPressEvent(event)


class ModeSetupTreeItem(QtGui.QWidget):
    """Widget used in the ModeSetupTree."""

    def __init__(self, circuit, vertical):
        super(ModeSetupTreeItem, self).__init__()
        self.circuit = circuit
        self.vertical = vertical
        main_layout = QtGui.QHBoxLayout()
        self.label = QtGui.QLabel("AddMode(Vertical=%s," % vertical)
        self.line_edit = CustomLineEdit("ModeSetupLineEdit")
        close = QtGui.QLabel(')')

        main_layout.addWidget(self.label)
        main_layout.addWidget(self.line_edit)
        main_layout.addWidget(close)
        self.setLayout(main_layout)

    def getEdit(self):
        """Get the value of the text edit."""
        return self.line_edit.text()

    def setText(self, text):
        """Set the value of the text edit."""
        self.line_edit.setText(text)

    def getText(self):
        """Return the whole text of the widget."""
        return self.label.text() + ' ' + self.line_edit.text() + ')'

    def copy(self):
        """Return a copy of the widget. Needed when moving widgets around."""
        new_item = ModeSetupTreeItem(self.circuit, self.vertical)
        new_item.label.setText(self.label.text())
        new_item.line_edit.setText(self.line_edit.text())
        return new_item


class ModeSetupSaveItem(object):
    """Container for ModeSetupTreeItem state without Qt bindings.
    Used for saving.
    """

    def __init__(self, tree_item):
        self.circuit = tree_item.circuit.getSaveState()
        self.edit_text = tree_item.getEdit()
        self.vertical = tree_item.vertical

    def update(self, tree_item):
        """Update the save state to match the current state."""
        self.__init__(tree_item)

    def __str__(self):
        return "%s.AddMode(Vertical=%s, %s)" % (self.circuit.name, self.vertical,
                                                self.edit_text)


class ModeSetupSaveList(list):
    """List for saving all the individual save items."""

    def __init__(self):
        super(ModeSetupSaveList, self).__init__()

    def __str__(self):
        i = 0
        string = ""
        for item in self:
            if i != 0:
                string += "\n"
            string += str(item)
            i += 1
        return str(string)
