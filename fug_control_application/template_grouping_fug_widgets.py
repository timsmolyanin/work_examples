from PySide2 import QtCore, QtWidgets
from fug_control_widget_template import FugPSMainTemplateWidget
import styles


# It creates a grid layout with a number of widgets equal to the number of widgets passed to the class
class GroupOfFugPSMainTemplateWidgets(QtWidgets.QWidget):
    def __init__(self, parent=None, num_of_widget=None):
        """
        A constructor for the class.

        :param parent: The parent widget of the widget you're creating
        :param num_of_widget: The number of widgets you want to add to the layout
        """
        super(GroupOfFugPSMainTemplateWidgets, self).__init__(parent)

        self.num_of_widget = num_of_widget

        self.widget_grid_layout = QtWidgets.QGridLayout()
        self.setMaximumSize(1200, 1000)

        self.setLayout(self.widget_grid_layout)

        z = 0
        j = 0

        for i, wid_id in enumerate(range(1, int(self.num_of_widget)+1)):
            setattr(self, f'ps_widget_{i}', FugPSMainTemplateWidget(idx=i))
            ps_widget = getattr(self, f'ps_widget_{i}')
            if i >= 2:
                if i >= 4:
                    ps_widget.setStyleSheet("background-color: #D6D3D3")
                    self.widget_grid_layout.addWidget(ps_widget, z, 2)
                    z += 1
                else:
                    ps_widget.setStyleSheet("background-color: #E8E7E7")
                    self.widget_grid_layout.addWidget(ps_widget, j, 1)
                    j += 1

            else:
                ps_widget.setStyleSheet("background-color: #D6D3D3")
                self.widget_grid_layout.addWidget(ps_widget, i, 0)


