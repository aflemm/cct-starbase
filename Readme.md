# CCT Starbase

Starbase is the public, static firmware distribution service for Curling Tools products. GitHub Pages serves the [`docs`](docs) directory at
`https://starbase.curling.tools`.

## Repository layout

Each product has a self-contained subtree below `docs/products`:

```text
docs/
└── products/
    └── <product-id>/
        └── firmware/
            ├── channels/
            │   ├── beta.json
            │   └── <channel>.json
            └── releases/
                ├── manifest.json
                └── <version>/
                    ├── <firmware-image>.bin
                    └── SHA256SUMS
```

Paths use the stable product ID reported by the device, rather than a product
name. Current product IDs are SmartBroom `3.2`, LightBroom `5.1`, and SmartBeam
`4.1`. For example, SmartBroom's beta endpoint is:

```text
/products/3.2/firmware/channels/beta.json
```

Firmware images are immutable once published. A corrected or new build must
use a new version directory; do not replace an existing image or its checksum.

## Manifest model

All manifests currently use `schemaVersion: 1`. There is no `latest` field.
Instead, a channel exposes all of its active release candidates in its
`releases` array. This is necessary when separate hardware revisions have
different compatible update tracks.

### Channel manifest

`/products/<product-id>/firmware/channels/<channel>.json` is the endpoint clients check
for updates. It contains only the releases that are currently offered on that
channel.

```json
{
  "schemaVersion": 1,
  "productId": "3.2",
  "productName": "SmartBroom",
  "channel": "beta",
  "releases": [
    {
      "version": "1.0.812",
      "channel": "beta",
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

Required manifest fields are `schemaVersion`, `productId`, `productName`,
`channel`, and `releases`. Required candidate fields are `version`, `channel`, `publishedAt`,
`presentation`, `compatibility`, `image`, and `releaseNotes`.

- `productId` is the exact dotted numeric product ID reported by the device and
  must match the product-ID path component. `productName` is display metadata.
- `version` is a dotted numeric firmware version.
- `publishedAt` is a UTC ISO 8601 timestamp.
- `presentation` is `automatic` when an app may proactively offer the update,
  or `manual` when it should only be shown in a manual update flow. Neither
  value permits installation without user confirmation.
- `compatibility.minimumHardwareVersion` and
  `compatibility.minimumCurrentFirmwareVersion` are inclusive. Omit
  `compatibility.maximumHardwareVersion` when there is no upper hardware
  bound; when present it is inclusive.
- `image.url` is resolved relative to the manifest URL. `image.size` is the
  exact byte count and `image.sha256` is verified before installation.
- `releaseNotes` is Markdown. Clients should render its paragraphs, headings,
  lists, and inline formatting as Markdown rather than displaying markers as
  literal text.

Clients must validate the schema, product ID, and channel, filter candidates for
their hardware and installed firmware version, then select the newest eligible
candidate. For automatic checks, only consider `presentation: "automatic"`.
This selection belongs in the app, not in Starbase, because only the app knows
the connected product's hardware and installed firmware.

### Release catalog

`/products/<product-id>/firmware/releases/manifest.json` is the complete catalog of every
published release for that product, across all channels and hardware tracks.
Its shape is:

```json
{
  "schemaVersion": 1,
  "productId": "3.2",
  "productName": "SmartBroom",
  "releases": ["...the same release candidate objects used by channels..."]
}
```

The catalog is for discovery, history, and tooling. It is not an update
endpoint: clients must use a channel manifest to determine what is actively
offered.

## Publishing a SmartBroom beta

From the `smartbroom-firmware` repository:

1. Create the OTA artifact with `tools/package_smartbroom_beta_release.sh`.
2. Publish it with `tools/publish_smartbroom_beta.sh`.
3. Review and commit the new immutable release directory, the beta channel
   manifest, and the product release catalog together.

The publisher copies the image and `SHA256SUMS`, calculates the image metadata,
and merges the candidate into both:

- `docs/products/3.2/firmware/channels/beta.json`
- `docs/products/3.2/firmware/releases/manifest.json`

The following environment variables configure a beta publication when a
hardware-specific track needs different bounds or release notes:

```text
PRESENTATION
MINIMUM_HARDWARE_VERSION
MAXIMUM_HARDWARE_VERSION
MINIMUM_CURRENT_FIRMWARE_VERSION
RELEASE_NOTES
STARBASE_DIR
```

The beta profile is intentionally unsigned until field provisioning moves to
secure boot.
