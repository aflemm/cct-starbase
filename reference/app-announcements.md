# App announcements

Announcements belong to an app and may be shown in either an app-wide or a
connected-device context. Channels are additive: external-release builds read
`release`, external-beta builds combine `release` and `beta`, and CCT-internal
builds combine `release`, `beta`, and `alpha`. Add a post pointer only to its
most-specific channel; clients de-duplicate posts by UUID.

```text
v1/apps/<app-id>/announcements/
├── channels/
│   ├── alpha.json
│   ├── beta.json
│   └── release.json
└── posts/YYYY/MM/DD/<announcement-uuid>.json
```

The channel index contains only identities and relative post URLs. Its schema
remains version 1; the `schemaVersion` on a post is a separate contract:

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

## Post schema versions

Posts are durable records with a UUID, timestamp, severity, title, Markdown
body, and optional external HTTPS action. Schema version 1 is the original
app-wide format. Schema version 2 adds an explicit audience. Clients must
continue to decode versions 1 and 2; they must not display posts with an
unsupported schema version or an invalid audience.

### Version 1: app-wide

Version 1 posts have no `audience` field and are treated as app-wide. They may
include an optional range of app marketing versions:

```json
{
  "schemaVersion": 1,
  "id": "0198b8e3-54e4-7d8d-9f81-55e6c6b77501",
  "appId": "smartbroom",
  "publishedAt": "2026-09-10T18:00:00Z",
  "severity": "warning",
  "title": "Update SmartBroom",
  "body": "Please update the app.",
  "appVersionRange": {
    "minimumInclusive": "2026.9",
    "maximumExclusive": "2026.11"
  }
}
```

Do not add device targeting to a version 1 post. Older clients may ignore
unknown JSON fields and otherwise display the post without applying its target.

### Version 2: explicit audience

Version 2 posts require an `audience` object. Its `type` is either `app` or
`device`:

- `{"type":"app"}` makes the post eligible for the app-wide announcement
  surface.
- `{"type":"device","deviceTarget":{...}}` makes it eligible only in the
  connected-device context when that device matches every supplied selector.

An `app` audience must not include `deviceTarget`; a `device` audience must
include a valid `deviceTarget`.

App-wide version 2 example:

```json
{
  "schemaVersion": 2,
  "id": "0198b8e3-54e4-7d8d-9f81-55e6c6b77502",
  "appId": "smartbroom",
  "publishedAt": "2026-09-10T18:00:00Z",
  "severity": "info",
  "title": "SmartBroom news",
  "body": "A new update is available.",
  "audience": { "type": "app" }
}
```

Device-targeted version 2 example:

```json
{
  "schemaVersion": 2,
  "id": "0198b8e3-54e4-7d8d-9f81-55e6c6b77503",
  "appId": "smartbroom",
  "publishedAt": "2026-09-10T18:00:00Z",
  "severity": "warning",
  "title": "Check this SmartBroom",
  "body": "Please contact support before your next use.",
  "audience": {
    "type": "device",
    "deviceTarget": {
      "productIds": ["3.2"],
      "hardwareVersions": ["0.2"],
      "firmwareVersionRange": { "minimumInclusive": "1.2.0" },
      "serialNumbers": [
        { "productId": "3.2", "year": 2026, "month": 7, "unit": 1 }
      ]
    }
  }
}
```

`deviceTarget` must contain at least one selector:

- `productIds`: non-empty array of exact stable product IDs, such as `3.2`.
- `hardwareVersions`: optional non-empty array of exact hardware versions, such
  as `0.2`.
- `hardwareVersionRange`: optional range over hardware versions.
- `firmwareVersions`: optional non-empty array of exact firmware versions,
  such as `1.2.0`.
- `firmwareVersionRange`: optional range over firmware versions.
- `serialNumbers`: non-empty array of exact serial identities. Each identity
  contains a `productId`, positive integer `year`, integer `month` from 1
  through 12, and positive integer `unit`. Product ID is part of the identity
  because serial values are only unique within a product line.

`deviceTarget` must contain at least one of these selectors. Each supplied
array must be non-empty. Every selector present in `deviceTarget` must match.
Values within `productIds`, `hardwareVersions`, and `firmwareVersions`, and
objects within `serialNumbers`, are alternatives within their selector.
Separate selectors combine with AND; for example, if both `productIds` and
`serialNumbers` are present, a serial identity must match and its product ID
must also be in `productIds`.

## Version ranges

Schema version 1 is frozen: its `appVersionRange` supports only
`minimumInclusive` and `maximumExclusive`. Do not add the other bound fields to
a version 1 post, because older clients may ignore them. The four-bound rules
below apply to `appVersionRange` on schema version 2 and to
`hardwareVersionRange` and `firmwareVersionRange` in a device target.
In a version 1 range, the minimum is inclusive, the maximum is exclusive, at
least one must be present, and the maximum must be later than the minimum.

These ranges use the same four optional bounds:

- `minimumInclusive`: version must be greater than or equal to this lower bound.
- `minimumExclusive`: version must be greater than this lower bound.
- `maximumInclusive`: version must be less than or equal to this upper bound.
- `maximumExclusive`: version must be less than this upper bound.

A range must contain at least one bound. It may contain at most one minimum
bound and at most one maximum bound; for example, `minimumInclusive` and
`minimumExclusive` cannot both appear in the same range. A lower bound must
precede the upper bound. Equal bounds are valid only when both are inclusive,
which selects exactly that version. Missing lower or upper bounds are
unbounded in that direction. Invalid or empty ranges must not match.

App versions use `YYYY.M[.Patch]`: a four-digit year, a month from `1` through
`12` (without zero-padding requirements), and an optional non-negative patch.
An omitted patch is `0`, so `2026.9` and `2026.9.0` are the same version.
Compare year, month, and patch numerically.

Hardware version values and range bounds use two non-negative decimal integer
components (`major.minor`) and compare numerically. Firmware values and range
bounds use three non-negative decimal integer components
(`major.minor.build`), with the firmware-specific ordering below.

Firmware version ordering follows the SmartBroom and SmartBeam release policy:
`major.minor` identifies a release line; build `0` is that line's production
release, while positive builds are development or beta builds. Compare
`major.minor` numerically first. Within the same `major.minor` line, positive
builds sort numerically before build `0`, so a beta such as `1.2.100` is older
than its release `1.2.0`. This ordering applies to all firmware-version range
bounds. For example, `maximumExclusive: "1.2.0"` includes `1.2.100`, while
`minimumInclusive: "1.2.0"` excludes it. Exact-value selectors such as
`firmwareVersions` continue to match only the listed version.

Invalid targets or ranges must not match. If a connected device is missing or
has not yet reported a value required by a selector, the device-targeted post
must not be shown for it.

`appVersionRange` is optional in both schema versions. When absent, a post
applies to every app version. When present, the app version must satisfy its
range. In schema version 2, this is an independent filter: both the app version
and audience must match.

### Compatibility and privacy

Clients treat version 1 as app-wide and require an explicit valid audience on
version 2. Unknown schema versions, unknown audience types, and malformed
audience data must be skipped. Keep app-wide version 1 posts when older app
releases should continue to receive them; older clients that only support
version 1 will skip version 2 posts.

Starbase documents are publicly distributed static content. Device targeting
is a client-side presentation filter, not access control. In particular,
serial numbers included in a `deviceTarget` are visible to anyone who can
retrieve the announcement post; do not use this mechanism when the recipient
list must remain confidential.

Never change or remove a published post; issue a new UUID to correct it. A
channel may stop delivering a post by removing its pointer. Clients validate
the index and posts, and persist read state by UUID. Device-targeted clients
should scope read state by both post UUID and physical device identity so that
reading a post for one device does not mark it read for another.
