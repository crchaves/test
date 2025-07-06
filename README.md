# COTS Monitoring and Control Application

This repository contains a small example Python application used to monitor and
control a (simulated) Commercial Off-The-Shelf (COTS) equipment device.

The application periodically polls the device with a configurable housekeeping
interval, records the parameters into a SQLite database and prints events. The
recorded session can later be replayed. It also supports sending simple control
commands to the equipment.


Each command used to talk to the equipment is stored once in the database with
a unique identifier. These entries live in the `commands` table and allow a
single ID to be referenced for a request.

Command sets for each supported hardware type live in `src/hardware`. The
`simulated` module lists the commands used by the built-in simulated device.

Command sets for each supported hardware type now live in `.ini` files under
`src/driver_configs`. Each file contains a comma separated list of commands in
a `[commands]` section. These files are loaded automatically and used by the
monitoring script.

## Checkout and Setup

Clone the repository and create a virtual environment (optional):



The application only relies on the Python standard library so no additional
packages are required.


## Usage


## Serving the Application over HTTPS

To view the HTML interface or any generated data in a browser, you can run a
simple HTTPS server using the provided `serve_https.py` script. First generate a
self‑signed certificate (if you don't have one already):


To send a control command to the device:

```bash
python src/monitor.py control --cmd RESET
```

The script uses a default database file `monitor.db` in the current directory
and restricts the polling interval to the range of 1–10 seconds.


## Configurable Parameter Interface

A helper script `src/ui.py` reads parameter groups from an ini file and
prints them as a simple text interface. Each section in the ini file is treated
as a parameter group. Example configuration:

```ini
[inputs]
set_voltage = SET_VOLTAGE
enable = ENABLE_OUTPUT

[outputs]
temperature = READ_TEMPERATURE
voltage = READ_VOLTAGE
```

Run the interface with:

```bash
python src/ui.py config.ini
```

This will display the defined parameter groups and the associated values.

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

### SNMP Devices

Devices that expose an SNMP interface can also be monitored. For each hardware
type with an accompanying MIB, add an ini file under `src/driver_configs` with a
`[parameters]` section mapping parameter names to OIDs. Example:

```ini
[parameters]
temperature = 1.3.6.1.4.1.9999.1.1
voltage = 1.3.6.1.4.1.9999.1.2
```

Use the `snmp` command to start monitoring:

```bash
python src/monitor.py snmp --config config.json --db snmp.db
```


## AIS Map

The `index.html` page now displays a small map using the Leaflet library. When
served with `serve_https.py`, it will load sample AIS data from
`ais_sample.json` and plot vessel positions. Edit the JSON file or replace it
with real AIS traffic to visualize different data.


### AIS Traffic Replay

Recorded AIS NMEA sentences can be replayed using the simulator. Each
non‑empty line from a log file is printed back to the console. Use the
`ais` command of `simulator/simulate.py`:

```bash
python -m simulator.simulate ais path/to/traffic.log --delay 0.5
```

The optional `--delay` parameter sets a fixed delay between messages.


### AIS Driver

An `AISDriver` class is provided to read AIS messages over a TCP stream. Messages
are expected as newline separated JSON objects. Configure the feed address in
`ais_config.json`:

```json
{
  "ip": "127.0.0.1",
  "port": 10110
}
```

Example usage:

```python
from src.ais_driver import AISDriver

with AISDriver("127.0.0.1", 10110) as drv:
    message = drv.read_message()
    print(message)
```


### NMEA Driver

`NMEADriver` connects to a TCP source that streams NMEA 0183 navigation
sentences such as ``GGA``, ``GLL`` and ``GSA``. Provide the IP address and port
of the feed:

```python
from src.nmea_driver import NMEADriver

with NMEADriver("192.168.1.10", 5000) as drv:
    sentence = drv.read_sentence({"GGA", "GLL", "GSA"})
    print(sentence)
```
