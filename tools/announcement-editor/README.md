# Starbase Announcement Editor

`Announcement Editor.html` is a self-contained, dependency-free editor for
Starbase announcement streams. Double-click it from Finder or Windows Explorer
(or open it in a current Chromium browser such as Chrome or Edge), click
**Open Starbase folder**, and select the root of this clone.
The editor loads all app announcement collections below `docs/v1/apps`.

It validates announcement posts, version targeting, optional HTTPS actions, and
the mutable `alpha`, `beta`, and `release` channel indices. Its three-step flow
is: open the folder, write or choose an announcement, then review and save the
changes. Review and commit them with Git as normal; the editor never commits or
pushes.

## Saving

Chrome and Edge can write the selected repository folder directly. If browser
folder writing is unavailable, use **Choose folder (read-only)** then **Step 3:
Review & save → Download changes as a patch**, and apply it from the repository
root:

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
an existing post in the editor creates a corrected new post with a new UUID and
replaces the old channel pointer. Use **Change who sees this** to promote or
demote an unchanged post without changing that immutable record. **Stop showing
this announcement** only removes its channel pointer; the old post file is
retained.
