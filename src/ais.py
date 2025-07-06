"""AIS traffic replay utilities."""

from __future__ import annotations

import time


def replay_ais(path: str, *, delay: float = 0.0) -> None:
    """Replay AIS NMEA sentences from ``path``.

    Each non-empty line is printed to ``stdout``. If ``delay`` is greater than
    zero, the function waits the specified number of seconds between lines.
    """
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            sentence = line.strip()
            if not sentence:
                continue
            print(sentence)
            if delay > 0:
                time.sleep(delay)

__all__ = ["replay_ais"]
