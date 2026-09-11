# CCT Subspace

Subspace is the public, static distribution service for Curling Tools products
and apps. GitHub Pages serves the [`docs`](docs) directory at
`https://subspace.curling.tools`.

It distributes public content only. Clients must validate every downloaded
document and retain a safe local fallback when a request or validation fails.

## Concerns

- [Firmware distribution](docs/reference/firmware.md) — hardware-specific,
  cryptographically verified OTA releases.
- [Deactivated serial numbers](docs/reference/deactivated-serial-numbers.md) —
  hardware-specific device restriction manifests.
- [App announcements](docs/reference/app-announcements.md) — app-scoped,
  durable announcement posts delivered through beta and release channels.
- [App About content](docs/reference/app-about-content.md) — app-scoped,
  mutable informational sections delivered through versioned contracts.

## Repository layout

```text
docs/
├── apps/
│   └── <app-id>/
│       ├── announcements/
│       └── about/
│           └── v<contract-version>/
└── products/
    └── <product-id>/
        ├── blacklist-serial-numbers.json
        └── firmware/
```

App content is scoped to an app or product family. Firmware and deactivation
manifests are scoped to the exact stable product ID reported by a device. Do
not infer a product ID from a product name.

## Publishing

Review a changed document against its concern contract before committing it.
Published firmware images and announcement posts are immutable; their channel
indices and mutable About manifests are not. Test new app-facing content on
the beta channel before promoting an equivalent change to release.

For SmartBroom firmware beta publication, create the OTA artifact with
`tools/package_smartbroom_beta_release.sh`, publish it with
`tools/publish_smartbroom_beta.sh`, then review and commit the immutable
release directory and beta channel manifest together.
