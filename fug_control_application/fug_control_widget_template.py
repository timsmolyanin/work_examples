from PySide2 import QtWidgets, QtCore, QtGui
import sys
import styles


# It's a template for a group box that contains a bunch of widgets that are used to control a power supply
class FugPSControlElementsTemplate(QtWidgets.QGroupBox):
    def __init__(self, parent=None, idx=None, tab_id=None):

        super(FugPSControlElementsTemplate, self).__init__(parent)

        self.idx = idx
        self.tab_id = tab_id
        '''
        Setting values
        '''
        self.main_grid_layout_widget = QtWidgets.QGridLayout()
        self.setLayout(self.main_grid_layout_widget)

        self.setting_values_group_box = QtWidgets.QGroupBox('Setting values')
        self.setting_values_group_box.setFont(styles.group_box_font)
        self.setting_values_group_box.setAlignment(QtCore.Qt.AlignCenter)

        self.setting_value_vbox_layout = QtWidgets.QVBoxLayout()

        self.setting_voltage_hbox_layout = QtWidgets.QHBoxLayout()

        self.setting_voltage_lbl = QtWidgets.QLabel('U Nom')
        self.setting_voltage_lbl.setFont(styles.lables_font)

        self.setting_voltage_value = QtWidgets.QDoubleSpinBox()
        self.setting_voltage_value.setFont(styles.lables_font)
        self.setting_voltage_value.setAlignment(QtCore.Qt.AlignCenter)
        self.setting_voltage_value.setStyleSheet("background-color: white")
        # self.set_voltage_value.setMinimum(-6.5)
        # self.set_voltage_value.setMaximum(6.5)

        self.setting_voltage_hbox_layout.addWidget(self.setting_voltage_lbl)
        self.setting_voltage_hbox_layout.addWidget(self.setting_voltage_value)

        self.setting_current_hbox_layout = QtWidgets.QHBoxLayout()

        self.setting_current_lbl = QtWidgets.QLabel('I Max')
        self.setting_current_lbl.setFont(styles.lables_font)

        self.setting_current_value = QtWidgets.QDoubleSpinBox()
        self.setting_current_value.setAlignment(QtCore.Qt.AlignCenter)
        self.setting_current_value.setFont(styles.lables_font)
        self.setting_current_value.setStyleSheet("background-color: white")

        self.setting_current_hbox_layout.addWidget(self.setting_current_lbl)
        self.setting_current_hbox_layout.addWidget(self.setting_current_value)

        self.setting_ramp_hbox_layout = QtWidgets.QHBoxLayout()

        self.setting_ramp_lbl = QtWidgets.QLabel('U Ramp')
        self.setting_ramp_lbl.setFont(styles.lables_font)

        self.setting_voltage_ramp_value = QtWidgets.QDoubleSpinBox()
        self.setting_voltage_ramp_value.setAlignment(QtCore.Qt.AlignCenter)
        self.setting_voltage_ramp_value.setFont(styles.lables_font)
        self.setting_voltage_ramp_value.setStyleSheet("background-color: white")

        self.setting_ramp_hbox_layout.addWidget(self.setting_ramp_lbl)
        self.setting_ramp_hbox_layout.addWidget(self.setting_voltage_ramp_value)

        self.setting_values_btn = QtWidgets.QPushButton('Setting values')
        self.setting_values_btn.setFont(styles.lables_font)

        self.reset_fug_btn = QtWidgets.QPushButton('Reset FuG')
        self.reset_fug_btn.setFont(styles.lables_font)

        self.setting_value_vbox_layout.addLayout(self.setting_voltage_hbox_layout)
        self.setting_value_vbox_layout.addLayout(self.setting_current_hbox_layout)
        self.setting_value_vbox_layout.addLayout(self.setting_ramp_hbox_layout)
        self.setting_value_vbox_layout.addWidget(self.setting_values_btn)
        self.setting_value_vbox_layout.addWidget(self.reset_fug_btn)

        self.setting_values_group_box.setLayout(self.setting_value_vbox_layout)

        '''
        Set values
        '''

        self.set_values_group_box = QtWidgets.QGroupBox('Set values')
        self.set_values_group_box.setFont(styles.group_box_font)
        self.set_values_group_box.setAlignment(QtCore.Qt.AlignCenter)

        self.set_value_vbox_layout = QtWidgets.QVBoxLayout()

        self.set_voltage_hbox_layout = QtWidgets.QHBoxLayout()

        self.set_voltage_lbl = QtWidgets.QLabel('U Nom')
        self.set_voltage_lbl.setFont(styles.lables_font)

        self.set_voltage_value = QtWidgets.QLabel()
        self.set_voltage_value.setStyleSheet('background-color: #E6E4E6')
        self.set_voltage_value.setFont(styles.lables_font)
        self.set_voltage_value.setFrameStyle(QtWidgets.QFrame.StyledPanel)
        self.set_voltage_value.setAlignment(QtCore.Qt.AlignCenter)
        self.setting_voltage_value.setMinimumWidth(60)

        self.set_voltage_hbox_layout.addWidget(self.set_voltage_lbl)
        self.set_voltage_hbox_layout.addWidget(self.set_voltage_value)

        self.set_current_hbox_layout = QtWidgets.QHBoxLayout()

        self.set_current_lbl = QtWidgets.QLabel('I Nom')
        self.set_current_lbl.setFont(styles.lables_font)

        self.set_current_value = QtWidgets.QLabel()
        self.set_current_value.setStyleSheet('background-color: #E6E4E6')
        self.set_current_value.setFrameStyle(QtWidgets.QFrame.StyledPanel)
        self.set_current_value.setAlignment(QtCore.Qt.AlignCenter)
        self.set_current_value.setFont(styles.lables_font)
        self.setting_current_value.setMinimumWidth(60)

        self.set_current_hbox_layout.addWidget(self.set_current_lbl)
        self.set_current_hbox_layout.addWidget(self.set_current_value)

        self.set_ramp_hbox_layout = QtWidgets.QHBoxLayout()

        self.set_ramp_lbl = QtWidgets.QLabel('U Ramp')
        self.set_ramp_lbl.setFont(styles.lables_font)

        self.voltage_ramp_value = QtWidgets.QLabel()
        self.voltage_ramp_value.setStyleSheet('background-color: #E6E4E6')
        self.voltage_ramp_value.setFrameStyle(QtWidgets.QFrame.StyledPanel)
        self.voltage_ramp_value.setAlignment(QtCore.Qt.AlignCenter)
        self.voltage_ramp_value.setFont(styles.lables_font)
        self.setting_voltage_ramp_value.setMaximumHeight(35)
        self.setting_voltage_ramp_value.setMinimumWidth(60)

        self.set_ramp_hbox_layout.addWidget(self.set_ramp_lbl)
        self.set_ramp_hbox_layout.addWidget(self.voltage_ramp_value)

        self.set_value_vbox_layout.addLayout(self.set_voltage_hbox_layout)
        self.set_value_vbox_layout.addLayout(self.set_current_hbox_layout)
        self.set_value_vbox_layout.addLayout(self.set_ramp_hbox_layout)

        self.set_values_group_box.setLayout(self.set_value_vbox_layout)

        '''
        Monitoring 
        '''
        mon_lbl_min_height = 25
        self.mon_values_group_box = QtWidgets.QGroupBox('Monitoring')
        self.mon_values_group_box.setFont(styles.group_box_font)
        self.mon_values_group_box.setAlignment(QtCore.Qt.AlignCenter)

        self.mon_value_vbox_layout = QtWidgets.QVBoxLayout()

        self.mon_voltage_hbox_layout = QtWidgets.QHBoxLayout()

        self.mon_voltage_lbl = QtWidgets.QLabel('U Mon')
        self.mon_voltage_lbl.setFont(styles.lables_font)

        self.actual_voltage_value = QtWidgets.QLabel()
        self.actual_voltage_value.setStyleSheet('background-color: #E6E4E6')
        self.actual_voltage_value.setFrameStyle(QtWidgets.QFrame.StyledPanel)
        self.actual_voltage_value.setAlignment(QtCore.Qt.AlignCenter)
        self.actual_voltage_value.setFont(styles.lables_font)
        self.actual_voltage_value.setMinimumHeight(mon_lbl_min_height)

        self.mon_voltage_hbox_layout.addWidget(self.mon_voltage_lbl)
        self.mon_voltage_hbox_layout.addWidget(self.actual_voltage_value)

        self.mon_current_hbox_layout = QtWidgets.QHBoxLayout()

        self.mon_current_lbl = QtWidgets.QLabel('I Mon')
        self.mon_current_lbl.setFont(styles.lables_font)

        self.actual_current_value = QtWidgets.QLabel()
        self.actual_current_value.setStyleSheet('background-color: #E6E4E6')
        self.actual_current_value.setFrameStyle(QtWidgets.QFrame.StyledPanel)
        self.actual_current_value.setAlignment(QtCore.Qt.AlignCenter)
        self.actual_current_value.setFont(styles.lables_font)
        self.actual_current_value.setMinimumHeight(mon_lbl_min_height)

        self.mon_current_hbox_layout.addWidget(self.mon_current_lbl)
        self.mon_current_hbox_layout.addWidget(self.actual_current_value)

        self.mon_control_hbox_layout = QtWidgets.QHBoxLayout()

        self.mon_control_lbl = QtWidgets.QLabel('Ctrl type')
        self.mon_control_lbl.setFont(styles.lables_font)

        self.ctrl_type_value = QtWidgets.QLabel()
        self.ctrl_type_value.setStyleSheet('background-color: #E6E4E6')
        self.ctrl_type_value.setFrameStyle(QtWidgets.QFrame.StyledPanel)
        self.ctrl_type_value.setAlignment(QtCore.Qt.AlignCenter)
        self.ctrl_type_value.setFont(styles.lables_font)
        # self.ctrl_type_value.setMinimumWidth(70)
        self.ctrl_type_value.setMinimumHeight(mon_lbl_min_height)

        self.mon_control_hbox_layout.addWidget(self.mon_control_lbl)
        self.mon_control_hbox_layout.addWidget(self.ctrl_type_value)

        self.mon_sense_error_hbox_layout = QtWidgets.QHBoxLayout()

        self.mon_sense_error_lbl = QtWidgets.QLabel('Sense err')
        self.mon_sense_error_lbl.setFont(styles.lables_font)

        self.sense_error_value = QtWidgets.QLabel()
        self.sense_error_value.setFrameStyle(QtWidgets.QFrame.StyledPanel)
        self.sense_error_value.setAlignment(QtCore.Qt.AlignCenter)
        self.sense_error_value.setFont(styles.lables_font)
        self.sense_error_value.setMinimumHeight(mon_lbl_min_height)

        self.mon_sense_error_hbox_layout.addWidget(self.mon_sense_error_lbl)
        self.mon_sense_error_hbox_layout.addWidget(self.sense_error_value)

        self.mon_value_vbox_layout.addLayout(self.mon_voltage_hbox_layout)
        self.mon_value_vbox_layout.addLayout(self.mon_current_hbox_layout)
        self.mon_value_vbox_layout.addLayout(self.mon_control_hbox_layout)
        # self.mon_value_vbox_layout.addLayout(self.mon_state_hbox_layout)
        self.mon_value_vbox_layout.addLayout(self.mon_sense_error_hbox_layout)

        self.mon_values_group_box.setLayout(self.mon_value_vbox_layout)

        '''
        Switch output values
        '''

        self.set_output_values_group_box = QtWidgets.QGroupBox('Switch output')
        self.set_output_values_group_box.setFont(styles.group_box_font)
        self.set_output_values_group_box.setAlignment(QtCore.Qt.AlignCenter)

        self.set_output_values_hbox_layout = QtWidgets.QHBoxLayout()

        self.output_on_values_btn = QtWidgets.QPushButton('ON')
        self.output_on_values_btn.setFont(styles.lables_font)
        self.output_off_values_btn = QtWidgets.QPushButton('OFF')
        self.output_off_values_btn.setFont(styles.lables_font)

        self.set_output_values_hbox_layout.addWidget(self.output_on_values_btn)
        self.set_output_values_hbox_layout.addWidget(self.output_off_values_btn)

        self.set_output_values_group_box.setLayout(self.set_output_values_hbox_layout)

        '''
        Device State
        '''
        self.state_group_box = QtWidgets.QGroupBox()

        self.mon_state_hbox_layout = QtWidgets.QHBoxLayout()

        self.mon_state_lbl = QtWidgets.QLabel('State')
        self.mon_state_lbl.setFont(styles.lables_font)

        self.fug_state_value = QtWidgets.QLabel()
        self.fug_state_value.setFrameStyle(QtWidgets.QFrame.StyledPanel)
        self.fug_state_value.setAlignment(QtCore.Qt.AlignCenter)
        self.fug_state_value.setFont(styles.lables_font)
        self.fug_state_value.setMinimumHeight(mon_lbl_min_height)

        self.mon_state_hbox_layout.addWidget(self.mon_state_lbl)
        self.mon_state_hbox_layout.addWidget(self.fug_state_value)

        self.state_group_box.setLayout(self.mon_state_hbox_layout)

        '''
        CV/CC mode
        '''
        self.cv_cc_group_box = QtWidgets.QGroupBox()

        self.cv_cc_hbox_layout = QtWidgets.QHBoxLayout()
        self.cv_vbox_layout = QtWidgets.QVBoxLayout()
        self.cc_vbox_layout = QtWidgets.QVBoxLayout()

        self.cc_mode_lbl = QtWidgets.QLabel('CC')
        self.cc_mode_lbl.setFont(styles.lables_font)
        self.cc_mode_lbl.setAlignment(QtCore.Qt.AlignCenter)

        self.cc_mode_value = QtWidgets.QLabel()
        self.cc_mode_value.setFrameStyle(QtWidgets.QFrame.StyledPanel)
        self.cc_mode_value.setFont(styles.lables_font)
        self.cc_mode_value.setAlignment(QtCore.Qt.AlignCenter)

        self.cc_vbox_layout.addWidget(self.cc_mode_lbl)
        self.cc_vbox_layout.addWidget(self.cc_mode_value)

        self.cv_cc_hbox_layout.addLayout(self.cc_vbox_layout)

        self.cv_mode_lbl = QtWidgets.QLabel('CV')
        self.cv_mode_lbl.setFont(styles.lables_font)
        self.cv_mode_lbl.setAlignment(QtCore.Qt.AlignCenter)

        self.cv_mode_value = QtWidgets.QLabel()
        self.cv_mode_value.setFrameStyle(QtWidgets.QFrame.StyledPanel)
        self.cv_mode_value.setFont(styles.lables_font)
        self.cv_mode_value.setAlignment(QtCore.Qt.AlignCenter)

        self.cv_vbox_layout.addWidget(self.cv_mode_lbl)
        self.cv_vbox_layout.addWidget(self.cv_mode_value)

        self.cv_cc_hbox_layout.addLayout(self.cv_vbox_layout)

        self.cv_cc_group_box.setLayout(self.cv_cc_hbox_layout)

        '''
        Put all widgets into main_grid_layout
        '''

        self.set_values_group_box.setMaximumWidth(200)
        self.set_values_group_box.setMaximumHeight(200)
        self.setting_values_group_box.setMaximumHeight(200)
        self.setting_values_group_box.setMaximumWidth(200)
        self.mon_values_group_box.setMaximumHeight(200)
        self.mon_values_group_box.setMaximumWidth(200)
        self.state_group_box.setMaximumHeight(200)
        self.state_group_box.setMaximumWidth(200)
        self.cv_cc_group_box.setMaximumHeight(200)
        self.cv_cc_group_box.setMaximumWidth(200)
        self.set_output_values_group_box.setMaximumHeight(200)
        self.set_output_values_group_box.setMaximumWidth(200)

        self.main_grid_layout_widget.addWidget(self.setting_values_group_box, 0, 1)
        self.main_grid_layout_widget.addWidget(self.set_values_group_box, 0, 2)
        self.main_grid_layout_widget.addWidget(self.mon_values_group_box, 0, 3)
        self.main_grid_layout_widget.addWidget(self.state_group_box, 1, 1)
        self.main_grid_layout_widget.addWidget(self.cv_cc_group_box, 1, 2)
        self.main_grid_layout_widget.addWidget(self.set_output_values_group_box, 1, 3)

        self.main_grid_layout_widget.setSpacing(3)
        self.main_grid_layout_widget.setMargin(3)
        self.main_grid_layout_widget.setHorizontalSpacing(10)
        self.main_grid_layout_widget.setVerticalSpacing(1)


# It's a QGroupBox that contains a QLabel, a QLabel, and a QGroupBox
class FugPSMainTemplateWidget(QtWidgets.QGroupBox):
    def __init__(self, parent=None, idx=None, tab_id=None):
        super(FugPSMainTemplateWidget, self).__init__(parent)

        self.idx = idx
        self.tab_id = tab_id

        self.fug_controls = FugPSControlElementsTemplate(idx=self.idx)
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.vbox_layout)

        self.vbox_layout.setMargin(0)
        self.vbox_layout.setSpacing(2)

        '''
        labels
        '''
        self.widgets_title_lbl = QtWidgets.QLabel()
        self.widgets_title_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.widgets_title_lbl.setFont(styles.widget_title_font)

        self.serial_number_value = QtWidgets.QLabel()
        self.serial_number_value.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.serial_number_value.setAlignment(QtCore.Qt.AlignCenter)
        self.serial_number_value.setFrameStyle(QtWidgets.QFrame.StyledPanel)
        self.serial_number_value.setFont(styles.serial_number_font)
        self.serial_number_value.setStyleSheet("background-color: #F4F3F3")

        self.widgets_title_lbl.setMinimumHeight(30)
        self.widgets_title_lbl.setMaximumHeight(30)

        self.serial_number_value.setMinimumHeight(30)
        self.serial_number_value.setMaximumHeight(30)

        self.setMaximumSize(700, 500)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        self.vbox_layout.addWidget(self.widgets_title_lbl)
        self.vbox_layout.addWidget(self.serial_number_value)
        self.vbox_layout.addWidget(self.fug_controls)


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = FugPSControlElementsTemplate()
    w.show()
    app.exec_()


if __name__ == '__main__':
    main()





