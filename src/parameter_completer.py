"""Module containing the ParameterCompleter."""

from PyQt4 import QtGui, QtCore


class ParameterCompleter(QtGui.QCompleter):
    """Completer to match ',' separated string with a tree model of strings."""

    def __init__(self):
        super(ParameterCompleter, self).__init__()

    def splitPath(self, path):
        """Split the path to list of its components."""
        split = path.split(',')
        # Strip the individual items of white space and
        # values given after '=' sign.
        for item in split:
            item_index = split.index(item)
            item = item.strip()
            eq_index = item.find('=')
            if eq_index != -1:
                item = item[:eq_index+1]
            split[item_index] = item
        return split

    def pathFromIndex(self, index):
        """Return the text that is inserted when the item given by index
        is selected."""
        prefix = self.completionPrefix()
        prefix_split = prefix.split(",")
        # If an item is a substring of index data the replace it with
        # the index data.
        for item in prefix_split:
            if item.lstrip() in index.data():
                i = prefix_split.index(item)
                prefix_split[i] = prefix_split[i].replace(item.lstrip(), "")
                prefix_split[i] += index.data()
        prefix = ",".join(prefix_split)
        return prefix

    def getRecievers(self, signal):
        """Return the number of recievers for the given signal."""
        return self.receivers(QtCore.SIGNAL(signal))
