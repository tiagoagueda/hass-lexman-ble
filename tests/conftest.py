"""Pytest configuration: make the vendored lexman_ble package importable."""

import sys
from pathlib import Path

# Add custom_components/lexman_ble to sys.path so `import lexman_ble` works
# in tests (the package lives at custom_components/lexman_ble/lexman_ble/).
sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent / "custom_components" / "lexman_ble")
)
