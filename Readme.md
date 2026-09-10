# CCT Starbase

Starbase is the public, static distribution service for Curling Tools products
and apps. GitHub Pages serves the [`docs`](docs) directory at
`https://starbase.curling.tools`.

## Repository layout

Firmware is scoped to the exact stable product ID reported by a device:

```text
docs/
└── products/
    └── <product-id>/
        └── firmware/
            ├── channels/
            │   ├── beta.json
            │   └── <channel>.json
            └── releases/
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

### Deactivated serial numbers

`/products/<product-id>/blacklist-serial-numbers.json` contains the serial
numbers deactivated for that exact device product ID. Clients may restrict a
device only after successfully fetching and validating the manifest:

```json
{
  "schemaVersion": 1,
  "productId": "3.2",
  "serialNumbers": [
    "202607-1"
  ]
}
```

`serialNumbers` contains canonical serial strings exactly as reported by the
device. A request, schema, or product-ID validation failure must not deactivate
a device.

## App announcements

Announcements are scoped to an app (or product family), rather than to an
exact hardware product ID. For example, the SmartBroom app supports both 3.1
and 3.2 SmartBrooms, so it reads one common announcements feed even though
only 3.2 firmware is distributed here. The initial app IDs are `smartbroom`
and `smartbeam`.

```text
docs/
└── apps/
    └── <app-id>/
        └── announcements/
            ├── channels/
            │   ├── beta.json
            │   └── release.json
            └── posts/
                └── YYYY/MM/DD/
                    └── <announcement-uuid>.json
```

The app fetches one channel index:

```text
/apps/<app-id>/announcements/channels/<channel>.json
```

The mutable channel index is only a list of currently deliverable post
identities and relative URLs. It intentionally does not duplicate announcement
content. Internal builds use `beta`; external builds use `release`. A post is
tested by adding it to the beta index first, then promoted by adding the same
pointer to release after approval:

```json
{
  "schemaVersion": 1,
  "appId": "smartbroom",
  "announcements": [
    {
      "id": "0198b8e3-54e4-7d8d-9f81-55e6c6b77501",
      "url": "../posts/2026/09/10/0198b8e3-54e4-7d8d-9f81-55e6c6b77501.json"
    }
  ]
}
```

Each post is the complete, durable record:

```json
{
  "schemaVersion": 1,
  "id": "0198b8e3-54e4-7d8d-9f81-55e6c6b77501",
  "appId": "smartbroom",
  "publishedAt": "2026-09-10T18:00:00Z",
  "severity": "info",
  "title": "SmartBroom announcements are here",
  "body": "## Keep up with SmartBroom\\n\\nThis is an in-app announcement.",
  "action": {
    "title": "Learn more",
    "url": "https://curling.tools/pages/smartbroom"
  }
}
```

`action` is optional. When present, it has this shape:

```json
{
  "title": "Visit SmartBroom",
  "url": "https://curling.tools/smartbroom"
}
```

`title` is the button label shown beneath the post's Markdown body. `url` must
be an absolute HTTPS URL; clients reject posts whose action URL is missing a
host or uses another scheme. Actions open as an external link. App deep links
are not part of the announcement action contract.

`id` is a UUID and is the announcement's permanent identity. A post's path is
derived from its immutable `publishedAt` date in UTC, making the archive easy
to browse chronologically. Never change or remove a published post. To correct
one, publish a new UUID (optionally with a future `supersedes` field) and
remove the previous entry from the channel index when it should no longer be
delivered.
The publisher must refuse to overwrite an existing post path or UUID.

Clients validate the index and each post's schema, app ID, UUID, and relative
URL before displaying it. They persist read state by UUID through the app's
iCloud key-value store. Removing an entry from the index stops new delivery but
does not invalidate a post already read by a client.

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

## Publishing a SmartBroom beta

From the `smartbroom-firmware` repository:

1. Create the OTA artifact with `tools/package_smartbroom_beta_release.sh`.
2. Publish it with `tools/publish_smartbroom_beta.sh`.
3. Review and commit the new immutable release directory and beta channel
   manifest together.

The publisher copies the image and `SHA256SUMS`, calculates the image metadata,
and merges the candidate into `docs/products/3.2/firmware/channels/beta.json`.

The following environment variables configure a beta publication when a
hardware-specific track needs different bounds or release notes:

```text
PRESENTATION
MINIMUM_HARDWARE_VERSION
MAXIMUM_HARDWARE_VERSION
MINIMUM_CURRENT_FIRMWARE_VERSION
STARBASE_DIR
```

SmartBroom beta OTA images are signed with the production Secure Boot key so
they can install on production-provisioned hardware.
