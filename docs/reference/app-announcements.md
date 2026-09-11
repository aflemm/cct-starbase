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
optional external HTTPS action. Never change or remove a published post; issue
a new UUID to correct it. A channel may stop delivering a post by removing its
pointer. Clients validate the index and posts, and persist read state by UUID.
