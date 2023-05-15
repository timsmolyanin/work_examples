#!/home/tango/wk/python/py39/bin/python

import queue
import select
import socket
import time
import logging

from tango import DevState, DevFloat, Util
from tango.server import Device, attribute, command, device_property
from logging.handlers import RotatingFileHandler
from pathlib import Path

from comm_thread import CommThread
from proc_data_funcs import _ieee754_to_decimal, _calculate_checksum256, _format_packet, _compare_checksum256
from tango_cmd_allowed import is_cmd_allowed


class EksisThermoanemome(Device):
    """

    """
    # -----------------
    # Device Properties
    # -----------------
    ip = device_property(
        dtype=str,
    )

    port = device_property(
        dtype=int,
    )
    sensor_id = device_property(
        dtype=[int, ],
    )

    # ----------
    # Attributes
    # ----------

    # ---------------
    # General methods
    # ---------------

    def init_device(self):
        try:
            Device.init_device(self)
            self.set_state(DevState.INIT)
            self.sensors_on_set = set()
            self.sensors_fault_set = set()
            self.default_timeout = 5

            util = Util.instance()
            self.ds_instance = util.get_ds_inst_name()
            self.ds_exec_name = util.get_ds_exec_name()

            pth = Path(__file__)
            if pth.is_symlink():
                self.symlink = pth.readlink()
                self.main_script_cwd = self.symlink.parent
            else:
                self.main_script_cwd = pth.parent

            work_dir_path = self.main_script_cwd / f'{self.ds_exec_name}_log_{self.ds_instance}.log'

            self.logger = logging.getLogger()  # smart logging
            self.logger.setLevel(logging.DEBUG)

            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            fh = RotatingFileHandler(work_dir_path, maxBytes=10000, backupCount=3, encoding='utf-8')  # log file

            fh.setLevel(logging.INFO)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

            self.logger.info("Device initialization finished")
        except Exception as e:
            print(e)

    def initialize_dynamic_attributes(self):
        attrs = ('temp', 'speed')
        try:
            for idx in self.sensor_id:
                for attr in attrs:
                    tmp_attr = attribute(
                        name=f'{attr}_{idx}',
                        dtype=DevFloat,
                        archive_abs_change=0.1,
                        archive_period=3600000,
                    )
                    self.add_attribute(tmp_attr, EksisThermoanemome.read_attrs, None, None)
                    setattr(self, f'{attr}_{idx}_value', 0.0)
                    self.set_archive_event(tmp_attr.name, True, True)
        except Exception as e:
            print(e)

    def read_attrs(self, attr):
        attr_name = str(attr.get_name())
        attr_value = getattr(self, f'{attr_name}_value')
        attr.set_value(attr_value)
        return attr

    @is_cmd_allowed('is_connect_allowed')
    @command(polling_period=10000)
    def connect(self):
        self.logger.info("Connect method started")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(self.default_timeout)
        try:
            self.s.connect((self.ip, self.port))
            self.cmd_queue = queue.Queue()
            self.com_thread = CommThread(tango_class=self)
            self.com_thread.setDaemon(True)
            self.com_thread.start()
            self.logger.info("Connection to device was done")
            check_sensors = self.check_sensors_addrs(self.s)
            self.logger.info("Checked that addresses of EKSIS sensors are available")
            self.logger.info(f"ON state addresses: {self.sensors_on_set}")
            self.logger.info(f"FAULT state addresses: {self.sensors_fault_set}")
            if check_sensors:
                self.set_state(DevState.ON)
            else:
                self.set_state(DevState.OFF)
            self.logger.info("Connect method was finished")
        except Exception as exc:
            # Exception which we can get:
            # - [Errno 113] No route to host
            self.logger.info(f"Connect method had exception with description: {exc}")
            self.set_state(DevState.DISABLE)
            self.s.close()
            time.sleep(self.default_timeout)

    def is_connect_allowed(self):
        return self.get_state() in [DevState.INIT, DevState.DISABLE, DevState.FAULT]

    def check_sensors_addrs(self, sock_obj):
        sock = sock_obj
        for addr in self.sensor_id:
            sens_id = f'000{addr}'
            cmd_str = f'${sens_id}RR000404'
            checksum = _calculate_checksum256(cmd_str)
            cmd_bytes = _format_packet(cmd_str, checksum)
            sock.send(cmd_bytes)
            infds, outfds, errfds = select.select([sock], [], [], 5)
            if bool(infds):
                data = self.s.recv(64)
                self.sensors_on_set.add(addr)
                self.sensors_fault_set.discard(addr)
            else:
                self.sensors_on_set.discard(addr)
                self.sensors_fault_set.add(addr)
        if self.sensors_fault_set:
            return False
        else:
            return True

    @command(polling_period=10000)
    def set_ds_status(self):
        composed_status = ''
        channel_status_line = ''
        tango_status = f"This device is in {self.get_state()} state."  # required for Status Composer DS

        for on_addrs in self.sensors_on_set:
            channel_status_line += f"\nSensor with address {on_addrs}: ON"
        for fault_addrs in self.sensors_fault_set:
            channel_status_line += f"\nSensor with address {fault_addrs}: OFF"

        composed_status = f'{tango_status}{channel_status_line}'
        self.set_status(composed_status)  # set DS status

    @is_cmd_allowed('is_read_temp_allowed')
    @command(polling_period=2000)
    def read_temp(self):
        """
        Format of read flow temperature command:
        $[Addr]RR000404[ch](0D) where:
        $ - reserved symbol of packet beginning
        Addr - sensor ID
        RR000404 some necessary symbols for this protocol
        ch - checksum
        0D - terminator string \r
        """
        for addr in self.sensors_on_set:
            sens_id = f'000{addr}'
            cmd_str = f'${sens_id}RR000404'
            checksum = _calculate_checksum256(cmd_str)
            cmd_bytes = _format_packet(cmd_str, checksum)
            cmd_name = 'read_temp'
            self.cmd_queue.put((cmd_name, addr, cmd_bytes))

    def is_read_temp_allowed(self):
        return self.get_state() in [DevState.ON, DevState.OFF]

    @is_cmd_allowed('is_read_speed_allowed')
    @command(polling_period=2000)
    def read_speed(self):
        """
        Format of read flow speed command:
        $[Addr]RR000004[ch](0D) where:
        $ - reserved symbol of packet beginning
        Addr - sensor ID
        RR000004 some necessary symbols for this protocol
        ch - checksum
        0D - terminator string \r
        """
        for addr in self.sensors_on_set:
            sens_id = f'000{addr}'
            cmd_str = f'${sens_id}RR000004'
            checksum = _calculate_checksum256(cmd_str)
            cmd_bytes = _format_packet(cmd_str, checksum)
            cmd_name = 'read_speed'
            self.cmd_queue.put((cmd_name, addr, cmd_bytes))

    def is_read_speed_allowed(self):
        return self.get_state() in [DevState.ON, DevState.OFF]

    def cb(self, event):
        cmd_name, addr, data = event
        attr = cmd_name.split('_')[1]
        dt = data.decode('ascii')
        if _compare_checksum256(data):
            attr_bytes = f'{dt[-5]}{dt[-4]}{dt[-7]}{dt[-6]}{dt[-9]}{dt[-8]}{dt[-11]}{dt[-10]}'
            attr_value = _ieee754_to_decimal(packet=attr_bytes)
            attr_name = f'{attr}_{addr}'
            setattr(self, f'{attr_name}_value', round(attr_value, 2))
            self.push_archive_event(attr_name, round(attr_value, 2))
        else:
            self.logger.info(f"Checksum error, params: {cmd_name}, {addr}, {data}")

    def timeout_cb(self, event):
        self.logger.info(f"Timeout callback, params: {event}")
        self.set_state(DevState.FAULT)


# ----------
# Run server
# ----------
if __name__ == '__main__':
    EksisThermoanemome.run_server()



