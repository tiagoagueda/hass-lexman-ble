# Contributing

Contributions are welcome — bug reports, protocol findings, fixes and new features.

## Reporting bugs

Open an issue on the [issue tracker](https://github.com/tiagoagueda/hass-lexman-ble/issues).
A good report includes:

- Home Assistant version and integration version (`manifest.json` → `version`).
- Your Bluetooth setup: built-in adapter, USB dongle, or ESPHome Bluetooth proxy.
- The bulb model / product page, and what its advertisement looks like if you have it.
- What you expected, what actually happened, and steps to reproduce.
- Debug logs — see [Enabling debug logs](README.md#enabling-debug-logs) in the README.

## Pull requests

1. Fork the repo and branch from `main`.
2. Keep the change focused, and update the documentation it affects.
3. Follow the existing style: `ruff`-formatted Python (88 columns, double quotes),
   type hints on public functions, `from __future__ import annotations` at the top.
4. Use [Conventional Commits](https://www.conventionalcommits.org/) for commit
   messages (`fix:`, `feat:`, `docs:`, `chore:` …).
5. Add an entry under `## [Unreleased]` in [CHANGELOG.md](CHANGELOG.md).
6. Open the pull request.

## Repository layout

This repo ships the integration and nothing else — no build system, no test suite,
no linters, no CI. Home Assistant loads the files as they are.

```text
custom_components/lexman_ble/          # the integration (HA-facing code)
custom_components/lexman_ble/lexman_ble/   # vendored BLE device library
hacs.json                              # HACS metadata
```

Keep the BLE wire protocol inside the vendored library and keep Home Assistant
imports out of it, so it stays testable and reusable on its own.

The full development environment — uv, pre-commit, devcontainer, hassfest/HACS CI —
lives in the upstream project,
[davidsmfreire/lexman-ble](https://github.com/davidsmfreire/lexman-ble). If a change
needs that tooling, work there or set it up here in a separate PR.

## Testing a change

There is no automated test suite. To verify a change by hand:

1. Copy `custom_components/lexman_ble/` into your Home Assistant `config/custom_components/`
   directory (or symlink it) and restart Home Assistant.
2. Add the integration and exercise on/off, brightness and colour temperature —
   including changes made from another controller, to confirm push updates arrive.
3. Attach the debug logs for the scenario you fixed to the pull request.

## Releasing (maintainers)

1. Bump `version` in [`custom_components/lexman_ble/manifest.json`](custom_components/lexman_ble/manifest.json).
2. Move the `## [Unreleased]` entries into a new dated version section in `CHANGELOG.md`.
3. Tag and publish a GitHub release on the mirror — HACS offers the update from there.

## License

By contributing, you agree that your contributions will be licensed under the
project's [MIT License](LICENSE).
