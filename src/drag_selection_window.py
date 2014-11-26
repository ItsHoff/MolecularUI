"""
Contains all the base classes for the drag selection windows.
Classes:
    - DragSelectionWindow
    - DragSelectionTree
    - DragSelectionTreeItem
"""

from PyQt4 import QtGui, QtCore
import sys


class DragSelectionWindow(QtGui.QDialog):
    """Base class for a window that allows the user to select actions
    from option tree by dragging them to the selection tree.
    """

    def __init__(self, parent=None):
        super(DragSelectionWindow, self).__init__(parent)
        self.setModal(True)
        self.setAcceptDrops(True)
        self.initUI()

    def initUI(self):
        """Initialise the widgets and add them to the window layout."""
        self.resize(600, 400)
        main_layout = QtGui.QGridLayout()

        self.option_tree = QtGui.QTreeWidget()
        self.option_tree.setHeaderLabel("Options")
        self.option_tree.setSizePolicy(QtGui.QSizePolicy.Fixed,
                                       QtGui.QSizePolicy.Expanding)
        self.option_tree.setDragEnabled(True)
        self.loadOptions()

        self.selection_tree = SelectionTree()
        self.selection_tree.setHeaderLabel("Selections")
        self.loadSelections()

        done_button = QtGui.QPushButton("Done")
        # cancel_button = QtGui.QPushButton("Cancel")
        QtCore.QObject.connect(done_button, QtCore.SIGNAL("clicked()"),
                               self.hide)

        main_layout.addWidget(self.option_tree, 0, 0)
        main_layout.addWidget(self.selection_tree, 0, 1)
        main_layout.addWidget(done_button, 1, 0, 1, 2)
        # main_layout.addWidget(cancel_button, 1, 1)
        self.setLayout(main_layout)

    def showWindow(self):
        """Update the window to reflect the current state
        and show it.
        """
        self.updateNames()
        self.show()

    def updateNames(self):
        """Update the names of the window items. By default will be called
        everytime window is shown.  Should be reimplemented by subclasses.
        """
        pass

    def loadOptions(self):
        """Load all the possible options into the option tree.
        Should be reimplemented by subclasses."""
        pass

    def loadSelections(self):
        """Load all the readily selected items into the selection tree.
        Should be reimplemented by subclasses."""
        pass

    def getSaveState(self):
        """Return the save state of the window for saving."""
        self.updateNames()
        return self.selection_tree.getSaveState()

    def loadSaveState(self, save_state):
        """Load the selection tree to the state given in save_state."""
        self.selection_tree.loadSaveState(save_state)

    def dragEnterEvent(self, event):
        """Delete dragged item from selection tree when it exits the widget
        ie. enters this one. Save the deleted item incase user wants to
        drop it back.
        """
        if event.source() == self.selection_tree:
            current_item = self.selection_tree.currentItem()
            if current_item is not None:
                widget = self.selection_tree.itemWidget(current_item, 0)
                if widget is not None:
                    self.selection_tree.deleted_widget = widget.copy()
                index = self.selection_tree.currentIndex().row()
                deleted_item = self.selection_tree.takeTopLevelItem(index)
                self.selection_tree.deleted_item = deleted_item
                self.selection_tree.setCurrentItem(None)

    def clearSelections(self):
        """Clear all the selections from the selection tree."""
        self.selection_tree.clear()


class SelectionTree(QtGui.QTreeWidget):
    """Tree widget that holds the selections of the window."""

    def __init__(self):
        super(SelectionTree, self).__init__()
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,
                           QtGui.QSizePolicy.Expanding)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(False)
        self.deleted_item = None
        self.deleted_widget = None

    def getSaveState(self):
        """Return a list of save_states for the tree items.
        Should be reimplemeted by subclasses.
        """
        pass

    def loadSaveState(self, save_state):
        """Add the tree items defined in save_state to the tree."""
        self.clear()
        for save_item in save_state:
            new_item, widget = self.createLoadedItem(save_item)
            if new_item is not None:
                self.addTopLevelItem(new_item)
            if widget is not None:
                self.setItemWidget(new_item, 0, widget)

    def dropEvent(self, event):
        """Add a new selection item to the tree if user drags an item from
        option tree or move items around if the drag source is self.
        Have to account for the situation that drag from self has exited the
        widget and the dragged item was thus deleted.
        """
        event.accept()
        if event.source() == self:
            # If current item is none the drag has exited the widget and
            # the item was deleted.
            if self.currentItem() is None:
                widget = self.deleted_widget
                drag_item = self.deleted_item
            else:
                widget = self.itemWidget(self.currentItem(), 0)
                drag_item = self.takeTopLevelItem(self.currentIndex().row())
            item_at = self.itemAt(event.pos())
            # Insert item to bottom if no items are under its drop position
            # Otherwise insert the item on top of the item under the drop
            # position.
            if item_at is None:
                self.addTopLevelItem(drag_item)
            else:
                index = self.indexOfTopLevelItem(item_at)
                self.insertTopLevelItem(index, drag_item)
            if widget is not None:
                widget = widget.copy()
                self.setItemWidget(drag_item, 0, widget)
            # Set current item to the dropped item to make dropping
            # more obvious to the user.
            self.setCurrentItem(drag_item)
        else:
            dropped_item = event.source().currentItem()
            parent_item = dropped_item.parent()
            new_item, widget = self.createNewItem(dropped_item, parent_item)
            item_at = self.itemAt(event.pos())
            # Insert item to bottom if no items are under its drop position
            # Otherwise insert the item on top of the item under the drop
            # position.
            if item_at is None:
                self.addTopLevelItem(new_item)
            else:
                index = self.indexOfTopLevelItem(item_at)
                self.insertTopLevelItem(index, new_item)
            if widget is not None:
                self.setItemWidget(new_item, 0, widget)
            # Set current item to the dropped item and make this tree the
            # focus to make dropping more obvious to the user.
            self.setCurrentItem(new_item)
            self.setFocus(QtCore.Qt.MouseFocusReason)

    def createNewItem(self, dropped_item, parent_item):
        """Create a new tree widget item and possible custom widget used
        with the tree item. Should be reimplemented by subclasses.
        Return: tree widget item, custom widget (None if not used)."""
        new_item = QtGui.QTreeWidgetItem()
        new_item.setText(0, parent_item.text(0) + '.' +
                         dropped_item.text(0))
        return new_item, None

    def createLoadedItem(self, save_state):
        """Create a tree widget item matching the save_state.
        Should be reimplemented by subclasses.
        """
        pass

    def keyPressEvent(self, event):
        """Remove the current item if delete is pressed."""
        if event.key() == QtCore.Qt.Key_Delete:
            current_item = self.currentItem()
            index = self.indexOfTopLevelItem(current_item)
            self.takeTopLevelItem(index)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = DragSelectionWindow()
    sys.exit(app.exec_())
