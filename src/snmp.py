"""Minimal SNMPv1 client utilities using only the Python standard library."""

from __future__ import annotations

import random
import socket
from typing import Dict, Optional


# --- Basic BER encoding helpers -------------------------------------------------

def _encode_length(length: int) -> bytes:
    if length < 0x80:
        return bytes([length])
    pieces = []
    while length > 0:
        pieces.insert(0, length & 0xFF)
        length >>= 8
    return bytes([0x80 | len(pieces)]) + bytes(pieces)


def _encode_integer(value: int) -> bytes:
    if value == 0:
        content = b"\x00"
    else:
        negative = value < 0
        if negative:
            value = -value - 1
        chunks = []
        while value:
            chunks.insert(0, value & 0xFF)
            value >>= 8
        if chunks and chunks[0] & 0x80:
            chunks.insert(0, 0)
        content = bytes(chunks)
        if negative:
            content = bytes(b ^ 0xFF for b in content)
    return b"\x02" + _encode_length(len(content)) + content


def _encode_octet_string(value: str | bytes) -> bytes:
    if isinstance(value, str):
        value = value.encode()
    return b"\x04" + _encode_length(len(value)) + value


def _encode_null() -> bytes:
    return b"\x05\x00"


def _encode_oid(oid: str) -> bytes:
    parts = [int(p) for p in oid.strip(".").split(".")]
    if len(parts) < 2:
        raise ValueError("OID must have at least two numbers")
    first = 40 * parts[0] + parts[1]
    encoded = bytes([first])
    for part in parts[2:]:
        stack = []
        while True:
            stack.insert(0, part & 0x7F)
            part >>= 7
            if part == 0:
                break
        for i in range(len(stack) - 1):
            stack[i] |= 0x80
        encoded += bytes(stack)
    return b"\x06" + _encode_length(len(encoded)) + encoded


def _encode_sequence(content: bytes, tag: bytes = b"\x30") -> bytes:
    return tag + _encode_length(len(content)) + content


# --- Basic BER decoding helpers -------------------------------------------------

def _decode_length(data: bytes, offset: int) -> tuple[int, int]:
    first = data[offset]
    offset += 1
    if first & 0x80 == 0:
        return first, offset
    n = first & 0x7F
    length = 0
    for _ in range(n):
        length = (length << 8) | data[offset]
        offset += 1
    return length, offset


def _decode_integer(data: bytes, offset: int) -> tuple[int, int]:
    assert data[offset] == 0x02
    length, offset = _decode_length(data, offset + 1)
    value = int.from_bytes(data[offset: offset + length], "big", signed=True)
    offset += length
    return value, offset


def _decode_octet_string(data: bytes, offset: int) -> tuple[str, int]:
    assert data[offset] == 0x04
    length, offset = _decode_length(data, offset + 1)
    value = data[offset: offset + length].decode()
    offset += length
    return value, offset


def _decode_oid(data: bytes, offset: int) -> tuple[str, int]:
    assert data[offset] == 0x06
    length, offset = _decode_length(data, offset + 1)
    end = offset + length
    oid_bytes = data[offset:end]
    offset = end
    if not oid_bytes:
        return "", offset
    first = oid_bytes[0]
    oid = [first // 40, first % 40]
    value = 0
    for b in oid_bytes[1:]:
        value = (value << 7) | (b & 0x7F)
        if not b & 0x80:
            oid.append(value)
            value = 0
    return ".".join(str(i) for i in oid), offset


# --- SNMP message helpers -------------------------------------------------------

def _build_get_request(request_id: int, community: str, oid: str) -> bytes:
    varbind = _encode_sequence(_encode_oid(oid) + _encode_null())
    varlist = _encode_sequence(varbind)
    pdu_body = (
        _encode_integer(request_id)
        + _encode_integer(0)
        + _encode_integer(0)
        + varlist
    )
    pdu = _encode_sequence(pdu_body, tag=b"\xA0")
    msg_body = _encode_integer(0) + _encode_octet_string(community) + pdu
    return _encode_sequence(msg_body)


def _build_set_request(request_id: int, community: str, oid: str, value: str) -> bytes:
    value_field = _encode_octet_string(value)
    varbind = _encode_sequence(_encode_oid(oid) + value_field)
    varlist = _encode_sequence(varbind)
    pdu_body = (
        _encode_integer(request_id)
        + _encode_integer(0)
        + _encode_integer(0)
        + varlist
    )
    pdu = _encode_sequence(pdu_body, tag=b"\xA3")
    msg_body = _encode_integer(0) + _encode_octet_string(community) + pdu
    return _encode_sequence(msg_body)


def _parse_get_response(data: bytes) -> tuple[int, Dict[str, str]]:
    off = 0
    assert data[off] == 0x30
    _, off = _decode_length(data, off + 1)
    _, off = _decode_integer(data, off)
    _, off = _decode_octet_string(data, off)
    assert data[off] == 0xA2
    _, off = _decode_length(data, off + 1)
    request_id, off = _decode_integer(data, off)
    error_status, off = _decode_integer(data, off)
    _, off = _decode_integer(data, off)  # error index
    if error_status != 0:
        return request_id, {}
    assert data[off] == 0x30
    _, off = _decode_length(data, off + 1)
    assert data[off] == 0x30
    _, off = _decode_length(data, off + 1)
    oid, off = _decode_oid(data, off)
    tag = data[off]
    if tag == 0x04:
        value, off = _decode_octet_string(data, off)
    elif tag == 0x02:
        value, off = _decode_integer(data, off)
        value = str(value)
    else:
        length, off = _decode_length(data, off + 1)
        value = data[off: off + length].hex()
        off += length
    return request_id, {oid: value}


# --- Public API -----------------------------------------------------------------

def snmp_get(host: str, oid: str, *, community: str = "public", port: int = 161, timeout: float = 2.0) -> Optional[str]:
    request_id = random.randint(0, 0x7FFFFFFF)
    msg = _build_get_request(request_id, community, oid)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    sock.sendto(msg, (host, port))
    data, _ = sock.recvfrom(4096)
    resp_id, values = _parse_get_response(data)
    if resp_id != request_id:
        return None
    return next(iter(values.values()))


def snmp_set(host: str, oid: str, value: str, *, community: str = "public", port: int = 161, timeout: float = 2.0) -> bool:
    request_id = random.randint(0, 0x7FFFFFFF)
    msg = _build_set_request(request_id, community, oid, value)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    sock.sendto(msg, (host, port))
    data, _ = sock.recvfrom(4096)
    resp_id, _ = _parse_get_response(data)
    return resp_id == request_id


class SNMPDevice:
    """Utility class to query parameters defined in ``params`` mapping."""

    def __init__(self, host: str, params: Dict[str, str], *, community: str = "public", port: int = 161) -> None:
        self.host = host
        self.port = port
        self.community = community
        self.params = params

    def read_all(self) -> Dict[str, Optional[str]]:
        results: Dict[str, Optional[str]] = {}
        for name, oid in self.params.items():
            try:
                results[name] = snmp_get(self.host, oid, community=self.community, port=self.port)
            except Exception:
                results[name] = None
        return results

    def set_value(self, name: str, value: str) -> bool:
        if name not in self.params:
            raise ValueError(f"Unknown parameter: {name}")
        return snmp_set(self.host, self.params[name], value, community=self.community, port=self.port)
