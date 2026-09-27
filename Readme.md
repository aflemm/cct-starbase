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
manifests are scoped to the exact stable product ID reported by a device. The
sole exception is TNG-era SmartBroom hardware, which does not report a product
ID: clients identify its TNG calibration service and use the stable `2.0`
product ID for deactivation checks.

## SmartBeam endpoints

SmartBeam uses app ID `smartbeam` and hardware product ID `4.1`. Its firmware
catalogues, announcement indices, and serial blacklist are provisioned at the
standard v1 endpoints under `docs/v1`:

- Firmware: `products/4.1/firmware/channels/{alpha,beta,release}.json`
- Announcements: `apps/smartbeam/announcements/channels/{alpha,beta,release}.json`
- Serial blacklist: `products/4.1/blacklist-serial-numbers.json`

Keep each endpoint present even when its collection is empty. The 4.1 blacklist
starts with no entries; add only serial numbers confirmed for deactivation.
Firmware artifacts are immutable and referenced by the channel manifest.

## Publishing

Review a changed document against its concern contract before committing it.
Published firmware images and announcement posts are immutable; their channel
indices and mutable About manifests are not. Firmware and announcements are
additive: publish CCT-internal-only content to alpha, external-beta content to
beta, and production content to release. About content remains one complete
manifest per selected channel.

For SmartBroom firmware beta publication, create the OTA artifact with
`tools/package_smartbroom_beta_release.sh`, publish it with
`tools/publish_smartbroom_beta.sh`, then review and commit the immutable
release directory and beta channel manifest together.
