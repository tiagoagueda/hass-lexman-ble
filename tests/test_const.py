"""Tests for the vendored library's const.py helpers."""

from lexman_ble.const import _hex_string_formatting
from lexman_ble.const import CctSmartBulbCommand


def test_hex_string_formatting_no_placeholders() -> None:
    """A template with no placeholders is returned unchanged."""
    assert (
        _hex_string_formatting(CctSmartBulbCommand.PING.query_cmd, 0)
        == "00:00:20:01:02:00:02"
    )


def test_hex_string_formatting_single_placeholder() -> None:
    """A single {0} placeholder is filled with the low byte of the value."""
    result = _hex_string_formatting(CctSmartBulbCommand.SWITCH.set_cmd, 1)
    assert result == "00:00:10:01:03:01:00:00"


def test_hex_string_formatting_value_254() -> None:
    """Value 254 formats as fe in the low byte."""
    result = _hex_string_formatting(CctSmartBulbCommand.BRIGHTNESS.set_cmd, 254)
    assert result == "00:00:11:01:03:fe:00:00"


def test_hex_string_formatting_double_placeholder() -> None:
    """TEMPERATURE set uses {1} (high byte) and {0} (low byte)."""
    # temperature 300 -> 0x012c -> {1}=01, {0}=2c
    result = _hex_string_formatting(CctSmartBulbCommand.TEMPERATURE.set_cmd, 300)
    assert result == "00:00:12:01:04:01:2c:00:00"
