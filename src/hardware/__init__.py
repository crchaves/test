"""Hardware command sets for the monitoring application.

Command lists are stored in ``.ini`` files located in ``src/driver_configs``.
Each file has a ``[commands]`` section with a comma separated ``list`` of
commands. All ``.ini`` files in that directory are automatically loaded at
import time.
"""

from __future__ import annotations

import configparser
from pathlib import Path
from typing import Dict, List, Tuple


def _load_config(path: Path) -> Tuple[list[str], Dict[str, str]]:
    parser = configparser.ConfigParser()
    parser.read(path)
    commands: list[str] = []
    params: Dict[str, str] = {}
    if parser.has_section("commands"):
        raw = parser.get("commands", "list", fallback="")
        if raw:
            commands = [c.strip() for c in raw.split(",") if c.strip()]
    if parser.has_section("parameters"):
        for name, oid in parser.items("parameters"):
            params[name] = oid.strip()
    return commands, params


def _discover_configs() -> Tuple[Dict[str, List[str]], Dict[str, Dict[str, str]]]:
    base = Path(__file__).resolve().parent.parent / "driver_configs"
    command_sets: Dict[str, List[str]] = {}
    parameter_sets: Dict[str, Dict[str, str]] = {}
    if base.exists():
        for ini in base.glob("*.ini"):
            cmds, params = _load_config(ini)
            command_sets[ini.stem] = cmds
            parameter_sets[ini.stem] = params
    return command_sets, parameter_sets


AVAILABLE_COMMAND_SETS, AVAILABLE_SNMP_PARAMS = _discover_configs()
