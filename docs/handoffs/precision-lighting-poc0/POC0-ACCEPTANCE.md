---
id: OVR-HOF-0002
title: PoC 0 — Acceptance Criteria
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
| **P0-AC-02** deps/build inventory | exact Kit/channel, extensions, declared RTX build and actual internal revision or unavailable reason, embedded USD/Python, package refs/hashes; identity method and policy/evidence references | inventory completeness: resolved values or explicit missing reasons; critical RTX identity: A authoritative mapping, or B only after the adopted ADR-0002 policy and all B01–B08/E01–E08 evidence plus human acceptance | missing critical identity or incomplete/unadopted B blocks full environment Go; hashes alone do not resolve vendor provenance |
| **P0-AC-03** machine inventory | Windows build, RTX GPU/VRAM, driver, 64GB RAM measured, sanitized logs | target matches requested hardware, driver and OS source given | mismatch ⇒ block target-hardware signoff, allow diagnostic |
| **P0-AC-04** Kit + USD | startup/shutdown logs, stage, prim dumps pre/post, fixed ON/OFF captures | exit cleanly (or documented recoverable shutdown defect), stage roundtrip values equal, finite visible light-dependent difference | black frames w/o diagnosis ≠ pass |
| **P0-AC-05** RT 2.0 and PT | per-mode exact selection settings, renderer confirmation, captures | both modes identified and render baseline, repeated once | one missing ⇒ no full Go; investigate fallback |
| **P0-AC-06** projector inspection | tested property full names/types/namespace, authored+reopened metadata, scene comparisons | completed property discovery probe and honest per-level result; **not** necessarily projector rendered | invented API/property = fail; missing property may be genuine `unsupported` |
| **P0-AC-07** AOV inventory/export | per-mode settings and individual attempts for DI, GI, illuminance, world position; raw data or negative logs | every requested probe attempted or explicitly justified `blocked`, each outcome accurate | AOV absence not automatically core No-Go |
| **P0-AC-08** result integrity | manifest schema validation, evidence refs/files, command transcript, negative-case test | every task has status, provenance, reproducibility, no fabricated evidence | missing artifacts/secret exposures = fail |
| **P0-AC-09** fallback governance | 110.4 blocker cause and version impact memo | maintain 110.4 unless recorded reproducible blocker + reviewer approves 110.3 scoped comparison | silent swap = fail |

### Accepted research identity policy and adoption boundary

[OVR-ADR-0002](../../research/OVR-ADR-0002-poc0-binary-identity-policy.md) is the sole detailed A/B policy contract. This is a **substantive acceptance change** explicitly accepted by the human owner on 2026-10-17, not a claim that the old AC-02 already accepted binary identity. Research publication and implementation adoption remain distinct: current implementation lock `27ab5add5c62692d47662e32401df860a82136cf` is unchanged, full environment Go=blocked and Full Gate0 not-assessed. Neither human policy acceptance nor L01–L05 principle acceptance approves a binary baseline or B result.

After separate policy acceptance/publication and reviewed implementation adoption, B may satisfy the critical identity purpose only for its approved local PoC scope, with every B/E condition and pre-run approval/post-run human acceptance complete. `internal_revision` remains unavailable; vendor provenance stays unresolved. Diagnostic pass, inventory pass, B final identity acceptance and full environment Go are separate. No historical run is relabeled. Other AC requirements, the four Gate decisions below, and Conditional Go restrictions are unchanged. Neither this PR nor a future policy merge authorizes PR-02.

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
