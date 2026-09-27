#!/usr/bin/env python3
"""Render the docs tree as a GitHub Pages artifact with its source commit time."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import re
import shutil
import subprocess


TIME_ELEMENT = re.compile(
    r'(<time id="starbase-latest-commit" datetime=")[^"]+(">)[^<]*(</time>)'
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", required=True, help="Commit whose committer time is displayed")
    parser.add_argument("--destination", default="_site", help="Output directory inside the repository")
    args = parser.parse_args()

    repository = Path(__file__).resolve().parents[1]
    source = repository / "docs"
    destination = (repository / args.destination).resolve()
    if destination == source or source in destination.parents:
        raise SystemExit("The output directory must not overwrite or be inside docs/.")
    if repository not in destination.parents:
        raise SystemExit("The output directory must be inside the repository.")
    if destination.exists():
        raise SystemExit(f"Output directory already exists: {destination}")

    raw_time = subprocess.check_output(
        ["git", "show", "-s", "--format=%cI", args.commit],
        cwd=repository,
        text=True,
    ).strip()
    committed_at = datetime.fromisoformat(raw_time).astimezone(timezone.utc)
    timestamp = committed_at.strftime("%Y-%m-%dT%H:%M:%SZ")

    shutil.copytree(source, destination)
    index = destination / "index.html"
    html = index.read_text(encoding="utf-8")
    rendered, replacements = TIME_ELEMENT.subn(
        lambda match: f"{match.group(1)}{timestamp}{match.group(2)}{timestamp}{match.group(3)}",
        html,
    )
    if replacements != 1:
        raise SystemExit(
            f"Expected one latest-commit time element in {index}, found {replacements}."
        )
    index.write_text(rendered, encoding="utf-8")
    print(f"Rendered public root timestamp {timestamp} from commit {args.commit}.")


if __name__ == "__main__":
    main()
