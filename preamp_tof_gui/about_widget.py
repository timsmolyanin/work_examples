
from PySide2 import QtWidgets, QtCore

import styles


class AboutErrors(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AboutErrors, self).__init__(parent)

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.app_table_colors_vertical_layout = QtWidgets.QVBoxLayout()
        self.app_status_vertical_layout = QtWidgets.QVBoxLayout()

        self.app_table_color_box = QtWidgets.QGroupBox('Description of table colors')
        self.app_status_box = QtWidgets.QGroupBox('Description of application statuses')

        self.no_response_color_lbl = QtWidgets.QLabel('-')
        self.no_response_color_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.no_response_color_lbl.setFixedSize(48, 20)
        self.no_response_color_lbl.setStyleSheet('background-color: #deca99')
        self.no_response_color_lbl_text = QtWidgets.QLabel('This color means that the preamp with this ID is not responding.')
        self.no_response_color_lbl_text.setFont(styles.status_font)

        hbox_no_response = QtWidgets.QHBoxLayout()
        hbox_no_response.addWidget(self.no_response_color_lbl)
        hbox_no_response.addWidget(self.no_response_color_lbl_text)
        self.app_table_colors_vertical_layout.addLayout(hbox_no_response)

        self.mod_off_color_lbl = QtWidgets.QLabel('-')
        self.mod_off_color_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.mod_off_color_lbl.setFixedSize(48, 20)
        self.mod_off_color_lbl.setStyleSheet('background-color: #f0b49c')
        self.mod_off_color_lbl_text = QtWidgets.QLabel('This color means that power is not supplied to the preamplifier with this ID.')
        self.mod_off_color_lbl_text.setFont(styles.status_font)

        hbox_power_off = QtWidgets.QHBoxLayout()
        hbox_power_off.addWidget(self.mod_off_color_lbl)
        hbox_power_off.addWidget(self.mod_off_color_lbl_text)
        self.app_table_colors_vertical_layout.addLayout(hbox_power_off)

        self.app_table_color_box.setLayout(self.app_table_colors_vertical_layout)

        self.warning_lbl = QtWidgets.QLabel('Warning!')
        self.warning_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.warning_lbl.setFixedSize(48, 20)
        self.warning_lbl.setStyleSheet('background-color: #f0b49c')
        self.warning_txt = QtWidgets.QLabel('Some preamp modules are not responding or are not powered')
        self.warning_txt.setFont(styles.status_font)

        hbox_warning = QtWidgets.QHBoxLayout()
        hbox_warning.addWidget(self.warning_lbl)
        hbox_warning.addWidget(self.warning_txt)

        # self.app_status_box.setLayout(hbox_warning)
        self.app_status_vertical_layout.addLayout(hbox_warning)

        self.error_status_lbl = QtWidgets.QLabel('Error!')
        self.error_status_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.error_status_lbl.setFixedSize(48, 20)
        self.error_status_lbl.setStyleSheet('background-color: #d4a3a3')
        self.error_status_lbl_text = QtWidgets.QLabel('Cant subscribe to event for device tango, maybe device server is off')
        self.error_status_lbl_text.setFont(styles.status_font)

        hbox_error_status = QtWidgets.QHBoxLayout()
        hbox_error_status.addWidget(self.error_status_lbl)
        hbox_error_status.addWidget(self.error_status_lbl_text)

        # self.app_status_box.setLayout(hbox_error_status)
        self.app_status_vertical_layout.addLayout(hbox_error_status)

        self.ok_status_lbl = QtWidgets.QLabel('OK state')
        self.ok_status_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.ok_status_lbl.setFixedSize(48, 20)
        self.ok_status_lbl.setStyleSheet('background-color: #5d735e')
        self.ok_status_lbl_text = QtWidgets.QLabel('Everything is fine, the device server is running')
        self.ok_status_lbl_text.setFont(styles.status_font)

        hbox_ok_status = QtWidgets.QHBoxLayout()
        hbox_ok_status.addWidget(self.ok_status_lbl)
        hbox_ok_status.addWidget(self.ok_status_lbl_text)

        # self.app_status_box.setLayout(hbox_ok_status)
        self.app_status_vertical_layout.addLayout(hbox_ok_status)

        self.app_status_box.setLayout(self.app_status_vertical_layout)

        self.verticalLayout.addWidget(self.app_table_color_box)
        self.verticalLayout.addWidget(self.app_status_box)

        self.pushButton = QtWidgets.QPushButton(self)

        self.pushButton.clicked.connect(self.btnClosed)
        self.verticalLayout.addWidget(self.pushButton)
        self.setWindowTitle("About")
        self.pushButton.setText("Close")

    def btnClosed(self):
        self.close()