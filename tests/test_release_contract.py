import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_manifest_matches_processed_evidence():
    manifest = json.loads((ROOT / "data" / "manifest.json").read_text())
    entry = manifest["files"][0]
    evidence = ROOT / entry["path"]
    assert evidence.stat().st_size == entry["bytes"]
    assert digest(evidence) == entry["sha256"]


def test_frozen_statistics_match_published_headlines():
    release_id = (ROOT / "results" / "CURRENT").read_text().strip()
    result = json.loads((ROOT / "results" / "frozen" / release_id / "statistics.json").read_text())
    assert result["T"] == 21949
    assert result["N"] == 4
    assert result["white_rc"]["pvalue"] == 1.0
    assert result["hansen_spa"]["pvalue"] == 0.9945
    assert max(item["dsr"] for item in result["dsr"].values()) < 0.01
