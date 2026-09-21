# Starbase Announcement Editor

`Announcement Editor.html` is a self-contained, dependency-free editor for
Starbase announcement streams. Double-click it from Finder or Windows Explorer
(or open it in a current Chromium browser such as Chrome or Edge), click
**Open Starbase folder**, and select the root of this clone.
The editor loads all app announcement collections below `docs/v1/apps`.

It validates and stages immutable posts, version targeting, optional HTTPS
actions, and the mutable `alpha`, `beta`, and `release` channel indices. Review
the changes in the editor, then review and commit them with Git as normal. The
editor never commits or pushes.

## Saving

Chrome and Edge can write the selected repository folder directly. If browser
folder writing is unavailable, use **Choose folder (read-only)** then **Review
& publish → Download git patch**, and apply it from the repository root:

```sh
git apply starbase-announcements.patch
```

This fallback makes the editor usable from a simple double-click on macOS and
Windows without a runtime or package installation. File-system access remains
browser- and permission-dependent.

## Publishing model

The UI follows the announcement contract in
[`reference/app-announcements.md`](../../reference/app-announcements.md):

- Release clients receive `release`.
- External beta clients receive `release` and `beta`.
- CCT-internal clients receive `release`, `beta`, and `alpha`.

Place each post only in its most-specific stream. Posts are immutable; editing
an existing post in the editor stages a replacement with a new UUID and replaces
the old channel pointer. Use **Move delivery here** to promote or demote an
unchanged post without changing that immutable record. Removing an entry only
removes its channel pointer; the old post file is retained.
