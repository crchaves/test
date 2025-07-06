# COTS Monitoring Application

This repository contains a small example Python application used to monitor a
(simulated) Commercial Off-The-Shelf (COTS) equipment device.

The application periodically polls the device with a configurable housekeeping
interval, records the parameters into a SQLite database and prints events. The
recorded session can later be replayed.

Command sets for each supported hardware type now live in `.ini` files under
`src/driver_configs`. Each file contains a comma separated list of commands in
a `[commands]` section. These files are loaded automatically and used by the
monitoring script.

## Usage


## Serving the Application over HTTPS

To view the HTML interface or any generated data in a browser, you can run a
simple HTTPS server using the provided `serve_https.py` script. First generate a
self‑signed certificate (if you don't have one already):

```bash
openssl req -new -x509 -nodes -out cert.pem -keyout key.pem -days 365
```

Then start the server:

```bash
python serve_https.py --cert cert.pem --key key.pem --directory . --port 8443
```

Open `https://localhost:8443/` in Chrome or Firefox. You may need to accept the
self‑signed certificate warning.
=======
