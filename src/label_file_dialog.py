'''
Created on Jun 19, 2014

@author: keisano1
'''

from PyQt4 import QtGui, QtCore


class LabelFileDialog(QtGui.QWidget):
    """File dialog widget that contains label showing the current file
    and a button to open the dialog to select the file.
    """

    def __init__(self):
        """Create the label and the button for the widget and connect
        the button to open the dialog. Finally add them into a horizontal
        layout.
        """
        super(LabelFileDialog, self).__init__()
        self.file_path = None
        self.button = QtGui.QToolButton(self)
        self.button.setIcon(self.style().standardIcon(QtGui.QStyle.SP_DirIcon))
        self.label = QtGui.QLabel("No file selected", self)
        self.layout = QtGui.QHBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        QtCore.QObject.connect(self.button, QtCore.SIGNAL("clicked()"),
                               self.openDialog)

    def openDialog(self):
        """Open a file dialog to select a file. If file was selected
        call setFileName to change the label.
        """
        filename = QtGui.QFileDialog.getOpenFileName(self, "Select file",
                                                     self.file_path)
        if filename:
            self.setValue(filename)

    def setValue(self, value):
        """Set the value of the widget to match value. Display the folder
        and filename of the given path on the label.
        """
        self.file_path = value
        split = value.split("/")
        self.label.setText(split[-1])

    def getValue(self):
        """Return the value of the widget."""
        return self.file_path

    def clearValue(self):
        """Clear the value of the widget."""
        self.file_path = None
        self.label.setText("No file selected")
