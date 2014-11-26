'''
Created on Jun 24, 2014

@author: keisano1
'''

from PyQt4 import QtGui
from label_file_dialog import LabelFileDialog


class LabelDirDialog(LabelFileDialog):
    """Reimplementation of file dialog. Select directories instead of files.
    Reimplemented functions:
        openDialog
        setFileName
    """

    def __init__(self):
        """Call the super and just set a proper label text."""
        super(LabelDirDialog, self).__init__()
        self.label.setText("No directory selected")

    def openDialog(self):
        """Open the dialog for selecting directories. If selected
        call setFileName to change label."""
        filename = QtGui.QFileDialog.getExistingDirectory(self, "Select folder",
                                                          self.file_path)
        if filename:
            self.setValue(filename)

    def setValue(self, value):
        """Set the value of the widget to value and set label to show the
        last two directories of the path.
        """
        self.file_path = value
        split = value.split("/")
        length = len(split)
        self.label.setText(split[length-2] + '/' + split[length-1])

    def clearValue(self):
        """Clear the value of the widget."""
        self.file_path = None
        self.label.setText("No directory selected")
