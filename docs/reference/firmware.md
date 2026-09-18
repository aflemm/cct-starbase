# Firmware distribution

Firmware is scoped to the exact stable product ID reported by a device. Current
product IDs include SmartBroom `3.2`, LightBroom `5.1`, and SmartBeam `4.1`.

```text
v1/products/<product-id>/firmware/
├── channels/
│   ├── beta.json
│   └── release.json
└── releases/<version>/
    ├── <firmware-image>.bin
    └── SHA256SUMS
```

For example, SmartBroom's beta endpoint is
`/v1/products/3.2/firmware/channels/beta.json`.

All manifests use `schemaVersion: 1`. A channel exposes every currently
offered candidate; it has no `latest` field. The app validates the manifest,
filters it for its connected device's hardware and installed firmware, and
selects the newest eligible candidate.

Each release has a required `presentation` field:

- `automatic` makes a compatible update available when the device connects.
- `manual` makes it available only when the user explicitly checks for updates.

An optional `urgency` field controls the presentation of an automatic update:

- Omit it, or use `normal`, for ordinary update availability.
- Use `high` to show an update-available alert once during each device
  connection. Choosing **Not Now** dismisses the alert until that device is
  disconnected and connected again.

Urgency never installs firmware without the user's confirmation. `high` is
valid only with `presentation: "automatic"`.

```json
{
  "schemaVersion": 1,
  "productId": "3.2",
  "productName": "SmartBroom",
  "channel": "beta",
  "releases": [
    {
      "version": "1.0.812",
      "publishedAt": "2026-09-07T17:51:09Z",
      "presentation": "automatic",
      "urgency": "high",
      "compatibility": {
        "minimumHardwareVersion": "0.2",
        "maximumHardwareVersion": "1.0",
        "minimumCurrentFirmwareVersion": "1.0.600"
      },
      "image": {
        "url": "../releases/1.0.812/SmartBroom_OTA-1.0.812.bin",
        "size": 762128,
        "sha256": "<64-character lowercase SHA-256 hex digest>"
      },
      "releaseNotes": "Markdown release notes"
    }
  ]
}
```

Firmware images are immutable once published. A correction requires a new
version directory and checksum. Clients must verify image size and SHA-256
before installation.
