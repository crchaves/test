"""Simple driver to monitor Keysight equipment using SCPI commands."""

from __future__ import annotations

import socket
from typing import Optional

from . import COMMANDS


class KeysightDriver:
    """A minimal TCP driver for Keysight equipment using SCPI commands."""

    def __init__(self, host: str, port: int = 5025, timeout: float = 5.0) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self._sock: Optional[socket.socket] = None

    def connect(self) -> None:
        """Open the socket connection to the instrument."""
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

    def send_command(self, name: str, value: Optional[str] = None) -> Optional[str]:
        """Send a SCPI command by name.

        Parameters
        ----------
        name: str
            Name of the command as listed in :mod:`keysight_driver`.
        value: Optional[str]
            Optional value to format into the command.

        Returns
        -------
        Optional[str]
            Response from the instrument if the command is a query, otherwise
            ``None``.
        """
        if name not in COMMANDS:
            raise KeyError(f"Unknown command: {name}")

        cmd_template = COMMANDS[name]
        if '{value}' in cmd_template:
            if value is None:
                raise ValueError(f"Command '{name}' requires a value")
            command = cmd_template.format(value=value)
        else:
            command = cmd_template
        return self.raw(command)

    def raw(self, command: str) -> Optional[str]:
        """Send raw SCPI command string.

        If the command ends with a '?', the response is returned as a string.
        Otherwise ``None`` is returned.
        """
        if self._sock is None:
            raise RuntimeError("Driver is not connected")
        # Ensure command ends with newline
        message = command.strip() + '\n'
        self._sock.sendall(message.encode())

        if command.strip().endswith('?'):
            # For query commands, read until newline
            chunks = []
            while True:
                chunk = self._sock.recv(4096)
                if not chunk:
                    break
                chunks.append(chunk)
                if b'\n' in chunk:
                    break
            return b''.join(chunks).decode().strip()
        return None

    def __enter__(self) -> "KeysightDriver":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
