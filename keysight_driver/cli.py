"""Command line interface to send SCPI commands to Keysight equipment."""

import argparse
from typing import Optional

from .driver import KeysightDriver
from . import COMMANDS


def list_commands() -> None:
    for name, scpi in COMMANDS.items():
        print(f"{name}: {scpi}")


def main(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Keysight SCPI command utility")
    parser.add_argument("host", help="IP address of the instrument")
    parser.add_argument("command", nargs="?", help="Command name to send")
    parser.add_argument("value", nargs="?", help="Optional value for the command")
    parser.add_argument("--port", type=int, default=5025, help="Instrument port")
    parser.add_argument("--list", action="store_true", help="List available commands")
    args = parser.parse_args(argv)

    if args.list:
        list_commands()
        return

    if args.command is None:
        parser.error("command name required unless --list is given")

    driver = KeysightDriver(args.host, port=args.port)
    with driver:
        response = driver.send_command(args.command, args.value)
        if response is not None:
            print(response)


if __name__ == "__main__":
    main()
