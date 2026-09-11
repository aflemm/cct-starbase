# App About content

About content is public, mutable configuration for the informational portion
of an app's About screen. It cannot invoke native app actions. The app owns
announcements, app version information, and any internal-only tools.

## Endpoints and compatibility

The contract version is part of the endpoint:

```text
/apps/<app-id>/about/v1/channels/beta.json
/apps/<app-id>/about/v1/channels/release.json
```

Each app bundles a valid manifest for the contract version it supports. It uses
a previously validated cached response when one exists; otherwise it uses the
bundled content. It only replaces either with a complete, validated remote
manifest.

Within a contract version, publishers may change copy, destinations, section
order, and rows using already defined types. They must not add a new row type
or change existing type semantics. A new capability requires a new endpoint
version (for example, `v2`) and an app release that bundles and fetches it.
Older installs remain on their existing contract endpoint.

## V1 document

```json
{
  "schemaVersion": 1,
  "appId": "smartbroom",
  "revision": 1,
  "updatedAt": "2026-09-11T17:00:00Z",
  "sections": [
    {
      "id": "smartbroom",
      "rows": [
        {
          "id": "about-smartbroom",
          "type": "link",
          "title": "About SmartBroom",
          "systemImage": "info.circle",
          "url": "https://curling.tools/pages/smartbroom"
        }
      ]
    }
  ]
}
```

`schemaVersion`, `appId`, a positive integer `revision`, and UTC ISO 8601
`updatedAt` are required. Increment `revision` and update `updatedAt` on every
published change. Section and row IDs must be unique, non-empty stable
identifiers. A document must contain at least one section and one row.

### V1 row types

- `link`: an external `https` or `mailto` link. Requires `title` and `url`.
  `systemImage` is optional.
- `detailLink`: an external `https` or `mailto` link with a subtitle. Requires
  `title`, `detail`, and `url`.
- `text`: non-interactive information. Requires `title`; `detail` and
  `systemImage` are optional.

Sections may have optional `title` and `footer`. URLs are always opened
externally. Clients reject an entire remote document with unknown types,
duplicate IDs, invalid URLs, unsupported schemas, or invalid app IDs, and keep
their last known valid content.
