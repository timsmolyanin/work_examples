import sys
import os
import configparser
import logging
from logging.handlers import RotatingFileHandler
import time

import tango
from PySide2 import QtWidgets, QtCore, QtGui

import qgraphics_widget
from template_grouping_fug_widgets import GroupOfFugPSMainTemplateWidgets
import app_mainwindow
import styles
import fug_logo_2

fug_attrs = ('set_current', 'set_voltage', 'actual_current', 'actual_voltage', 'voltage_ramp',
             'serial_number', 'ctrl_type', 'sense_error', 'cv_mode', 'cc_mode', 'fug_state')


class FugControlPanel(app_mainwindow.MainWindow):
    def __init__(self, parent=None):
        super(FugControlPanel, self).__init__(parent)

        # create logger
        self.logger = logging.getLogger()  # smart logging
        self.logger.setLevel(logging.DEBUG)

        dir_path = str(os.getcwd())

        work_dir_path = f'{dir_path}\ fug_app_log_file.log'

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh = RotatingFileHandler(work_dir_path, maxBytes=10000, backupCount=3, encoding='utf-8')  # log file

        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        self.logger.debug('Debug mode is ON')

        self.delay_value = 0
        self.dev_errors_and_states = dict()
        self.current_idx = None
        self.event_type = None

        self.tab_id_detectors = {'0': [self.qgraphics_detectors.rect, self.qgraphics_detectors.rect1],
                                 '1': [self.qgraphics_detectors.rect2, ],
                                 '2': [self.qgraphics_detectors.rect3, ]}

        self.fug_config = configparser.ConfigParser()
        self.fug_config.read('fug_app_config.ini')
        update_time = int(self.fug_config['DEFAULT']['update_main_window_time'])

        self.num_of_tabs = self.fug_config['DEFAULT']['num_of_tabs']

        self.additional_menu = app_mainwindow.AdditionalMenu()
        self.additional_menu.setting_delay.clicked.connect(self.setting_delay_value)
        self.additional_menu.switch_all_ps_on.clicked.connect(self.setting_and_switch_on_of_all)
        self.additional_menu.switch_all_ps_off.clicked.connect(self.switch_off_of_all)
        self.additional_menu.reset_all_fugs_btn.clicked.connect(self.reset_all_fugs)

        self.generate_main_window()
        self.subscribe_on_ds_attrs()

        self.update_main_window_timer = QtCore.QTimer()
        self.update_main_window_timer.timeout.connect(self.update_main_window)
        self.update_main_window_timer.start(update_time)

    def generate_main_window(self):
        self.setWindowTitle('FugControlApplication')

        for tab_id in range(0, int(self.num_of_tabs)):  # cycle for number of tabs
            num_of_fugs = self.fug_config[f'tab_{tab_id}'][
                'num_of_ps']  # getting number of fugs in this tab from config.ini
            tab_name = self.fug_config[f'tab_{tab_id}']['tab_name']  # getting this tab name from config.ini

            # setting group of fugs widget on this tab
            setattr(self, f'fug_widget_tab_{tab_id}', GroupOfFugPSMainTemplateWidgets(num_of_widget=int(num_of_fugs)))
            fug_widgets = getattr(self, f'fug_widget_tab_{tab_id}')  # and getting its
            num_of_fug_widgets = fug_widgets.num_of_widget  # getting number of fug widgets in this group of fug widgets
            self.tab_widget.addTab(fug_widgets, tab_name)  # adding this group widgets on this tab
            self.tab_widget.idx = tab_id
            for n, ps_id in enumerate(range(0, num_of_fug_widgets)):  # cycle for number of fug widgets on this tab
                fug_widget = getattr(fug_widgets, f'ps_widget_{n}')  # getting one of group fug widget
                fug_ps_name = self.fug_config[f'tab_{tab_id}'][
                    f'fug_ps_name_{n}']  # getting users name for this fug widget from config.ini
                fug_widget.widgets_title_lbl.setText(fug_ps_name)  # and putting it to this fug widget
                fug_widget.fug_controls.idx = ps_id  # getting id of this fug widget on this tab
                fug_widget.fug_controls.tab_id = tab_id  # getting tab id

                # connecting clicked button signals from this fug widget to slots
                fug_widget.fug_controls.setting_values_btn.clicked.connect(self.setting_values_clicked)
                fug_widget.fug_controls.output_on_values_btn.clicked.connect(self.switch_output_on_value_clicked)
                fug_widget.fug_controls.output_off_values_btn.clicked.connect(self.switch_output_off_value_clicked)
                fug_widget.fug_controls.reset_fug_btn.clicked.connect(self.reset_fug_clicked)

    def subscribe_on_ds_attrs(self):
        self.ds_name_to_widget = dict()
        for tab_id in range(0, int(self.num_of_tabs)):
            fug_widgets = getattr(self, f'fug_widget_tab_{tab_id}')
            num_of_fug_widgets = fug_widgets.num_of_widget
            for n, ps_id in enumerate(range(0, num_of_fug_widgets)):
                fug_widget = getattr(fug_widgets, f'ps_widget_{n}')
                tango_ds_name = self.fug_config[f'tab_{tab_id}'][f'tango_ds_{n}']
                self.ds_name_to_widget[tango_ds_name] = fug_widget
                self.dev_errors_and_states[f'{tango_ds_name}'] = {'error': None, 'error_desc': None, 'state': None}
                if tango_ds_name != 'None':
                    setattr(self, f'{tango_ds_name}', tango.DeviceProxy(tango_ds_name))
                    try:
                        for attr in fug_attrs:
                            self.event_id = getattr(self, f'{tango_ds_name}').subscribe_event(
                                attr,
                                tango.EventType.CHANGE_EVENT,
                                self.callback,
                                [],
                                True
                            )
                    except Exception as e:
                        print(e)

    def callback(self, event):
        error_flag = event.err
        dev_name_list = event.attr_name.split('/')[3:6]
        dev_name = f'{dev_name_list[0]}/{dev_name_list[1]}/{dev_name_list[2]}'
        if error_flag:
            errors = event.errors[0]
            error_desc = errors.desc
            self.dev_errors_and_states[dev_name]['error'] = error_flag
            self.dev_errors_and_states[dev_name]['error_desc'] = error_desc
        else:
            try:
                self.dev_errors_and_states[dev_name]['error'] = error_flag
                self.dev_errors_and_states[dev_name]['error_desc'] = None
                attr_name = event.attr_value.name
                attr_value = event.attr_value.value
                setattr(self, f'{dev_name}/{attr_name}_value', str(attr_value))
                if attr_name == 'fug_state':
                    self.dev_errors_and_states[dev_name]['state'] = attr_value
            except Exception as e:
                print(e)

    def update_main_window(self):
        """
        It updates the main window with the values of the attributes of the devices that are connected to the tabs
        """
        for tab_id in range(0, int(self.num_of_tabs)):  # cycle for the tabs
            fug_widgets = getattr(self, f'fug_widget_tab_{tab_id}')  # getting the fug widgets which is belong the tab
            num_of_fug_widgets = fug_widgets.num_of_widget  # getting the number of fug widgets which is belong the tab
            for n, ps_id in enumerate(range(0, num_of_fug_widgets)):  # cycle for the number of fug widgets on this tab
                fug_widget = getattr(fug_widgets, f'ps_widget_{n}')  # getting one of fug widget
                tango_dev_name = self.fug_config[f'tab_{tab_id}'][
                    f'tango_ds_{n}']  # getting tango device name which is belong to this fug widget
                if tango_dev_name != 'None':  # if tango device name is writing in config.ini
                    tango_dev_error_flag = self.dev_errors_and_states[tango_dev_name][
                        'error']  # getting the tango device error flag
                    if not tango_dev_error_flag:  # cheking that this tango device is not have any errors
                        for attr in fug_attrs:  # and cycle for all fug tango device attributes
                            attr_exist_flag = hasattr(self, f'{tango_dev_name}/{attr}_value')
                            if attr_exist_flag:  # cheking that the attr for this fug tango device was creating in callback method
                                attr_value = getattr(self, f'{tango_dev_name}/{attr}_value')  # getting value
                                if attr == 'serial_number':
                                    var = str(attr_value).strip('\n\r')
                                    fug_widget.serial_number_value.setText(var)
                                elif attr == 'fug_state':
                                    state_val = float(attr_value)
                                    fug_state_widget = getattr(fug_widget.fug_controls, f'{attr}_value')
                                    if state_val == 0:
                                        fug_state_widget.setStyleSheet(styles.on_state_color)
                                        fug_state_widget.setText('ON')
                                    elif state_val == 1:
                                        fug_state_widget.setStyleSheet(styles.off_state_color)
                                        fug_state_widget.setText('OFF')
                                elif attr == 'cv_mode':
                                    cv_val = float(attr_value)
                                    fug_cv_widget = getattr(fug_widget.fug_controls, f'{attr}_value')
                                    if cv_val == 0:
                                        fug_cv_widget.setText('')
                                        fug_cv_widget.setStyleSheet(styles.off_state_color)
                                    else:
                                        fug_cv_widget.setText('')
                                        fug_cv_widget.setStyleSheet(styles.on_state_color)
                                elif attr == 'cc_mode':
                                    cc_val = float(attr_value)
                                    fug_cc_widget = getattr(fug_widget.fug_controls, f'{attr}_value')
                                    if cc_val == 0:
                                        fug_cc_widget.setText('')
                                        fug_cc_widget.setStyleSheet(styles.off_state_color)
                                    else:
                                        fug_cc_widget.setText('')
                                        fug_cc_widget.setStyleSheet(styles.on_state_color)
                                elif attr == 'ctrl_type':
                                    ctrl_type_val = float(attr_value)
                                    fug_ctrl_type_val_widget = getattr(fug_widget.fug_controls, f'{attr}_value')
                                    if ctrl_type_val == 0:
                                        fug_ctrl_type_val_widget.setText('Analog')
                                        fug_ctrl_type_val_widget.setStyleSheet('background-color: #E6E4E6')
                                    else:
                                        fug_ctrl_type_val_widget.setText('Digital')
                                        fug_ctrl_type_val_widget.setStyleSheet('background-color: #E6E4E6')
                                elif attr == 'sense_error':
                                    sense_error_val = float(attr_value)
                                    fug_sense_error_val_widget = getattr(fug_widget.fug_controls, f'{attr}_value')
                                    if sense_error_val == 0:
                                        fug_sense_error_val_widget.setStyleSheet(styles.alarm_state_color)
                                        fug_sense_error_val_widget.setText('Error')
                                    else:
                                        fug_sense_error_val_widget.setStyleSheet(styles.default_color)
                                        fug_sense_error_val_widget.setText('')
                                else:
                                    fug_controls_widget = getattr(fug_widget.fug_controls, f'{attr}_value')
                                    fug_controls_widget.setText(str(attr_value))
                                    fug_controls_widget.setStyleSheet('background-color: #E6E4E6')
                    else:
                        for attr in fug_attrs:
                            if attr == 'fug_state':
                                fug_state_widget = getattr(fug_widget.fug_controls, f'{attr}_value')
                                fug_state_widget.setStyleSheet(styles.disable_state_color)
                                fug_state_widget.setText('DISABLE')
                            elif attr == 'serial_number':
                                fug_widget.serial_number_value.setText('-')
                            else:
                                fug_controls_widget = getattr(fug_widget.fug_controls, f'{attr}_value')
                                fug_controls_widget.setStyleSheet(styles.default_color)
                                fug_controls_widget.setText('-')

    def rect_and_tab_right_click(self, event):
        self.event_type = type(event)
        if self.event_type is app_mainwindow.SpecialTabWidget:
            self.current_idx = self.tab_widget.currentIndex()
        elif self.event_type is qgraphics_widget.ClRect:
            self.current_idx = event.idx
        else:
            print('What it is!?')

        self.additional_menu.additional_menu_gr_box.show()

    def rect_click(self, rect):
        """
        It takes the index of the rectangle that was clicked, and then sets the current tab to that index

        :param rect: the rectangle that was clicked
        """
        rect_id = rect.idx
        self.tab_and_qgraphics_clicks(rect_id)
        self.tab_widget.setCurrentIndex(rect_id)

    def tab_click(self, tab_id):
        """
        It takes a tab_id as an argument, and then calls another function that takes the tab_id as an argument

        :param tab_id: the id of the tab that was clicked
        """
        self.tab_and_qgraphics_clicks(tab_id)

    def tab_and_qgraphics_clicks(self, idx):
        """
        It takes a tab index and highlights the detectors in the QGraphicsView that are associated with that tab

        :param idx: the index of the tab that was clicked
        """
        for value in self.tab_id_detectors.values():
            for rect in value:
                rect.setPen(self.qgraphics_detectors.default_pen)
        var = self.tab_id_detectors[str(idx)]
        for rect_id in var:
            rect_id.setPen(self.qgraphics_detectors.highlight_pen)

    def setting_values_clicked(self):
        ps_id = self.sender().parent().parent().idx
        tab_id = self.sender().parent().parent().tab_id
        dev_server_name = self.fug_config[f'tab_{tab_id}'][f'tango_ds_{ps_id}']
        state = self.dev_errors_and_states[dev_server_name]['error']
        error_desc = self.dev_errors_and_states[dev_server_name]['error_desc']
        if state or state is None:
            self.logger.debug(
                f'Tango device server {ds_name} has error state {state} and error description {error_desc}')
        elif not state:
            try:
                fug_widget = self.ds_name_to_widget[str(dev_server_name)]
                setting_voltage_value = fug_widget.fug_controls.setting_voltage_value.value()
                setting_current_value = fug_widget.fug_controls.setting_current_value.value()
                setting_u_ramp_value = fug_widget.fug_controls.setting_voltage_ramp_value.value()
                device = tango.DeviceProxy(dev_server_name)
                device.command_inout('set_voltage', setting_voltage_value)
                device.command_inout('set_current', setting_current_value)
                device.command_inout('set_voltage_ramp', setting_u_ramp_value)
            except Exception as e:
                self.logger.debug(f'Exception {dev_server_name} with desc {e}')
        else:
            self.logger.debug(f'Something Unexpected {self.dev_errors_and_states[dev_server_name]}')

    def reset_fug_clicked(self):
        ps_id = self.sender().parent().parent().idx
        tab_id = self.sender().parent().parent().tab_id
        cmd = 'device_clear'
        dev_server_name = self.fug_config[f'tab_{tab_id}'][f'tango_ds_{ps_id}']
        self.send_cmd_to_one_dev(ps_id, tab_id, cmd, dev_server_name)

    def switch_output_on_value_clicked(self):
        ps_id = self.sender().parent().parent().idx
        tab_id = self.sender().parent().parent().tab_id
        cmd = 'switch_output_on'
        dev_server_name = self.fug_config[f'tab_{tab_id}'][f'tango_ds_{ps_id}']
        self.send_cmd_to_one_dev(ps_id, tab_id, cmd, dev_server_name)

    def switch_output_off_value_clicked(self):
        ps_id = self.sender().parent().parent().idx
        tab_id = self.sender().parent().parent().tab_id
        cmd = 'switch_output_off'
        dev_server_name = self.fug_config[f'tab_{tab_id}'][f'tango_ds_{ps_id}']
        self.send_cmd_to_one_dev(ps_id, tab_id, cmd, dev_server_name)

    def send_cmd_to_one_dev(self, fug_idx, tab_idx, cmdx, ds_name):
        ps_id = fug_idx
        tab_id = tab_idx
        cmd = cmdx
        dev_server_name = ds_name
        state = self.dev_errors_and_states[dev_server_name]['error']
        error_desc = self.dev_errors_and_states[dev_server_name]['error_desc']
        if state or state is None:
            self.logger.debug(
                f'Tango device server {dev_server_name} has error state {state} and error description {error_desc}')
        elif not state:
            try:
                device = tango.DeviceProxy(dev_server_name)
                device.command_inout(cmd)
            except Exception as e:
                self.logger.debug(f'Exception {dev_server_name} with desc {e}')
        else:
            self.logger.debug(f'Something Unexpected {self.dev_errors_and_states[ds_name]}')

    ''' Additional menu'''

    def setting_delay_value(self):
        value = self.additional_menu.value_of_delay.value()
        self.delay_value = value / 1000

    def setting_and_switch_on_of_all(self):
        data = self.get_values_from_tab(self.current_idx)
        fug_widgets = data[0]
        tango_devs = data[1]
        for n, fug_widget in enumerate(fug_widgets):
            voltage_values = fug_widget.fug_controls.setting_voltage_value.value()
            current_value = fug_widget.fug_controls.setting_current_value.value()
            voltage_ramp_value = fug_widget.fug_controls.setting_voltage_ramp_value.value()
            ds_name = tango_devs[n]
            state = self.dev_errors_and_states[ds_name]['error']
            error_desc = self.dev_errors_and_states[ds_name]['error_desc']
            if state or state is None:
                self.logger.debug(
                    f'Tango device server {ds_name} has error state {state} and error description {error_desc}')
            elif not state:
                try:
                    device = tango.DeviceProxy(ds_name)
                    device.command_inout('set_voltage', voltage_values)
                    device.command_inout('set_current', current_value)
                    device.command_inout('set_voltage_ramp', voltage_ramp_value)
                    device.command_inout('switch_output_on')
                    time.sleep(self.delay_value)
                except Exception as e:
                    self.logger.debug(f'Exception {ds_name} with desc {e}')
            else:
                self.logger.debug(f'Something Unexpected {self.dev_errors_and_states[ds_name]}')

    def switch_off_of_all(self):
        data = self.get_values_from_tab(self.current_idx)
        fug_widgets = data[0]
        tango_devs = data[1]
        cmd = 'switch_output_off'
        self.send_cmd_to_several_devs(fug_widgets, tango_devs, cmd)

    def reset_all_fugs(self):
        cmd = 'device_clear'
        for num_of_tab in range(0, int(self.num_of_tabs)):
            data = self.get_values_from_tab(num_of_tab)
            fug_widgets = data[0]
            tango_devs = data[1]
            self.send_cmd_to_several_devs(fug_widgets, tango_devs, cmd)

    def send_cmd_to_several_devs(self, fug_widgets_list, tango_dev_names_list, cmd_list):
        fug_widgets = fug_widgets_list
        tango_devs = tango_dev_names_list
        cmd = cmd_list
        for n, fug_widget in enumerate(fug_widgets):
            ds_name = tango_devs[n]
            state = self.dev_errors_and_states[ds_name]['error']
            error_desc = self.dev_errors_and_states[ds_name]['error_desc']
            if state or state is None:
                self.logger.debug(
                    f'Tango device server {ds_name} has error state {state} and error description {error_desc}')
            elif not state:
                try:
                    device = tango.DeviceProxy(ds_name)
                    device.command_inout(cmd)
                except Exception as e:
                    self.logger.debug(f'Exception {ds_name} with desc {e}')
            else:
                self.logger.debug(f'Something Unexpected {self.dev_errors_and_states[ds_name]}')

    def get_values_from_tab(self, tab_id):
        fug_widgets = getattr(self, f'fug_widget_tab_{tab_id}')
        num_of_fug_widgets = fug_widgets.num_of_widget
        list_of_widgets = list()
        list_of_ds = list()
        for n, ps_id in enumerate(range(0, num_of_fug_widgets)):
            fug_widget = getattr(fug_widgets, f'ps_widget_{n}')
            tango_ds_name = self.fug_config[f'tab_{tab_id}'][f'tango_ds_{n}']
            list_of_widgets.append(fug_widget)
            list_of_ds.append(tango_ds_name)

        return list_of_widgets, list_of_ds

    def closeEvent(self, event):
        tango.ApiUtil.cleanup()
        event.accept()


def main():
    app = QtWidgets.QApplication(sys.argv)
    QtCore.QLocale.setDefault(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
    app.setStyle('Fusion')
    w = FugControlPanel()
    w.setWindowIcon(QtGui.QIcon(':/fug_logo_2.png'))
    w.show()
    app.exec_()


if __name__ == '__main__':
    main()
