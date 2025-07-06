import socket
import threading

import pytest

from src.snmp import snmp_get, _encode_sequence, _encode_integer, _encode_octet_string, _encode_oid


class DummySNMPServer(threading.Thread):
    def __init__(self, oid: str, value: str):
        super().__init__(daemon=True)
        self.oid = oid
        self.value = value
        self.port = None
        self._stop = threading.Event()

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("localhost", 0))
        self.port = sock.getsockname()[1]
        while not self._stop.is_set():
            try:
                data, addr = sock.recvfrom(4096)
            except Exception:
                continue
            pos = data.find(b"\xa0")
            if pos == -1:
                continue
            length = data[pos + 1]
            req_pos = pos + 2
            if data[req_pos] != 0x02:
                continue
            req_len = data[req_pos + 1]
            req_id = int.from_bytes(data[req_pos + 2 : req_pos + 2 + req_len], "big")
            vb = _encode_sequence(_encode_oid(self.oid) + _encode_octet_string(self.value))
            vbl = _encode_sequence(vb)
            body = _encode_integer(req_id) + _encode_integer(0) + _encode_integer(0) + vbl
            pdu = _encode_sequence(body, tag=b"\xA2")
            resp = _encode_sequence(_encode_integer(0) + _encode_octet_string("public") + pdu)
            response = resp
            sock.sendto(response, addr)
        sock.close()

    def stop(self):
        self._stop.set()


def test_snmp_get():
    server = DummySNMPServer("1.3.6.1.2.1.1.1.0", "demo")
    server.start()
    while server.port is None:
        pass

    result = snmp_get("localhost", "1.3.6.1.2.1.1.1.0", port=server.port)
    server.stop()
    assert result == "demo"
