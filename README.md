# Test Repository

This repository contains a static web page and a simple subsystem for recording
and replaying sessions.

## Replay Subsystem

The `replay.py` script can replay events from a JSON log file. A sample log
(`example_log.json`) is provided.

### Usage

```
python replay.py example_log.json --delay 1
```

This will print each recorded event, waiting one second between events.

You can also use `SessionRecorder` from the script to record new sessions and
export them as JSON logs.
