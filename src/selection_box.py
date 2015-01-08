from PyQt4 import QtGui, QtCore


class SelectionBox(QtGui.QGraphicsItem):
    """Rubberband selection box."""

    def __init__(self, origin, parent=None, scene=None):
        super(SelectionBox, self).__init__(parent, scene)
        self.setPos(origin)
        self.setZValue(2)
        self.origin = origin
        self.corner = origin

    def setCorner(self, corner):
        """Set the corner to the new value. Signal the geometry change."""
        self.prepareGeometryChange()
        self.corner = corner

    def selectionArea(self):
        """Return the area under the box in scene coordinates."""
        return self.mapToScene(self.boundingRect())

    def boundingRect(self):
        """Return the bounding rectangle of the box in item coordinates.
        Make sure that width and height are positive."""
        w = self.corner.x() - self.origin.x()
        h = self.corner.y() - self.origin.y()
        x = min(0, w)
        y = min(0, h)
        return QtCore.QRectF(x, y, abs(w), abs(h))

    def paint(self, painter, options, widget):
        """Paint the box."""
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        painter.setPen(pen)
        painter.setBrush(QtGui.QColor(200, 200, 200))
        painter.setOpacity(0.4)
        painter.drawRect(self.boundingRect())
