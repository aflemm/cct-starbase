# Firmware distribution

Firmware is scoped to the exact stable product ID reported by a device. Current
product IDs include SmartBroom `3.2`, LightBroom `5.1`, and SmartBeam `4.1`.

```text
products/<product-id>/firmware/
├── channels/
│   ├── beta.json
│   └── release.json
└── releases/<version>/
    ├── <firmware-image>.bin
    └── SHA256SUMS
```

For example, SmartBroom's beta endpoint is
`/products/3.2/firmware/channels/beta.json`.

All manifests use `schemaVersion: 1`. A channel exposes every currently
offered candidate; it has no `latest` field. The app validates the manifest,
filters it for its connected device's hardware and installed firmware, and
selects the newest eligible candidate.

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
