#!/home/tango/wk/python/py39/bin/python
# -*- coding: utf-8 -*-

from queue import Queue

from pymodbus.client.sync import ModbusTcpClient as ModbusClient

from tango import DevState
from tango.server import Device, attribute, command, device_property

from comm_thread import CommThread
from tango_cmd_allowed import is_cmd_allowed


class BMNTarget(Device):
    """
    BMNTarget tango device server
    """
    ip = device_property(dtype=str, default_value='10.18.88.125', doc='IP address of the BMN target')
    port = device_property(dtype=int, default_value=502, doc='Default Modbus TCP/IP port')

    current_target = attribute(dtype=int, polling_period=5000,
                               archive_period=3600000,
                               archive_abs_change=0.5,
                               fread='read_attr',
                               fisallowed='deny_read'
                               )

    def init_device(self):
        """
        device initialization and variable containers
        :return:
        """
        self.set_state(DevState.INIT)
        Device.init_device(self)
        self.client = ModbusClient(self.ip, port=self.port, timeout=1)
        self._first_target_status_reg = 1024
        # self._first_target_status_reg = 2048
        self._number_of_status_regs = 4
        self.current_target_value = 0

    def read_attr(self, attr):
        """
        common read method for all attributes
        :param attr: attribute object
        :return:
        """
        attr_name = str(attr.get_name())  # Get name from sender object (attr)
        attr_value = getattr(self, f'{attr_name}_value')
        attr.set_value(attr_value)
        return attr

    def deny_read(self, attr):
        return self.get_state() not in (DevState.DISABLE, DevState.UNKNOWN, DevState.INIT)

    @is_cmd_allowed('is_connect_allowed')
    @command(polling_period=5000)
    def connect(self):
        status = self.client.connect()
        if status:
            self.msg_queue = Queue()
            self.comm_thread = CommThread(cmd_queue=self.msg_queue, client=self.client, cb=self.process_data)
            self.comm_thread.start()
            self.set_state(DevState.ON)
        else:
            self.set_state(DevState.DISABLE)

    def is_connect_allowed(self):
        return self.get_state() in [DevState.DISABLE, DevState.INIT]

    @is_cmd_allowed('is_read_allowed')
    @command(polling_period=2000)
    def read_target_status(self):
        self.msg_queue.put(('read', self._first_target_status_reg, self._number_of_status_regs))

    def is_read_allowed(self):
        return self.get_state() not in [DevState.DISABLE, DevState.INIT]

    def process_data(self, data):
        state, data_raw = data
        print(data_raw)
        if state == 'DISABLE':
            self.set_state(DevState.DISABLE)
            status = f'{data_raw}'
            status += f'\nDevice disconnected.'
            self.set_status(status)
        elif state == 'ON':
            self.set_state(DevState.ON)
            status = f'This device is in {self.get_state()} state.'
            self.set_status(status)
            if data_raw[0]:
                self.current_target_value = 1
            elif data_raw[1]:
                self.current_target_value = 2
            elif data_raw[2]:
                self.current_target_value = 3
            elif data_raw[3]:
                self.current_target_value = 4
            else:
                self.current_target_value = 0


if __name__ == "__main__":
    BMNTarget.run_server()
