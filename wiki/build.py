#!/usr/bin/env python3
"""Check the categorized wiki contract, front matter, and local links."""

from __future__ import annotations
import re
import sys
from pathlib import Path
from urllib.parse import unquote

WIKI = Path(__file__).resolve().parent
REQUIRED = {"README.md", "START-HERE.md", "INDEX.md", "CONTRIBUTING.md",
 "GLOSSARY.md", "LIMITATIONS.md", "REPRODUCIBILITY.md",
 "architecture/Research-System-Map.md", "claims/Current-Claim-Language.md",
 "claims/Historical-Claim-Ledger.md", "datasets/Dataset-Registry.md",
 "decisions/0001-free-data-audit-boundary.md", "evidence/Evidence-Ledger.md",
 "governance/License-and-Assets.md", "manuscript/Paper-Export-Contract.md",
 "methods/Audit-Method.md", "operations/Research-Workflow.md",
 "references/Technical-Source-Map.md", "results/Scientific-Results.md",
 "status/Project-Status.md"}
LINK = re.compile(r"!?\[[^]]*\]\(([^)]+)\)")
FRONT = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)

def check() -> None:
    pages = sorted(WIKI.rglob("*.md"))
    errors = [f"missing required wiki page: {n}" for n in sorted(REQUIRED)
              if not (WIKI / n).is_file()]
    for page in pages:
        text = page.read_text(encoding="utf-8")
        rel = page.relative_to(WIKI)
        front = FRONT.match(text)
        if not front:
            errors.append(f"{rel}: missing YAML front matter")
        else:
            fields = {line.split(":", 1)[0].strip() for line in front.group("body").splitlines() if ":" in line}
            for field in ("title", "status", "paper_source"):
                if field not in fields: errors.append(f"{rel}: missing {field}")
            if not ({"last_updated", "date"} & fields): errors.append(f"{rel}: missing date")
        for raw in LINK.findall(text):
            target = unquote(raw.strip().split("#", 1)[0])
            if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I): continue
            resolved = (page.parent / target).resolve()
            if WIKI.resolve() in (resolved, *resolved.parents) and not resolved.exists():
                errors.append(f"{rel}: broken local link: {raw}")
    if errors: raise SystemExit("\n".join(errors))
    print(f"wiki valid: {len(pages)} Markdown pages; categorized contract complete")

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] != "check": raise SystemExit("usage: python wiki/build.py check")
    check()
