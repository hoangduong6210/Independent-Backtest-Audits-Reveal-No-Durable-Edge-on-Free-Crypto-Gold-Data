# Result freezing

1. Recompute into `results/audit/`; never write directly into `results/frozen/`.
2. Review numerical, methodological, and disclosure boundaries.
3. Create a new UTC-dated release identifier.
4. Copy only reviewed evidence into `results/frozen/<release-id>/`.
5. Write checksums and a release note inside the frozen directory.
6. Update `results/CURRENT`, manifests, evidence references, and manuscript.
7. Run `scripts/validate_release.py`, `pytest`, and `wiki/build.py check`.

Frozen directories are immutable. Corrections create a new release and an errata
record; they do not mutate the historical evidence silently.
