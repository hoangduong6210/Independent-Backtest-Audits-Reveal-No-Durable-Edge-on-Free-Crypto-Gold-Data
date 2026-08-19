#!/usr/bin/env python3
"""Validate public release structure, evidence checksum, and current pointer."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    manifest = json.loads((ROOT / "data" / "manifest.json").read_text(encoding="utf-8"))
    for entry in manifest["files"]:
        path = ROOT / entry["path"]
        if not path.is_file():
            raise SystemExit(f"missing evidence file: {entry['path']}")
        if sha256(path) != entry["sha256"]:
            raise SystemExit(f"checksum mismatch: {entry['path']}")
    release_id = (ROOT / "results" / "CURRENT").read_text(encoding="utf-8").strip()
    release_dir = ROOT / "results" / "frozen" / release_id
    if not release_dir.is_dir():
        raise SystemExit(f"CURRENT points to missing release: {release_id}")
    print(f"release valid: {release_id}; {len(manifest['files'])} evidence file(s)")


if __name__ == "__main__":
    main()
