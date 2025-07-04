# COTS Monitoring Application

This repository contains a small example Python application used to monitor a
(simulated) Commercial Off-The-Shelf (COTS) equipment device.

The application periodically polls the device with a configurable housekeeping
interval, records the parameters into a SQLite database and prints events. The
recorded session can later be replayed.

Command sets for each supported hardware type live in `src/hardware`. The
`simulated` module lists the commands used by the built-in simulated device.

## Usage

```bash
python src/monitor.py run --db monitor.db --interval 5
```

Stop the monitoring with `Ctrl+C`. To replay all recorded measurements:

```bash
python src/monitor.py replay --db monitor.db
```

The script uses a default database file `monitor.db` in the current directory
and restricts the polling interval to the range of 1–10 seconds.
