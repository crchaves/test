"""Minimal driver to read navigation NMEA sentences from a TCP stream."""
from __future__ import annotations

import socket
from typing import Optional, Iterable


class NMEADriver:
    """Receive NMEA0183 sentences over a TCP connection."""

    def __init__(self, host: str, port: int, timeout: float = 5.0) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self._sock: Optional[socket.socket] = None
        self._buffer = b""

    def connect(self) -> None:
        """Open the socket connection to the NMEA feed."""
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

    def read_sentence(self, allowed: Optional[Iterable[str]] = None) -> Optional[str]:
        """Read a single NMEA sentence from the stream.

        Parameters
        ----------
        allowed:
            Optional iterable of 3-letter sentence identifiers to filter. If
            provided, sentences that don't match are skipped until a matching one
            is read.
        """
        if self._sock is None:
            raise RuntimeError("Driver is not connected")
        allowed_set = {s.upper() for s in allowed} if allowed else None
        while True:
            while b"\n" not in self._buffer:
                data = self._sock.recv(4096)
                if not data:
                    return None
                self._buffer += data
            line, self._buffer = self._buffer.split(b"\n", 1)
            sentence = line.strip().decode()
            if not sentence:
                continue
            if allowed_set:
                # Sentence type is characters 3-5 after the '$' prefix
                name = sentence.lstrip("$")[:5]
                msg_id = name[2:5] if len(name) >= 5 else name
                if msg_id.upper() not in allowed_set:
                    continue
            return sentence

    def __enter__(self) -> "NMEADriver":
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

__all__ = ["NMEADriver"]
