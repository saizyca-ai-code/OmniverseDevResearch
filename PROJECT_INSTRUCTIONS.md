# OmniverseDevResearch — Project Instructions

## Mission
Research publicly available NVIDIA Omniverse repositories, SDKs, Extensions, APIs, tools, architecture, and version history. Prefer source-backed implementation analysis over high-level summaries when questions concern actual behavior.

## Canonical starting points
- Artifact repository: https://github.com/saizyca-ai-code/OmniverseDevResearch
- NVIDIA Omniverse repositories: https://github.com/orgs/NVIDIA-Omniverse/repositories
- NVIDIA Omniverse organization: https://github.com/NVIDIA-Omniverse

The upstream repository list changes. Verify repository existence, visibility, default branch, and relevant commit/tag during research. Public repositories do not necessarily represent all internal NVIDIA implementation.

## Before research
1. Search this artifact repository for existing reports and unresolved questions.
2. Define the question, scope, non-goals, and expected deliverable.
3. Record each upstream repository and the branch/tag/commit inspected.
4. Check official documentation, source, tests, examples, issues, pull requests, and release notes as relevant.

## Analysis standard
Investigate entry points, initialization, modules, classes, functions, configuration, callers/callees, control and data flow, dependency boundaries, events, callbacks, asynchronous behavior, lifecycle, cleanup, tests, runtime evidence, and version changes as relevant. Do not infer behavior from names or README text alone. Never invent source paths, line numbers, APIs, commits, access, or test results.

## Evidence and citations
Link to exact upstream sources and prefer commit-pinned file links. Record commit SHA or exact tag for each materially relevant repository. Separate directly observed facts, cross-checked findings, inferences, and unknowns. State whether each important result is source-inspected, static-checked, test-executed, runtime-verified, or not verified.

## Artifact workflow
Use a template in templates/. Save substantial reports in docs/research/ with a stable ID. Record experiment steps and environment under experiments/. Update catalog/repositories.yaml when repository metadata changes. Run python scripts/validate_research.py, python scripts/build_index.py, and pytest -q before proposing changes. Summarize changed files, evidence, unresolved questions, and checks performed. Never claim a Git operation succeeded unless it actually did.

## GitHub access
Use only an explicitly connected and authorized GitHub integration. Prefer feature branches and pull requests. Read access does not imply write access. If writing is unavailable, provide a patch and state that the repository was not modified.

## Safety and licensing
Prefer original analysis, short quotations, and source links over copying upstream files. Follow source licenses. Never commit secrets, access tokens, personal data, proprietary content, or unlicensed source dumps.

## Language
Use Traditional Chinese by default. Preserve original English names for APIs, classes, functions, paths, and technical terms.
