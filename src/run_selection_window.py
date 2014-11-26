"""
Contains all the classes for the run selection window.
Classes:
    - RunSelectionWindow
    - RunSelectionTree
    - RunSelectionTreeItem
"""

import sys

from PyQt4 import QtGui, QtCore

from custom_line_edit import CustomLineEdit
import drag_selection_window
import circuits


class RunSelectionWindow(drag_selection_window.DragSelectionWindow):
    """Subclass of DragSelection window used for selecting the runtime
    operations of the pyvafm."""

    def __init__(self, main_widget):
        self.main_widget = main_widget
        super(RunSelectionWindow, self).__init__(main_widget)
        self.resize(700, 400)
        self.setWindowTitle("Select runtime operations")
        self.selection_tree = RunSelectionTree()
        self.selection_tree.setHeaderLabel("Selected operations")
        self.layout().addWidget(self.selection_tree, 0, 1)

    def loadOptions(self):
        """Add all the circuits with runtime operations to the option tree."""
        new_item = QtGui.QTreeWidgetItem(self.option_tree)
        new_item.setText(0, "Machine")
        circuit = MachineDummy()
        new_item.setData(0, QtCore.Qt.UserRole, circuit)
        new_item.setFlags(new_item.flags() &
                          ~QtCore.Qt.ItemIsDragEnabled)
        for function in circuits.run_time_functions["Machine"]:
            function_split = function.split("#")
            sub_item = QtGui.QTreeWidgetItem(new_item)
            sub_item.setText(0, function_split[0])
            sub_item.setData(0, QtCore.Qt.UserRole, function)

        for circuit in self.main_widget.machine_widget.circuits:
            circuit_type = circuit.circuit_info.circuit_type
            if circuit_type in circuits.run_time_functions:
                new_item = QtGui.QTreeWidgetItem(self.option_tree)
                new_item.setText(0, circuit.name)
                new_item.setData(0, QtCore.Qt.UserRole, circuit)
                new_item.setFlags(new_item.flags() &
                                  ~QtCore.Qt.ItemIsDragEnabled)
                for function in circuits.run_time_functions[circuit_type]:
                    function_split = function.split("#")
                    sub_item = QtGui.QTreeWidgetItem(new_item)
                    sub_item.setText(0, function_split[0])
                    sub_item.setData(0, QtCore.Qt.UserRole, function)

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
            widget = self.selection_tree.itemWidget(top_item, 0)
            if widget.circuit.scene() is None:
                i = self.selection_tree.indexOfTopLevelItem(top_item)
                self.selection_tree.takeTopLevelItem(i)
            else:
                widget.updateText()


class RunSelectionTree(drag_selection_window.SelectionTree):
    """Subclass of the selection tree to be used in run selection
    window.
    """

    def __init__(self):
        super(RunSelectionTree, self).__init__()

    def getSaveState(self):
        save_state = []
        for i in range(self.topLevelItemCount()):
            top_item = self.topLevelItem(i)
            widget = self.itemWidget(top_item, 0)
            save_item = RunSelectionSaveItem(widget)
            save_state.append(save_item)
        return save_state

    def createNewItem(self, dropped_item, parent_item):
        """Create a empty tree widget item and a custom widget to use
        with the item.
        """
        new_item = QtGui.QTreeWidgetItem()
        circuit = parent_item.data(0, QtCore.Qt.UserRole)
        function = dropped_item.data(0, QtCore.Qt.UserRole)
        item_widget = RunSelectionTreeItem(circuit, function)
        # Set the tree item size hint to match the widget size hint.
        size_hint = item_widget.sizeHint()
        new_item.setSizeHint(0, size_hint)
        return new_item, item_widget

    def createLoadedItem(self, save_state):
        new_item = QtGui.QTreeWidgetItem()
        circuit = save_state.circuit.loaded_item
        item_widget = RunSelectionTreeItem(circuit, save_state.function)
        item_widget.setEdit(save_state.edit_text)
        # Set the tree item size hint to match the widget size hint.
        size_hint = item_widget.sizeHint()
        new_item.setSizeHint(0, size_hint)
        return new_item, item_widget


class RunSelectionTreeItem(QtGui.QWidget):
    """Custom widget to be used in run selection tree. Holds label telling the
    function and a line edit to edit the function parameters."""

    def __init__(self, circuit, function):
        super(RunSelectionTreeItem, self).__init__()
        self.circuit = circuit
        self.function = function
        main_layout = QtGui.QHBoxLayout()
        self.label = QtGui.QLabel()

        main_layout.addWidget(self.label)
        function_split = function.split("#")
        if len(function_split) > 1:
            self.line_edit = CustomLineEdit(function_split[1])
            main_layout.addWidget(self.line_edit)
            close = QtGui.QLabel(')')
            main_layout.addWidget(close)
        else:
            self.line_edit = None
        self.setLayout(main_layout)
        self.updateText()

    def getEdit(self):
        """Return the text value of the line edit."""
        if self.line_edit is not None:
            return self.line_edit.text()
        else:
            return None

    def setEdit(self, text):
        """Set the value of the line edit to match text."""
        if self.line_edit is not None:
            self.line_edit.setText(text)

    def updateText(self):
        """Update the text of the widget to match the current name of
        self.circuit.
        """
        function_split = self.function.split("#")
        if self.line_edit is None:
            self.label.setText(self.circuit.name + '.' + function_split[0] + '()')
        else:
            self.label.setText(self.circuit.name + '.' + function_split[0] + '(')

    def text(self):
        """Reimplementation. Return the text of the labels and parameters
        given in line edit as one string.
        """
        self.updateText()
        if self.line_edit is not None:
            return self.label.text() + self.line_edit.text() + ')'
        else:
            return self.label.text()

    def copy(self):
        """Return a copy of the widget. Needed when moving widgets around."""
        new_item = RunSelectionTreeItem(self.circuit, self.function)
        if self.line_edit is not None:
            new_item.setEdit(self.line_edit.text())
        return new_item


class RunSelectionSaveItem(object):
    """Container for RunSelectionTreeItem state without Qt bindings.
    Used for saving.
    """

    def __init__(self, tree_item):
        self.circuit = tree_item.circuit.save_state
        self.function = tree_item.function
        self.edit_text = tree_item.getEdit()

    def update(self, tree_item):
        """Update the save state to match the current state."""
        self.__init__(tree_item)


class MachineDummy(object):
    """Dummy class used to pass as a machine circuit."""

    def __init__(self):
        self.name = "machine"
        self.save_state = self
        self.loaded_item = self

    def getSaveState(self):
        """Return the save state of the object."""
        return self.save_state

    def scene(self):
        """Return something not None to signal that the dummy is
        part of a scene.
        """
        return "Global"

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = RunSelectionWindow()
    sys.exit(app.exec_())
