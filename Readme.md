Hello
# CCT Starbase

Starbase is the public firmware distribution service for Curling Club Technology
products. GitHub Pages serves the `docs` directory at
`https://starbase.curling.tools`.

## Firmware channels

Apps must read a product channel manifest rather than infer a release from a
directory listing. A channel manifest contains the active immutable release
candidates for that channel, allowing parallel hardware-revision tracks. Each
candidate includes its byte size, SHA-256 digest, compatibility constraints,
and presentation. The app filters candidates by hardware and installed
firmware, then selects the newest compatible automatic candidate. A release
may also declare a maximum hardware version when a later board revision is
incompatible; omission means there is no upper hardware limit.

- SmartBroom beta: `/products/smartbroom/channels/beta.json`

Versioned binaries live beneath `/products/<product>/releases/<version>/`. They
are never replaced. `/products/<product>/releases/manifest.json` is the
cross-channel catalog of every published release; channel manifests contain
only releases that are active candidates for their respective channel.

`presentation` controls whether clients should proactively offer a release
(`automatic`) or leave it for the user to discover (`manual`). Automatic means
the app may prompt; it never installs firmware without confirmation.

## Publishing a SmartBroom beta

From the `smartbroom-firmware` repository, create the image with
`tools/package_smartbroom_beta_release.sh` and publish it with
`tools/publish_smartbroom_beta.sh`. The beta profile is intentionally unsigned
until field provisioning moves to secure boot.
