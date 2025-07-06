"""Hardware command sets for the monitoring application.

Command lists are stored in ``.ini`` files located in ``src/driver_configs``.
Each file has a ``[commands]`` section with a comma separated ``list`` of
commands. All ``.ini`` files in that directory are automatically loaded at
import time.
"""

from __future__ import annotations

import configparser
from pathlib import Path
from typing import Dict, List


def _load_command_set(path: Path) -> list[str]:
    parser = configparser.ConfigParser()
    parser.read(path)
    commands: list[str] = []
    if parser.has_section("commands"):
        raw = parser.get("commands", "list", fallback="")
        if raw:
            commands = [c.strip() for c in raw.split(",") if c.strip()]
    return commands


def _discover_command_sets() -> Dict[str, List[str]]:
    base = Path(__file__).resolve().parent.parent / "driver_configs"
    command_sets: Dict[str, List[str]] = {}
    if base.exists():
        for ini in base.glob("*.ini"):
            command_sets[ini.stem] = _load_command_set(ini)
    return command_sets


AVAILABLE_COMMAND_SETS: Dict[str, List[str]] = _discover_command_sets()
