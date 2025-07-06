import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]/"src"))
from src.monitor import EquipmentStatus
from src.equipment_pb import serialize_status, parse_status


def test_round_trip() -> None:
    status = EquipmentStatus(timestamp=1.0, temperature=25.0, voltage=3.3, event="OK")
    data = serialize_status(status)
    result = parse_status(data)
    assert result == status
