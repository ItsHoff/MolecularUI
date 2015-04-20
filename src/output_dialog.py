import sys

from PyQt4 import QtGui, QtCore

import settings


class OutputDialog(QtGui.QDialog):

    def __init__(self, parent):
        super(OutputDialog, self).__init__(parent)
        self.setModal(True)
        layout = QtGui.QGridLayout(self)
        layout.addWidget(QtGui.QLabel("Layers to output"), 0, 0)
        layout.addWidget(QtGui.QLineEdit(), 0, 1)

        layout.setRowMinimumHeight(1, 10)

        layout.addWidget(QtGui.QLabel("Surface atom types:"), 2, 0)
        self.surface_layout = QtGui.QHBoxLayout()
        self.surface_layout.addWidget(QtGui.QLineEdit())
        self.surface_layout.addWidget(QtGui.QLineEdit())
        self.surface_layout.addWidget(QtGui.QLineEdit())
        self.surface_layout.addWidget(QtGui.QLineEdit())
        self.surface_layout.addWidget(QtGui.QLineEdit())
        layout.addLayout(self.surface_layout, 3, 0, 1, 2)


        layout.addWidget(QtGui.QLabel("Substrate atom types:"), 4, 0)
        self.substrate_layout = QtGui.QHBoxLayout()
        self.substrate_layout.addWidget(QtGui.QLineEdit())
        self.substrate_layout.addWidget(QtGui.QLineEdit())
        self.substrate_layout.addWidget(QtGui.QLineEdit())
        self.substrate_layout.addWidget(QtGui.QLineEdit())
        self.substrate_layout.addWidget(QtGui.QLineEdit())
        layout.addLayout(self.substrate_layout, 5, 0, 1, 2)

        layout.setRowMinimumHeight(6, 15)

        cancel_button = QtGui.QPushButton("Cancel")
        self.connect(cancel_button, QtCore.SIGNAL("pressed()"), self.reject)
        ok_button = QtGui.QPushButton("OK")
        ok_button.setDefault(True)
        self.connect(ok_button, QtCore.SIGNAL("pressed()"), self.accept)
        layout.addWidget(cancel_button, 7, 0)
        layout.addWidget(ok_button, 7, 1)

        self.setMaximumSize(self.minimumSize())

    def showDialog(self):
        scene = self.parent().graphics_scene
        layer_edit = self.layout().itemAtPosition(0, 1).widget()
        layer_edit.setText(str(len(scene.layers)-1))
        for i, atom in enumerate(scene.surface.atom_types):
            edit = self.surface_layout.itemAt(i).widget()
            edit.setText(atom)
        for j, atom in enumerate(scene.substrate_atom_types):
            edit = self.substrate_layout.itemAt(j).widget()
            edit.setText(atom)
        return self.exec_()

    def getOptions(self):
        options = {"layers_to_draw": None, "surface_atom_types": [],
                   "substrate_atom_types": []}
        layer_edit = self.layout().itemAtPosition(0, 1).widget()
        options["layers_to_draw"] = int(layer_edit.text())
        for i in range(5):
            edit = self.surface_layout.itemAt(i).widget()
            options["surface_atom_types"].append(edit.text())
        for j in range(5):
            edit = self.substrate_layout.itemAt(j).widget()
            options["substrate_atom_types"].append(edit.text())
        return options

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = OutputDialog()
    print w.showDialog()
    sys.exit(app.exec_())
