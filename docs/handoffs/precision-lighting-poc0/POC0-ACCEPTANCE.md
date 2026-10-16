# PoC 0 — Acceptance Criteria and Gate Decision

> Draft 2026-10-16; source: OVR-INV-0003 PoC 0 P0-01..07. No executable Kit/RTX validation yet.

## Rules
- `pass`: stated assertion was **actually observed** on target configuration with required evidence.
- `fail`: completed probe contradicts assertion (incl. bad roundtrip/light difference).
- `blocked`: necessary dependency/environment unavailable; no valid conclusion about runtime behavior.
- `not-run`: not attempted (different from blocked).
- Each test requires run ID, exact build + renderer where relevant, assertion/evidence reference, observed output, time and executor. Evidence hash recommended.
- Single unknown/unsupported AOV must not be silently marked pass; it can be a recorded non-blocking limitation if core probe is complete.

| Acceptance | Required proof | Pass | Fail/Block guidance |
|---|---|---|---|
| **P0-AC-01** SDK/template provenance | pinned template commit, SDK resolution output, package IDs/channel/license review, commands | actual 110.4 candidate binary resolved and licensed, or clearly documented approved equivalent | SDK inaccessible = blocked; no substitution |
| **P0-AC-02** deps/build inventory | exact Kit build/channel, extensions, RTX build, embedded USD, Python, package refs/hashes or `unavailable` notes | each required version resolved or explicit missing reason; full environment Go requires critical versions resolved | missing critical SDK/RTX identity blocks Go |
| **P0-AC-03** machine inventory | Windows build, RTX GPU/VRAM, driver, 64GB RAM measured, sanitized logs | target matches requested hardware, driver and OS source given | mismatch ⇒ block target-hardware signoff, allow diagnostic |
| **P0-AC-04** Kit + USD | startup/shutdown logs, stage, prim dumps pre/post, fixed ON/OFF captures | exit cleanly (or documented recoverable shutdown defect), stage roundtrip values equal, finite visible light-dependent difference | black frames w/o diagnosis ≠ pass |
| **P0-AC-05** RT 2.0 and PT | per-mode exact selection settings, renderer confirmation, captures | both modes identified and render baseline, repeated once | one missing ⇒ no full Go; investigate fallback |
| **P0-AC-06** projector inspection | tested property full names/types/namespace, authored+reopened metadata, scene comparisons | completed property discovery probe and honest per-level result; **not** necessarily projector rendered | invented API/property = fail; missing property may be genuine `unsupported` |
| **P0-AC-07** AOV inventory/export | per-mode settings and individual attempts for DI, GI, illuminance, world position; raw data or negative logs | every requested probe attempted or explicitly justified `blocked`, each outcome accurate | AOV absence not automatically core No-Go |
| **P0-AC-08** result integrity | manifest schema validation, evidence refs/files, command transcript, negative-case test | every task has status, provenance, reproducibility, no fabricated evidence | missing artifacts/secret exposures = fail |
| **P0-AC-09** fallback governance | 110.4 blocker cause and version impact memo | maintain 110.4 unless recorded reproducible blocker + reviewer approves 110.3 scoped comparison | silent swap = fail |

### Gate 0 decision
**GO:** AC-01…05 and AC-08 pass on approved target hardware; AC-06/07 completed to a truthful level (can contain supported/unsupported/unknown claims and conditional gaps) and AC-09 respected. Projector visible/rendered success is PoC 1 feasibility gate, **not** necessarily PoC 0 Gate 0.

**CONDITIONAL GO:** baseline SDK/USD/at least one RTX mode works but one mode, critical version identity, or critical capability remains incomplete and is explicitly scoped. Allows safe parallel Pure Core work; **does not authorize unverified RTX Adapter implementation assumptions**.

**BLOCKED:** no usable SDK/license, no approved GPU environment, no reproducible renderer startup, or no trustworthy evidence.

**NO-GO:** reproducible negative results demonstrate candidate environment cannot satisfy required two-renderer baseline or fundamental stage/light behavior; preserve reproducer and propose approved fallback. A single absent AOV alone does not imply No-Go.

**Reviewer signoff fields (blank until executed):**
```
reviewer: TBD
reviewed_run_ids: []
candidate_build: TBD
decision: not-assessed
blocking_ACs: []
accepted_limitations: []
fallback_approval: not-requested
date: TBD
```

### Relationship to PoC 1
PoC 0 intentionally does not sign off AC-01..10 of PoC 1, A2/A1 texture refresh, homography error, direct/indirect spill correctness, latency p95, or physical lux.