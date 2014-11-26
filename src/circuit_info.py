'''
Created on Jun 12, 2014

@author: keisano1
'''

groups = ["Mathematics", "Signal Generation", "Signal Processing",
          "Signal Control", "Output", "Flip-Flops", "Custom", "Cantilever",
          "Interpolation", "Scanner", "Van der Waals",
          "Scanning Tunneling Microscope", "Recently Used"]


class CircuitInfo(object):
    """Container for all the general circuit parameters."""

    def __init__(self, name, group, inputs=[], outputs=[],
                 param_window_style={}, default_values={},
                 script_format=None):
        """Save all the parameters."""
        self.circuit_type = name
        self.group = group
        self.params = []
        self.default_values = default_values
        self.param_window_style = param_window_style
        self.script_format = script_format
        self.inputs = inputs
        self.outputs = outputs
