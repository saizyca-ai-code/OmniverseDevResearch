import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'build_index.py'
spec = importlib.util.spec_from_file_location('build_index', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_index_includes_specs_and_handoff(tmp_path, monkeypatch):
    root = tmp_path
    specs = root / 'docs' / 'specs'
    handoffs = root / 'docs' / 'handoffs'
    specs.mkdir(parents=True)
    handoffs.mkdir(parents=True)
    (specs / 'example.md').write_text('---\nid: OVR-PRD-0001\ntitle: Foo | Bar\n'
                                    'type: prd\nstatus: planned\n---\n', encoding='utf-8')
    (handoffs / 'example.md').write_text('---\nid: OVR-HOF-0001\ntitle: Handoff\n'
                                       'type: handoff\nstatus: planned\n---\n', encoding='utf-8')
    monkeypatch.setattr(module, 'ROOT', root)
    monkeypatch.setattr(module, 'SEARCH_DIRS', (specs, handoffs))
    monkeypatch.setattr(module, 'OUTPUT', root / 'docs' / 'GENERATED-RESEARCH-INDEX.md')
    module.main()
    content = module.OUTPUT.read_text(encoding='utf-8')
    assert 'Documents indexed: 2' in content
    assert 'OVR-PRD-0001' in content and 'OVR-HOF-0001' in content
    assert 'Foo \\| Bar' in content
    assert '(specs/example.md)' in content
    assert '(handoffs/example.md)' in content


def test_index_ignores_readme(tmp_path, monkeypatch):
    directory = tmp_path / 'docs' / 'research'
    directory.mkdir(parents=True)
    (directory / 'README.md').write_text('# readme only\n', encoding='utf-8')
    monkeypatch.setattr(module, 'ROOT', tmp_path)
    monkeypatch.setattr(module, 'SEARCH_DIRS', (directory,))
    monkeypatch.setattr(module, 'OUTPUT', tmp_path / 'docs' / 'GENERATED-RESEARCH-INDEX.md')
    module.main()
    assert 'Documents indexed: 0' in module.OUTPUT.read_text(encoding='utf-8')
