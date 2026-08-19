import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_required_repository_sections_exist():
    required = ["src", "experiments", "configs", "data", "results", "figures", "paper", "docs", "wiki"]
    assert all((ROOT / name).is_dir() for name in required)


def test_historical_dates_are_explicit():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    history = (ROOT / "HISTORY.md").read_text(encoding="utf-8")
    assert "Historical project notice" in readme
    assert "2026-06-30" in history
    assert "2026-08-19" in history
    assert "not been rewritten or backdated" in history


def test_wiki_links_are_valid():
    spec = importlib.util.spec_from_file_location("wiki_build", ROOT / "wiki" / "build.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    module.check()
