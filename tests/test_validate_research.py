import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'validate_research.py'
spec = importlib.util.spec_from_file_location('validate_research', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def document(front, tmp_path):
    path = tmp_path / 'test.md'
    path.write_text('---\n' + front + '\n---\n# Test\n', encoding='utf-8')
    return path


def valid_front(doc_id='OVR-INV-1234', doc_type='investigation'):
    return (f'id: {doc_id}\ntitle: Test\ntype: {doc_type}\nstatus: planned\n'
            'created: 2026-10-14\nupdated: 2026-10-14\n'
            'domains: []\nrepositories: []\ntags: []')


def test_valid_front_matter(tmp_path):
    assert module.validate_file(document(valid_front(), tmp_path)) == []


def test_valid_new_artifact_types(tmp_path):
    for prefix, doc_type in [('PRD', 'prd'), ('DES', 'technical-design'), ('HOF', 'handoff')]:
        assert module.validate_file(document(valid_front(f'OVR-{prefix}-1234', doc_type), tmp_path)) == []


def test_missing_front_matter(tmp_path):
    path = tmp_path / 'no-frontmatter.md'
    path.write_text('# No metadata\n', encoding='utf-8')
    assert any('front matter' in e for e in module.validate_file(path))


def test_invalid_status(tmp_path):
    assert any('invalid status' in e for e in module.validate_file(
        document(valid_front().replace('status: planned', 'status: done-ish'), tmp_path)))


def test_id_type_mismatch(tmp_path):
    assert any('does not match type' in e for e in module.validate_file(
        document(valid_front('OVR-HOF-1000', 'prd'), tmp_path)))


def test_impossible_calendar_date(tmp_path):
    assert any('real calendar date' in e for e in module.validate_file(
        document(valid_front().replace('2026-10-14', '2026-02-30'), tmp_path)))


def test_date_order(tmp_path):
    assert any('created date must not be after updated date' in e for e in module.validate_file(
        document(valid_front().replace('updated: 2026-10-14', 'updated: 2026-10-13'), tmp_path)))


def test_catalog_valid(tmp_path):
    p = tmp_path / 'catalog.yaml'
    p.write_text('schema_version: 1\nrepositories:\n  - id: kit\n    name: Kit\n'
                 '    url: https://github.com/NVIDIA-Omniverse/kit-app-template\n'
                 '    kind: upstream-repository\n', encoding='utf-8')
    assert module.validate_catalog(p) == []


def test_catalog_duplicate_id(tmp_path):
    p = tmp_path / 'catalog.yaml'
    entry = ('  - id: kit\n    name: Kit\n'
             '    url: https://github.com/NVIDIA-Omniverse/kit-app-template\n'
             '    kind: upstream-repository\n')
    p.write_text('schema_version: 1\nrepositories:\n' + entry + entry, encoding='utf-8')
    assert any('duplicate repository id' in e for e in module.validate_catalog(p))
