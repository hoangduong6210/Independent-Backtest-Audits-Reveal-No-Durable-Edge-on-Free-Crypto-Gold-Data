# Project history and date provenance

This file separates the dates of the research from later repository maintenance.
Git records when a version was committed; it does not necessarily record when
the underlying experiments were first run. The dates below are based on the
original Git commit, generated-artifact metadata, Word core properties, and the
preserved local workspace.

## Timeline

| Period | Activity | Evidence |
|---|---|---|
| 2023-12-27 to 2026-06-28 | Observation window of the aligned BTC-hourly evidence matrix | `data/manifest.json`; this is a market-data range, not the research-work period |
| 2026-06-28 | Research charter and first work orders created | Preserved `Trading/CHARTER.md` and `WO-001` timestamps begin at 21:33-21:34 UTC+8 |
| 2026-06-28 to 2026-06-30 | Core campaign: strategy tests, cost audit, basis audit, statistical checks, external reproduction, and paper preparation | Preserved work orders `WO-001` through `WO-024`, reports, return dumps, and build artifacts |
| 2026-06-30 10:47 UTC+8 | Aligned BTC return matrix finalized | Preserved `returns_matrix.csv` filesystem timestamp and released checksum |
| 2026-06-30 10:48 UTC+8 | English and Vietnamese preprint PDFs generated | Embedded PDF creation metadata in the preserved preprints |
| 2026-06-30 11:43 UTC+8 | Original public GitHub release committed | Git commit `7efa1523d7c7d34c539bcb1f13cde3639c63660e` |
| 2026-07-06 to 2026-07-17 | Journal-style manuscript review and revision | Word core properties: created 2026-07-06, modified 2026-07-17, revision 20 |
| 2026-08-19 | Existing project reorganized into an auditable repository; documentation, wiki, tests, metadata, and editorial style updated | Current working-tree maintenance; no new trading experiment or new result release |

## Interpretation for reviewers

The August maintenance commit should be read as a preservation and publication
engineering update to research completed earlier. It must not be used to infer
that all experiments in this repository were designed or executed on the commit
date. The frozen numerical release remains `20260630_public_release`, and the
paper continues to cite 30 June 2026 as its original release date.

The repository intentionally keeps the true Git commit date for maintenance
work. Commit timestamps have not been rewritten or backdated.

## Evidence quality

The original Git commit and embedded PDF/DOCX metadata are durable provenance
records. Local filesystem timestamps provide supporting chronology but may be
changed by cloud synchronization or file copying, so they are not treated as
cryptographic proof. Numerical evidence is identified independently by SHA-256
in `data/manifest.json` and the frozen release.
