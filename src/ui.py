import argparse
import configparser
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class ParameterGroup:
    """Group of parameters defined in the config file."""

    name: str
    parameters: List[Tuple[str, str]]


def load_groups(config_path: str) -> List[ParameterGroup]:
    """Load parameter groups from an ini configuration file."""
    parser = configparser.ConfigParser()
    parser.read(config_path)
    groups: List[ParameterGroup] = []
    for section in parser.sections():
        items = list(parser.items(section))
        groups.append(ParameterGroup(name=section, parameters=items))
    return groups


def display_interface(groups: List[ParameterGroup]) -> None:
    """Display the groups and their parameters on the console."""
    for group in groups:
        print(f"{group.name}:")
        for key, value in group.parameters:
            print(f"  {key} = {value}")
        print()


def main() -> None:
    argp = argparse.ArgumentParser(
        description="Display a simple interface defined by an ini file"
    )
    argp.add_argument("config", help="Path to the ini configuration file")
    args = argp.parse_args()

    groups = load_groups(args.config)
    display_interface(groups)


if __name__ == "__main__":
    main()
