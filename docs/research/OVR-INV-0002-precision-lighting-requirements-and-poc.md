---
id: OVR-INV-0002
title: Precision Lighting Requirements Baseline and PoC Roadmap
type: investigation
status: in-progress
created: 2026-10-15
updated: 2026-10-15
domains:
  - omniverse-kit
  - rtx-lighting
  - openusd
repositories: []
tags:
  - precision-lighting
  - virtual-first
  - requirements
  - poc
---

# Precision Lighting — Requirements Baseline and PoC Roadmap

> **Scope:** consolidated, user-confirmed product needs and proposed validation plan. **Not** a completed source investigation. Checked on: 2026-10-15. Validation: `not-verified` for software/RTX/runtime, `source-inspected` for this research repository's governance and schemas. This record deliberately does not invent upstream commit SHAs or observed experiments.

## Problem and desired outcome

Exhibition designers need to illuminate precise regions of booths, kiosks, display tables, wall-mounted exhibits and logos, while controlling edge sharpness, shape, CCT, rotation, perspective distortion and spill. Current project objective: build an authorable precision lighting system first; eventually synchronize scene lighting with actual on-site fixtures through DMX-over-IP and validate it as a calibrated Digital Twin.

## User-confirmed requirements

- **Strategy:** Virtual-First, Physical-Ready. Do not make lack of real fixtures or measured photometry block useful production visuals.
- **Platform:** reusable Omniverse Kit Extensions in a custom USD Composer-style Kit app.
- **Authoring:** both manual fixture/framing adjustments and selecting desired illumination regions in the viewport.
- **Targets:** planar signage/walls/logo regions, 3D products and future multi-surface booth regions plus exclusion zones.
- **Effects:** color/CCT, intensity, focusing and feather, free masks/polygons, framing/cropping, rotation, gobos and RTX haze/visible beams.
- **Inputs:** manual, later Art-Net and sACN. Live preview and offline design are both required.
- **Scale:** target control/update capacity 64–128 fixtures, **not** a promise of 128 simultaneously full-quality RTX projectors.
- **Development hardware:** Windows 11; GeForce RTX 5080 (16 GB VRAM); 64 GB system RAM.
- **Available physical evidence:** no fixture hardware and no measured photometric dataset at this time; visual and physical accuracy are intended as separate staged acceptance tracks.
- **Implementation status:** no product code or GPU testing performed or authorized in this stage.

## Scope and non-goals

PoC 1 should demonstrate one *Virtual Precision Projector* and planar surface targeting, authored masking and measurable render behavior. 3D silhouette targeting, volumetrics and projector direction LUT are exploratory. Real equipment calibration, GDTF/MVR support, DMX receiver, full moving-head optics and 128-fixture performance are out of scope of PoC 1.

## Preliminary solution and data boundaries — design hypothesis (C)

Keep `LightingDesignIntent` (target regions/exclusion regions), `FixtureState` and `ProjectionProfile` (transform, mask, focus, CCT, controls), and `RendererAdapter` (USD/RTX realization) separate. Future `FixtureDefinition`, `PhysicalConstraints`, `DMXMapping` and `CalibrationProfile` constrain, calibrate or synchronize that model, rather than replacing it. Uncalibrated fixture state must be explicit. See [OVR-ADR-0001](OVR-ADR-0001-virtual-first-physical-ready.md).

## Candidate public sources: **entry points only**, not commit-pinned implementation evidence

| Topic | Public source | Verification gap |
|---|---|---|
| Omniverse light/projector functionality | https://docs.omniverse.nvidia.com/materials-and-rendering/latest/lighting.html | Pin Kit/renderer release; test `RectLight` projector, texture mask semantics and persistence |
| OpenUSD light shaping | https://openusd.org/release/user_guides/schemas/usdLux/ShapingAPI.html | Verify versioned USD API, renderer mapping and interactions |
| Kit app template | https://github.com/NVIDIA-Omniverse/kit-app-template | Pin full commit SHA and resolved package versions |
| GDTF format | https://gdtf-development.com/help/developers/gdtf_1_2/file-format-definition/index.html | Evaluate per-fixture completeness and physical calibration usefulness |
| GDTF/MVR converter precedent | https://github.com/MomentFactory/Omniverse-MVR-GDTF-converter | Check license, exact commit, supported Kit version and real behavior |

**Version policy:** Kit 110.3 and 110.4 were discussed as *candidate* versions, not approved, pinned or tested. No vendor-provided claim in this document establishes actual RTX accuracy. Upstream source-level findings belong in a follow-up version-pinned investigation.

## Surface targeting and spill semantics

- **Planar target:** polygon anchored to a USD surface, reverse projection to a mask; geometric boundary error measured in world units.
- **3D target (exploratory):** light-view mesh silhouette, occlusion/raycasting and explicit background/table spill assessment.
- **Exclusion zones:** surfaces where added light should remain below a stated threshold.
- **Projection-based** behavior preserves illumination propagation and reflections; any artist-directed/non-physical effect must be visibly labeled.
- **Direct spill** is primary illumination outside the selected region. **Indirect spill** is bounce/reflection/transmission. **Optical spill** requires measured fixture optics in a later stage.
- Final sRGB images alone cannot prove direct-vs-indirect separation or absolute lux. Use geometry checks and, if the chosen RTX version supports them, appropriate linear render channels/AOVs; otherwise identify outputs as *relative proxies*.

## PoC roadmap — proposed (no experiments executed)

| Phase | Goal | Stop/go evidence |
|---|---|---|
| PoC 0 | Pin actual Kit, template commit, renderer, Windows build, GPU driver; verify minimal RTX environment | Reproducible startup, versions and initial render |
| PoC 1 | Single RTX projector with planar target and editable masks | Reproducible mask geometry, actual rendered light boundaries and scene reload |
| PoC 2 | Fixture constraints, feasibility statuses and safe/local control source experiments | Correct mappings, explicit achievable/approximate/unachievable/unknown states |
| PoC 3 | Benchmark 8/32/64/128 fixtures with differentiated quality workload | Measured FPS, p95 control-to-visible latency, VRAM, frame timing and quality |

## PoC 1 test matrix

| Test | Scene / operation | Mandatory? |
|---|---|---|
| T01 | Flat logo rectangle, basic projection | yes |
| T02 | Oblique exhibition wall, trapezoidal target | yes |
| T03 | Irregular polygon (3–12 vertices), edge feather and rotation | yes |
| T04 | 3D product on a table; silhouette, shadows and unwanted spill | exploratory |
| T05 | RTX Real-Time vs Path Tracing comparison under fixed camera/exposure | yes |
| T06 | Save, close and reopen stage + mask dependencies | yes |

## PoC 1 provisional acceptance matrix

| ID | Required observation | Test / threshold |
|---|---|---|
| AC-01 | Projector produces actual scene illumination | Runtime render and inspected USD state |
| AC-02 | CCT/intensity/rotation changes are visible | Fixed-camera A/B renders |
| AC-03 | Rectangular, trapezoidal and polygon masks generate correctly | Deterministic unit tests for valid/degenerate masks |
| AC-04 | Planar inverse projection aligns geometry | Candidate ≤10 mm boundary error in a defined small reference scene; **not** universal |
| AC-05 | Rendered spill is measurable | Candidate ≤1% relative signal at 20 mm beyond hard edge; pending texture/filter and light characterization |
| AC-06 | Feather produces measurable transition | Linear-image edge profiles under fixed conditions |
| AC-07 | Fixture, target and external mask links persist | Save/reopen and compare |
| AC-08 | RTX renderer-mode differences are recorded | Config/preset-pinned side-by-side captures, without expecting pixel identity |
| AC-09 | Unsupported controls or absent AOVs are reported rather than simulated as success | Explicit failed/blocked log |

**Critical distinction:** AC-04 geometry passing does not prove AC-05 renderer lighting passing. Lux targets, true CCT/spectral fidelity and physical fixture light distribution require future measurement and are not PoC 1 sign-off criteria.

## Go / no-go rule

If native RTX projector textures cannot produce reproducible, controllable illuminated borders, halt expansion into the full UI, physical mapping or 128-fixture scale. Investigate texture semantics, direction LUT, projection mathematics and occluder geometry as alternatives first.

## Evidence matrix

| Claim | Classification | State | Basis |
|---|---|---|---|
| User product goals, target hardware and absence of physical measurements | requirements record (not technical evidence grade) | user-confirmed | Project design conversation, 2026-10-15 |
| Proposed modular boundaries and solver options | C | not-verified | Engineering design hypothesis |
| Exact RTX projector/volumetric behavior on target GPU | U | not-verified | Requires PoC 0–1 |
| 64–128 fixture runtime performance | U | not-verified | Requires PoC 3 |
| Measured physical Digital Twin parity | U | not-verified | Physical reference measurements unavailable |

## Open questions / follow-up

1. Pin the USD Composer template, Kit/RTX packages and their exact compatible versions.
2. Read version-matched official API docs and source/tests where public; record actual refs, paths and symbols.
3. Verify mask filtering, projection clipping, dynamic texture updates and available renderer AOVs.
4. Define a persistent USD/sidecar representation and texture asset portability before implementation.
5. Establish a fixed benchmark scene and metric definitions, then lock AC-05 tolerances based on evidence.
6. When physical data becomes available, design separate photometric/colorimetric and scene-camera validation protocols.

## Related artifacts

- [OVR-ADR-0001 — Virtual-First, Physical-Ready](OVR-ADR-0001-virtual-first-physical-ready.md)
