import struct

from .monitor import EquipmentStatus


def _encode_varint(value: int) -> bytes:
    out = bytearray()
    while value > 0x7F:
        out.append((value & 0x7F) | 0x80)
        value >>= 7
    out.append(value)
    return bytes(out)


def _decode_varint(data: bytes, offset: int) -> tuple[int, int]:
    shift = 0
    value = 0
    while True:
        b = data[offset]
        offset += 1
        value |= (b & 0x7F) << shift
        if not (b & 0x80):
            break
        shift += 7
    return value, offset


def serialize_status(status: EquipmentStatus) -> bytes:
    out = bytearray()
    # field 1: timestamp (double, wire type 1)
    out += _encode_varint(1 << 3 | 1)
    out += struct.pack('<d', status.timestamp)
    # field 2: temperature (double)
    out += _encode_varint(2 << 3 | 1)
    out += struct.pack('<d', status.temperature)
    # field 3: voltage (double)
    out += _encode_varint(3 << 3 | 1)
    out += struct.pack('<d', status.voltage)
    # field 4: event (string, optional)
    if status.event is not None:
        data = status.event.encode()
        out += _encode_varint(4 << 3 | 2)
        out += _encode_varint(len(data))
        out += data
    return bytes(out)


def parse_status(data: bytes) -> EquipmentStatus:
    offset = 0
    kwargs = {'timestamp': 0.0, 'temperature': 0.0, 'voltage': 0.0, 'event': None}
    while offset < len(data):
        tag, offset = _decode_varint(data, offset)
        field = tag >> 3
        wire = tag & 0x7
        if field == 1 and wire == 1:
            kwargs['timestamp'] = struct.unpack_from('<d', data, offset)[0]
            offset += 8
        elif field == 2 and wire == 1:
            kwargs['temperature'] = struct.unpack_from('<d', data, offset)[0]
            offset += 8
        elif field == 3 and wire == 1:
            kwargs['voltage'] = struct.unpack_from('<d', data, offset)[0]
            offset += 8
        elif field == 4 and wire == 2:
            length, offset = _decode_varint(data, offset)
            kwargs['event'] = data[offset:offset+length].decode()
            offset += length
        else:
            if wire == 0:
                _, offset = _decode_varint(data, offset)
            elif wire == 1:
                offset += 8
            elif wire == 2:
                length, offset = _decode_varint(data, offset)
                offset += length
            elif wire == 5:
                offset += 4
            else:
                raise ValueError('Unsupported wire type')
    return EquipmentStatus(**kwargs)

__all__ = ['serialize_status', 'parse_status']
