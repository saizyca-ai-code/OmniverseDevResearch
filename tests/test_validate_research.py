import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_research.py"
spec = importlib.util.spec_from_file_location("validate_research", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_valid_front_matter(tmp_path):
    path = tmp_path / "valid.md"
    path.write_text(
        "---\nid: OVR-INV-1234\ntitle: Test\ntype: investigation\nstatus: planned\n"
        "created: 2026-10-14\nupdated: 2026-10-14\ndomains: []\nrepositories: []\ntags: []\n---\n# Test\n",
        encoding="utf-8",
    )
    assert module.validate_file(path) == []


def test_missing_front_matter(tmp_path):
    path = tmp_path / "no-frontmatter.md"
    path.write_text("# No metadata\n", encoding="utf-8")
    errors = module.validate_file(path)
    assert errors and "front matter" in errors[0]


def test_invalid_status(tmp_path):
    path = tmp_path / "bad-status.md"
    path.write_text(
        "---\nid: OVR-INV-1234\ntitle: Test\ntype: investigation\nstatus: done-ish\n"
        "created: 2026-10-14\nupdated: 2026-10-14\ndomains: []\nrepositories: []\ntags: []\n---\n",
        encoding="utf-8",
    )
    assert any("invalid status" in error for error in module.validate_file(path))
