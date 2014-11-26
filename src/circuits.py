'''
Created on Jun 12, 2014

@author, keisano1
'''
from circuit_info import CircuitInfo
from collections import OrderedDict

machine_param_window_style = OrderedDict([
                            ("PyVAFM src", "DirDialog"),
                            ("dt", "FloatLineEdit"),
                            ("Pushed", "CheckBox")
                            ])

run_time_functions = {"Machine": ["Wait#FloatLineEdit"],
                      "Scanner": ["Place#ThreeDimensionLineEdit",
                                  "Move#MoveLineEdit", "MoveTo#MoveLineEdit",
                                  "MoveRecord#MoveRecordLineEdit", "ScanArea"],
                      "output" : ["Dump", "Stop", "Start"]
                      }

global_channels = ["time"]

circuits = OrderedDict([
# MATHEMATICS
("opAdd", CircuitInfo(
    name                =   "opAdd",
    group               =   "Mathematics",
    inputs              =   ["in#Factors"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Factors", "IntLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    default_values      =   {"Factors": 2},
    script_format       =   "formats/opAdd.format"
)),
("opSub", CircuitInfo(
    name                =   "opSub",
    group               =   "Mathematics",
    inputs              =   ["in1", "in2"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/opSub.format"
)),
("opMul", CircuitInfo(
    name                =   "opMul",
    group               =   "Mathematics",
    inputs              =   ["in#Factors"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    default_values      =   {"Factors": 2},
    script_format       =   "formats/opMul.format"
)),
("opDiv", CircuitInfo(
    name                =   "opDiv",
    group               =   "Mathematics",
    inputs              =   ["in1", "in2"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/opDiv.format"
)),
("opLinC", CircuitInfo(
    name                =   "opLinC",
    group               =   "Mathematics",
    inputs              =   ["ina#Factors", "inb#Factors"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Factors", "IntLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    default_values      =   {"Factors": 2},
    script_format       =   "formats/opLinC.format"
)),
("opPow", CircuitInfo(
    name                =   "opPow",
    group               =   "Mathematics",
    inputs              =   ["signal"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Power", "FloatLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/opPow.format"
)),
("opAbs", CircuitInfo(
    name                =   "opAbs",
    group               =   "Mathematics",
    inputs              =   ["signal"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/opAbs.format"
)),

("Greater or Equal", CircuitInfo(
    name                =   "GreaterOrEqual",
    group               =   "Mathematics",
    inputs              =   ["in1", "in2"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/GreaterOrEqual.format"
)),
("Less or Equal", CircuitInfo(
    name                =   "LessOrEqual",
    group               =   "Mathematics",
    inputs              =   ["in1", "in2"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/LessOrEqual.format"
)),
("Equal", CircuitInfo(
    name                =   "Equal",
    group               =   "Mathematics",
    inputs              =   ["in1", "in2"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/Equal.format"
)),

("Not", CircuitInfo(
    name                =   "NOT",
    group               =   "Mathematics",
    inputs              =   ["signal"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/NOT.format"
)),
("And", CircuitInfo(
    name                =   "AND",
    group               =   "Mathematics",
    inputs              =   ["in#Factors"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Factors", "IntLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    default_values      =   {"Factors": 2},
    script_format       =   "formats/AND.format"
)),
("Or", CircuitInfo(
    name                =   "OR",
    group               =   "Mathematics",
    inputs              =   ["in#Factors"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Factors", "IntLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    default_values      =   {"Factors": 2},
    script_format       =   "formats/OR.format"
)),
("XOr", CircuitInfo(
    name                =   "XOR",
    group               =   "Mathematics",
    inputs              =   ["in#Factors"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Factors", "IntLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    default_values      =   {"Factors": 2},
    script_format       =   "formats/XOR.format"
)),
("NOr", CircuitInfo(
    name                =   "NOR",
    group               =   "Mathematics",
    inputs              =   ["in#Factors"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Factors", "IntLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    default_values      =   {"Factors": 2},
    script_format       =   "formats/NOR.format"
)),

# SIGNAL GENERATION
("Waver", CircuitInfo(
    name                =   "waver",
    group               =   "Signal Generation",
    inputs              =   ["freq", "amp", "offset"],
    outputs             =   ["sin", "cos", "saw"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/waver.format"
)),
("Square", CircuitInfo(
    name                =   "square",
    group               =   "Signal Generation",
    inputs              =   ["freq", "amp", "offset", "duty"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/square.format"
)),

# SIGNAL PROCESSING
("SKLP", CircuitInfo(
    name                =   "SKLP",
    group               =   "Signal Processing",
    inputs              =   ["signal"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Gain", "IntLineEdit"),
                            ("Q", "FloatLineEdit"),
                            ("FCut", "IntLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/SKLP.format"
)),
("SKHP", CircuitInfo(
    name                =   "SKHP",
    group               =   "Signal Processing",
    inputs              =   ["signal"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Gain", "IntLineEdit"),
                            ("Q", "FloatLineEdit"),
                            ("FCut", "IntLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/SKHP.format"
)),
("SKBP", CircuitInfo(
    name                =   "SKBP",
    group               =   "Signal Processing",
    inputs              =   ["signal"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Gain", "IntLineEdit"),
                            ("FCut", "IntLineEdit"),
                            ("Band", "IntLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/SKBP.format"
)),
("RCLP", CircuitInfo(
    name                =   "RCLP",
    group               =   "Signal Processing",
    inputs              =   ["signal"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("FCut", "IntLineEdit"),
                            ("Order", "IntLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/RCLP.format"
)),
("RCHP", CircuitInfo(
    name                =   "RCHP",
    group               =   "Signal Processing",
    inputs              =   ["signal"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("FCut", "IntLineEdit"),
                            ("Order", "IntLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/RCHP.format"
)),

("Avg", CircuitInfo(
    name                =   "avg",
    group               =   "Signal Processing",
    inputs              =   ["signal"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Time", "FloatLineEdit"),
                            ("Moving", "CheckBox"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/avg.format"
)),

("Gain", CircuitInfo(
    name                =   "gain",
    group               =   "Signal Processing",
    inputs              =   ["signal"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Gain", "FloatLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/gain.format"
)),
("Min Max", CircuitInfo(
    name                =   "minmax",
    group               =   "Signal Processing",
    inputs              =   ["signal"],
    outputs             =   ["max", "min", "amp", "offset"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("CheckTime", "FloatLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/minmax.format"
)),
("Limiter", CircuitInfo(
    name                =   "limiter",
    group               =   "Signal Processing",
    inputs              =   ["signal", "min", "max"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/limiter.format"
)),
("Derivative", CircuitInfo(
    name                =   "derivative",
    group               =   "Signal Processing",
    inputs              =   ["signal"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/derivative.format"
)),
("Integral", CircuitInfo(
    name                =   "integral",
    group               =   "Signal Processing",
    inputs              =   ["signal"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/integral.format"
)),
("Delay", CircuitInfo(
    name                =   "delay",
    group               =   "Signal Processing",
    inputs              =   ["signal"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("DelayTime", "IntLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/delay.format"
)),
("Peaker", CircuitInfo(
    name                =   "peaker",
    group               =   "Signal Processing",
    inputs              =   ["signal"],
    outputs             =   ["tick", "peak", "delay"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Up", "CheckBox"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/peaker.format"
)),
("Phasor", CircuitInfo(
    name                =   "phasor",
    group               =   "Signal Processing",
    inputs              =   ["in1", "in2"],
    outputs             =   ["tick", "delay"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/phasor.format"
)),
("Flip", CircuitInfo(
    name                =   "flip",
    group               =   "Signal Processing",
    inputs              =   ["signal"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/flip.format"
)),

# SIGNAL CONTROL
("PI", CircuitInfo(
    name                =   "PI",
    group               =   "Signal Control",
    inputs              =   ["signal", "set", "Ki", "Kp"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/PI.format"
)),
("PID", CircuitInfo(
    name                =   "PID",
    group               =   "Signal Control",
    inputs              =   ["signal", "set", "Kd", "Ki", "Kp"],
    outputs             =   ["out"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/PID.format"
)),

# OUTPUT
("Output", CircuitInfo(
    name                =   "output",
    group               =   "Output",
    inputs              =   ["record"],
    outputs             =   [],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("File", "FileLineEdit"),
                            ("Dump", "IntLineEdit"),
                            ("Register", "RegisterDialog"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/output.format"
)),

# FLIP-FLOPS
("SR Flip Flop", CircuitInfo(
    name                =   "SRFlipFlop",
    group               =   "Flip-Flops",
    inputs              =   ["S", "R", "clock"],
    outputs             =   ["Q", "Qbar"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/SRFlipFlop.format"
)),
("JK Flip Flop", CircuitInfo(
    name                =   "JKFlipFlop",
    group               =   "Flip-Flops",
    inputs              =   ["J", "K", "clock"],
    outputs             =   ["Q", "Qbar"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/JKFlipFlop.format"
)),
("D Flip Flop", CircuitInfo(
    name                =   "DFlipFlop",
    group               =   "Flip-Flops",
    inputs              =   ["D", "clock"],
    outputs             =   ["Q", "Qbar"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/DFlipFlop.format"
)),
("DR Flip Flop", CircuitInfo(
    name                =   "DRFlipFlop",
    group               =   "Flip-Flops",
    inputs              =   ["D", "R", "clock"],
    outputs             =   ["Q", "Qbar"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/DRFlipFlop.format"
)),

# CUSTOM
("aPLL", CircuitInfo(
    name                =   "aPLL",
    group               =   "Custom",
    inputs              =   ["signal1", "signal2", "f0"],
    outputs             =   ["sin", "cos", "df", "dbg"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Filters", "TripleIntLineEdit"),
                            ("Kp", "FloatLineEdit"),
                            ("Ki", "FloatLineEdit"),
                            ("Gain", "FloatLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/aPLL.format"
)),
("dPFD", CircuitInfo(
    name                =   "dPFD",
    group               =   "Custom",
    inputs              =   ["ref", "vco", "f0", "KI", "KP"],
    outputs             =   ["sin", "cos", "df", "dbg"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Gain", "FloatLineEdit"),
                            ("Fcut", "IntLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/dPFD.format"
)),
("aAMPD", CircuitInfo(
    name                =   "aAMPD",
    group               =   "Custom",
    inputs              =   ["signal"],
    outputs             =   ["amp", "norm"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Fcut", "IntLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/aAMPD.format"
)),

# CANTILEVER
("Simple Cantilever", CircuitInfo(
    name                =   "SiCanti",
    group               =   "Cantilever",
    inputs              =   ["holderz", "fz", "exciter"],
    outputs             =   ["ztip", "zabs", "vz"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("StartingZ", "FloatLineEdit"),
                            ("Q", "FloatLineEdit"),
                            ("k", "FloatLineEdit"),
                            ("f0", "FloatLineEdit"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/simple_canti.format"
)),
("Advanced Cantilever", CircuitInfo(
    name                =   "AdCanti",
    group               =   "Cantilever",
    inputs              =   ["exciterz", "excitery", "Holderx",
                            "Holdery", "Holderz", "ForceV", "ForceL"],
    outputs             =   ["zPos", "yPos", "xABS", "yABS", "zABS",
                            "vV#NumberOfModesV", "vL#NumberOfModesL",
                            "yL#NumberOfModesL", "zV#NumberOfModesV"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("NumberOfModesV", "IntLineEdit"),
                            ("NumberOfModesL", "IntLineEdit"),
                            ("StartingPos", "TripleFloatLineEdit"),
                            ("Modes", "ModeSetup"),
                            ("Pushed", "CheckBox")
                            ]),
    default_values      =   {"NumberOfModesV": 1, "NumberOfModesL": 1},
    script_format       =   "formats/advanced_canti.format"
)),

# INTERPOLATION
("1d Linear Interpolation", CircuitInfo(
    name                =   "i1Dlin",
    group               =   "Interpolation",
    inputs              =   ["x"],
    outputs             =   ["F#Components"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Components", "IntLineEdit"),
                            ("Step", "FloatLineEdit"),
                            ("Data", "LineEdit"),
                            ("PBC", "CheckBox"),
                            ("Pushed", "CheckBox")
                            ]),
    default_values      =   {"Components": 1},
    script_format       =   "formats/i1Dlin.format"
)),
("3d Linear Interpolation", CircuitInfo(
    name                =   "i3Dlin",
    group               =   "Interpolation",
    inputs              =   ["x", "y", "z"],
    outputs             =   ["F#Components"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Components","IntLineEdit"),
                            ("Steps", "TripleFloatLineEdit"),
                            ("Npoints", "TripleIntLineEdit"),
                            ("PBC", "TripleBoolLineEdit"),
                            ("Force Multiplier", "FloatLineEdit"),
                            ("Data", "FileDialog"),
                            ("Pushed", "CheckBox")
                            ]),
    default_values      =   {"Components": 3},
    script_format       =   "formats/i3Dlin.format"
)),
("4d Linear Interpolation", CircuitInfo(
    name                =   "i4Dlin",
    group               =   "Interpolation",
    inputs              =   ["x", "y", "z", "V"],
    outputs             =   ["F#Components"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Components","IntLineEdit"),
                            ("BiasStep", "FloatLineEdit"),
                            ("StartingV", "FloatLineEdit"),
                            ("PBC", "FourBoolLineEdit"),
                            ("VASP Data", "FileDialog"),
                            ("Pushed", "CheckBox")
                            ]),
    default_values      =   {"Components": 1},
    script_format       =   "formats/i4Dlin.format"
)),

# SCANNER
("Scanner", CircuitInfo(
    name                =   "Scanner",
    group               =   "Scanner",
    inputs              =   [],
    outputs             =   ["x", "y", "z", "record"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Resolution", "DoubleIntLineEdit"),
                            ("ImageArea", "DoubleFloatLineEdit"),
                            ("Recorder", "RecorderSelect"),
                            ("BlankLines", "CheckBox"),
                            ("Pushed", "CheckBox")
                            ]),
    script_format       =   "formats/scanner.format"
)),

# VAN DER WAALS
("Van der Waals Force", CircuitInfo(
    name                =   "VDW",
    group               =   "Van der Waals",
    inputs              =   ["ztip"],
    outputs             =   ["fz"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("Alpha", "FloatLineEdit"),
                            ("Hamaker", "FloatLineEdit"),
                            ("Radius", "FloatLineEdit"),
                            ("Offset", "FloatLineEdit"),
                            ("Pushed", "CheckBox"),
                            ]),
    script_format       =   "formats/VDW.format"
)),
("VDWtorn", CircuitInfo(
    name                =   "VDWtorn",
    group               =   "Van der Waals",
    inputs              =   ["ztip"],
    outputs             =   ["fz"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("A1", "FloatLineEdit"),
                            ("A2", "FloatLineEdit"),
                            ("A3", "FloatLineEdit"),
                            ("A4", "FloatLineEdit"),
                            ("A5", "FloatLineEdit"),
                            ("A6", "FloatLineEdit"),
                            ("Tip Offset", "FloatLineEdit"),
                            ("Pushed", "CheckBox"),
                            ]),
    script_format       =   "formats/VDWtorn.format"
)),

# SCANNING TUNNELING MICROSCOPE
("STM", CircuitInfo(
    name                =   "STM",
    group               =   "Scanning Tunneling Microscope",
    inputs              =   ["Density"],
    outputs             =   ["Current"],
    param_window_style  =   OrderedDict([
                            ("Name", "NameLineEdit"),
                            ("WorkFunction", "FloatLineEdit"),
                            ("WaveFunctionOverlap", "FloatLineEdit"),
                            ("Pushed", "CheckBox"),
                            ]),
    default_values      =   {"WorkFunction": 4, "WaveFunctionOverlap": 2},
    script_format       =   "formats/STM.format"
))
])

# Header text for scripts
blocks = [
"""'Block 0'
'Imports and machine setup'
""",
"""'Block 1'
'Initialisation of circuits and basic setup'
""",
"""'Block 2'
'Connections'
""",
"""'Block 3'
'Additional setup'
""",
"""'Block 4'
'Runtime operations'
"""]
