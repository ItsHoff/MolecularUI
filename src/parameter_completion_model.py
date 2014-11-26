"""Module containing the ParameterCompletionModel."""

from PyQt4 import QtCore


class ParameterCompletionModel(QtCore.QAbstractItemModel):
    """Tree based completion model that takes a list of strings and
    gives an infinite list of completions based on that list. Model will
    allways set the parent to the last of the current completions such that
    next item will allways be offered first."""

    def __init__(self, completion_list):
        super(ParameterCompletionModel, self).__init__()
        self.completion_table = [completion_list]

    def index(self, row, column, parent=QtCore.QModelIndex()):
        """Return the ModelIndex object matching the given parameters.
        If no match is found, return invalid ModelIndex."""
        # print "index"
        # print "parent: " + self.printIndex(parent)
        # print "column: %d, row: %d" % (column, row)
        # print "table: " + str(self.completion_table)
        if column != 0:
            return QtCore.QModelIndex()
        else:
            column = self.getColumn(parent) + 1
            self.updateTable(row, column, parent)
            index = self.createIndex(row, column)
            # print "index: " + self.printIndex(index)
            return index

    def updateTable(self, row, column, parent):
        """Update the completion table such that the parent is at
        the bottom of the current column while preserving the order.
        """
        if len(self.completion_table) == column:
            row_count = self.rowCount(parent)
            self.completion_table.append([None]*row_count)
            parent_column = self.completion_table[column-1]
            for i in range(row_count):
                item_index = (parent.row()+i+1) % row_count
                self.completion_table[column][i] = parent_column[item_index]
        elif len(self.completion_table) < column:
            print "Something went wrong: Length is smaller than index"
        elif parent.isValid():
            row_count = self.rowCount(parent)
            parent_column = self.completion_table[column-1]
            for i in range(row_count):
                item_index = (parent.row()+i+1) % row_count
                self.completion_table[column][i] = parent_column[item_index]

    def getColumn(self, index):
        """Get the column for the given index."""
        column = -1
        # Get the value of the valid parent indexes which is equal to the
        # column value of the index.
        while index.isValid():
            column += 1
            index = index.parent()
        return column

    def printIndex(self, index):
        return "column: %d, row:%d, data:%s" % (index.column(), index.row(),
                                                index.data())

    def parent(self, index):
        """Return the parent index of the given index."""
        # Parent is the item in the previous column whose data matches
        # the data of this columns last item.
        column = index.column()
        if column == 0:
            return QtCore.QModelIndex()
        parent_data = self.completion_table[column][-1]
        parent_row = self.completion_table[column-1].index(parent_data)
        return self.createIndex(parent_row, column-1)

    def data(self, index, role):
        """Return the date with the given row matching the index."""
        if index.isValid():
            if role == QtCore.Qt.EditRole or role == QtCore.Qt.DisplayRole:
                return self.completion_table[index.column()][index.row()]

    def rowCount(self, parent=QtCore.QModelIndex()):
        """Return the row count of the submodel with given parent."""
        # All rows are equal length so we can return the length of the
        # first one.
        return len(self.completion_table[0])

    def columnCount(self, parent=QtCore.QModelIndex()):
        """Return the column count of the submodel with given parent."""
        return 1


def test():
    """Small test for the basic functionality."""
    test_list = ["a", "b", "c"]
    model = ParameterCompletionModel(test_list)
    index = model.index(0, 0)
    child_index = model.index(0, 0, index)
    child_child = model.index(0, 0, child_index)
    new_child = model.index(1, 0, index)
    print model.completion_table
    new_index = model.index(1, 0)
    print model.completion_table
    new_child_child = model.index(1, 0, new_child)
    print model.completion_table


if __name__ == '__main__':
    test()
