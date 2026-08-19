# Data

The public release contains only the load-bearing aligned return matrix. Raw
OHLCV, funding, open-interest, and trade data are not redistributed.

- `processed/returns_matrix.csv`: four net-return series on a shared BTC hourly
  axis, with transaction costs already included.
- `manifest.json` and `manifest.yaml`: machine- and human-readable identity,
  scope, and checksum metadata.
- `checksums.sha256`: integrity check for the processed release data.
- `raw/README.md`: upstream source and re-download policy.
- `licenses/README.md`: data-rights boundary.

Run `python scripts/validate_release.py` from the repository root to check the
published evidence identity.
