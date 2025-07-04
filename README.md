# COTS Monitoring Application

This repository contains a small example Python application used to monitor a
(simulated) Commercial Off-The-Shelf (COTS) equipment device.

The application periodically polls the device with a configurable housekeeping
interval, records the parameters into a SQLite database and prints events. The
recorded session can later be replayed.

Command sets for each supported hardware type live in `src/hardware`. The
`simulated` module lists the commands used by the built-in simulated device.

## Checkout and Setup

Clone the repository and create a virtual environment (optional):

```bash
git clone <repository-url>
cd <repository-directory>
python -m venv .venv
source .venv/bin/activate
```

The application only relies on the Python standard library so no additional
packages are required.

## Usage

```bash
python src/monitor.py run --db monitor.db --interval 5 --config config.json
```

Stop the monitoring with `Ctrl+C`. To replay all recorded measurements:

```bash
python src/monitor.py replay --db monitor.db
```

The script uses a default database file `monitor.db` in the current directory
and restricts the polling interval to the range of 1–10 seconds.

### Simulator vs Real Device

Runtime options are read from `config.json`. Edit this file to switch between
the built-in simulator and a real device:

```json
{
  "hardware_type": "simulated",
  "ip": "127.0.0.1",
  "port": 10000
}
```

Set `hardware_type` to `real` and provide the `ip` and `port` of your device to
connect to actual hardware. Leaving the default values runs the simulator.
