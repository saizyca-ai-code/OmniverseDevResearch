#!/usr/bin/env python3
"""Validate YAML front matter and stable IDs in research Markdown."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SEARCH_DIRS = (ROOT / "docs" / "research", ROOT / "experiments")
VALID_STATUS = {"planned", "in-progress", "review", "verified", "stale", "superseded", "accepted"}
VALID_TYPES = {"repository-analysis", "investigation", "version-comparison", "experiment", "decision"}
ID_RE = re.compile(r"^OVR-(REPO|INV|VER|EXP|ADR)-\d{4}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_front_matter(path: Path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML front matter at file start")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("front matter closing delimiter '---' not found")
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        raise ValueError("front matter must be a YAML mapping")
    return data


def validate_file(path: Path):
    errors = []
    try:
        data = parse_front_matter(path)
    except Exception as exc:
        return [f"{path}: {exc}"]

    required = ("id", "title", "type", "status", "created", "updated", "domains", "repositories", "tags")
    for key in required:
        if key not in data:
            errors.append(f"{path}: missing required field '{key}'")
    if "id" in data and not ID_RE.match(str(data["id"])):
        errors.append(f"{path}: invalid id '{data['id']}' (expected OVR-REPO/INV/VER/EXP/ADR-NNNN)")
    if "type" in data and data["type"] not in VALID_TYPES:
        errors.append(f"{path}: invalid type '{data['type']}'")
    if "status" in data and data["status"] not in VALID_STATUS:
        errors.append(f"{path}: invalid status '{data['status']}'")
    for key in ("domains", "repositories", "tags"):
        if key in data and not isinstance(data[key], list):
            errors.append(f"{path}: '{key}' must be a YAML list")
    for key in ("created", "updated"):
        if key in data and not DATE_RE.match(str(data[key])):
            errors.append(f"{path}: '{key}' must use YYYY-MM-DD")
    return errors


def main():
    docs = []
    for directory in SEARCH_DIRS:
        if directory.exists():
            docs.extend(p for p in directory.rglob("*.md") if p.name.lower() != "readme.md")
    errors = []
    seen = {}
    for path in sorted(docs):
        errors.extend(validate_file(path))
        try:
            data = parse_front_matter(path)
            doc_id = data.get("id")
            if doc_id:
                if doc_id in seen:
                    errors.append(f"duplicate id '{doc_id}': {seen[doc_id]} and {path}")
                else:
                    seen[doc_id] = path
        except Exception:
            pass
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print(f"Validated {len(docs)} research document(s); IDs are unique.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
