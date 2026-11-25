"""Tests for the vendored library's LexmanCCTSmartBulbState model."""

from lexman_ble.models import LexmanCCTSmartBulbState


def test_temperature_kelvin_none() -> None:
    """A state with no temperature returns None kelvin."""
    state = LexmanCCTSmartBulbState()
    assert state.temperature_kelvin is None


def test_temperature_kelvin_min() -> None:
    """Device temperature min (153) maps to 6500 K (cool)."""
    state = LexmanCCTSmartBulbState(temperature=153)
    assert state.temperature_kelvin == 6500


def test_temperature_kelvin_max() -> None:
    """Device temperature max (454) maps to 2700 K (warm)."""
    state = LexmanCCTSmartBulbState(temperature=454)
    assert state.temperature_kelvin == 2700


def test_temperature_kelvin_mid() -> None:
    """Mid-range device temperature maps to mid-range kelvin."""
    # (303 - 153) * (2700 - 6500) / (454 - 153) + 6500
    # = 150 * (-3800) / 301 + 6500
    # = -570000 / 301 + 6500
    # = -1893.69... + 6500 = 4606.31... -> 4606
    state = LexmanCCTSmartBulbState(temperature=303)
    assert state.temperature_kelvin == 4606


def test_state_defaults() -> None:
    """A fresh state has all fields None."""
    state = LexmanCCTSmartBulbState()
    assert state.power is None
    assert state.brightness is None
    assert state.temperature is None
