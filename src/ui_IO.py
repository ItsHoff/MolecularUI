'''
Created on Jun 17, 2014

@author: keisano1
'''

from PyQt4 import QtGui, QtCore

from parameter_window import InputValueWindow


class UIIO(QtGui.QGraphicsItem):
    """Graphics item that represents the inputs and outputs of the machine."""

    def __init__(self, name, io_type, circuit):
        """Create a new input or output with a given name and type.
        Parent should be the circuit this io belongs to.
        io_type should be "in" for input and "out" for output.
        """
        super(UIIO, self).__init__(circuit)
        self.name = name
        self.circuit = circuit
        self.xsize = 16
        self.ysize = 16
        self.io_type = io_type
        self.value_window = None
        self.save_state = None

    def nConnections(self):
        """Check how many connections are connected to this io.
        This should be max. 1 for inputs.
        """
        n = 0
        for connection in self.scene().connections:
            if connection.input_ == self or connection.output == self:
                n += 1
        return n

    def addContextActions(self, menu):
        """Add input and output specific context actions into the menu."""
        remove = QtGui.QAction("Remove all connections from "+self.name, menu)
        QtCore.QObject.connect(remove, QtCore.SIGNAL("triggered()"),
                               self.removeConnections)

        menu.addAction(remove)

    def removeConnections(self):
        """Call the scene to remove all the connections connected
        to this io."""
        self.scene().removeConnectionsFrom(self)

    def getSaveState(self):
        """Return the current state of the io without the Qt bindings
        for saving.
        """
        if self.save_state is None:
            self.save_state = SaveIO(self)
        else:
            self.save_state.update(self)
        return self.save_state

    def boundingRect(self):
        """Return the bounding rectangle of the io.
        Defines where all the painting takes place.
        Required by the scene.
        """
        x_border = 50
        y_border = 10
        return QtCore.QRectF(-x_border, -y_border,
                             self.xsize + x_border, self.ysize + y_border)

    def shape(self):
        """Return the shape of the io. Used for collision detection."""
        shape = QtGui.QPainterPath()
        shape.addRect(0, 0, self.xsize, self.ysize)
        return shape

    def paint(self, painter, options, widget):
        """Paint the io and add the name text."""
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        pen.setWidthF(1.25)
        painter.setPen(pen)
        painter.setFont(QtGui.QFont("", 6))
        if self.io_type == "in":
            painter.setBrush(QtGui.QColor(12, 169, 255))
        else:
            painter.setBrush(QtGui.QColor(255, 62, 66))
        painter.drawRect(0, 0, self.xsize, self.ysize)
        if self.io_type == "in":
            rect = QtCore.QRect(0, 0, 35, 10)
            rect.moveBottomRight(self.shape().boundingRect().topLeft().toPoint())
            rect.moveRight(rect.right()-2)
            # painter.drawText(-self.xsize-4, -1, self.name)
            painter.drawText(rect, QtCore.Qt.AlignRight, self.name)
        else:
            rect = QtCore.QRect(0, 0, 35, 10)
            rect.moveBottomLeft(self.shape().boundingRect().topRight().toPoint())
            rect.moveLeft(rect.left()+2)
            painter.drawText(rect, QtCore.Qt.AlignLeft, self.name)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawPoint(0.5*self.xsize, 0.5*self.ysize)

    def mousePressEvent(self, event):
        """When mouse is pressed try to create create a new connection
        or connect a incomplete connection.
        """
        # We need to check that event position in contained inside the io
        # since otherwise opening a context menu on the io will send the
        # following two clicks to the io as well disregarding the click
        # position.
        status_bar = self.scene().parent().window().statusBar()
        if (event.button() == QtCore.Qt.LeftButton and
           self.contains(event.pos())):
            if self.scene().new_connection is None:
                self.scene().createNewConnection(self, event.scenePos())
            else:
                if self.scene().new_connection.addIO(self):
                    self.scene().addConnection()
                else:
                    self.scene().deleteNewConnection()
                    status_bar.showMessage("Connection failed", 3000)

    def mouseDoubleClickEvent(self, event):
        """Open a window for setting constant value if io is input."""
        self.scene().deleteNewConnection()
        if self.value_window is not None:
            self.value_window.showWindow()
        elif self.io_type == "in":
            self.value_window = InputValueWindow(self)
            self.value_window.showWindow()


class SaveIO(object):
    """Container for UIIO state without Qt bindings. Used for saving."""

    def __init__(self, io):
        self.name = io.name
        self.io_type = io.io_type
        self.loaded_item = None         # Do not set this before saving

    def update(self, io):
        """Update the save state to match current machine state."""
        self.__init__(io)
