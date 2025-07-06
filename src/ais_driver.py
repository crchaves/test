"""Minimal driver to read AIS messages from a TCP stream."""
from __future__ import annotations

import json
import socket
from typing import Optional, Dict, Any


class AISDriver:
    """Receive AIS traffic as JSON objects over a TCP connection."""

    def __init__(self, host: str, port: int, timeout: float = 5.0) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self._sock: Optional[socket.socket] = None
        self._buffer = b""

    def connect(self) -> None:
        """Open the socket connection to the AIS feed."""
        if self._sock is not None:
            return
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        sock.connect((self.host, self.port))
        self._sock = sock

    def close(self) -> None:
        """Close the socket connection."""
        if self._sock is not None:
            try:
                self._sock.close()
            finally:
                self._sock = None

    def read_message(self) -> Optional[Dict[str, Any]]:
        """Read a single AIS message from the stream.

        Messages are expected to be newline separated JSON strings. The
        dictionary representation is returned or ``None`` if the connection
        closes.
        """
        if self._sock is None:
            raise RuntimeError("Driver is not connected")
        while b"\n" not in self._buffer:
            data = self._sock.recv(4096)
            if not data:
                return None
            self._buffer += data
        line, self._buffer = self._buffer.split(b"\n", 1)
        line = line.strip()
        if not line:
            return None
        return json.loads(line.decode())

    def __enter__(self) -> "AISDriver":
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
