import numpy as np
from collections import OrderedDict

LEFT_H_POS = np.array([0.276, 0.5, 0])
RIGHT_H_POS = np.array([0.724, 0.5, 0])
X_SCALE = 7.68
Y_SCALE = -3.84
Z_SCALE = 2.994
TOTAL_SCALE = np.array((X_SCALE, Y_SCALE, Z_SCALE))
X_OFFSET = np.array([7.68, 0, 0])
Y_OFFSET = np.array([0, -3.84, 0])
Z_OFFSET = np.array([0, 0, -5.171981])
INITIAL_Z = np.array([0, 0, -2.50465])
LAYER_Z = [np.array([0, 0, 0]),
          np.array([0, 0, -1.43264]),
          np.array([0, 0, -2.71328]),
          np.array([0, 0, -3.89135])]
LAYER_LEFT = [np.array([1.994680, 0, 0]),
             np.array([3.839680, 0, 0]),
             np.array([3.839680, -1.92, 0]),
             np.array([1.897680, -1.92, 0])]
LAYER_RIGHT = [np.array([5.684680, 0, 0]),
              np.array([7.679680, 0, 0]),
              np.array([7.679680, -1.92, 0]),
              np.array([5.781680, -1.92, 0])]
LEFT_BOTTOM_H = [np.array([-1.16, 0, -0.82]),
                 np.array([0, -1.16, -0.82])]
RIGHT_BOTTOM_H = [np.array([1.16, 0, -0.82]),
                  np.array([0, 1.16, -0.82])]

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
