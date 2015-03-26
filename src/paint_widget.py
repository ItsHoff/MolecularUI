from PyQt4 import QtGui, QtCore

sheets = ["* {background: rgb(255, 0, 0);}",
          "* {background: rgb(255, 255, 0);}",
          "* {background: rgb(0, 255, 0);}",
          "* {background: rgb(0, 255, 255);}",
          "* {background: rgb(0, 0, 255);}"]

class PaintWidget(QtGui.QWidget):

    def __init__(self, parent):
        super(PaintWidget, self).__init__(parent)
        self.layout = QtGui.QHBoxLayout()
        self.button_group = QtGui.QButtonGroup()
        self.button_group.setExclusive(True)
        self.tool_bar = QtGui.QToolBar(self)
        for i in range(5):
            widget = PaintWidgetAction(i, self.button_group, self.tool_bar)
            self.tool_bar.addAction(widget)
        self.layout.addWidget(self.tool_bar)
        self.setLayout(self.layout)
        self.show()

    def updateLabels(self):
        for item in self.tool_bar.children():
            if isinstance(item, PaintSelector):
                item.updateLabel()

class PaintWidgetAction(QtGui.QWidgetAction):
    """Required to make tool_bar collapse properly."""

    def __init__(self, index, btn_grp, parent):
        super(PaintWidgetAction, self).__init__(parent)
        self.widget = PaintSelector(index, btn_grp)

    def createWidget(self, parent):
        """Return the widget thats added to parent. This has to be
        different for each parent widget.
        """
        if isinstance(parent, QtGui.QToolBar):
            self.widget.setParent(parent)
            return self.widget
        else:
            widget = PaintSelector(self.widget.index, self.widget.button_group)
            widget.setParent(parent)
            return widget

class PaintSelector(QtGui.QWidget):

    def __init__(self, index, btn_grp):
        super(PaintSelector, self).__init__()
        self.index = index
        self.button_group = btn_grp
        self.button = QtGui.QPushButton(str(self.index+1))
        self.button.setStyleSheet(sheets[self.index])
        self.button.setCheckable(True)
        if index == 0:
            self.button.setChecked(True)
        btn_grp.addButton(self.button)
        self.label = QtGui.QLineEdit()
        self.label.setMinimumWidth(30)
        self.button.setMinimumWidth(30)
        self.setMaximumHeight(60)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        layout = QtGui.QVBoxLayout()
        layout.setSpacing(1)
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        layout.setAlignment(self.button, QtCore.Qt.AlignCenter)
        self.setLayout(layout)
        self.connect(self.label, QtCore.SIGNAL("editingFinished()"),
                     self.updateLayerAtomType)
        self.connect(self.button, QtCore.SIGNAL("pressed()"), self.updateLayerPaintAtom)

    def updateLayerAtomType(self):
        current_layer = self.window().centralWidget().graphics_scene.current_layer
        current_layer.atom_types[self.index] = self.label.text()

    def updateLabel(self):
        self.label.setText(self.window().centralWidget().graphics_scene.current_layer
                           .atom_types[self.index])

    def updateLayerPaintAtom(self):
        current_layer = self.window().centralWidget().graphics_scene.current_layer
        current_layer.current_atom = self.index


    def paintEvent(self, event):
        p = QtGui.QPainter()
        p.begin(self)
        p.setBrush(QtGui.QColor(50, 50, 50))
        p.setOpacity(0.8)
        p.drawRect(event.rect())
