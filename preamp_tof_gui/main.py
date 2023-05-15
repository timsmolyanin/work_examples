import sys
import numpy as np
import configparser

import tango
from PySide2 import QtWidgets, QtCore, QtGui

from mainwindow import UiMainWindow
from custom_menu import CustomMenu
from about_widget import AboutErrors
import styles
import resources


class PreampTof(QtWidgets.QMainWindow, UiMainWindow):

    def __init__(self, parent=None):
        super(PreampTof, self).__init__(parent)     # init and inherit from multiple parents

        menu_bar = self.menuBar()

        button_action = QtWidgets.QAction('&About...', self)
        button_action.triggered.connect(self.about_click)

        help_menu = menu_bar.addMenu('&Help')
        help_menu.addAction(button_action)

        self.app_status = self.statusBar()

        self.list_of_devices_proxy = list()
        self.preamps_all_ids = list()

        self.powered_off_ids = set()
        self.no_responding_ids = set()
        self.state = ''
        self.ok_state_mod = set()
        self.error_state = 0

        config = configparser.ConfigParser()
        config.read('config.ini')
        self.window_title = config['DEFAULT']['window_title']

        sections = config.sections()

        for idx, i in enumerate(sections):
            self.list_of_devices_proxy.append(config[i]['Device_proxy'])
            setattr(self, f'preamp_srv_ids_range_{idx+1}', (config[i]['Read_from_to']).split(':'))
            temp_list = list()
            temp = getattr(self, f'preamp_srv_ids_range_{idx + 1}')
            for j in range(int(temp[0]), int(temp[1]) + 1):
                temp_list.append(j)
                setattr(self, f'preamp_srv_ids_{idx + 1}', temp_list)

        for i in range(len(sections)):
            temp_ids = getattr(self, f'preamp_srv_ids_{i + 1}')
            self.preamps_all_ids += temp_ids

        self.setup_ui(self, self.preamps_all_ids)
        self.table_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.open_menu)

        self.start_tango_attrs()

    def about_click(self):
        test = AboutErrors(self)
        test.exec_()

    def start_tango_attrs(self):
        status_attr_list = ['State', 'no_response_mod', 'power_off_mod', ]

        for ind, dev in enumerate(self.list_of_devices_proxy):
            dev_proxy = tango.DeviceProxy(dev)
            setattr(self, f'dev_proxy_{ind}', dev_proxy)

        for idx, proxy in enumerate(self.list_of_devices_proxy):
            self.dev_proxy = getattr(self, f'dev_proxy_{idx}')
            preamp_attrs_ids = getattr(self, f'preamp_srv_ids_{idx + 1}')

            attrs_names = ['vplus_{}', 'vminus_{}', 'vdelta_{}', 'tboard_{}', 'vpower_{}', 'dac_{}', 'tgas_{}']
            preamp_attrs = list()
            for names in range(len(attrs_names)):
                for idx in preamp_attrs_ids:
                    preamp_attrs.append(attrs_names[names].format(idx))
            for attr in preamp_attrs:
                self.event_id = self.dev_proxy.subscribe_event(
                    attr,
                    tango.EventType.CHANGE_EVENT,
                    self.recv_event,
                    [],
                    True
                )
            for status_attr in status_attr_list:
                self.dev_proxy.subscribe_event(status_attr, tango.EventType.CHANGE_EVENT, self.recv_status, [], True)

        self.update_table_timer = QtCore.QTimer()
        self.update_table_timer.timeout.connect(self.update_table_text)
        self.update_table_timer.start(2000)

    def recv_status(self, event):
        error = event.err
        error_attr_value = event.attr_value

        if error or not error_attr_value:
            desc = event.errors[0].desc
            self.error_state = 1
        else:
            self.error_state = 0
            try:
                attr_name = event.attr_value.name
                attr_value = event.attr_value.value
                if attr_name == 'State':
                    self.state = str(attr_value)
                elif attr_name == 'state':
                    self.state = str(attr_value)
                elif attr_name == 'power_off_mod':
                    if isinstance(attr_value, np.ndarray):
                        self.powered_off_ids = attr_value
                    else:
                        self.powered_off_ids = set()
                elif attr_name == 'no_response_mod':
                    if isinstance(attr_value, np.ndarray):
                        self.no_responding_ids = attr_value
                    else:
                        self.no_responding_ids = set()
            except Exception as e:
                print(e)

    def recv_event(self, event):
        error = event.err
        error_attr_value = event.attr_value
        if event.err or not error_attr_value:
            desc = event.errors[0].desc
            self.error_state = 1
        else:
            self.error_state = 0
            try:
                attr_name = event.attr_value.name
                attr_value = event.attr_value.value
                attr_type, idx = attr_name.split('_')
                amp = getattr(self, f'amp_{idx}')
                setattr(amp, f'{attr_type}', attr_value)
                if int(idx) not in self.powered_off_ids or self.no_responding_ids:
                    self.ok_state_mod.add(int(idx))
                else:
                    self.ok_state_mod.discard(int(idx))
            except Exception as e:
                print(e)

    def update_table_text(self):
        color_no_resp = [222, 202, 153]
        color_power_off = [240, 180, 156]
        error_color = [212, 163, 163]

        if self.error_state:
            self.powered_off_ids = self.preamps_all_ids
            self.app_status.showMessage('Error!')
            print('Error state')
            self.app_status.setStyleSheet('background-color: #d4a3a3')
            self.app_status.setFont(styles.state_font)
            self.app_status.setMaximumWidth(100)
            self.paint_statuses_of_preamps(self.preamps_all_ids, error_color)

        elif self.state == 'DISABLE':
            print('DISABLE')
            self.app_status.showMessage('Warning!')
            self.app_status.setStyleSheet('background-color: #f0b49c')
            self.app_status.setFont(styles.state_font)
            self.app_status.setMaximumWidth(100)
            self.paint_statuses_of_preamps(self.powered_off_ids, color_power_off)

        elif self.state == 'FAULT':
            print('FAULT')
            self.app_status.showMessage('Warning!')
            self.app_status.setStyleSheet('background-color: #f0b49c')
            self.app_status.setFont(styles.state_font)
            self.app_status.setMaximumWidth(100)

            self.set_ok_state_preamp_values()
            self.paint_statuses_of_preamps(self.no_responding_ids, color_no_resp)
            self.paint_statuses_of_preamps(self.powered_off_ids, color_power_off)

        elif self.state == 'ON':
            print('ON')
            self.app_status.showMessage('OK State!')
            self.app_status.setStyleSheet('background-color: #5d735e')
            self.app_status.setFont(styles.state_font)
            self.app_status.setMaximumWidth(100)

            self.set_ok_state_preamp_values()
            self.paint_statuses_of_preamps(self.no_responding_ids, color_no_resp)
            self.paint_statuses_of_preamps(self.powered_off_ids, color_power_off)

    def set_ok_state_preamp_values(self):
        color_gray = [235, 235, 235]
        color_white = [255, 255, 255]

        for i in list(self.ok_state_mod):
            amp = getattr(self, f'amp_{i}')
            getattr(amp, 'id_cell').setText(str(i))
            getattr(amp, 'vplus_cell').setText(str(getattr(amp, 'vplus')))
            getattr(amp, 'vminus_cell').setText(str(getattr(amp, 'vminus')))
            getattr(amp, 'vdelta_cell').setText(str(getattr(amp, 'vdelta')))
            getattr(amp, 'vpower_cell').setText(str(getattr(amp, 'vpower')))
            getattr(amp, 'dac_cell').setText(str(getattr(amp, 'dac')))
            getattr(amp, 'tboard_cell').setText(str(getattr(amp, 'tboard')))
            getattr(amp, 'tgas_cell').setText(str(getattr(amp, 'tgas')))

            if i % 2 == 0:
                self.paint_the_rows(amp, color_white)
            else:
                self.paint_the_rows(amp, color_gray)

    def paint_statuses_of_preamps(self, status, color):

        for i in list(status):
            amp = getattr(self, f'amp_{i}')
            getattr(amp, 'id_cell').setText(str(i))
            getattr(amp, 'vplus_cell').setText('-')
            getattr(amp, 'vminus_cell').setText('-')
            getattr(amp, 'vdelta_cell').setText('-')
            getattr(amp, 'vpower_cell').setText('-')
            getattr(amp, 'dac_cell').setText('-')
            getattr(amp, 'tboard_cell').setText('-')
            getattr(amp, 'tgas_cell').setText('-')

            self.paint_the_rows(amp, color)

    def closeEvent(self, event):
        print('closing')
        self.update_table_timer.stop()
        tango.ApiUtil.cleanup()
        event.accept()

    def open_menu(self, pos):
        menu = QtWidgets.QMenu()
        menu.setStyleSheet("QMenu { font-size:14px;}")
        amps = [int(self.table_widget.item(i.row(), 0).text()) for i in self.table_widget.selectedIndexes()]

        reset = menu.addAction("Reset")
        on = menu.addAction("Turn on")
        off = menu.addAction("Turn off")

        self.dac_input = CustomMenu(type=1)
        widget_action = QtWidgets.QWidgetAction(self)
        widget_action.setDefaultWidget(self.dac_input)
        menu.addAction(widget_action)
        self.dac_input.set_button.clicked.connect(lambda: self.set_dac(amps))

        self.vdelta_input = CustomMenu()
        vdelta_action = QtWidgets.QWidgetAction(self)
        vdelta_action.setDefaultWidget(self.vdelta_input)
        menu.addAction(vdelta_action)

        self.vdelta_input.set_button.clicked.connect(lambda: self.set_vdelta(amps))
        tmp = (set(self.powered_off_ids) & set(amps)) or (set(self.no_responding_ids) & set(amps))

        if bool(tmp):
            pass
        else:
            action = menu.exec_(QtGui.QCursor().pos())

            if action == reset:
                self.reset_dac(amps)
            elif action == on:
                self.turn_on(amps)
            elif action == off:
                self.turn_off(amps)

    def set_vdelta(self, amps):
        try:
            value = int(self.vdelta_input.input.text())
            if value < 0 or value > 500:
                raise Exception
            for i in amps:
                amp = getattr(self, 'amp_{}'.format(i))
                dac_from_amp = getattr(amp, 'dac')
                dac_now = round(((dac_from_amp * 256) / 3300))
                dac_value = int((dac_now - (value - getattr(amp, 'vdelta')) / 5) * 3300 / 256)
                self.dev_proxy.command_inout('set_dac', [int(i), dac_value])

            self.vdelta_input.input.setStyleSheet('border: 1px solid black;')
        except:
            self.vdelta_input.input.setStyleSheet('border: 2px solid red;')

    def set_dac(self, amps):
        try:
            value = int(self.dac_input.input.text())
            if value < 0 or value > 3300:
                raise Exception
            for amp in amps:
                self.dev_proxy.command_inout('set_dac', [int(amp), value])

            self.dac_input.input.setStyleSheet('border: 1px solid black;')
        except:
            self.dac_input.input.setStyleSheet('border: 2px solid red;')

    def reset_dac(self, amps):
        for amp in amps:
            try:
                self.dev_proxy.command_inout('reset_dac', int(amp))
            except Exception as e:
                print(e)

    def turn_on(self, amps):
        for amp in amps:
            try:
                self.dev_proxy.command_inout('turn_on', int(amp))
            except Exception as e:
                print(e)

    def turn_off(self, amps):
        for amp in amps:
            try:
                self.dev_proxy.command_inout('turn_off', int(amp))
            except Exception as e:
                print(e)


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = PreampTof()
    form.setWindowIcon(QtGui.QIcon(':/icon.ico'))
    form.setWindowTitle(form.window_title)
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
