import numpy as np
from collections import OrderedDict

LEFT_H_POS = np.array([0.276, 0.5, 0])
RIGHT_H_POS = np.array([0.724, 0.5, 0])
X_SCALE = 7.68
Y_SCALE = -3.84
Z_SCALE = 2.994
TOTAL_SCALE = np.array((X_SCALE, Y_SCALE, Z_SCALE))

def getClockwiseRotationM(angle):
    """Return the rotation matrix for rotating by given angle in clockwise
    direction."""
    angle = np.radians(angle)
    rotation_m = np.array([[np.cos(angle), -np.sin(angle), 0],
                          [np.sin(angle), np.cos(angle), 0],
                           [0, 0, 1]])
    return rotation_m

def getCounterClockwiseRotationM(angle):
    """Return the rotation matrix for rotating by given angle in
    counterclockwise direction."""
    angle = np.radians(angle)
    rotation_m = np.array([[np.cos(angle), np.sin(angle), 0],
                          [-np.sin(angle), np.cos(angle), 0],
                           [0, 0, 1]])
    return rotation_m
