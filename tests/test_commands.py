"""Tests for CctSmartBulbCommandInstance request building and response matching."""

from lexman_ble.const import CctSmartBulbCommand


def test_switch_set_request_bytes() -> None:
    """SWITCH.set(1) builds the correct request bytes."""
    cmd = CctSmartBulbCommand.SWITCH.set(1)
    assert cmd.request_bytes == bytes.fromhex("0000100103010000")


def test_switch_set_zero_request_bytes() -> None:
    """SWITCH.set(0) builds the correct request bytes."""
    cmd = CctSmartBulbCommand.SWITCH.set(0)
    assert cmd.request_bytes == bytes.fromhex("0000100103000000")


def test_switch_query_request_bytes() -> None:
    """SWITCH.query builds the correct request bytes."""
    cmd = CctSmartBulbCommand.SWITCH.query
    assert cmd.request_bytes == bytes.fromhex("00001002")


def test_brightness_set_request_bytes() -> None:
    """BRIGHTNESS.set(128) builds the correct request bytes."""
    cmd = CctSmartBulbCommand.BRIGHTNESS.set(128)
    assert cmd.request_bytes == bytes.fromhex("0000110103800000")


def test_temperature_set_request_bytes() -> None:
    """TEMPERATURE.set(300) builds the correct request bytes."""
    cmd = CctSmartBulbCommand.TEMPERATURE.set(300)
    assert cmd.request_bytes == bytes.fromhex("0000120104012c0000")


def test_match_response_switch_on() -> None:
    """A SWITCH on response matches and returns value 1."""
    cmd = CctSmartBulbCommand.SWITCH.set(1)
    matched, value = cmd.match_response("00:00:10:03:02:01:01")
    assert matched is True
    assert value == 1


def test_match_response_switch_off() -> None:
    """A SWITCH off response matches and returns value 0."""
    cmd = CctSmartBulbCommand.SWITCH.set(0)
    matched, value = cmd.match_response("00:00:10:03:02:00:00")
    assert matched is True
    assert value == 0


def test_match_response_switch_wrong_value() -> None:
    """A SWITCH response that does not match the expected value does not match."""
    cmd = CctSmartBulbCommand.SWITCH.set(1)
    matched, _value = cmd.match_response("00:00:10:03:02:00:00")
    assert matched is False


def test_match_response_brightness() -> None:
    """A BRIGHTNESS response matches and returns the brightness byte."""
    cmd = CctSmartBulbCommand.BRIGHTNESS.query
    matched, value = cmd.match_response("00:00:11:03:02:80:80")
    assert matched is True
    assert value == 0x80


def test_match_response_temperature() -> None:
    """A TEMPERATURE response matches and returns the temperature."""
    cmd = CctSmartBulbCommand.TEMPERATURE.query
    matched, value = cmd.match_response("00:00:12:03:04:01:2c:01:2c")
    assert matched is True
    assert value == 0x012C  # 300


def test_match_response_unknown() -> None:
    """A response that matches no command returns no match."""
    cmd = CctSmartBulbCommand.SWITCH.query
    matched, _value = cmd.match_response("00:00:99:00:00:00:00")
    assert matched is False


def test_ping_query_request_bytes() -> None:
    """PING.query builds the correct request bytes."""
    cmd = CctSmartBulbCommand.PING.query
    assert cmd.request_bytes == bytes.fromhex("00002001020002")


def test_ping_match_response() -> None:
    """A PING response matches the PING query template."""
    cmd = CctSmartBulbCommand.PING.query
    matched, _value = cmd.match_response("00:00:20:03:02:00:02")
    assert matched is True
