#!/home/tango/wk/python/py39/bin/python
# -*- coding: utf-8 -*-
import queue
import socket
import time
import tango
import atexit
import os

from tango import DevState
from tango.server import Device, attribute, command, device_property
from itertools import count

from tango_cmd_allowed import is_cmd_allowed
from comm_thread import CommThread

fug_attrs = ('set_current', 'set_voltage', 'actual_current', 'actual_voltage', 'current_ramp',
             'voltage_ramp', 'ctrl_type', 'sense_error', 'cv_mode', 'cc_mode', 'serial_number',
             'fug_state',
             )
fug_cmds = ('read_actual_current', 'read_actual_voltage', 'read_set_current', 'read_set_voltage',
            'read_sense_error', 'read_cc_mode', 'read_cv_mode', 'read_ctrl_type', 'read_current_ramp',
            'read_voltage_ramp',
            )


class FugControl(Device):
    """
    FugControl tango device server
    """
    # -----------------
    # Device Properties
    # -----------------

    host = device_property(dtype=str, default_value='159.93.121.94', doc='IP address of the device server')
    port = device_property(dtype=int, default_value=2101, doc='Port of the device server')

    # ----------
    # Attributes
    # ----------

    # ---------------
    # General methods
    # ---------------

    def init_device(self):
        """
        device initialization and variable containers
        :return:
        """
        Device.init_device(self)
        self.set_state(DevState.INIT)

        self._default_timeout = 6
        self.unique = count()

    def initialize_dynamic_attributes(self):
        """
        dynamic attribute initialization
        :return:
        """
        for attr in fug_attrs:
            setattr(self, f'{attr}_value', 0)
            if attr == 'serial_number':
                tmp_str_attr = attribute(name=attr,
                                         dtype='str',
                                         archive_period=1800000,
                                         period=120,
                                         fisallowed='deny_read'
                                         )
                self.add_attribute(tmp_str_attr, self.read_fug_attrs, None, None)
                # Events pushed by code, verify event settings
                self.set_change_event(tmp_str_attr.name, True, True)
                self.set_change_event(tmp_str_attr.name, True, True)
                #
                self.set_archive_event(tmp_str_attr.name, True, True)
                self.set_archive_event(tmp_str_attr.name, True, True)

            else:
                tmp_attr = attribute(name=attr,
                                     dtype='float',
                                     archive_period=1800000,
                                     archive_abs_change=0.01,
                                     abs_change=0.01,
                                     period=120,
                                     fisallowed='deny_read'
                                     )
                self.add_attribute(tmp_attr, self.read_fug_attrs, None, None)

                # Events pushed by code, verify event settings
                self.set_change_event(tmp_attr.name, True, True)
                self.set_change_event(tmp_attr.name, True, True)
                #
                self.set_archive_event(tmp_attr.name, True, True)
                self.set_archive_event(tmp_attr.name, True, True)

    def read_fug_attrs(self, attr):
        """
        common read method for all attributes
        :param attr: attribute object
        :return:
        """
        attr_name = str(attr.get_name())
        attr_value = getattr(self, f'{attr_name}_value')
        attr.set_value(attr_value)
        return attr

    def deny_read(self, attr):
        """
        disable reading atts in the tango.DISABLE state
        :param attr: attribute object
        :return:
        """
        return self.get_state() not in [DevState.DISABLE]

    @is_cmd_allowed('is_connect_allowed')
    @command(polling_period=6000)
    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self._default_timeout / 2)
            self.sock.connect((self.host, self.port))
            self.cmd_queue = queue.PriorityQueue()
            self.comm_thread = CommThread(self.cmd_queue, self.sock, cb=self.cb, prnt=self)
            self.comm_thread.setDaemon(True)
            self.comm_thread.start()
            self.set_state(DevState.ON)
        except Exception as exc:
            print(exc)
            self.sock.close()
            self.set_state(DevState.DISABLE)

    def is_connect_allowed(self):
        return self.get_state() in [DevState.DISABLE, DevState.INIT]

    @is_cmd_allowed('is_device_clear_allowed')
    @command()
    def device_clear(self):
        """
        Effects of Device Clear:
        - all setvalues are set to zero
        - setvalue ramp-function is reset to the calibrated default value from EEPROM
        - setvalue ramp-speed is reset to the calibrated default value from EEPROM
        - all digital outputs are reset
        - monitor selector is reset to the calibrated value from EEPROM
        - Service Request Mask is set to zero
        - Service Request Register is set to zero
        - ADC integration times are reset to its calibrated values from EEPROM
        - Terminator character for answer strings is reset to its calibrated value from EEPROM
        :return:
        """
        priority = 1
        cmd_name = 'device_clear'
        cmd = '=\r\n'
        self.cmd_queue.put((priority, next(self.unique), cmd_name, cmd))

    def is_device_clear_allowed(self):
        return self.get_state() in [DevState.ON, DevState.OFF]

    @is_cmd_allowed('is_set_voltage_ramp_allowed')
    @command(dtype_in=tango.DevDouble)
    def set_voltage_ramp(self, value):
        """
        voltage ramp rate command
        :param value: set voltage ramp rate value
        :return:
        """
        priority = 1

        cmds = {'v_ramp_rate_test': '>s0b 2\r\n', 'set_voltage_ramp': f'>s0r {value}\r\n'}
        for cmd_name, cmd in cmds.items():
            self.cmd_queue.put((priority, next(self.unique), cmd_name, cmd))

    def is_set_voltage_ramp_allowed(self):
        return self.get_state() in [DevState.ON, DevState.OFF]

    @is_cmd_allowed('is_set_voltage_allowed')
    @command(dtype_in=tango.DevDouble)
    def set_voltage(self, value):
        """
        set voltage command
        :param value: set voltage value
        :return:
        """
        priority = 1
        cmd_name = 'set_voltage'
        cmd = f'>s0 {value}\r\n'
        self.cmd_queue.put((priority, next(self.unique), cmd_name, cmd))

    def is_set_voltage_allowed(self):
        return self.get_state() in [DevState.ON, DevState.OFF]

    @is_cmd_allowed('is_set_current_allowed')
    @command(dtype_in=tango.DevDouble)
    def set_current(self, value):
        """
        set current command
        :param value: set current value
        :return:
        """
        priority = 1
        cmd_name = 'set_current'
        cmd = f'>s1 {value}\r\n'
        self.cmd_queue.put((priority, next(self.unique), cmd_name, cmd))

    def is_set_current_allowed(self):
        return self.get_state() in [DevState.ON, DevState.OFF]

    @is_cmd_allowed('is_switch_output_on_allowed')
    @command()
    def switch_output_on(self):
        """
        turn on the output voltage
        :return:
        """
        priority = 1
        cmd_name = 'switch_output_on'
        cmd = 'f1\r\n'
        self.cmd_queue.put((priority, next(self.unique), cmd_name, cmd))

    def is_switch_output_on_allowed(self):
        return self.get_state() in [DevState.ON, DevState.OFF]

    @is_cmd_allowed('is_switch_output_off_allowed')
    @command()
    def switch_output_off(self):
        """
        turn off the output voltage
        :return:
        """
        priority = 1
        cmd_name = 'switch_output_off'
        cmd = 'f0\r\n'
        self.cmd_queue.put((priority, next(self.unique), cmd_name, cmd))

    def is_switch_output_off_allowed(self):
        return self.get_state() in [DevState.ON, DevState.OFF]

    @is_cmd_allowed('is_read_mon_values_allowed')
    @command(polling_period=3000)
    def read_mon_values(self):
        """
        command to read monitored atts (which will be archived)
        :return:
        """
        priority = 2
        cmds = {'read_actual_current': '>m1?\r\n', 'read_actual_voltage': '>m0?\r\n', 'read_set_current': '>s1?\r\n',
                'read_set_voltage': '>s0?\r\n', 'read_fug_state': '>don?\r\n', 'read_sense_error': '>dx?\r\n'}
        for cmd_name, cmd in cmds.items():
            self.cmd_queue.put((priority, next(self.unique), cmd_name, cmd))

    def is_read_mon_values_allowed(self):
        return self.get_state() in [DevState.ON, DevState.OFF]

    @is_cmd_allowed('is_read_misc_values_allowed')
    @command(polling_period=5000)
    def read_misc_values(self):
        """
        command to misc atts (necessary for the operation of the control application)
        :return:
        """
        priority = 2
        cmds = {'read_cc_mode': '>dir?\r\n', 'read_cv_mode': '>dvr?\r\n', 'read_ctrl_type': '>dsd?\r\n',
                'read_current_ramp': '>s1r?\r\n', 'read_voltage_ramp': '>s0r?\r\n',
                'read_serial_number': '?\r\n'}
        for cmd_name, cmd in cmds.items():
            self.cmd_queue.put((priority, next(self.unique), cmd_name, cmd))

    def is_read_misc_values_allowed(self):
        return self.get_state() in [DevState.ON, DevState.OFF]

    def cb(self, event):
        """
        callback from the thread (ReadThread)
        :param: event: data from the ReadThread()
        :return:
        """
        # print('eveeeeeent', event)

        ds_state = event[0]
        if ds_state == 'connection error':
            self.set_state(DevState.DISABLE)
            tango_ds_status = f'This device is in {self.get_state()} state.'
            self.set_status(tango_ds_status)
            self.fug_state_value = self.get_state()
            self.push_change_event('fug_state', self.fug_state_value)
            self.push_archive_event('fug_state', self.fug_state_value)
        elif ds_state == 'OK':
            cmd = event[1]
            data = event[2]
            data_split = data.split(':')
            if cmd == 'read_fug_state':
                value = int(data_split[1])
                self.set_ds_state_(bool(value))
                self.fug_state_value = self.get_state()
                self.push_change_event('fug_state', self.fug_state_value)
                self.push_archive_event('fug_state', self.fug_state_value)
            elif cmd == 'read_serial_number':
                value = data_split[0]
                self.serial_number_value = value
            elif cmd in fug_cmds:
                split_cmd = cmd.split('_')
                attr_name = f'{split_cmd[1]}_{split_cmd[2]}'
                value = float(data_split[1])
                self.push_change_event(attr_name, round(value, 2))
                self.push_archive_event(attr_name, round(value, 2))
                setattr(self, f'{attr_name}_value', round(value, 2))

    def set_ds_state_(self, state):
        """
        set tango device server state
        :param: state: shows the actual state of the tango ds
        :return:
        """
        tango_ds_status = ''
        if state:
            self.set_state(DevState.ON)
        else:
            self.set_state(DevState.OFF)
        tango_ds_status = f'This device is in {self.get_state()} state.'
        self.set_status(tango_ds_status)


if __name__ == "__main__":
    FugControl.run_server()
