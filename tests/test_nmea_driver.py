import socket
import threading

from src.nmea_driver import NMEADriver


class DummyNMEAServer(threading.Thread):
    def __init__(self, sentence: str):
        super().__init__(daemon=True)
        self.sentence = sentence
        self.port = None
        self._stop = threading.Event()

    def run(self) -> None:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("localhost", 0))
        self.port = server.getsockname()[1]
        server.listen(1)
        conn, _ = server.accept()
        data = self.sentence.encode() + b"\n"
        conn.sendall(data)
        conn.close()
        server.close()
        self._stop.set()

    def stop(self) -> None:
        self._stop.set()


def test_read_sentence() -> None:
    sentence = "$GPGGA,1234,N,5678,E,1,08,1.0,10,M,,,*47"
    server = DummyNMEAServer(sentence)
    server.start()
    while server.port is None:
        pass

    driver = NMEADriver("localhost", server.port)
    with driver:
        result = driver.read_sentence({"GGA", "GLL", "GSA"})
    server.stop()

    assert result == sentence
