#!/usr/bin/env python3
"""Check that the versioned wiki is complete and locally navigable."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

WIKI = Path(__file__).resolve().parent
ROOT = WIKI.parent
REQUIRED = {
    "Home.md", "Wiki-Index.md", "Project-Status.md", "Scientific-Results.md",
    "Claims-and-Limits.md", "Evidence-Sources.md", "Reproduce-and-Audit.md",
    "Audit-Protocol.md", "Authoring-and-Snapshots.md", "Full-Manuscript.md",
    "References.md", "_Sidebar.md",
}
LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")


def check() -> None:
    missing = sorted(name for name in REQUIRED if not (WIKI / name).is_file())
    errors = [f"missing required wiki page: {name}" for name in missing]
    for page in WIKI.glob("*.md"):
        text = page.read_text(encoding="utf-8")
        for raw in LINK.findall(text):
            target = unquote(raw.split("#", 1)[0])
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (page.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{page.name}: broken local link: {raw}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"wiki valid: {len(list(WIKI.glob('*.md')))} Markdown pages")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] != "check":
        raise SystemExit("usage: python wiki/build.py check")
    check()
