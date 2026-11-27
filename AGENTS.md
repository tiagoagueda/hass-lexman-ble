# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, Codex, etc.) when working with code in this repository.

## What this repo is

A **self-contained Home Assistant custom integration** (Home Assistant Marketplace — formerly HACS, built into Core since 2026.11 — category `integration`) for Lexman/Leroy Merlin CCT smart bulbs over Bluetooth LE. Everything shippable lives under [custom_components/lexman_ble/](custom_components/lexman_ble/); the rest of the repo is documentation.

This is a **distribution-only repo**: there is no build system or dependency manager. Nothing here is installed or compiled — Home Assistant imports the files as they are. Do not add `poetry`/`uv` commands to docs or assume they exist; if you need that tooling, add it deliberately and update this file (`AGENTS.md`). The upstream project [davidsmfreire/lexman-ble](https://github.com/davidsmfreire/lexman-ble) still carries the full dev environment.

Dev tooling used by Forgejo CI (`ruff`, `pytest`) is declared in `requirements-dev.txt` (hassfest runs as a Docker action) and is **not** shipped to users — it is only used by CI and contributors. See the Continuous integration section below.

Git origin is a self-hosted forge (`source.tiagoagueda.com`); `github.com/tiagoagueda/hass-lexman-ble` is the public mirror and the URL the Marketplace installs from, so all user-facing links in docs and `manifest.json` must point at GitHub.

## Versioning & releases

**Only one version number exists**: `version` in [manifest.json](custom_components/lexman_ble/manifest.json). Bump it by hand when you want the Marketplace to offer users an update, and add a matching entry to [CHANGELOG.md](CHANGELOG.md). The Marketplace picks the new version up from a **published** GitHub release (a bare tag is not enough; without releases it falls back to the default branch). `version` must match the release tag.

The BLE library is **vendored**, not a dependency — editing it takes effect for users on the next integration update, with no publish step. The only third-party runtime requirement is `parse` (declared in `manifest.json` `requirements`). Home Assistant's Bluetooth stack already provides `bleak`, `bleak-retry-connector` and `bluetooth-data-tools`, so those are **not** redeclared.

## Marketplace / hassfest compliance

- `manifest.json` keys: `domain`, `name`, then the rest **alphabetically** (hassfest enforces this). Do **not** put `homeassistant` in `manifest.json` — the custom-integration schema rejects it; the minimum HA version lives in [hacs.json](hacs.json).
- `categories` (`lighting.bulbs_lamps`) is required by the Marketplace validator.
- Brand images live in [brand/](custom_components/lexman_ble/brand/) (`icon.png` 256×256, `@2x` 512×512, `logo.png`); [images/](images/) holds the copies the README uses.
- The GitHub mirror needs a description, topics and issues enabled for the Marketplace checks.

## Library architecture (vendored: `custom_components/lexman_ble/lexman_ble/`)

Imported by relative import (`from .lexman_ble import ...`). Keep Home Assistant imports out of this package — it must stay a plain BLE library.

The device protocol lives in [lexman_ble/const.py](custom_components/lexman_ble/lexman_ble/const.py):

- `CctSmartBulbCommand` is an `Enum` where each member carries a `(set, query, response)` triple of colon-separated hex templates with `{0}`/`{1}` byte placeholders (little-endian, split across bytes).
- `_hex_string_formatting` fills placeholders to build request bytes; `_hex_string_parsing` reverse-parses notification responses back into an int, validating that repeated placeholders agree.
- `CctSmartBulbCommandInstance` is a per-call wrapper (`.set(value)` / `.query` / `.match_response(...)`) that holds the concrete value and produces `request_bytes`.

[lexman_ble/cct_smart_bulb.py](custom_components/lexman_ble/lexman_ble/cct_smart_bulb.py) — `LexmanCCTSmartBulb` is the connection-managing device class, modeled on the `led_ble` / Bluetooth-Devices pattern:

- Uses `bleak` + `bleak_retry_connector` (`establish_connection`, `@retry_bluetooth_connection_error`).
- Lazy connect on command, auto-disconnect after `DISCONNECT_DELAY` (120 s) of inactivity; `_connect_lock` and `_operation_lock` serialize access.
- Commands are **fire-and-confirm**: writes go to `WRITE_CHAR_UUID`, and the _actual_ state is updated in `_notification_handler` from notifications on `READ_CHAR_UUID`, then `_fire_callbacks()` notifies subscribers (the HA coordinator). `set_*` methods optimistically update local state too.
- Brightness is 0–254 on the wire but exposed as 0–255 (HA) and set via 0–100 (%). Colour temperature maps between device units (153 cool … 454 warm) and Kelvin (6500 cool … 2700 warm) — note the inverted ordering, see `CCT_TEMPERATURE_*` constants.

## Integration architecture (`custom_components/lexman_ble/`)

Standard modern HA BLE config-entry integration. Note two `const.py`/`models.py` pairs exist — one for the integration, one for the vendored library; they are distinct modules.

- [config_flow.py](custom_components/lexman_ble/config_flow.py) — Bluetooth discovery flow. Devices are identified by the vendor service UUID `SERVICE_UUID` (see [const.py](custom_components/lexman_ble/const.py)), **not** the generic advertised name. The manifest `bluetooth` matcher pairs `manufacturer_id: 5393` with that custom UUID — do not relax it to `manufacturer_id` alone (sibling Lexman/Adeo BLE products share the manufacturer id but speak a different protocol; the comment on `SERVICE_UUID` explains this).
- [`__init__.py`](custom_components/lexman_ble/__init__.py) — `async_setup_entry` resolves the `BLEDevice` from the address, builds a `LexmanCCTSmartBulb`, wraps it in a `DataUpdateCoordinator` (polls every `UPDATE_SECONDS` = 15 s), registers a passive BLE advertisement callback to refresh the device handle, and waits for a first notification (`startup_event`) before declaring the entry ready.
- Runtime objects are passed via `entry.runtime_data` typed as `LexmanConfigEntry` ([typing.py](custom_components/lexman_ble/typing.py)) holding `LexmanCCTSmartBulbData` ([models.py](custom_components/lexman_ble/models.py)).
- [light.py](custom_components/lexman_ble/light.py) — the only platform (`Platform.LIGHT`); a `CoordinatorEntity` + `LightEntity` in `COLOR_TEMP` mode. It subscribes to the device's own callback in `async_added_to_hass` for push updates, on top of coordinator polling.
- Config-flow UI strings: [strings.json](custom_components/lexman_ble/strings.json) is the source, but custom integrations are **not** processed by Core's translation build step, so a literal-English [translations/en.json](custom_components/lexman_ble/translations/en.json) (with `[%key:...%]` references resolved) must be shipped and kept in sync.

## Conventions

- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/). Nothing enforces or automates this here — it is stylistic.
- Code style is `ruff`-formatted (88 cols, double quotes) to match upstream; `ruff check` and `ruff format --check` run in Forgejo CI.
- When extending: keep the BLE wire protocol in the vendored library, keep HA imports out of it, bump `manifest.json` `version` and update `CHANGELOG.md` to release.

## Continuous integration

Forgejo CI runs on every push and pull request to `main` (`.forgejo/workflows/ci.yml`):

1. **lint** — `ruff check` and `ruff format --check` on the integration and tests.
2. **test** — `pytest` against `tests/` (pure logic: hex formatting/parsing, command matching, temperature/brightness conversions — no BLE hardware required).
3. **hassfest** — Home Assistant's `hassfest` validator, run via the official `home-assistant/actions/hassfest` Docker action (hassfest is part of Core, not a pip package); this job is **blocking** because it enforces `manifest.json` key ordering, `strings.json`/`translations` consistency and Marketplace compliance.

Locally, you can run the CI-equivalent checks with:

```sh
pip install -r requirements-dev.txt
ruff check custom_components/lexman_ble tests
ruff format --check custom_components/lexman_ble tests
pytest -v tests
docker run --rm -v "$PWD":/github/workspace ghcr.io/home-assistant/hassfest
```

Tests live in `tests/` and exercise only the vendored library's pure-logic functions — no real BLE device is needed.
