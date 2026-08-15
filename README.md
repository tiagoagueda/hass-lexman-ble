# LexmanBLE

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![Community Forum][forum-shield]][forum]

Home Assistant custom integration for controlling [Lexman (Leroy Merlin / ENKI brand) CCT smart bulbs][product] locally over Bluetooth LE — no cloud, no hub, no vendor app.

![logo][lexmanimg]

The integration is **self-contained**: the BLE device library is vendored under
[`custom_components/lexman_ble/lexman_ble/`](custom_components/lexman_ble/lexman_ble/),
so there is nothing extra to install from PyPI.

## Features

| Platform | Description                                                      |
| -------- | ---------------------------------------------------------------- |
| `light`  | On/off, brightness and colour temperature for a Lexman CCT bulb. |

- **Local push** — the bulb notifies Home Assistant of state changes made from
  a physical switch or another app, with a 15 s poll as a safety net.
- **Automatic discovery** — bulbs are found by the Bluetooth integration and
  appear under **Settings → Devices & Services** with no configuration.
- Colour temperature range: **2700 K (warm) – 6500 K (cool)**.

## Supported devices

Lexman/ENKI CCT (tunable white) BLE bulbs advertising manufacturer ID `5393`
together with service UUID `0000a100-1115-1000-0001-617573746f6d`, such as the
[E27 806 lm connected LED bulb][product].

> [!NOTE]
> Other Lexman/Adeo products share manufacturer ID `5393` but speak a different
> protocol. Discovery deliberately also requires the service UUID above, so those
> devices are ignored rather than added and left broken.

RGB bulbs are **not** supported — only the CCT (white-tuning) models.

## Requirements

- Home Assistant **2025.1.0** or newer.
- A working Bluetooth adapter with the
  [Bluetooth integration](https://www.home-assistant.io/integrations/bluetooth/)
  set up. An [ESPHome Bluetooth proxy](https://esphome.io/projects/?type=bluetooth)
  works too and is the easiest way to reach bulbs far from the HA host.

## Installation

### HACS (recommended)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.][hacs-repo-shield]][hacs-repo]

1. In Home Assistant, open **HACS → ⋮ (top right) → Custom repositories**.
2. Add `https://github.com/tiagoagueda/hass-lexman-ble` with type **Integration**.
3. Search for **LexmanBLE**, download it, and restart Home Assistant.

### Manual

1. Open the directory (folder) of your HA configuration (where `configuration.yaml` lives).
2. If there is no `custom_components` directory there, create it.
3. Copy `custom_components/lexman_ble/` from this repository — including the nested
   `lexman_ble/` library folder — into your `custom_components` directory.
4. Restart Home Assistant.

## Configuration

Configuration is done entirely in the UI; there is nothing to add to `configuration.yaml`.

Powered-on bulbs in range are discovered automatically — look for a **LexmanBLE**
discovery card in **Settings → Devices & Services** and click **Configure**.

To add one manually:

[![Open your Home Assistant instance and start setting up a new integration.][config-flow-shield]][config-flow]

**Settings → Devices & Services → + Add Integration → LexmanBLE**, then pick your
bulb from the list of discovered devices.

Each bulb becomes one device with a single `light` entity.

## Troubleshooting

### No devices found during setup

- Make sure the bulb is powered on and within range of the adapter or Bluetooth proxy.
- The bulb cannot be connected to another client at the same time — close the
  vendor app and disconnect any other controller.
- Confirm the Bluetooth integration itself sees traffic: **Settings → Devices &
  Services → Bluetooth → Configure**.

### Enabling debug logs

Open the integration page and use **Enable debug logging**, or add to
`configuration.yaml` and restart:

```yaml
logger:
  default: warning
  logs:
    custom_components.lexman_ble: debug
    bleak: debug
    bleak_retry_connector: debug
```

Please include these logs when opening an issue.

## Contributing

Bug reports and pull requests are welcome — please open them on the
[issue tracker][issues] and read the [contribution guidelines](CONTRIBUTING.md)
first. When reporting a problem, include your Home Assistant version, the
integration version, your Bluetooth setup (adapter or proxy) and debug logs.

Notable changes are recorded in the [changelog](CHANGELOG.md).

## Credits

This is a fork of [@davidsmfreire](https://github.com/davidsmfreire)'s
[lexman-ble](https://github.com/davidsmfreire/lexman-ble) project, with the BLE
library vendored into the integration. Consider supporting the original author:
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

The original project was generated from [@oncleben31](https://github.com/oncleben31)'s
[Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component)
template, with code template mainly taken from [@Ludeeus](https://github.com/ludeeus)'s
[integration_blueprint][integration_blueprint] template.

The `lexman_ble` library implementation was inspired by
[@Bluetooth-Devices](https://github.com/Bluetooth-Devices)'
[led_ble](https://github.com/Bluetooth-Devices/led-ble) project.

## License

MIT — see [LICENSE](LICENSE).

---

[product]: https://www.leroymerlin.fr/produits/decoration-eclairage/ampoule-et-led/ampoule-led/ampoule-e27/ampoule-led-connectee-e27-806lm-60w-variations-blanc-couleurs-lexman-enki-84372272.html
[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[buymecoffee]: https://www.buymeacoffee.com/davidsmfreire
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/tiagoagueda/hass-lexman-ble.svg?style=for-the-badge
[commits]: https://github.com/tiagoagueda/hass-lexman-ble/commits/main
[config-flow]: https://my.home-assistant.io/redirect/config_flow_start/?domain=lexman_ble
[config-flow-shield]: https://my.home-assistant.io/badges/config_flow_start.svg
[forum]: https://community.home-assistant.io/
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[hacs-repo]: https://my.home-assistant.io/redirect/hacs_repository/?owner=tiagoagueda&repository=hass-lexman-ble&category=integration
[hacs-repo-shield]: https://my.home-assistant.io/badges/hacs_repository.svg
[issues]: https://github.com/tiagoagueda/hass-lexman-ble/issues
[lexmanimg]: images/logo.png
[license-shield]: https://img.shields.io/github/license/tiagoagueda/hass-lexman-ble.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40tiagoagueda-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/tiagoagueda/hass-lexman-ble.svg?style=for-the-badge
[releases]: https://github.com/tiagoagueda/hass-lexman-ble/releases
[user_profile]: https://github.com/tiagoagueda
