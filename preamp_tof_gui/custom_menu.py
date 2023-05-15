
from PySide2 import QtWidgets
import styles


class CustomMenu(QtWidgets.QWidget):

    def __init__(self, parent=None, type=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.layout = QtWidgets.QGridLayout()
        # self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.input = QtWidgets.QLineEdit()
        self.layout.addWidget(self.input, 0, 0)

        self.set_button = QtWidgets.QPushButton()
        self.layout.addWidget(self.set_button, 0, 1)
        range_lbl = QtWidgets.QLabel()
        self.layout.addWidget(range_lbl, 1, 0, 2, 1)
        if type == 1:
            self.set_button.setText('Set DAC')
            range_lbl.setText('<font size=3>Min: 0, Max: 3300</font>')
        else:
            self.set_button.setText('Set Vdelta')
            range_lbl.setText('<font size=3>Min: 0, Max: 500</font>')