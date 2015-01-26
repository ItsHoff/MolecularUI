import math

from PyQt4 import QtGui, QtCore
import numpy as np

from hydrogen import Hydrogen
import output

CONTACT_XSIZE = 3*Hydrogen.XSIZE
CONTACT_YSIZE = 4*Hydrogen.YSIZE
CONTACT_PATH = QtGui.QPainterPath()
CONTACT_PATH.setFillRule(QtCore.Qt.WindingFill)
tip_angle = math.degrees(math.atan(13.0/27 * CONTACT_YSIZE/CONTACT_XSIZE))
CONTACT_PATH.moveTo(4*CONTACT_XSIZE/13 + 20, 0)
CONTACT_PATH.arcTo(4*CONTACT_XSIZE/13 - 10, 0, 20, 20, 90, tip_angle)
CONTACT_PATH.arcTo(0, CONTACT_YSIZE/3 - 10, 20, 20, 90 + 2*tip_angle, 90 - 2*tip_angle)
CONTACT_PATH.arcTo(0, 2*CONTACT_YSIZE/3 - 10, 20, 20, 180, 90 - 2*tip_angle)
CONTACT_PATH.arcTo(4*CONTACT_XSIZE/13 - 10, CONTACT_YSIZE - 20, 20, 20, 270 - tip_angle, tip_angle)
CONTACT_PATH.arcTo(CONTACT_XSIZE - 20, CONTACT_YSIZE - 20, 20, 20, 270, 90)
CONTACT_PATH.arcTo(CONTACT_XSIZE - 20, 0, 20, 20, 0, 90)
CONTACT_PATH.closeSubpath()

class MoleculeInfo(object):

    def __init__(self, name, size, output_file, color=(255, 255, 255),
                 snap=(Hydrogen.XSIZE, Hydrogen.YSIZE),
                 scene_translation=(0, 0), output_translation=(0, 0, output.Z_SCALE),
                 rotating=False, rotation_axis=(0, 0), special_shape=None):
        self.name = name
        self.size = size
        self.output_file = output_file
        self.color = color
        self.snap = snap
        self.scene_translation = scene_translation
        self.output_translation = output_translation
        self.rotating = rotating
        self.rotation_axis = rotation_axis
        self.special_shape = special_shape


contacts = [
    MoleculeInfo(
        name                =   "Contact",
        size                =   (3*Hydrogen.XSIZE, 4*Hydrogen.YSIZE),
        output_file         =   "contact.xyz",
        color               =   (241, 231, 65),
        snap                =   (Hydrogen.XSIZE/2, Hydrogen.YSIZE),
        scene_translation   =   (-Hydrogen.XSIZE/2, -Hydrogen.YSIZE),
        output_translation  =   (output.X_SCALE, 2*output.Y_SCALE, output.Z_SCALE),
        rotating            =   True,
        rotation_axis       =   (Hydrogen.XSIZE, 2*Hydrogen.YSIZE),
        special_shape       =   "Contact"
        )
]

molecules = [
    MoleculeInfo(
        name                =   "Test Molecule",
        size                =   (Hydrogen.XSIZE, 2*Hydrogen.YSIZE),
        output_file         =   "test_molecule.xyz",
        color               =   (255, 0, 0),
        snap                =   (Hydrogen.XSIZE, Hydrogen.YSIZE),
        scene_translation   =   (0, 0),
        output_translation  =   (0, 0, 0),
        rotating            =   False,
        rotation_axis       =   (0, 0),
        special_shape       =   None
        )
]

shapes = {"Contact": CONTACT_PATH}
