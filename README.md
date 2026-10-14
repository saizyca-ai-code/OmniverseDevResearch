# OmniverseDevResearch

Research artifacts for NVIDIA Omniverse repositories, SDKs, extensions, APIs, architecture, and reproducible experiments.

## Start here

1. Read [`PROJECT_INSTRUCTIONS.md`](PROJECT_INSTRUCTIONS.md).
2. Follow [`docs/governance/research-methodology.md`](docs/governance/research-methodology.md) and [`docs/governance/evidence-policy.md`](docs/governance/evidence-policy.md).
3. Register upstream repositories in [`catalog/repositories.yaml`](catalog/repositories.yaml).
4. Start new reports from `templates/`.
5. Run `python -m pip install -r requirements-dev.txt`, `python scripts/validate_research.py`, `python scripts/build_index.py`, and `pytest -q`.

## Layout

- `PROJECT_INSTRUCTIONS.md` — shared AI and researcher workflow.
- `catalog/` — machine-readable repository inventory.
- `docs/governance/` — research and evidence policies.
- `docs/research/` — durable research reports.
- `experiments/` — reproducible experiment records and scripts.
- `templates/` — standard report templates.
- `scripts/` — validation and index generation.
- `tests/` — automated tests.
- `.github/workflows/` — CI quality gates.

## Principles

Pin source-level claims to an upstream tag or commit SHA; distinguish observed facts from inference; never claim a test or runtime run that did not happen; do not store secrets or bulk copies of upstream source. Generated indexes are derived artifacts.
