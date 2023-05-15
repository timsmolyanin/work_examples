import sys

from PySide2.QtCore import Qt
from PySide2.QtGui import QBrush, QPainter, QPen, QColor
from PySide2.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QWidget,
)
from PySide2 import QtWidgets, QtCore, QtGui


# It's a subclass of QGraphicsRectItem that emits a signal when it's clicked
class ClRect(QGraphicsRectItem):
    click_signal_left_btn = QtCore.Signal(object)
    click_signal_right_btn = QtCore.Signal(object)

    def __init__(self, *args):
        """
        The function __init__ is a constructor that takes in a variable number of arguments and passes them to the
        QGraphicsRectItem constructor
        """
        QGraphicsRectItem.__init__(self, *args)
        self.name = None
        self.idx = None

    def mousePressEvent(self, event):
        """
        It emits a signal that is connected to a slot in the main window

        :param event: The event that triggered the mousePressEvent
        """
        if event.button() == QtCore.Qt.LeftButton:
            self.scene().click_signal_left_btn.emit(self)
        else:
            self.scene().click_signal_right_btn.emit(self)


# It's a subclass of QGraphicsScene that emits a signal when the user clicks on it
class GraphicsScene(QGraphicsScene):
    click_signal_left_btn = QtCore.Signal(object)
    click_signal_right_btn = QtCore.Signal(object)


# We create a scene, add some items to it, and then add the scene to a view
class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(380, 610)

        # Defining a scene rect of 400x200, with it's origin at 0,0.
        # If we don't set this on creation, we can set it later with .setSceneRect
        self.scene = GraphicsScene(0, 0, 360, 600)

        self.default_pen = QPen(Qt.black)
        self.default_pen.setWidth(1)

        self.highlight_pen = QPen(Qt.red)
        self.highlight_pen.setWidth(3)

        self.rect = ClRect(0, 190, 50, 200)
        self.rect.name = 'fsd0'
        self.rect.idx = 0
        brush = QBrush(QColor(0, 129, 167))
        self.rect.setBrush(brush)

        self.rect1 = ClRect(96, 127, 50, 322)
        self.rect1.name = 'fsd1'
        self.rect1.idx = 0
        brush = QBrush(QColor(0, 175, 185))
        self.rect1.setBrush(brush)

        self.rect2 = ClRect(193, 64, 50, 450)
        self.rect2.name = 'fsd2'
        self.rect2.idx = 1
        brush = QBrush(QColor(254, 217, 183))
        self.rect2.setBrush(brush)

        self.rect3 = ClRect(290, 0, 50, 578)
        self.rect3.name = 'fsd3'
        self.rect3.idx = 2
        brush = QBrush(QColor(240, 113, 103))
        self.rect3.setBrush(brush)

        # Add the items to the scene. Items are stacked in the order they are added.
        self.scene.addItem(self.rect)
        self.scene.addItem(self.rect1)
        self.scene.addItem(self.rect2)
        self.scene.addItem(self.rect3)

        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setMaximumSize(1200, 800)
        self.view.setMinimumSize(150, 200)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.view)
        self.setLayout(hbox)

    def resizeEvent(self, event):
        """
        The function resizes the view to fit the scene, keeping the aspect ratio

        :param event: The event object
        """
        qrect = self.view.sceneRect()
        self.view.fitInView(qrect, QtCore.Qt.KeepAspectRatioByExpanding)
        event.accept()

    def showEvent(self, event):
        """
        The function showEvent() is called when the widget is shown. It sets the view to fit the scene

        :param event: The event object
        """
        qrect = self.view.sceneRect()
        self.view.fitInView(qrect, QtCore.Qt.KeepAspectRatioByExpanding)
        event.accept()


# def main():
#     app = QtWidgets.QApplication(sys.argv)
#     w = Window()
#     w.show()
#     app.exec_()
#
#
# if __name__ == '__main__':
#     main()
