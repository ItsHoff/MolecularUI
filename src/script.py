#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Jun 23, 2014

@author: keisano1

Module that handles the script creation.

The script will be first saved as a list of strings
and the file creation is handled by the main window.
The blocks will be written in in order but content inside
the blocks can be in any order.

The format:
    Delimiters:
    !               at the start of the line followed by number 0-4 to define the
                    block in which the following lines will be written.
    %Parameter%     to signal a parameter, these will be replaced by the corresponding
                    values from parameters dictionary and as such must match the
                    names given in param_window_format.
                    example: %Name%
    $Statement$     to signal an optional parameter, anything inside these will not
                    be written if the parameter is missing. These should be used
                    to enclose the parameter name in addition to the value so that
                    they're not mistakingly added when the parameter is not set.
                    example: $parameter = '%Parameter%'$
    £Line£          to signal optional line, these lines will not be written
                    if no OPTIONAL parameters (defined by $$) are contained inside.
                    example: £%name%.Configure($parameter = %Parameter%$)£

    Wildcard statements:
    INPUTS          is used to define where all input values of the circuit
                    are written. Needs to be added inside optional and
                    parameter delimiters ($%INPUTS%$).
                    example: machine.AddCircuit(type='Example', name = '%Name%', $%INPUTS%$)
"""

# TODO: Handle invalid formats


def createFromFormat(blocks, format_file, parameters):
    """Clean format_file lines and insert the right parameters.
    After cleaning append the line to the right block.
    """
    f = format_file
    block = -1
    for line in f:
        # set the current block
        if line.startswith('!'):
            # TODO: handle not setting a block
            block = int(line[1])
        else:
            if block == -1:
                raise SyntaxError("Block is not set on %s." % f.name)
            elif line.startswith('£'):
                if containsSetOptionalParameters(line, parameters):
                    clean_line = createCleanLine(line, parameters)
                    blocks[block] += clean_line
            elif containsParameters(line):
                clean_line = createCleanLine(line, parameters)
                blocks[block] += clean_line
            else:
                blocks[block] += line


def createCleanLine(line, parameters):
    """Clean the line from extra formatting characters and
    insert the right parameters. Then return the clean line.
    if circuit.circuit_info.type
    """
    if containsInputs(line):
        line = addInputs(line, parameters)
    if getOptionalParameters(line):
        line = cleanOptionalBlocks(line, parameters)
    for label, value in parameters.iteritems():
        replaced = '%'+label+'%'
        line = line.replace(str(replaced), str(value))
    line = line.replace('£', '')
    line = line.replace('$', '')
    return line


def addInputs(string, parameters):
    """Add manually set inputs into the string."""
    start = string.find("INPUTS")
    insert = start - 2
    for key in parameters.keys():
        if key.startswith("INPUT"):
            name = key.split(":")[-1]
            input_string = "$"+name+"="+"%"+key+"%$, "
            string = string[:insert] + input_string + string[insert:]
    return string


def cleanOptionalBlocks(string, parameters):
    """Remove all the optional blocks that have unset parameters.
    Return the line after the removals."""
    blocks = []
    start = string.find('$') + 1
    i = start-1
    while start:
        end = string.find('$', start)
        if containsSetParameters(string[start:end], parameters):
            blocks.append(string[start:end])
        start = string.find('$', end+1) + 1
    string = string.replace(string[i:end+1], '')
    if len(blocks) < 1:
        rcomma = string.rfind(',')
        string = string[:rcomma] + string[rcomma+1:]
    for block in blocks:
        rbracket = string.find(')')
        if block == blocks[0]:
            string = string[:rbracket] + block + string[rbracket:]
        else:
            string = string[:rbracket] + ", " + block + string[rbracket:]
    return string


def containsParameters(string):
    """Return True if string contains parameters and False otherwise."""
    start = string.find('%')
    end = string.find('%', start+1)
    if start != -1 and end != -1:
        return True
    else:
        return False


def containsSetParameters(string, parameters):
    """Return True if string contains parameters given in parameters
    dictionary otherwise return False.
    """
    for parameter in getParameters(string):
        if parameter in parameters:
            return True
    return False


def containsSetOptionalParameters(string, parameters):
    """Return True if string contains optional parameters that
    have been given in parameters.
    """
    for parameter in getOptionalParameters(string):
        if parameter in parameters:
            return True
    return False


def containsInputs(string):
    """Return whether string takes input values or not."""
    found = string.find("INPUTS")
    if found != -1:
        return True
    else:
        return False


def getParameters(string):
    """Find all parameters in the string.
    Return list of found parameters.
    """
    parameters = []
    start = string.find('%') + 1
    while start:
        end = string.find('%', start)
        parameters.append(string[start:end])
        start = string.find('%', end + 1) + 1
    return parameters


def getOptionalParameters(string):
    """Find all optional parameters in the string.
    Return list of the found optional parameters.
    """
    parameters = []
    start_opt = string.find('$') + 1
    while start_opt:
        end_opt = string.find('$', start_opt)
        start = string.find('%', start_opt, end_opt) + 1
        end = string.rfind('%', start_opt, end_opt+1)
        parameters.append(string[start:end])
        start_opt = string.find('$', end_opt) + 1
    return parameters
