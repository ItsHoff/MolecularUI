import math

from PyQt4 import QtGui, QtCore
import numpy as np

from atom_pair import AtomPair
import output


class MoleculeInfo(object):

    def __init__(self, name, size, output_file, color=(255, 255, 255),
                 snap=(AtomPair.XSIZE, AtomPair.YSIZE),
                 scene_translation=(0, 0), output_translation=(0, 0, output.Z_SCALE),
                 rotating=False, rotation_axis=(0, 0), shape=None):
        self.name = name
        self.size = size
        self.output_file = output_file
        self.color = color
        self.snap = snap
        self.scene_translation = scene_translation
        self.output_translation = output_translation
        self.rotating = rotating
        self.rotation_axis = rotation_axis
        self.shape = shape
