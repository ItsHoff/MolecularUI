"""Module for creating small widgets mainly for parameter window.

Current widgets:
    - LineEdit
        - subtypes
    - CheckBox
    - FileDialog
    - DirDialog
    - RegisterDialog
    - ModeSetup
    - RecorderSelect
"""

from PyQt4 import QtGui

from custom_line_edit import CustomLineEdit
from state_check_box import StateCheckBox
from label_file_dialog import LabelFileDialog
from label_dir_dialog import LabelDirDialog
from register_selection_window import RegisterSelectionButton
from mode_setup_window import ModeSetupButton
from recorder_select import RecorderSelect


def createLineEdit(label_text, subtype):
    """Create a line edit and a label with label_text."""
    label = QtGui.QLabel(label_text)
    text_edit = CustomLineEdit(subtype)
    return [label, text_edit]


def createCheckBox(label_text):
    """Create a check box and a label with label_text."""
    label = QtGui.QLabel(label_text)
    check_box = StateCheckBox()
    return [label, check_box]


def createFileDialog(label_text):
    """Create a file dialog and a label with label_text."""
    label = QtGui.QLabel(label_text)
    file_dialog = LabelFileDialog()
    return [label, file_dialog]


def createDirDialog(label_text):
    """Create a directory dialog and a label with label_text."""
    label = QtGui.QLabel(label_text)
    dir_dialog = LabelDirDialog()
    return [label, dir_dialog]


def createRegisterDialog(label_text, central_widget, parent):
    """Create a button to open the register dialog and
    a label with label text.
    """
    label = QtGui.QLabel(label_text)
    button = RegisterSelectionButton(central_widget, parent)
    return [label, button]


def createModeSetup(label_text, parent):
    """Create a button to open the mode setup and
    a label with label text.
    """
    label = QtGui.QLabel(label_text)
    button = ModeSetupButton(parent)
    return [label, button]

def createRecorderSelect(label_text):
    """Create a recorder select widget and a label with label_text."""
    label = QtGui.QLabel(label_text)
    button = RecorderSelect()
    return [label, button]

