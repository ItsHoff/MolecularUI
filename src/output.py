import numpy as np
from collections import OrderedDict

LEFT_H_POS = np.array([0.276, 0, 0.5])
RIGHT_H_POS = np.array([0.724, 0, 0.5])
X_SCALE = np.array([7.68, 0, 0])
Y_SCALE = np.array([0, 0, 3.84])
HEIGHT = np.array([0, 2.994, 0])
TOTAL_SCALE = X_SCALE + Y_SCALE + HEIGHT
# RIGHT_OFFSET = np.array([3.44, 0, 0])
# LEFT_H_POS = np.array([(1-RIGHT_OFFSET[0]/X_SCALE[0])/2, 0.5])
# RIGHT_H_POS = LEFT_H_POS + np.array([RIGHT_OFFSET[0]/X_SCALE[0], 0])

def getClockwiseRotationM(angle):
    angle = np.radians(angle)
    rotation_m = np.array([[np.cos(angle), 0, -np.sin(angle)],
                          [0, 1, 0],
                          [np.sin(angle), 0, np.cos(angle)]])
    return rotation_m

def getCounterClockwiseRotationM(angle):
    angle = np.radians(angle)
    rotation_m = np.array([[np.cos(angle), 0, np.sin(angle)],
                          [0, 1, 0],
                          [-np.sin(angle), 0, np.cos(angle)]])
    return rotation_m

contacts = OrderedDict([
    ("contact", {
        "default_translation"   : np.array([0, 0, 0]),
        "rotation_translation"  : np.array([0, 0, 0])
    })
])
