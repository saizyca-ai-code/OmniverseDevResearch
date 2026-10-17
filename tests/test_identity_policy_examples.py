"""Check published synthetic digest vectors and the non-observed example.

These validate research examples, not an implementation acceptance checker.
"""
import hashlib
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
ADR = ROOT / 'docs/research/OVR-ADR-0002-poc0-binary-identity-policy.md'
text = ADR.read_text(encoding='utf-8')
block = text.split('<!-- CANONICAL-VECTORS-BEGIN -->', 1)[1].split(
    '<!-- CANONICAL-VECTORS-END -->', 1
)[0]
VECTORS = json.loads(block.split('```json\n', 1)[1].split('\n```', 1)[0])


@pytest.mark.parametrize('vector', VECTORS, ids=lambda v: v['name'])
def test_published_canonical_bytes_and_digest(vector):
    payload = vector['payload']
    if payload['schema'] == 'poc0-binary-set/1':
        payload = dict(payload, files=sorted(
            payload['files'], key=lambda f: (f['root'], f['path'])
        ))
    raw = (json.dumps(payload, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True) + '\n').encode('ascii')
    assert raw == vector['canonical_ascii'].encode('ascii')
    assert vector['expected_id'] == 'sha256:' + hashlib.sha256(raw).hexdigest()
    assert raw.endswith(b'\n') and not raw.endswith(b'\n\n')


def test_synthetic_file_hashes_are_raw_bytes():
    vector = next(v for v in VECTORS if v['name'] == 'synthetic-binary')
    sources = {('kit', 'b.txt'): b'x\n', ('registry', 'a.txt'): b''}
    files = vector['payload']['files']
    assert {(f['root'], f['path']) for f in files} == set(sources)
    for file in files:
        raw = sources[file['root'], file['path']]
        assert type(file['size_bytes']) is int
        assert file['size_bytes'] == len(raw)
        assert file['sha256'] == hashlib.sha256(raw).hexdigest()
    assert hashlib.sha256(b'x\n').digest() != hashlib.sha256(b'x\r\n').digest()


def test_manifest_example_cannot_be_mistaken_for_observed_acceptance():
    example = json.loads((ROOT / 'docs/handoffs/precision-lighting-poc0/'
                          'expected-manifest.example.json').read_text(encoding='utf-8'))
    assert example['schema_version'] == '0.2'
    assert example['run_id'] is None and example['timestamp_utc'] is None
    assert example['status'] == 'not-run'
    identity = example['identity']
    assert identity['method'] is None
    assert identity['adopted_policy_revision'] is None
    assert identity['internal_revision'] is None
    assert identity['binary_set']['binary_set_id'] is None
    assert identity['run_environment']['environment_id'] is None
    assert identity['pre_run_approval']['actor'] is None
    assert identity['post_run_review']['actor'] is None
    assert identity['post_run_review']['decision'] is None
    assert identity['machine_evidence_ref'] is None
    assert identity['post_run_review']['reviewed_machine_evidence_ref'] is None
    assert set(identity['evidence_items']) == {f'E{i:02}' for i in range(1, 9)}
    assert all(item == {'status': 'not-run', 'evidence_refs': []}
               for item in identity['evidence_items'].values())
    assert example['result_levels']['diagnostic_status'] == 'not-run'
    assert example['result_levels']['identity_acceptance_status'] == 'blocked'
    assert example['result_levels']['full_environment_go'] == 'blocked'
    assert example['gate']['decision'] == 'not-assessed'


def test_published_evidence_chain_is_immutable_acyclic_and_bound():
    """Validate only the published synthetic example, not a B checker."""
    chain_block = text.split('<!-- EVIDENCE-CHAIN-BEGIN -->', 1)[1].split(
        '<!-- EVIDENCE-CHAIN-END -->', 1
    )[0]
    records = json.loads(chain_block.split('```json\n', 1)[1].split('\n```', 1)[0])
    seen = {}
    binding_keys = ('run_id', 'policy_revision', 'binary_set_id',
                    'environment_id', 'pre_run_approval_id')
    binding = None
    contents = []
    for record in records:
        path, digest, raw = (record[k] for k in ('path', 'sha256', 'raw_ascii'))
        assert path not in seen
        assert hashlib.sha256(raw.encode('ascii')).hexdigest() == digest
        content = json.loads(raw)
        actual_binding = {k: content[k] for k in binding_keys}
        if binding is None:
            binding = actual_binding
        assert actual_binding == binding
        for ref in content['refs']:
            # Only earlier artifacts may be referenced, preventing backedges.
            assert seen[ref['path']] == ref['sha256']
        seen[path] = digest
        contents.append(content)
    machine, review, summary = contents
    assert [c['kind'] for c in contents] == [
        'machine-evidence', 'human-review', 'summary'
    ]
    assert machine['refs'] == []
    assert 'decision' not in machine and 'post_run_review_ref' not in machine
    assert review['refs'] == [review['reviewed_machine_evidence_ref']]
    assert summary['machine_evidence_ref'] == review['reviewed_machine_evidence_ref']
    assert summary['post_run_review_ref'] == {
        'path': records[1]['path'], 'sha256': records[1]['sha256']
    }
    assert summary['refs'] == [summary['machine_evidence_ref'],
                               summary['post_run_review_ref']]
