'''
Created on Jun 16, 2014

@author: keisano1
'''

from PyQt4 import QtGui, QtCore

SCROLL_DISTANCE = 50
SCROLL_SPEED = 20
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


class MachineView(QtGui.QGraphicsView):
    """Graphics view that is used to show the contents of the
    machine_widget scene.
    """

    def __init__(self):
        """Call super and set the default flags and parameters."""
        super(MachineView, self).__init__()
        self.setAcceptDrops(True)
        self.panning = False
        self.mouse_pos = None
        self.scale_factor = 1
        self.min_factor = 0.3
        self.max_factor = 2.5

        self.scroll_dir = None
        self.scroll_timer = QtCore.QTimer(self)
        self.scroll_timer.start(20)
        QtCore.QObject().connect(self.scroll_timer, QtCore.SIGNAL("timeout()"),
                                 self.scrollTimeOut)

        self.setRenderHint(QtGui.QPainter.Antialiasing, True)
        # self.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)

    def autoScroll(self, point):
        """Check if the point is close to an edge and set the scroll direction
        to that edge if it is.
        point = scene point
        """
        self.scroll_dir = None
        view_pos = self.mapFromScene(point)
        if view_pos.x() < SCROLL_DISTANCE:
            self.scroll_dir = LEFT
        elif self.width() - view_pos.x() < SCROLL_DISTANCE:
            self.scroll_dir = RIGHT
        elif view_pos.y() < SCROLL_DISTANCE:
            self.scroll_dir = UP
        elif self.height() - view_pos.y() < SCROLL_DISTANCE:
            self.scroll_dir = DOWN

    def scrollTimeOut(self):
        """Scroll the scene on scroll timer timeout if direction is set."""
        if self.scroll_dir == LEFT:
            scroll_bar = self.horizontalScrollBar()
            scroll_bar.setValue(scroll_bar.value() - SCROLL_SPEED)
        elif self.scroll_dir == RIGHT:
            scroll_bar = self.horizontalScrollBar()
            scroll_bar.setValue(scroll_bar.value() + SCROLL_SPEED)
        elif self.scroll_dir == UP:
            scroll_bar = self.verticalScrollBar()
            scroll_bar.setValue(scroll_bar.value() - SCROLL_SPEED)
        elif self.scroll_dir == DOWN:
            scroll_bar = self.verticalScrollBar()
            scroll_bar.setValue(scroll_bar.value() + SCROLL_SPEED)
        self.update()

    def wheelEvent(self, event):
        """Scale the view when wheel is scrolled."""
        self.setTransformationAnchor(self.AnchorUnderMouse)
        factor = 1 + 0.1* abs(event.delta()/120.0)
        if event.delta() < 0:
            factor = 1.0/factor
        if (self.scale_factor*factor > self.min_factor and
                self.scale_factor*factor < self.max_factor):
            self.scale_factor *= factor
            self.scale(factor, factor)

    def mousePressEvent(self, event):
        """Start panning the scene if middle mouse button is pressed."""
        super(MachineView, self).mousePressEvent(event)
        if (event.button() == QtCore.Qt.MiddleButton    or
               (event.button() == QtCore.Qt.LeftButton  and
                event.modifiers() & QtCore.Qt.ControlModifier)):
            self.panning = True
            self.mouse_pos = event.pos()

    def mouseReleaseEvent(self, event):
        """Stop panning if middle mouse button is released."""
        super(MachineView, self).mouseReleaseEvent(event)
        self.panning = False
        self.mouse_pos = None

    def mouseMoveEvent(self, event):
        """If user is panning, move the scene based on the
        movement of the mouse.
        """
        super(MachineView, self).mouseMoveEvent(event)
        if self.panning:
            diff = event.pos() - self.mouse_pos
            self.mouse_pos = event.pos()
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - diff.y())
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - diff.x())
            self.scene().update()
