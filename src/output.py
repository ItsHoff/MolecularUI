import numpy as np
from collections import OrderedDict

LEFT_H_POS = np.array([0.276, 0, 0.5])
RIGHT_H_POS = np.array([0.724, 0, 0.5])
X_SCALE = np.array([7.68, 0, 0])
Y_SCALE = np.array([0, 0, 3.84])
HEIGHT = np.array([0, 2.994, 0])
TOTAL_SCALE = X_SCALE + Y_SCALE + HEIGHT

def getClockwiseRotationM(angle):
    """Return the rotation matrix for rotating by given angle in clockwise
    direction."""
    angle = np.radians(angle)
    rotation_m = np.array([[np.cos(angle), 0, -np.sin(angle)],
                          [0, 1, 0],
                          [np.sin(angle), 0, np.cos(angle)]])
    return rotation_m

def getCounterClockwiseRotationM(angle):
    """Return the rotation matrix for rotating by given angle in
    counterclockwise direction."""
    angle = np.radians(angle)
    rotation_m = np.array([[np.cos(angle), 0, np.sin(angle)],
                          [0, 1, 0],
                          [-np.sin(angle), 0, np.cos(angle)]])
    return rotation_m
