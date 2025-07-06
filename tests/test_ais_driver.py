import json
import socket
import threading

import pytest

from src.ais_driver import AISDriver


class DummyAISServer(threading.Thread):
    def __init__(self, message: dict[str, str]):
        super().__init__(daemon=True)
        self.message = message
        self.port = None
        self._stop = threading.Event()

    def run(self) -> None:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("localhost", 0))
        self.port = server.getsockname()[1]
        server.listen(1)
        conn, _ = server.accept()
        data = json.dumps(self.message).encode() + b"\n"
        conn.sendall(data)
        conn.close()
        server.close()
        self._stop.set()

    def stop(self) -> None:
        self._stop.set()


def test_read_message() -> None:
    msg = {"type": "1", "mmsi": "123456789"}
    server = DummyAISServer(msg)
    server.start()
    while server.port is None:
        pass

    driver = AISDriver("localhost", server.port)
    with driver:
        result = driver.read_message()
    server.stop()

    assert result == msg
