import math

from PyQt4 import QtGui, QtCore

from atom_pair import AtomPair
from molecule_info import MoleculeInfo
import output

# DEFAULTS

number_of_layers = 5
max_number_of_layers = 100
surface_atom_types = ["H", "H", "H", "H", "H"]
substrate_atom_types = ["SI", "SI", "SI", "SI", "SI"]


# CONTACTS

contacts = [
    MoleculeInfo(
        name                =   "Contact",
        size                =   (3*AtomPair.XSIZE, 4*AtomPair.YSIZE),
        output_file         =   "contact.xyz",
        color               =   (241, 231, 65),
        snap                =   (AtomPair.XSIZE/2, AtomPair.YSIZE),
        scene_translation   =   (-AtomPair.XSIZE/2, -AtomPair.YSIZE),
        output_translation  =   (output.X_SCALE, 2*output.Y_SCALE, output.Z_SCALE),
        rotating            =   True,
        rotation_axis       =   (AtomPair.XSIZE, 2*AtomPair.YSIZE),
        shape               =   "Contact"
        )
]

# MOLECULES

molecules = [
    MoleculeInfo(
        name                =   "Test Molecule",
        size                =   (AtomPair.XSIZE, AtomPair.YSIZE),
        output_file         =   "test_molecule.xyz",
        color               =   (255, 0, 0),
        snap                =   (AtomPair.XSIZE, AtomPair.YSIZE),
        scene_translation   =   (0, 0),
        output_translation  =   (0, 0, 0),
        rotating            =   False,
        rotation_axis       =   (0, 0),
        shape               =   "Rounded Rectangle"
        )
]

# MOLECULE SHAPES
def getShape(key, xsize, ysize):
    if key == "Contact":
        contact_xsize = 3*AtomPair.XSIZE
        contact_ysize = 4*AtomPair.YSIZE
        contact_path = QtGui.QPainterPath()
        contact_path.setFillRule(QtCore.Qt.WindingFill)
        tip_angle = math.degrees(math.atan(13.0/27 * contact_ysize/contact_xsize))
        contact_path.moveTo(4*contact_xsize/13 + 20, 0)
        contact_path.arcTo(4*contact_xsize/13 - 10, 0, 20, 20, 90, tip_angle)
        contact_path.arcTo(0, contact_ysize/3 - 10, 20, 20, 90 + 2*tip_angle, 90 - 2*tip_angle)
        contact_path.arcTo(0, 2*contact_ysize/3 - 10, 20, 20, 180, 90 - 2*tip_angle)
        contact_path.arcTo(4*contact_xsize/13 - 10, contact_ysize - 20, 20, 20, 270 - tip_angle, tip_angle)
        contact_path.arcTo(contact_xsize - 20, contact_ysize - 20, 20, 20, 270, 90)
        contact_path.arcTo(contact_xsize - 20, 0, 20, 20, 0, 90)
        contact_path.closeSubpath()
        return contact_path
    elif key == "Rectangle":
        rect = QtGui.QPainterPath()
        rect.addRect(0, 0, xsize, ysize)
        return rect
    elif key == "Ellipse":
        ellipse = QtGui.QPainterPath()
        ellipse.addEllipse(0, 0, xsize, ysize)
        return ellipse
    elif key == "Rounded Rectangle":
        rounded_rect = QtGui.QPainterPath()
        rounded_rect.addRoundedRect(0, 0, xsize, ysize, 10, 10)
        return rounded_rect
    else:
        return None
