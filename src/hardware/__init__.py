"""Hardware command sets for the monitoring application."""

from . import simulated

AVAILABLE_COMMAND_SETS = {
    "simulated": simulated.COMMANDS,
}
