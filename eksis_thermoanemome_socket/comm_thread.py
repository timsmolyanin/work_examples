from threading import Thread
import select


class CommThread(Thread):
    def __init__(self, tango_class, parent=None):
        super(CommThread, self).__init__(parent)
        self.tg_class = tango_class
        self.cmd_queue = self.tg_class.cmd_queue
        self.hostname = self.tg_class.ip
        self.port = self.tg_class.port
        self.callback = self.tg_class.cb
        self.timeout_callback = self.tg_class.timeout_cb

    def run(self):
        while True:
            try:
                self.s = self.tg_class.s
                data = ''  # an empty string for complete TCP package received
                cmd_name, addr, cmd = self.cmd_queue.get()
                self.s.send(cmd)
                infds, outfds, errfds = select.select([self.s], [], [], 5)
                if bool(infds):
                    data = self.s.recv(64)
                    self.callback([cmd_name, addr, data])
                else:
                    self.timeout_callback(['timeout IF', cmd_name, addr, cmd])
                    data = ''
                    break
            except Exception as exc:
                self.timeout_callback(('timeout EXC', exc))
