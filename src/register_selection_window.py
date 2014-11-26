"""
Contains all the classes for the register selection window.
Classes:
    - RegisterSelectionWindow
    - RegisterSelectionTree
    - RegisterSelectionTreeItem
    - GlobalDummy
"""

import sys

from PyQt4 import QtGui, QtCore

import drag_selection_window
import circuits


class RegisterSelectionButton(QtGui.QPushButton):
    """Button wrapper for the window. Its purpose is to give a common interface
    for all parameter window widgets."""

    def __init__(self, central_widget, parent):
        super(RegisterSelectionButton, self).__init__("Select Channels")
        self.window = RegisterSelectionWindow(central_widget, parent)
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


class RegisterSelectionWindow(drag_selection_window.DragSelectionWindow):
    """Subclass of DragSelectionWindow for selecting channels to
    register for the output.
    """

    def __init__(self, main_widget, parent=None):
        self.main_widget = main_widget
        super(RegisterSelectionWindow, self).__init__(parent)
        self.setWindowTitle("Select channels to register")
        self.selection_tree = RegisterSelectionTree()
        self.selection_tree.setHeaderLabel("Selected channels")
        self.layout().addWidget(self.selection_tree, 0, 1)

    def loadOptions(self):
        """Load the global channels that can be registered and all the
        outputs of the circuits to the option tree.
        """
        global_item = QtGui.QTreeWidgetItem(self.option_tree)
        global_item.setText(0, "global")
        global_item.setData(0, QtCore.Qt.UserRole, GlobalDummy())
        global_item.setFlags(global_item.flags() &
                             ~QtCore.Qt.ItemIsDragEnabled)
        for channel in circuits.global_channels:
            sub_item = QtGui.QTreeWidgetItem(global_item)
            sub_item.setText(0, channel)
        for circuit in self.main_widget.machine_widget.circuits:
            if circuit.ios:
                new_item = QtGui.QTreeWidgetItem(self.option_tree)
                new_item.setText(0, circuit.name)
                new_item.setData(0, QtCore.Qt.UserRole, circuit)
                new_item.setFlags(new_item.flags() &
                                  ~QtCore.Qt.ItemIsDragEnabled)
                for io in circuit.ios:
                    if io.io_type == "out":
                        sub_item = QtGui.QTreeWidgetItem(new_item)
                        sub_item.setText(0, io.name)

    def loadSelections(self):
        """Currently not required since window should never have to be
        deleted and loaded again.
        """
        pass

    def updateNames(self):
        """Update the circuit names that might have changed since the
        window was last opened and remove selections from removed circuits.
        """
        self.option_tree.clear()
        self.loadOptions()
        top_items = []
        for i in range(self.selection_tree.topLevelItemCount()):
            top_items.append(self.selection_tree.topLevelItem(i))
        for top_item in top_items:
            if top_item.io is None or top_item.io.scene() is None:
                i = self.selection_tree.indexOfTopLevelItem(top_item)
                self.selection_tree.takeTopLevelItem(i)
            else:
                top_item.updateText()


class RegisterSelectionTree(drag_selection_window.SelectionTree):
    """Subclass of the selection tree to be used in register selection
    window.
    """

    def __init__(self):
        super(RegisterSelectionTree, self).__init__()

    def getSaveState(self):
        save_state = RegisterSelectionSaveList()
        for i in range(self.topLevelItemCount()):
            top_item = self.topLevelItem(i)
            save_item = RegisterSelectionSaveItem(top_item)
            save_state.append(save_item)
        return save_state

    def createNewItem(self, dropped_item, parent_item):
        """Create a new tree item for the tree. Return new_item, None since
        no custom widget is used.
        """
        circuit = parent_item.data(0, QtCore.Qt.UserRole)
        new_item = RegisterSelectionTreeItem(circuit, dropped_item.text(0))
        return new_item, None

    def createLoadedItem(self, save_state):
        if isinstance(save_state.circuit, GlobalDummy):
            new_item = RegisterSelectionTreeItem(save_state.circuit,
                                                 save_state.channel)
        else:
            machine = self.window().parent().circuit.scene()
            circuit = machine.findMatchingCircuit(save_state.circuit)
            # No match is found so remove the item
            if circuit is None:
                return None, None
            new_item = RegisterSelectionTreeItem(circuit, save_state.channel)
        return new_item, None


class RegisterSelectionTreeItem(QtGui.QTreeWidgetItem):
    """Tree widget item used on register selection tree."""

    def __init__(self, circuit, channel):
        # Save references to the circuit and channel for easy updates
        self.circuit = circuit
        self.channel = channel
        self.io = self.circuit.findMatchingIO(self.channel)
        super(RegisterSelectionTreeItem, self).__init__()
        self.updateText()

    def updateText(self):
        """Update the text of the item to match the current name of
        self.circuit.
        """
        self.setText(0, self.circuit.name + '.' + self.channel)


class RegisterSelectionSaveItem(object):
    """Container for RunSelectionTreeItem state without Qt bindings.
    Used for saving.
    """

    def __init__(self, tree_item):
        self.circuit = tree_item.circuit.getSaveState()
        self.channel = tree_item.channel

    def update(self, tree_item):
        """Update the save state to match the current state."""
        self.__init__(tree_item)

    def __str__(self):
        return str("'" + self.circuit.name + "." + self.channel + "'")


class RegisterSelectionSaveList(list):
    """Convinience class for handling save items. Reimplements __str__
    to print out proper info for script.
    """

    def __init__(self):
        super(RegisterSelectionSaveList, self).__init__()

    def __str__(self):
        i = 0
        string = ""
        for item in self:
            if i != 0:
                string += ", "
            string += str(item)
            i += 1
        return str(string)


class GlobalDummy(object):
    """Dummy class used with global channels to pass as a global circuit."""

    def __init__(self):
        self.name = "global"
        self.save_state = self
        self.loaded_item = self

    def getSaveState(self):
        """Return the save state of the object for saving."""
        return self.save_state

    def findMatchingIO(self, channel):
        """Return something not None to signal that the channel is valid."""
        return self

    def scene(self):
        """Return something not None to tell it's part of a scene."""
        return "Global"


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = RegisterSelectionWindow()
    sys.exit(app.exec_())
