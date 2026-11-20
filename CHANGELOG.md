# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
The version that matters to users is the `version` field in
[`custom_components/lexman_ble/manifest.json`](custom_components/lexman_ble/manifest.json) —
that is what the Marketplace (formerly HACS) reads to offer an update.

## [Unreleased]

## [0.3.0] - 2026-11-20

### Added

- Brand images in `custom_components/lexman_ble/brand/` (icon and logo, light
  and @2x), as used by Home Assistant 2026.3+ and the Marketplace.
- `categories: ["lighting.bulbs_lamps"]` in `manifest.json` for the Marketplace.

### Changed

- Checked against Home Assistant 2026.11 and its built-in Marketplace (formerly
  HACS); README now documents installing from the Marketplace.
- Minimum Home Assistant version raised to 2025.2.0 (`hacs.json`); the light
  platform now uses `AddConfigEntryEntitiesCallback`.
- `CLAUDE.md` renamed to `AGENTS.md`.

### Fixed

- Removed the invalid `homeassistant` key from `manifest.json` (the minimum
  version lives in `hacs.json`) and sorted manifest keys as hassfest requires.

## [0.2.0] - 2026-08-15

### Added

- French (`fr`) and Portuguese (`pt`) translations for the config flow.
- `.gitattributes` pinning all text files to LF line endings.

### Changed

- Repository moved to `tiagoagueda/hass-lexman-ble`; `documentation` and
  `issue_tracker` in `manifest.json` now point there.
- Repository slimmed down to the shippable integration: `custom_components/`,
  `hacs.json` and docs. Development tooling (uv/pyproject, Makefile, pre-commit,
  devcontainer, CI workflows) is no longer carried here.
- Rewritten `README.md` with requirements, supported devices, troubleshooting
  and debug-logging instructions.

## [0.1.1] - 2026-03-03

### Added

- The `lexman_ble` BLE device library is now **vendored** into the integration at
  `custom_components/lexman_ble/lexman_ble/`. It is no longer a PyPI dependency,
  so protocol fixes ship straight through HACS with no package release.

### Fixed

- Light state coherency: the entity now reflects the state reported by the bulb's
  notifications instead of drifting from optimistic local updates.

## [0.1.0] - 2024-12-23

### Added

- Initial release: Bluetooth discovery config flow and a `light` platform with
  on/off, brightness and 2700 K–6500 K colour temperature control for Lexman CCT
  smart bulbs.

---

Releases up to and including 0.1.0 were made in the upstream project,
[davidsmfreire/lexman-ble](https://github.com/davidsmfreire/lexman-ble), from which
this integration is forked. See its
[CHANGELOG](https://github.com/davidsmfreire/lexman-ble/blob/main/CHANGELOG.md)
for the per-commit history of that period.

[unreleased]: https://github.com/tiagoagueda/hass-lexman-ble/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/tiagoagueda/hass-lexman-ble/releases/tag/v0.3.0
[0.2.0]: https://github.com/tiagoagueda/hass-lexman-ble/releases/tag/v0.2.0
[0.1.1]: https://github.com/tiagoagueda/hass-lexman-ble/releases/tag/v0.1.1
[0.1.0]: https://github.com/tiagoagueda/hass-lexman-ble/releases/tag/v0.1.0
