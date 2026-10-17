---
id: OVR-HOF-0003
title: PoC 0 — Verification Plan
type: handoff
status: planned
created: 2026-10-16
updated: 2026-10-17
domains: [omniverse-kit, rtx-lighting, openusd]
repositories:
  - https://github.com/NVIDIA-Omniverse/kit-app-template
  - https://github.com/PixarAnimationStudios/OpenUSD
tags: [precision-lighting, poc0, acceptance, validation]
---

# PoC 0 — Verification Plan and Evidence Checklist

> Draft 2026-10-16. This is a **future execution plan**, not test results.

## 1. Test levels
| Level | Test | Environment | Evidence |
|---|---|---|---|
| Static | Manifest schema, no secret/path leaks, required keys, evidence path resolution, correct statuses | Any approved CI | validator output |
| Unit | Probe status transitions, serialization, error paths, negative mocks for SDK/mode/property/AOV missing | ordinary Python | pytest report |
| Integration | SDK locator, resolved Kit Python/version probes, USD stage read/write | Installed Kit environment | exact logs + before/after stage dumps |
| Kit Runtime | Minimal app startup/stop; RectLight ON/OFF; save/reopen | Windows 11 target | stdout/stderr, USD, frames |
| RTX Visual | RT 2.0/PT separate mode selection, light-dependent pixels, orientation card | RTX 5080 / driver manifest | mode config + captures |
| RTX AOV | detect settings, enable and export channels per mode, finite buffer checks | RTX 5080 | raw AOV/channel metadata + failure reports |

## 2. Baseline fixtures
- `scene-flat-reference.usda`: static plane (material and normal held fixed), a USD RectLight, one calibrated/locked camera, fixed spatial scale (proposed 1 meter per USD unit; explicitly author), no auto-exposure if possible.
- Light ON/OFF renders, same camera/viewport/resolution/exposure, showing nonzero repeatable effect.
- `projector-orientation.png`: asymmetrical R/G/B corner markers and unique identifier for discovery experiment, not a final mask.
- Capture renderer settings, sample count, denoiser, color pipeline, background light, timestamp, output resolution.
- Choose scene geometry numerically before implementation; do not claim thresholds based on undocumented screenshot viewing alone.

## 3. Ordered runbook
1. Preflight permissions, repo and toolchain; record approved implementation path.
2. Inspect template at pinned commit and tool version; verify SDK acquisition entitlement/availability.
3. Capture host OS/GPU/driver/RAM and Kit/renderer/OpenUSD/Python resolved identities.
4. Launch minimal app with stdout/stderr + exit code; verify clean shutdown.
5. Author/save/close/reopen fixed stage and diff USD properties.
6. Select and confirm RT 2.0; ON/OFF control captures and finite-pixel checks; repeat.
7. Select and confirm Path Tracing; repeat and store actual sampling settings.
8. Inspect properties on ordinary/textured/projector candidate RectLight, author/reopen if supported.
9. Enumerate/test AOV availability/export separately for RT 2.0/PT; raw channels validated.
10. Validate manifest and evidence integrity, redact secrets, issue reviewer-ready gate report.
11. If failed, classify `fail|blocked|not-run`; keep original attempts immutable, add new run ID for retry.

## 4. Negative-case tests
- SDK resolution unavailable / auth rejected / wrong ABI → blocked with direct error.
- `nvidia-smi` not installed → host inventory partial; do not invent RTX model.
- Missing renderer mode → report unsupported/blocked, no automatic fallback renderer.
- No scene illumination due to source/camera/exposure → do not pass simply for a saved PNG.
- Missing guessed `isProjector` → no fabricated `CreateIsProjectorAttr()` or speculative USD attribute.
- AOV setting present but export absent → `discovered` not `exported`.
- AOV buffer all NaN/Inf or wrong dimensions → failed export validation.
- USD save succeeded but stage reopen differs → fail roundtrip.
- Image comparison affected by exposure/denoising → report confounders and retest.

## 5. Evidence bundle (proposed)
```
artifacts/runs/<run-id>/
  environment.json
  capabilities.json
  run-summary.json
  resolved-dependencies.json
  command-transcript.txt
  logs/{bootstrap,app,rt2,pt,property,aov}.log
  usd/{source,reopened,prim-before,prim-after}.* 
  captures/{light-on,light-off}-{rt2,pt}.*
  aov/{rt2,pt}/...                     # if exported
  evidence-index.sha256
  redaction-review.md
```
Do not put sensitive raw logs or proprietary SDK binaries in public GitHub. Keep evidence index paths relative. File generation/retention policy is determined by future implementation repository security settings, not invented here.

## 6. Metrics and assertions
- `stage_roundtrip_diff_count == 0` for explicitly listed expected authored prims/attributes; floating values compared by stored USD scalar values or explicitly documented tolerance, not screenshot comparison.
- Image validity: expected width/height, finite pixels, identifiable receiver geometry and light ON/OFF difference beyond observed noise floor. Exact difference threshold TBD after first baseline.
- Renderer identity: proven by actual recorded settings and logs, not filename.
- Reproducibility: two distinct attempts on same pinned environment for required startup/roundtrip/render steps.
- Probe coverage: all P0-01…07 outcomes accounted for; negative results not suppressed.
- No artificial measured FPS, latency, light intensity, AOV units.

## 7. Troubleshooting / escalation
| Symptom | First checks | Decision impact |
|---|---|---|
| Package failure | license, auth, platform ABI, SDK channel and dependency errors | blocked; version switch requires review |
| RTX mode absent | supported version matrix, renderer dependency, GPU/driver log | conditional/blocked |
| Blank frame | camera, light intensity/exposure, receiver normals, viewport, GPU log | redo baseline; not pass |
| Stage mismatch | edit target/layer, asset path, attribute type, flush/save | fail until reproducible |
| Projector no effect | ordinary vs textured vs enabled; full attribute dump | PoC 1 risk, not fake success |
| AOV blank/unavailable | mode support, settings and capture path, denoiser | record exact limitation |

## 8. Completion and report ownership
Agent attaches `run-summary.json`, AC matrix with evidence links, actual commands and exit codes, version manifest, unresolved items and gate proposal. Human reviewer signs off independently. No Kit/runtime evidence exists at the time this draft was created.

## 9. Candidate binary identity verification

This proposed extension is governed by [ADR-0002](../../research/OVR-ADR-0002-poc0-binary-identity-policy.md), including the sole detailed B01–B08/L01–L05/E01–E08 definitions, criticality/coverage, canonical identity v1 contract and synthetic test vectors. It is not adopted by the existing implementation lock; current Go remains blocked.

- Required source of inputs: reviewed source/acquisition/integrity issues (E01), full coverage classification and approved scan domains (E02), exact binary manifest and per-mode environment IDs (E03), named custodian/restorable evidence (E07). Unknown critical or unresolved concrete integrity concern blocks B. Environment records are not driver byte attestation.
- Implementation must independently verify canonical vectors and negative cases specified in ADR. Missing/extra/duplicate/unknown modules, bad schema/digest/path/link, source/environment drift, wrong approval/policy, absent pre/post evidence and impersonated human cannot yield B-pass. A successful diagnostic test is still reported pass at that level.
- Before an acceptance run: published/accepted policy plus reviewed implementation adoption, E04/E06 checker/control preparation, named human approval binding exact set/allowed mode environments/coverage/limitations and a separate execution authorization. No unapproved-baseline exploration may be retroactively called B acceptance.
- Each new required USD/RT2/PT run (two per probe/mode) records pre-covered-set, documented runtime loaded paths/hashes/exact plugin set/versions and sources, clean exit, post-covered-set and source fingerprints. Fixed scene/settings/command must match approved environment IDs. No in-place updates. Original failures remain immutable.
- After runs: automated assertions/missing lists are evidence for independent human E08 review, not self-signoff. Human can accept or reject actual E01–E07 evidence without requiring an already-existing B-pass. Only then evaluate B final identity acceptance; other AC and full Gate signoff remain separate.
- All E evidence is required before B final acceptance, **not all before S3 policy/implementation adoption**. Post-run evidence must not become a prerequisite for the reviewed adoption needed to generate it. Any not-run/blocked/fail requirement cannot silently pass; missing/failed evidence stops final B acceptance.

Required report levels and human record fields are defined in ADR, illustrated in [example0.2](expected-manifest.example.json). Research metadata/JSON/vector tests do not establish GPU behavior. This PR performs no new Kit/RTX run, baseline approval, B acceptance or PR-02 work.
