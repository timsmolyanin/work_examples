import queue
from threading import Thread


class CommThread(Thread):
    def __init__(self, cmd_queue, client, cb, parent=None):
        super(CommThread, self).__init__(parent)
        self.cmd_queue = cmd_queue
        self.client = client
        self.parent = parent
        self.callback = cb

    def run(self):
        while True:
            arg = self.cmd_queue.get()
            cmd, start_reg, num_of_regs = arg
            if cmd == 'read':
                self.read_target_status(start_reg, num_of_regs)

    def read_target_status(self, start_reg, num_of_reg):
        try:
            raw_data = self.client.read_discrete_inputs(start_reg, num_of_reg, unit=1)
            # raw_data = self.client.read_coils(start_reg, num_of_reg, unit=1)
            self.callback(('ON', raw_data.bits))
        except Exception as exc:
            self.callback(('DISABLE', exc))
            status = self.client.connect()
            if not status:
                try:
                    while True:
                        self.cmd_queue.get(False)
                except queue.Empty:
                    pass
