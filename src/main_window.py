import sys

import cPickle as pickle

import sip
API_NAMES = ["QDate", "QDateTime", "QString", "QTextStream", "QTime", "QUrl", "QVariant"]
API_VERSION = 2
for api_name in API_NAMES:
    sip.setapi(api_name, API_VERSION)
from PyQt4 import QtGui, QtCore

from molecular_view import MolecularView
from molecular_scene import MolecularScene


class MainWindow(QtGui.QMainWindow):
    """The main window of the UI."""

    def __init__(self):
        """Initialise the main window."""
        super(MainWindow, self).__init__()
        self.setGeometry(100, 100, 800, 500)
        self.setWindowTitle('MolecularUI')

        file_menu = QtGui.QMenu("File", self)

        save_action = QtGui.QAction("Save", self)
        save_action.setShortcut(QtGui.QKeySequence("Ctrl+S"))
        QtCore.QObject.connect(save_action, QtCore.SIGNAL("triggered()"),
                               self.save)

        load_action = QtGui.QAction("Load", self)
        load_action.setShortcut(QtGui.QKeySequence("Ctrl+L"))
        QtCore.QObject.connect(load_action, QtCore.SIGNAL("triggered()"),
                               self.load)

        insert_action = QtGui.QAction("Insert", self)
        insert_action.setShortcut(QtGui.QKeySequence("Ctrl+I"))
        QtCore.QObject.connect(insert_action, QtCore.SIGNAL("triggered()"),
                               self.insert)

        quit_action = QtGui.QAction("Quit", self)
        quit_action.setShortcut(QtGui.QKeySequence("Ctrl+Q"))
        QtCore.QObject.connect(quit_action, QtCore.SIGNAL("triggered()"),
                               self.close)

        file_menu.addAction(save_action)
        file_menu.addAction(load_action)
        file_menu.addAction(insert_action)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)
        self.menuBar().addMenu(file_menu)

        self.setCentralWidget(MainWidget())

        self.show()
        self.statusBar().showMessage("Ready!", 2000)

    def save(self):
        """Get the save state of the program and save it to the location
        returned from the file dialog."""
        self.statusBar().showMessage("Creating save state...", 10000)
        save_state = SaveState.create(self)
        save_file = QtGui.QFileDialog().getSaveFileName(self, "Save Setup", "../saves")
        if save_file:
            with open(save_file, "w") as f:
                pickle.dump(save_state, f)
                self.statusBar().showMessage("Creating save state... Done!", 2000)
        else:
            self.statusBar().showMessage("Creating save state... Failed!", 2000)

    def saveSelected(self):
        """Save the setup currently selected."""
        self.statusBar().showMessage("Creating save state...", 10000)
        save_state = SaveState.createFromSelected(self)
        save_file = QtGui.QFileDialog().getSaveFileName(self, "Save Selected", "../saves")
        if save_file:
            with open(save_file, "w") as f:
                pickle.dump(save_state, f)
                self.statusBar().showMessage("Creating save state... Done!", 2000)
        else:
            self.statusBar().showMessage("Creating save state... Failed!", 2000)

    def load(self):
        """Load the save state selected by the user."""
        self.statusBar().showMessage("Loading save state...", 10000)
        load_file = QtGui.QFileDialog().getOpenFileName(self, "Load Setup", "../saves")
        if load_file:
            with open(load_file, "r") as f:
                save_state = pickle.load(f)
                save_state.load(self)
                self.statusBar().showMessage("Loading save state... Done!", 2000)
        else:
            self.statusBar().showMessage("Loading save state... Failed!", 2000)

    def insert(self):
        """Insert the save state of users choice into the current setup."""
        self.statusBar().showMessage("Inserting save state...", 10000)
        load_file = QtGui.QFileDialog().getOpenFileName(self, "Insert Setup", "../saves")
        if load_file:
            with open(load_file, "r") as f:
                save_state = pickle.load(f)
                save_state.insert(self)
                self.statusBar().showMessage("Inserting save state... Done!", 2000)
        else:
            self.statusBar().showMessage("Inserting save state... Failed!", 2000)


class MainWidget(QtGui.QWidget):
    """The main widget of the UI. Holds all of the widgets except status
    and menubars.
    """

    def __init__(self):
        super(MainWidget, self).__init__()
        # Set up the left area of the UI
        left_area = QtGui.QVBoxLayout()

        # Set up the buttons on the top left of the UI
        button_grid = QtGui.QGridLayout()
        create_button = QtGui.QPushButton("Create Output")

        QtCore.QObject.connect(create_button, QtCore.SIGNAL("clicked()"),
                               self.createOutput)

        button_grid.addWidget(create_button, 0, 0)

        # Set up the tree widget holding the circuits
        tree_widget = QtGui.QTreeWidget(self)
        tree_widget.setSizePolicy(QtGui.QSizePolicy.Minimum,
                                  QtGui.QSizePolicy.Expanding)
        tree_widget.setHeaderLabel("Circuits")
        tree_widget.setDragEnabled(True)
        tree_widget.setFocusPolicy(QtCore.Qt.NoFocus)

        # Load the circuits from circuits.py into the tree_widget
        self.loadCircuits(tree_widget)

        # Set up the graphics view for the machine and set the scene
        self.graphics_view = MolecularView()
        self.graphics_scene = MolecularScene(tree_widget, self.graphics_view)
        self.graphics_view.setScene(self.graphics_scene)

        # Add widgets to the corresponding layouts
        left_area.addLayout(button_grid)
        left_area.addWidget(tree_widget)
        main_layout = QtGui.QHBoxLayout()
        main_layout.addLayout(left_area)
        main_layout.addWidget(self.graphics_view)
        self.setLayout(main_layout)

    def loadCircuits(self, tree_widget):
        """Load all the circuits from the circuits file to the tree_widget"""
        groups = {}
        top_item = QtGui.QTreeWidgetItem(tree_widget)
        top_item.setText(0, "Contacts")
        top_item.setFlags(top_item.flags() & ~QtCore.Qt.ItemIsDragEnabled
                          & ~QtCore.Qt.ItemIsSelectable)
        groups["Contacts"] = top_item
        top_item = QtGui.QTreeWidgetItem(tree_widget)
        top_item.setText(0, "Recently Used")
        top_item.setFlags(top_item.flags() & ~QtCore.Qt.ItemIsDragEnabled
                          & ~QtCore.Qt.ItemIsSelectable)
        groups["Recently Used"] = top_item
        sub_item = QtGui.QTreeWidgetItem(groups["Contacts"])
        sub_item.setText(0, "Contact")

    def createOutput(self):
        """Create a output file from the current state of the scene."""
        status_bar = self.window().statusBar()
        status_bar.showMessage("Creating output...", 10000)
        save_file = QtGui.QFileDialog.getSaveFileName(self, "Save output", "../output")
        if not save_file:
            status_bar.showMessage("Creating output... Failed!", 2000)
            return
        result = self.graphics_scene.getOutput()
        if not save_file.endswith(".xyz"):
            save_file = save_file + ".xyz"
        # Write all the lines to the savefile
        with open(save_file, 'w') as out:
            out.write(str(len(result)))
            out.write("\n\n")
            for line in result:
                out.write(line)
                out.write("\n")
        status_bar.showMessage("Creating output... Done!", 2000)
        return save_file

    def keyPressEvent(self, event):
        """Send all key presses to the graphics scene."""
        if self.graphics_view.underMouse():
            self.graphics_scene.handleKeyPress(event)


class SaveState(object):
    """Stores the global save state."""

    def __init__(self):
        self.surface = None

    @classmethod
    def create(cls, main_window):
        """Gather all the data for saving without Qt bindings."""
        scene = main_window.centralWidget().graphics_scene
        save_state = cls()
        save_state.surface = scene.surface.getSaveState()
        return save_state

    @classmethod
    def createFromSelected(cls, main_window):
        """Gather all the data from selected items for saving
        without Qt bindings.
        """
        machine_widget = main_window.centralWidget().machine_widget
        save_state = cls()
        for item in machine_widget.selectedItems():
            save_state.items.append(item.getSaveState())
        return save_state

    def load(self, main_window):
        """Load the save state stored in this object."""
        scene = main_window.centralWidget().graphics_scene
        scene.clearAll()
        self.surface.load(scene)
        scene.updateSceneRect()

    def insert(self, main_window):
        """Insert the save state into the current setup."""
        machine_widget = main_window.centralWidget().machine_widget
        machine_widget.clearSelection()
        for item in self.items:
            machine_widget.addLoadedCircuit(item)
        self.cleanLoadedItems(machine_widget)
        machine_widget.updateSceneRect()
        machine_widget.saveSelection(0)

    def cleanLoadedItems(self, machine_widget):
        """Clean the references to the loaded items from save states."""
        for item in machine_widget.items:
            item.getSaveState()


def main():
    """Start the program and open the main window."""
    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
