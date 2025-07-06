import argparse

import random
import sqlite3
import time
from dataclasses import asdict, dataclass

import json
import os
import random
import sqlite3
import time
from dataclasses import dataclass, asdict


from hardware import AVAILABLE_COMMAND_SETS

@dataclass
class Config:
    """Runtime configuration."""

    hardware_type: str = "simulated"
    ip: str | None = None
    port: int | None = None


def load_config(path: str) -> Config:
    """Load configuration from ``path`` if it exists."""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Config(
            hardware_type=data.get("hardware_type", "simulated"),
            ip=data.get("ip"),
            port=data.get("port"),
        )
    return Config()

@dataclass
class EquipmentStatus:
    timestamp: float
    temperature: float
    voltage: float
    event: str | None = None

class Equipment:
    """COTS equipment interface."""

    def __init__(
        self, hardware_type: str = "simulated", ip: str | None = None, port: int | None = None
    ) -> None:
        # Load the list of commands for the chosen hardware type
        self.commands = AVAILABLE_COMMAND_SETS.get(hardware_type, [])
        self.ip = ip
        self.port = port
        self.hardware_type = hardware_type

    def read_parameters(self) -> EquipmentStatus:
        """Read parameters using the configured command set."""
        # The commands would normally be sent to the equipment (possibly using
        # ``self.ip`` and ``self.port``); here we just simulate
        status = EquipmentStatus(
            timestamp=time.time(),
            temperature=20 + random.random() * 5,
            voltage=3.3 + random.random() * 0.1,
        )
        # Random event with low probability
        if random.random() < 0.1:
            status.event = random.choice(["ALARM", "WARN", "INFO"])
        return status

    def send_command(self, command: str) -> str:
        """Send a control command to the equipment."""
        if command not in self.commands:
            raise ValueError(f"Unsupported command: {command}")
        # In a real system this would communicate with the hardware.
        return f"Executed {command}"

def create_tables(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS measurements (
            timestamp REAL PRIMARY KEY,
            temperature REAL,
            voltage REAL,
            event TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT UNIQUE
        )
        """
    )
    conn.commit()

def populate_commands(conn: sqlite3.Connection, commands: list[str]) -> None:
    """Ensure each command exists in the commands table."""
    for cmd in commands:
        conn.execute(
            "INSERT OR IGNORE INTO commands (command) VALUES (?)",
            (cmd,),
        )
    conn.commit()

def store_status(conn: sqlite3.Connection, status: EquipmentStatus) -> None:
    conn.execute(
        "INSERT INTO measurements (timestamp, temperature, voltage, event) VALUES (?, ?, ?, ?)",
        (status.timestamp, status.temperature, status.voltage, status.event),
    )
    conn.commit()

def monitor(db_path: str, interval: int, config_path: str) -> None:
    config = load_config(config_path)
    conn = sqlite3.connect(db_path)
    create_tables(conn)

    equipment = Equipment()
    populate_commands(conn, equipment.commands)

    equipment = Equipment(config.hardware_type, config.ip, config.port)

    try:
        while True:
            status = equipment.read_parameters()
            store_status(conn, status)
            print(f"Stored status: {asdict(status)}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Monitoring stopped.")


def replay(db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    for row in conn.execute("SELECT timestamp, temperature, voltage, event FROM measurements ORDER BY timestamp"):
        ts, temp, volt, event = row
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))
        print(f"{t}: T={temp:.2f}C V={volt:.2f}V Event={event or 'None'}")


def control(command: str) -> None:
    equipment = Equipment()
    try:
        response = equipment.send_command(command)
        print(response)
    except ValueError as exc:
        print(f"Error: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Monitor and control simulated COTS equipment")
    sub = parser.add_subparsers(dest="command", required=True)

    mon = sub.add_parser("run", help="Start monitoring")
    mon.add_argument("--db", default="monitor.db", help="SQLite database path")
    mon.add_argument("--interval", type=int, default=5, help="Housekeeping interval (1-10 seconds)")
    mon.add_argument("--config", default="config.json", help="Path to configuration file")

    rep = sub.add_parser("replay", help="Replay recorded measurements")
    rep.add_argument("--db", default="monitor.db", help="SQLite database path")

    ctrl = sub.add_parser("control", help="Send a control command")
    ctrl.add_argument("--cmd", required=True, help="Command to send")

    args = parser.parse_args()

    if args.command == "run":
        interval = max(1, min(10, args.interval))
        monitor(args.db, interval, args.config)
    elif args.command == "replay":
        replay(args.db)
    elif args.command == "control":
        control(args.cmd)

if __name__ == "__main__":
    main()
