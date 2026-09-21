# CCT Starbase

Starbase is the public, static distribution service in the Subspace transport
layer for Curling Tools products and apps. GitHub Pages serves **only** the
[`docs`](docs) directory at `https://starbase.subspace.curling.tools`.
Everything under `docs/` is public, deployed payload; do not put internal
documentation, working notes, or other unpublished material there.

It distributes public content only. Clients must validate every downloaded
document and retain a safe local fallback when a request or validation fails.

## Concerns

- [Firmware distribution](reference/firmware.md) — hardware-specific,
  cryptographically verified OTA releases.
- [Deactivated serial numbers](reference/deactivated-serial-numbers.md) —
  hardware-specific device restriction manifests.
- [App announcements](reference/app-announcements.md) — app-scoped,
  durable announcement posts delivered through alpha, beta, and release channels.
- [App About content](reference/app-about-content.md) — app-scoped,
  mutable informational sections delivered through versioned contracts.

## Repository layout

```text
docs/
└── v1/
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
indices and mutable About manifests are not. Publish CCT-internal content to
alpha, external-beta content to beta, and production content to release.

For SmartBroom firmware beta publication, create the OTA artifact with
`tools/package_smartbroom_beta_release.sh`, publish it with
`tools/publish_smartbroom_beta.sh`, then review and commit the immutable
release directory and beta channel manifest together.
