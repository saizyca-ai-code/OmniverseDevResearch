---
id: OVR-ADR-0001
title: Virtual-First Physical-Ready Precision Lighting Architecture
type: decision
status: accepted
created: 2026-10-15
updated: 2026-10-16
domains:
  - omniverse-kit
  - rtx-lighting
  - architecture
repositories: []
tags:
  - virtual-first
  - physical-ready
  - lighting
  - digital-twin
---

# ADR: Virtual-First, Physical-Ready Precision Lighting

 > Accepted architectural direction following user approval and the merge of PR #3 on 2026-10-15; **not** a claim of verified implementation or photometric correctness. Runtime validation: `not-verified`.

## Context

For exhibits and kiosks, designers need freeform targeted lighting, edge control, color temperature, gobo and haze now. The longer-term outcome is a scene that reproduces and synchronizes real fixtures via Art-Net / sACN. No real fixture or measured light distribution is currently available, so making calibrated photometry a prerequisite would block useful visual production without providing verifiable Digital Twin accuracy.

## Decision

Adopt **Virtual-First, Physical-Ready** in the forthcoming Precision Lighting Engine:

1. First support artist-defined light masks and surface targeting as a virtual tool, not as a claim of physical fixture achievability.
2. Separate user intent/target surfaces, fixture control state, geometry and projector mask, and renderer-specific USD/RTX implementation.
3. Record units, anchors, uncalibrated status and external asset dependencies explicitly.
4. Introduce later optional physical fixture definitions, DMX mapping, reachability constraints and measured calibration without silently changing the meaning of saved virtual designs.
5. Label non-physical/art-directed exceptions; Physical Digital Twin mode must refuse or report targets it cannot reproduce with available fixture capabilities.
6. Treat photometric parity, visual similarity and real-time performance as separate verification tracks.

## Alternatives considered

| Option | Reason not selected for initial development |
|---|---|
| Physical fixture-first | Real measurements and complete real fixture optics are currently unavailable; limits necessary exhibition work |
| Only fixed generic spotlights | Inadequate framing, polygon target and logo precision |
| Light Linking / material tricks as physical spill solution | Rendering association/material effects do not reproduce true physical beam clipping |
| Custom rendering engine immediately | Cost and integration risk before measuring capabilities of RTX native projectors |

## Consequences and risks

- Enables immediate freeform masks and design iteration.
- Requires explicit separation of abstract brightness vs calibrated photometric quantity, design intent vs resulting light, and geometric boundaries vs rendered spill.
- Physical conversion of arbitrary virtual designs may be **unachievable**; present error and alternatives rather than synthetic success.
- RTX projector mask update semantics, renderer fidelity, haze and performance remain unknown pending tests.
- The 64–128 fixture requirement is a control-capacity target, not simultaneous high-quality rendering guarantee.

## Evidence and references

- [OVR-INV-0002 — Requirements and PoC baseline](OVR-INV-0002-precision-lighting-requirements-and-poc.md).
- Direct user-confirmed requirements from 2026-10-15 project planning discussion (decision context, not independently verified technical behavior).
- Public technical entry points and validation gaps documented in OVR-INV-0002; follow-up pinned source findings and PoC contract in [OVR-INV-0003](OVR-INV-0003-rtx-projector-source-investigation-and-poc.md). No upstream commit-pinned RTX runtime evidence is claimed.
- Evidence classification of implementation feasibility: **C** (proposed design); current runtime validation: `not-verified`.

## Revisit conditions

Reassess after PoC 1 demonstrates/falsifies actual RTX projector mask fidelity; if native RTX behavior makes key targets infeasible; when a real fixture/GDTF/IES and measured illumination become available; when a candidate Kit+Renderer version is pinned and major differences emerge; or when DMX feedback/actual outputs become part of the product scope.

## Review status

User direction approval was recorded on 2026-10-15 and [PR #3](https://github.com/saizyca-ai-code/OmniverseDevResearch/pull/3) merged on 2026-10-15. Governance status is now `accepted` in this follow-up research PR, correcting the historical `review` metadata. This accepts the Virtual-First, Physical-Ready **architectural decision only**, not RTX projector behavior, calibration, performance or product implementation. No code, RTX runtime test or deployment has been performed.
