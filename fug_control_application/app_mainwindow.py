from PySide2 import QtGui, QtCore, QtWidgets
from qgraphics_widget import Window
import styles


class AdditionalMenu(QtWidgets.QGroupBox):
    def __init__(self, parent=None, idx=None):
        super(AdditionalMenu, self).__init__(parent)

        ''' Additional menu '''
        self.additional_menu_grid_layout = QtWidgets.QGridLayout()
        self.additional_menu_gr_box = QtWidgets.QGroupBox('Setting for all Fugs on this tab')
        self.additional_menu_gr_box.setAlignment(QtCore.Qt.AlignCenter)
        self.additional_menu_gr_box.setFont(styles.group_box_test)
        self.additional_menu_gr_box.setMaximumSize(250, 300)
        self.additional_menu_gr_box.setMinimumSize(100, 250)
        self.additional_menu_gr_box.setWindowTitle('Settings')
        self.additional_menu_gr_box.setWindowIcon(QtGui.QIcon(':/fug_logo_2.png'))

        self.text_label_0 = QtWidgets.QLabel('Setting delay (ms)')
        self.text_label_0.setMinimumSize(150, 2)
        self.text_label_0.setFont(styles.lables_font)

        self.value_of_delay = QtWidgets.QDoubleSpinBox()
        self.value_of_delay.setMinimumSize(50, 30)
        self.value_of_delay.setMaximumSize(150, 30)
        self.value_of_delay.setMaximum(999999999)

        self.setting_delay = QtWidgets.QPushButton('Set')

        self.text_label_1 = QtWidgets.QLabel('Setting all and switch ON/OFF')
        self.text_label_1.setMinimumSize(220, 2)
        self.text_label_1.setFont(styles.lables_font)

        self.switch_all_ps_on = QtWidgets.QPushButton('SetAndON')
        self.switch_all_ps_on.setMinimumSize(30, 40)
        self.switch_all_ps_on.setMaximumSize(150, 40)

        self.switch_all_ps_off = QtWidgets.QPushButton('OFF')
        self.switch_all_ps_off.setMinimumSize(50, 40)
        self.switch_all_ps_off.setMaximumSize(150, 40)

        self.reset_all_fugs_btn = QtWidgets.QPushButton('RESET ALL FUGs')
        self.reset_all_fugs_btn.setMinimumSize(70, 40)

        self.additional_menu_grid_layout.addWidget(self.text_label_0, 0, 0)
        self.additional_menu_grid_layout.addWidget(self.value_of_delay, 1, 0)
        self.additional_menu_grid_layout.addWidget(self.setting_delay, 1, 1)
        self.additional_menu_grid_layout.addWidget(self.text_label_1, 2, 0)
        self.additional_menu_grid_layout.addWidget(self.switch_all_ps_on, 3, 0)
        self.additional_menu_grid_layout.addWidget(self.switch_all_ps_off, 3, 1)
        self.additional_menu_grid_layout.addWidget(self.reset_all_fugs_btn, 4, 0, 1, 0)
        self.additional_menu_gr_box.setLayout(self.additional_menu_grid_layout)


class SpecialTabWidget(QtWidgets.QTabWidget):
    click_signal_tab = QtCore.Signal(object)

    def __init__(self, *args):
        QtWidgets.QTabWidget.__init__(self, *args)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.click_signal_tab.emit(self)
        # else:
        #     super(SpecialTabWIdget, self).mousePressEvent(event)


# The MainWindow class is a QMainWindow that contains a QHBoxLayout, which contains a QSplitter, which contains a
# QGraphicsView and a QTabWidget
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.main_hbox_layout = QtWidgets.QHBoxLayout()

        self.centralwidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.setLayout(self.main_hbox_layout)

        self.setMinimumSize(1600, 800)
        self.setMaximumSize(2000, 800)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        self.tab_widget = SpecialTabWidget()

        self.topleft = QtWidgets.QFrame()
        self.topleft.setFrameShape(QtWidgets.QFrame.StyledPanel)

        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        self.main_hbox_layout.addWidget(self.splitter)

        self.qgraphics_detectors = Window()

        self.splitter.addWidget(self.qgraphics_detectors)
        self.splitter.addWidget(self.tab_widget)

        self.qgraphics_detectors.scene.click_signal_left_btn.connect(self.rect_click)
        self.qgraphics_detectors.scene.click_signal_right_btn.connect(self.rect_and_tab_right_click)
        self.tab_widget.tabBarClicked.connect(self.tab_click)
        self.tab_widget.click_signal_tab.connect(self.rect_and_tab_right_click)
