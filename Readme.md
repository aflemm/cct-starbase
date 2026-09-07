Hello
# CCT Starbase

Starbase is the public firmware distribution service for Curling Club Technology
products. GitHub Pages serves the `docs` directory at
`https://starbase.curling.tools`.

## Firmware channels

Apps must read a product channel manifest rather than infer a release from a
directory listing. A manifest names one immutable image and includes its byte
size and SHA-256 digest.

- SmartBroom beta: `/products/smartbroom/channels/beta.json`

Versioned binaries live beneath `/products/<product>/releases/<version>/`. They
are never replaced. A channel manifest is the only mutable release pointer.

## Publishing a SmartBroom beta

From the `smartbroom-firmware` repository, create the image with
`tools/package_smartbroom_beta_release.sh` and publish it with
`tools/publish_smartbroom_beta.sh`. The beta profile is intentionally unsigned
until field provisioning moves to secure boot.
