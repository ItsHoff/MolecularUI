'''
Created on Jun 18, 2014

@author: keisano1
'''

from PyQt4 import QtGui, QtCore


class UIConnection(QtGui.QGraphicsPathItem):
    """Graphics item that represents the connections of the machine."""

    def __init__(self, origin, mouse_pos, parent=None):
        """Create a new connection starting from input or output origin and
        ending at mouse_pos. Will give ValueError if trying to connect
        allready connected input.
        """
        self.input_ = None
        self.output = None
        self.save_state = None
        self.start = origin.scenePos()+QtCore.QPointF(0.5*origin.xsize,
                                                      0.5*origin.ysize)
        self.end = mouse_pos
        # Check if were trying to connect an input thats allready connected.
        if origin.io_type == "in":
            if origin.nConnections() >= 1:
                raise ValueError("Input can only have one connection!")
            else:
                self.input_ = origin
        else:
            self.output = origin
        super(UIConnection, self).__init__(parent)
        # pen = QtGui.QPen(QtGui.QColor(251, 182, 1))
        # pen = QtGui.QPen(QtGui.QColor(203, 107, 0))
        # pen = QtGui.QPen(QtGui.QColor(203, 75, 22))
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        pen.setWidth(2)
        self.setPen(pen)
        path = QtGui.QPainterPath(self.start)
        path.lineTo(self.end)
        self.setPath(path)
        # set Z value to guarantee that connection will be drawn on top.
        self.setZValue(3)

    def addContextActions(self, menu):
        """Add connection specific context actions to the menu."""
        remove = QtGui.QAction("Remove connection from " + self.input_.name +
                               " to " + self.output.name, menu)
        QtCore.QObject.connect(remove, QtCore.SIGNAL("triggered()"),
                               self.removeConnection)

        menu.addAction(remove)

    def removeConnection(self):
        """Call the scene to remove the connection."""
        self.scene().removeConnection(self)

    def addIO(self, io):
        """Add an ending point to the connection. Check that the io is
        correct type (output if input is allready set and vice versa) and
        that input isn't allready connected.
        Return True if adding was succesfull and False if it failed.
        """
        if io.io_type == "in" and self.input_ is None and io.nConnections() < 1:
            self.input_ = io
        elif io.io_type == "out" and self.output is None:
            self.output = io
        else:
            return False
        self.updatePath()
        return True

    def getSaveState(self):
        """Return the current state of the connection without the Qt bindings
        for saving.
        """
        if self.save_state is None:
            self.save_state = SaveConnection(self)
        else:
            self.save_state.update(self)
        return self.save_state

    def loadSaveState(self, save_state):
        """Load the state given in save_state."""
        save_state.loaded_item = self
        self.save_state = save_state
        self.input_ = save_state.input_.loaded_item
        self.output = save_state.output.loaded_item
        self.updatePath()

    def updateMousePos(self, scenePos):
        """Update the end point of the circuit to position given by scenePos.
        Used before connection is properly connected to make the connection
        follow the mouse.
        """
        self.end = scenePos
        path = QtGui.QPainterPath(self.start)
        path.lineTo(self.end)
        self.setPath(path)

    def updatePath(self):
        """Updates the path from input to output.
        Currently just draws a line from the center of the input
        to the center of the output.
        """
        self.start = self.input_.scenePos()+QtCore.QPointF(0.5*self.input_.xsize,
                                                           0.5*self.input_.ysize)
        self.end = self.output.scenePos()+QtCore.QPointF(0.5*self.output.xsize,
                                                         0.5*self.output.ysize)
        path = QtGui.QPainterPath(self.start)
        path.lineTo(self.end)
        self.setPath(path)


class SaveConnection(object):
    """Container for UIConnection state without Qt bindings. Used for saving."""

    def __init__(self, connection):
        self.input_ = connection.input_.save_state
        self.output = connection.output.save_state
        self.loaded_item = None         # Do not set this before saving

    def update(self, connection):
        """Update the save state to match current state."""
        self.__init__(connection)
