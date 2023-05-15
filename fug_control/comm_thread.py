import queue
from threading import Thread
import select


class CommThread(Thread):
    """
    Second thread to physically read hardware
    """

    def __init__(self, cmd_queue, sock, cb, prnt, parent=None):
        super(CommThread, self).__init__(parent)

        self.queue = cmd_queue
        self.sock = sock
        self.callback = cb
        self.parent = prnt

        self._default_timeout = 6

    def run(self):
        """
        The overriden Thread run() method, in which we do mainly all the physical I/O
        :return:
        """
        while True:
            args = self.queue.get()
            priority, counter, cmd_name, cmd = args
            self.communicate_with_fug(priority, cmd_name, cmd)

    def communicate_with_fug(self, priority, cmd_name, cmd):
        data = ''
        chunk = ''
        try:
            print(priority, cmd_name, cmd)
            self.sock.send(str.encode(cmd))
            while True:
                infds, outfds, errfds = select.select([self.sock], [], [], self._default_timeout / 2)
                if bool(infds):
                    chunk = self.sock.recv(64).decode()
                    data += chunk
                    # print(data)
                    if data[-2:] == '\r\n':
                        self.callback(['OK', cmd_name, data])
                        break
                else:
                    data = ''
                    self.callback(['connection error', ])
                    break
        except Exception as e:
            # print(e)
            self.callback(['connection error', ])
            '''
            clear the queue
            '''
            try:
                while True:
                    self.queue.get(False)
            except queue.Empty:
                pass
            self.sock.close()  # close connection
