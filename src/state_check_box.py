'''
Created on Jun 19, 2014

@author: keisano1
'''

from PyQt4 import QtGui, QtCore


class StateCheckBox(QtGui.QCheckBox):
    """Simple checkbox that changes its text based on its state."""

    def __init__(self, state=True):
        """Create the checkbox and connect it."""
        super(StateCheckBox, self).__init__()
        self.setChecked(state)
        self.setText(str(state))
        QtCore.QObject.connect(self, QtCore.SIGNAL("stateChanged(int)"),
                               self.changeText)

    def changeText(self):
        """Change text to match the state of the checkbox."""
        self.setText(str(self.isChecked()))

    def getValue(self):
        """Define a unified interface for getting widget values."""
        return self.text()

    def setValue(self, value):
        """Define a unified interface for setting widget values."""
        self.setText(str(value))
        self.setChecked(bool(value))

    def clearValue(self):
        """Revert the state to the defaul value."""
        self.setValue(True)
