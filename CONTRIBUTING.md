# Contributing Research Artifacts

## Branch and pull request policy
- Use research/<short-topic> for investigations and docs/<short-topic> for documentation-only changes.
- Keep pull requests focused on one question or a small related set.
- Once branch protection is enabled, avoid routine direct pushes to main.
- Summarize findings, upstream versions, validation performed, and known gaps in each pull request.

## Document requirements
- Start from a template in templates/.
- Assign each substantial document a unique ID such as OVR-INV-0001.
- Include upstream repository and commit/tag metadata.
- Cite material claims near the text they support.
- Mark assumptions and stale evidence explicitly.

## Local checks
    python -m pip install -r requirements-dev.txt
    python scripts/validate_research.py
    python scripts/build_index.py
    pytest -q

## Experiments
Record purpose, prerequisites, environment, exact commands, expected and actual output, and limitations. Avoid committing huge logs, caches, downloaded source trees, generated binaries, or credentials.
