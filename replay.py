import json
import time

class SessionEvent:
    def __init__(self, timestamp, event_type, data):
        self.timestamp = timestamp
        self.event_type = event_type
        self.data = data


class SessionRecorder:
    def __init__(self):
        self.events = []
        self.parameters = {}

    def record_event(self, event_type, data):
        self.events.append(SessionEvent(time.time(), event_type, data))

    def set_parameter(self, name, value):
        self.parameters[name] = value

    def export(self, path):
        with open(path, 'w') as f:
            json.dump(
                {
                    'parameters': self.parameters,
                    'events': [
                        {'timestamp': e.timestamp, 'type': e.event_type, 'data': e.data}
                        for e in self.events
                    ],
                },
                f,
                indent=2,
            )


class SessionReplayer:
    def __init__(self, log_path):
        with open(log_path) as f:
            data = json.load(f)
        self.parameters = data.get('parameters', {})
        self.events = data.get('events', [])
        self.index = 0

    def replay_next(self):
        if self.index < len(self.events):
            event = self.events[self.index]
            print(f"{event['timestamp']}: {event['type']} -> {event['data']}")
            self.index += 1
            return True
        return False

    def replay_all(self, delay=0):
        while self.replay_next():
            if delay:
                time.sleep(delay)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Replay session log')
    parser.add_argument('log', help='Path to log file')
    parser.add_argument('--delay', type=float, default=0, help='Delay between events')
    args = parser.parse_args()

    replayer = SessionReplayer(args.log)
    replayer.replay_all(delay=args.delay)
