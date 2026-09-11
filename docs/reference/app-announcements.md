# App announcements

Announcements are scoped to an app rather than a hardware product ID. Internal
builds read `beta`; external builds read `release`.

```text
apps/<app-id>/announcements/
├── channels/
│   ├── beta.json
│   └── release.json
└── posts/YYYY/MM/DD/<announcement-uuid>.json
```

The channel index contains only identities and relative post URLs:

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

Posts are durable records with a UUID, timestamp, title, Markdown body, and
optional external HTTPS action. A post may also target a range of app marketing
versions:

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

`appVersionRange` is optional. When it is absent, the post applies to every
app version. When present, it must contain at least one bound. A matching app
version is greater than or equal to `minimumInclusive` (when supplied) and
less than `maximumExclusive` (when supplied). The lower bound is inclusive and
the upper bound is exclusive.

App versions use `YYYY.M[.Patch]`: a four-digit year, a month from `1` through
`12` (without zero-padding requirements), and an optional non-negative patch.
For comparison, an omitted patch is `0`, so `2026.9` and `2026.9.0` are the
same version. Bounds must be valid versions, and a supplied upper bound must be
later than a supplied lower bound. Clients must not display a post with an
invalid range.

Never change or remove a published post; issue a new UUID to correct it. A
channel may stop delivering a post by removing its pointer. Clients validate
the index and posts, and persist read state by UUID.
