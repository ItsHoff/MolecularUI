from PyQt4.QtCore import QRegExp

from parameter_completion_model import ParameterCompletionModel

XTWO = "((%s),\s?)(%s)"
XTHREE = "((%s),\s?){2}(%s)"
XFOUR = "((%s),\s?){3}(%s)"
XFIVE = "((%s),\s?){4}(%s)"
BOOL_REGEXP = "T?r?u?e?|F?a?l?s?e?"
TRIPLE_BOOL_REGEXP = XTHREE % (BOOL_REGEXP, BOOL_REGEXP)
FOUR_BOOL_REGEXP = XFOUR % (BOOL_REGEXP, BOOL_REGEXP)
FLOAT_REGEXP = "[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?"
DOUBLE_FLOAT_REGEXP = XTWO % (FLOAT_REGEXP, FLOAT_REGEXP)
TRIPLE_FLOAT_REGEXP = XTHREE % (FLOAT_REGEXP, FLOAT_REGEXP)
DIM_REGEXP = "[x-z]?=[0-9.]*"
TRIPLE_DIM_REGEXP = XTHREE % (DIM_REGEXP, DIM_REGEXP)
INT_REGEXP = "[0-9]+"
DOUBLE_INT_REGEXP = XTWO % (INT_REGEXP, INT_REGEXP)
TRIPLE_INT_REGEXP = XTHREE % (INT_REGEXP, INT_REGEXP)
BIT_REGEXP = "1|0"
NAME_REGEXP = "[\d\w]+"
FILE_REGEXP = "[\d\w\./]+"
MOVE_BASE = "[x-zv]?=[+-]?[0-9.]*"
MOVE_REGEXP = XFOUR % (MOVE_BASE, MOVE_BASE)
MOVE_RECORD_BASE = "([x-zv]|p?o?i?n?t?s?)?=[+-]?[0-9.]*"
MOVE_RECORD_REGEXP = XFIVE % (MOVE_RECORD_BASE, MOVE_RECORD_BASE)
# MODE_SETUP_BASE = "V?e?r?t?i?c?a?l?=(%s)?|(([kQM]|f?0?)?=[0-9.]*)" % BOOL_REGEXP
MODE_SETUP_BASE = "([kQM]|f?0?)?=[0-9.]*"
MODE_SETUP_REGEXP = XFOUR % (MODE_SETUP_BASE, MODE_SETUP_BASE)


DIMENSION_LIST = ["x=", "y=", "z="]
BOOL_LIST = ["True", "False"]
MOVE_LIST = DIMENSION_LIST + ["v="]
MOVE_RECORD_LIST = MOVE_LIST + ["points="]
# MODE_SETUP_LIST = ["Vertical=", "k=", "Q=", "M=", "f0="]
MODE_SETUP_LIST = ["k=", "Q=", "M=", "f0="]

line_edits = {
    "LineEdit":{
        "CompletionModel"   : None,
        "RegExp"            : None,
        "PlaceholderText"   : ""
    },
    "NameLineEdit":{
        "CompletionModel"   : None,
        "RegExp"            : QRegExp(NAME_REGEXP),
        "PlaceholderText"   : "string"
    },
    "FileLineEdit":{
        "CompletionModel"   : None,
        "RegExp"            : QRegExp(FILE_REGEXP),
        "PlaceholderText"   : "filename"
    },
    "BitLineEdit":{
        "CompletionModel"   : None,
        "RegExp"            : QRegExp(BIT_REGEXP),
        "PlaceholderText"   : "1|0"
    },
    "ThreeDimensionLineEdit":{
        "CompletionModel"   : ParameterCompletionModel(DIMENSION_LIST),
        "RegExp"            : QRegExp(TRIPLE_DIM_REGEXP),
        "PlaceholderText"   : "x=float, y=float, z=float"
    },
    "TripleBoolLineEdit":{
        "CompletionModel"   : ParameterCompletionModel(BOOL_LIST),
        "RegExp"            : QRegExp(TRIPLE_BOOL_REGEXP),
        "PlaceholderText"   : "bool, bool, bool"
    },
    "FourBoolLineEdit":{
        "CompletionModel"   : ParameterCompletionModel(BOOL_LIST),
        "RegExp"            : QRegExp(FOUR_BOOL_REGEXP),
        "PlaceholderText"   : "bool, bool, bool, bool"
    },
    "IntLineEdit":{
        "CompletionModel"   : None,
        "RegExp"            : QRegExp(INT_REGEXP),
        "PlaceholderText"   : "int"
    },
    "DoubleIntLineEdit":{
        "CompletionModel"   : None,
        "RegExp"            : QRegExp(DOUBLE_INT_REGEXP),
        "PlaceholderText"   : "int, int"
    },
    "TripleIntLineEdit":{
        "CompletionModel"   : None,
        "RegExp"            : QRegExp(TRIPLE_INT_REGEXP),
        "PlaceholderText"   : "int, int, int"
    },
    "FloatLineEdit":{
        "CompletionModel"   : None,
        "RegExp"            : QRegExp(FLOAT_REGEXP),
        "PlaceholderText"   : "float"
    },
    "DoubleFloatLineEdit":{
        "CompletionModel"   : None,
        "RegExp"            : QRegExp(DOUBLE_FLOAT_REGEXP),
        "PlaceholderText"   : "float, float"
    },
    "TripleFloatLineEdit":{
        "CompletionModel"   : None,
        "RegExp"            : QRegExp(TRIPLE_FLOAT_REGEXP),
        "PlaceholderText"   : "float, float, float"
    },
    "MoveLineEdit":{
        "CompletionModel"   : ParameterCompletionModel(MOVE_LIST),
        "RegExp"            : QRegExp(MOVE_REGEXP),
        "PlaceholderText"   : "x=float, y=float, z=float, v=float"
    },
    "MoveRecordLineEdit":{
        "CompletionModel"   : ParameterCompletionModel(MOVE_RECORD_LIST),
        "RegExp"            : QRegExp(MOVE_RECORD_REGEXP),
        "PlaceholderText"   : "x=float, y=float, z=float, v=float, points=int"
    },
    "ModeSetupLineEdit":{
        "CompletionModel"   : ParameterCompletionModel(MODE_SETUP_LIST),
        "RegExp"            : QRegExp(MODE_SETUP_REGEXP),
        # "PlaceholderText"   : "Vertical=bool, k=float, Q=float, M=float, f0=float"
        "PlaceholderText"   : "k=float, Q=float, M=float, f0=float"
    },
}
