import socket
import threading

import pytest

from keysight_driver.driver import KeysightDriver
from keysight_driver import COMMANDS


class DummyServer(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.responses = {
            COMMANDS['GET_BFILE_FILE']: b'DEMO\n',
        }
        self._stop = threading.Event()
        self.port = None

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 0))
        self.port = server.getsockname()[1]
        server.listen(1)
        conn, _ = server.accept()
        while not self._stop.is_set():
            data = conn.recv(4096)
            if not data:
                break
            command = data.decode().strip()
            resp = self.responses.get(command)
            if resp:
                conn.sendall(resp)
        conn.close()
        server.close()

    def stop(self):
        self._stop.set()


def test_send_command():
    server = DummyServer()
    server.start()
    while server.port is None:
        pass

    driver = KeysightDriver('localhost', port=server.port)
    with driver:
        result = driver.send_command('GET_BFILE_FILE')
    server.stop()
    assert result == 'DEMO'
