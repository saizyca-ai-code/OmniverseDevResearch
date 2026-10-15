#!/usr/bin/env python3
"""Validate research/spec front matter, IDs, and the repository catalog."""
from __future__ import annotations

from datetime import date
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SEARCH_DIRS = tuple(ROOT / p for p in (
    'docs/research', 'experiments', 'docs/specs', 'docs/handoffs'
))
VALID_STATUS = {'planned', 'in-progress', 'review', 'verified', 'stale', 'superseded', 'accepted'}
TYPE_PREFIX = {
    'repository-analysis': 'REPO',
    'investigation': 'INV',
    'version-comparison': 'VER',
    'experiment': 'EXP',
    'decision': 'ADR',
    'prd': 'PRD',
    'technical-design': 'DES',
    'handoff': 'HOF',
}
VALID_TYPES = set(TYPE_PREFIX)
ID_RE = re.compile(r'^OVR-(REPO|INV|VER|EXP|ADR|PRD|DES|HOF)-\d{4}$')
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
CATALOG = ROOT / 'catalog' / 'repositories.yaml'


def parse_front_matter(path: Path):
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        raise ValueError('missing YAML front matter at file start')
    parts = text.split('---', 2)
    if len(parts) < 3:
        raise ValueError("front matter closing delimiter '---' not found")
    # Treat front-matter dates as strings so invalid calendar dates produce
    # a clear validation error rather than a YAML timestamp parsing exception.
    data = yaml.load(parts[1], Loader=yaml.BaseLoader)
    if not isinstance(data, dict):
        raise ValueError('front matter must be a YAML mapping')
    return data


def validate_file(path: Path):
    errors = []
    try:
        data = parse_front_matter(path)
    except Exception as exc:
        return [f'{path}: {exc}']

    required = ('id', 'title', 'type', 'status', 'created', 'updated', 'domains', 'repositories', 'tags')
    for key in required:
        if key not in data:
            errors.append(f"{path}: missing required field '{key}'")

    document_id = data.get('id')
    doc_type = data.get('type')
    if 'id' in data and not ID_RE.fullmatch(str(document_id)):
        errors.append(f"{path}: invalid id '{document_id}' (expected OVR-REPO/INV/VER/EXP/ADR/PRD/DES/HOF-NNNN)")
    if 'type' in data and doc_type not in VALID_TYPES:
        errors.append(f"{path}: invalid type '{doc_type}'")
    if doc_type in TYPE_PREFIX and document_id is not None and ID_RE.fullmatch(str(document_id)):
        prefix = str(document_id).split('-')[1]
        if prefix != TYPE_PREFIX[doc_type]:
            errors.append(f"{path}: id prefix '{prefix}' does not match type '{doc_type}'")

    if 'status' in data and data['status'] not in VALID_STATUS:
        errors.append(f"{path}: invalid status '{data['status']}'")
    if 'title' in data and (not isinstance(data['title'], str) or not data['title'].strip()):
        errors.append(f"{path}: title must be a non-empty string")
    for key in ('domains', 'repositories', 'tags'):
        if key in data and not isinstance(data[key], list):
            errors.append(f"{path}: '{key}' must be a YAML list")

    dates = {}
    for key in ('created', 'updated'):
        if key in data:
            value = str(data[key])
            if not DATE_RE.fullmatch(value):
                errors.append(f"{path}: '{key}' must use YYYY-MM-DD")
            else:
                try:
                    dates[key] = date.fromisoformat(value)
                except ValueError:
                    errors.append(f"{path}: '{key}' is not a real calendar date")
    if dates.get('created') and dates.get('updated') and dates['created'] > dates['updated']:
        errors.append(f'{path}: created date must not be after updated date')
    return errors


def validate_catalog(path: Path):
    """Validate local catalog structure without fetching upstream repositories."""
    if not path.exists():
        return [f'{path}: catalog is missing']
    try:
        data = yaml.safe_load(path.read_text(encoding='utf-8'))
    except (OSError, yaml.YAMLError) as exc:
        return [f'{path}: cannot parse catalog: {exc}']
    if not isinstance(data, dict) or data.get('schema_version') != 1:
        return [f'{path}: expected schema_version: 1 mapping']
    entries = data.get('repositories')
    if not isinstance(entries, list):
        return [f"{path}: 'repositories' must be a list"]
    errors, seen = [], set()
    for i, entry in enumerate(entries, start=1):
        loc = f'{path}: repositories[{i}]'
        if not isinstance(entry, dict):
            errors.append(f'{loc}: must be a mapping')
            continue
        entry_id = entry.get('id')
        if not isinstance(entry_id, str) or not entry_id.strip():
            errors.append(f'{loc}: id must be a non-empty string')
        elif entry_id in seen:
            errors.append(f'{loc}: duplicate repository id {entry_id}')
        else:
            seen.add(entry_id)
        url = entry.get('url')
        if not isinstance(url, str) or not url.startswith('https://github.com/'):
            errors.append(f'{loc}: url must be a canonical https://github.com/ URL')
        if not isinstance(entry.get('name'), str) or not entry['name'].strip():
            errors.append(f'{loc}: name must be a non-empty string')
        if not isinstance(entry.get('kind'), str) or not entry['kind']:
            errors.append(f'{loc}: kind must be a non-empty string')
    return errors


def main():
    docs = []
    for directory in SEARCH_DIRS:
        if directory.exists():
            docs.extend(p for p in directory.rglob('*.md') if p.name.lower() != 'readme.md')
    errors, seen = validate_catalog(CATALOG), {}
    for path in sorted(docs):
        errors.extend(validate_file(path))
        try:
            data = parse_front_matter(path)
            doc_id = data.get('id')
            if doc_id:
                if doc_id in seen:
                    errors.append(f"duplicate id '{doc_id}': {seen[doc_id]} and {path}")
                else:
                    seen[doc_id] = path
        except Exception:
            pass
    if errors:
        print('\n'.join(f'ERROR: {error}' for error in errors))
        return 1
    print(f'Validated {len(docs)} artifact document(s); IDs unique; catalog valid.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
