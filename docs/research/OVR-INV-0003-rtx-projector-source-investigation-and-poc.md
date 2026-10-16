---
id: OVR-INV-0003
title: RTX Projector Source Investigation and PoC 0-1 Validation Contract
type: investigation
status: review
created: 2026-10-16
updated: 2026-10-16
domains:
  - omniverse-kit
  - rtx-lighting
  - openusd
repositories:
  - https://github.com/NVIDIA-Omniverse/kit-app-template
  - https://github.com/PixarAnimationStudios/OpenUSD
tags:
  - precision-lighting
  - projector
  - texture-mask
  - poc
---

# RTX Projector — Source Investigation and PoC 0–1 Contract

> Checked on: 2026-10-16. **Validation:** `source-inspected` for pinned public source/config; vendor documentation inspected separately; **`not-verified` for Kit/RTX runtime, GPU, AOV correctness and measured performance**. This is a conditional PoC selection, not proof of a working projector.

## Research question and scope

Can a custom USD Composer-style Kit application on Windows 11, RTX 5080 (16 GB), 64 GB RAM realize a single controllable **Virtual Precision Projector** using native RTX RectLight projector textures, with persistent planar mask targeting, dynamic updates and measurable direct spill?

Scope: Kit SDK 110.3/110.4 candidate selection; authored USD light/projector properties; mask/UV and direction LUT; texture reload; real-time versus path-traced behavior and AOV; comparative PoC pathways. Excludes actual Extension implementation, physical fixture/IES calibration, DMX, and a 64–128 simultaneous RTX light claim. Requirements: [OVR-INV-0002](OVR-INV-0002-precision-lighting-requirements-and-poc.md); architecture [OVR-ADR-0001](OVR-ADR-0001-virtual-first-physical-ready.md).

**Falsification gate:** If the native projector cannot reliably modulate actual scene illumination, show controllable boundaries and refresh a mask without restarting Kit, do not expand into full UI/DMX/scale; investigate renderer semantics, direction mapping and physical occluders first.

## Repositories and exact source versions

| Repository or component | Pinned version / source | What the pin means |
|---|---|---|
| [NVIDIA-Omniverse/kit-app-template](https://github.com/NVIDIA-Omniverse/kit-app-template) | [`9cc43b764e6d4cd86cb6296a8440665c3c4f4843`](https://github.com/NVIDIA-Omniverse/kit-app-template/tree/9cc43b764e6d4cd86cb6296a8440665c3c4f4843) (2026-10-09 promotion of 110.4) | Actual public template commit, **not** a resolved Kit/RTX binary |
| Kit SDK | candidate 110.4.0, fallback 110.3.0 | [`VERSION.md`](https://github.com/NVIDIA-Omniverse/kit-app-template/blob/9cc43b764e6d4cd86cb6296a8440665c3c4f4843/VERSION.md); [`tools/deps/kit-sdk.packman.xml`](https://github.com/NVIDIA-Omniverse/kit-app-template/blob/9cc43b764e6d4cd86cb6296a8440665c3c4f4843/tools/deps/kit-sdk.packman.xml) declares `kit-kernel 110.4.0+feature.${platform_target_abi}.${config}`; installation unresolved |
| Kit template dependencies | `kit_core_templates` and `kit_sample_templates`: `110.4.0+feature.12163.dba6fe6d.gl` | [`tools/deps/repo-deps.packman.xml`](https://github.com/NVIDIA-Omniverse/kit-app-template/blob/9cc43b764e6d4cd86cb6296a8440665c3c4f4843/tools/deps/repo-deps.packman.xml); resolved extension tree not inspected |
| [PixarAnimationStudios/OpenUSD](https://github.com/PixarAnimationStudios/OpenUSD) | [v25.11 commit `363a7c8da8d1937072a5f0989e91faf72eb1fa76`](https://github.com/PixarAnimationStudios/OpenUSD/tree/363a7c8da8d1937072a5f0989e91faf72eb1fa76) | Upstream schema research baseline; **not proof** Kit embeds the identical binary |
| RTX Renderer | version **U** (resolve at PoC 0) | Vendor [Lighting](https://docs.omniverse.nvidia.com/materials-and-rendering/latest/lighting.html), [RT 2.0](https://docs.omniverse.nvidia.com/materials-and-rendering/latest/rtx-renderer_rt.html), [Path Tracing](https://docs.omniverse.nvidia.com/materials-and-rendering/latest/rtx-renderer_pt.html). These are floating `latest` docs, **not commit-pinned implementation** |

Template README distinguishes a feature-branch SDK from production NGC branch. PoC 0 must record build/channel and assess eventual production migration; template promotion alone does not grant long-term API stability.

## Findings: property boundaries and data flow

1. **OpenUSD-defined**: [`pxr/usd/usdLux/schema.usda` RectLight (lines 1131–1172)](https://github.com/PixarAnimationStudios/OpenUSD/blob/363a7c8da8d1937072a5f0989e91faf72eb1fa76/pxr/usd/usdLux/schema.usda#L1131-L1172) declares `inputs:width`, `inputs:height`, `inputs:texture:file` (asset, color texture). LightAPI defines `inputs:intensity`, `inputs:exposure`, `inputs:enableColorTemperature`, `inputs:colorTemperature` ([same schema](https://github.com/PixarAnimationStudios/OpenUSD/blob/363a7c8da8d1937072a5f0989e91faf72eb1fa76/pxr/usd/usdLux/schema.usda)). `ShapingAPI` is separate. **Do not assume `UsdLuxRectLight.CreateIsProjectorAttr()` exists**: `isProjector` is not a standard RectLight schema property in that inspected file.
2. **RTX-specific, documentation evidence**: NVIDIA [Lighting](https://docs.omniverse.nvidia.com/materials-and-rendering/latest/lighting.html) describes enabling `isProjector` for RectLight projector behavior and using `inputs:texture:file`; also describes `projection:directionTexture:file` for direction mapping. Exact attribute registration, fallback, authoring namespace, supported render modes and persistent behavior are **U until Kit property inspection**. Do not conflate ordinary textured RectLight with projector mode.
3. **Directional LUT is not a mask**: NVIDIA documents a 32-bit float OpenEXR encoding direction information; verify channel conventions and renderer-specific loading before authoring. Use `MaskTexture` for spatial illumination weights, `DirectionTexture` for ray-direction mapping. Do not promote LUT into the default PoC 1 path without evidence.
4. **Texture reload**: NVIDIA Kit 110.2 release notes describe automatic reload when on-disk textures change (historical document evidence). It is a **C inference**, not verified, that RTX projector textures in the 110.4 stack use the same invalidation path. Disk overwrite and new-URI asset setting must both be tested; shader/asset reload may differ from material textures.
5. **Projection geometry**: for a planar target and an empirically calibrated pinhole-like projector, a 3×3 homography maps plane points to UV. Geometry correctness can be unit-tested; **RTX's effective ray mapping and light area are unverified**. Establish orientation with an asymmetric four-corner calibration image; handle behind-projector points, singularities, clipping, handedness and image UV reversal.
6. **Render modes/AOV**: RTX Path Tracing documentation lists `/rtx/pathtracing/diAOV`, `giAOV`, `illuminanceAOV`, `worldPosAOV`. Their availability, quality, denoiser interactions and units in the selected runtime remain **U**. No equivalent RT 2.0 AOV parity is assumed. Simple Fog cannot stand in for physically scattering haze. Ignore haze as core PoC 1 go/no-go.
7. **USD controls**: `intensity`, `exposure`, CCT/color and transform are authoring foundations. `ShapingAPI` focus/cone softness is **not equivalent** to lens optical focus or custom polygon feather; no standard projector zoom contract established. Renderer acceptance is not implied by USD attribute existence.

### Conceptual data path — hypothesis, not inspected RTX call chain

`LightingDesignIntent / TargetPlane` → `ProjectionProfile (UV calibration, polygon/feather)` → `MaskTexture asset` → `UsdLuxRectLight + RTX-specific projector property` → `RTX Renderer` → `render/AOV measurement`.

Only upstream authoring schemas and template dependency declarations were inspected. RTX ingestion, sampling, cache invalidation, GPU data flow and cleanup are closed or uninspected implementation boundaries. **There is no evidenced source-level renderer call chain.**

## Evidence matrix

| ID | Claim | Grade | Validation | Basis / required follow-up |
|---|---|---|---|---|
| E01 | 110.4.0 template and package declarations exist | A | source-inspected | pinned template `VERSION.md`, `kit-sdk.packman.xml`, `repo-deps.packman.xml` |
| E02 | OpenUSD v25.11 RectLight declares an asset texture input | A | source-inspected | pinned `schema.usda`, `RectLight` |
| E03 | OpenUSD LightAPI defines intensity, exposure and CCT controls | A | source-inspected | pinned `schema.usda`, `LightAPI` |
| E04 | RTX docs describe isProjector and directionTexture | A | source-inspected (documentation) | NVIDIA Lighting URL, checked 2026-10-16; no public renderer implementation pin |
| E05 | Disk texture reload correction appears in Kit release notes | A | source-inspected (documentation) | [Kit 110.2 release notes](https://docs.omniverse.nvidia.com/kit/docs/kit-sdk/110.2.0/docs/overview/release-notes.html), path/version to reconfirm at runtime |
| E06 | Projector uses same reload path as general textures | C | not-verified | test same URI overwrite vs changing URI |
| E07 | Planar homography can produce correct mask UVs | C | not-verified | unit tests plus empirical projector calibration |
| E08 | Projector hard-edge/alpha/feather and shadow fidelity | U | not-verified | RTX RT 2.0 & PT comparison |
| E09 | RTX PT AOV settings are documented | A | source-inspected (documentation) | NVIDIA PT docs; actual working channels unverified |
| E10 | AOV outputs allow reproducible direct/indirect spill separation | C | not-verified | DI/illuminance/GI difference tests and controlled scene |
| E11 | GPU update latency, VRAM, alpha semantics, video texture projector support | U | not-verified | PoC 0/1 |
| E12 | Physical Lux/spectral parity, 64–128 simultaneous render quality | U | not-verified | outside PoC 1 |

No B rating is assigned for RTX runtime behavior: multiple vendor documents do not independently verify actual renderer output.

## Projector capability matrix and constraints

| Capability | Evidence / state | PoC disposition |
|---|---|---|
| Native RTX projector with RectLight + texture | A vendor docs; runtime U | mandatory |
| RGB/BW mask affecting actual scene lighting | C expected; U fidelity | mandatory, opaque grayscale first |
| Polygon (3–12 vertices) | C rasterization | mandatory geometry and render |
| Alpha channel semantics | U | isolate optional experiment, never assume transparency controls light |
| Hard edge, feather / sharpness | U render fidelity; C mask generation | mandatory measured edge profile |
| Perspective/oblique plane correction | C mapping; U renderer model | mandatory |
| Direction LUT EXR | A vendor docs; runtime U | exploratory only |
| Dynamic same-URI reload | C | mandatory |
| Dynamic new-URI update | C | mandatory |
| Intensity/CCT/rotation | A schema; U RTX behavior | mandatory |
| Focus/zoom | U specific optical implementation | explicit unsupported/approximate rather than invent |
| RT 2.0/PT shadows, haze and beams | U on chosen stack | shadow/mode comparison mandatory; haze exploratory |
| Direct/indirect spill AOV | A docs, U measured behavior | mandatory detection and truthful fallback |

## Alternatives and conditional selection

| Candidate | Expected benefits | Primary costs / unknowns | Decision |
|---|---|---|---|
| **A** Native RTX Projector + dynamic Mask | closest to authorable projector; renderer native lighting possible; compact USD scene | actual mask sampling, temporal filtering, reload, texture latency | **first PoC hypothesis; not product commitment** |
| **B** Projector + Direction LUT | optical distortion/nonstandard ray-direction calibration | EXR direction encoding, debugging and precision; LUT not mask substitute | only if calibration demonstrates need |
| **C** USD light + physical occluder geometry | explicit ray shadow geometry, diagnostic comparator | penumbra, near-field setup, occluder motion, authoring complexity | small fallback/reference experiment if A fails |
| **D** Other officially supported projections/video | potential streaming optimization | projector compatibility unknown | defer; no custom renderer by default |

Light linking/material changes are not accepted as physical beam clipping. Keep `LightingDesignIntent`, `FixtureState`, `ProjectionProfile`, `RendererAdapter` separate (existing ADR).

## PoC 0 — environment and dependency verification plan (not executed)

**Target:** Windows 11, RTX 5080 16 GB, 64 GB RAM, custom Kit USD Composer-style app. Begin with pinned template commit, 110.4.0 feature candidate. Compare 110.3 only if justified by reproducible 110.4 blocker.

| ID | Action | Required artifact / pass |
|---|---|---|
| P0-01 | Resolve Kit SDK/NGC availability, license, template/tooling and Windows installation | exact URLs, channel/build, package identifiers, download outcome |
| P0-02 | Capture SDK/RTX/OpenUSD extension dependency tree | version and hashes of actual installed packages; Python version |
| P0-03 | Capture Windows version, driver, GPU and renderer settings | reproducible environment manifest, no secrets |
| P0-04 | Launch minimal custom Kit app, load/save USD, ordinary RectLight | logs and valid baseline render |
| P0-05 | Select RTX Real-Time 2.0 and Path Tracing separately | launch logs, mode-specific renders/settings |
| P0-06 | Inspect actual USD properties for `isProjector`, texture and LUT; test persistence | prim dump before/after reopen, no invented API |
| P0-07 | Probe documented AOV enablement and export | sample outputs or explicit unsupported/blocked logs |

**Go:** reproducible startup, basic render and USD roundtrip in both rendering modes with version/driver evidence. **Blocked/No-Go:** unresolved package, unsupported renderer, or stable startup failure; investigate rather than silently switch SDK. Runtime results must be separately labeled `test-executed` / `runtime-verified` only after execution.

## PoC 1 — isolated work packages, fixtures and metrics (not executed)

**WP-01: Native projector contract**. Four control scenes: ordinary RectLight without texture; textured RectLight `isProjector=false`; projector with asymmetric RGB orientation card `isProjector=true`; projector + LUT (optional). Verify true surface lighting difference rather than mere visible source, CCT/intensity/rotation, shadows, save/reopen. Inspect property names/types and USD layer persistence.

**WP-02: Dynamic mask contract**. Use deterministic binary black/white masks with unique visible Update ID markers. DU-01 atomic publication of same-URI PNG; DU-02 new file/URI + `UsdAttribute.Set()`; DU-03 repeated A/B switching and fixed update cadence; DU-04 re-open USD/assets. Record `t0` mask ready, `t1` USD authored, `t2` first visible new mask, `t3` stable image, missed/stale states, FPS/frame spike, GPU VRAM, logs. `t2-t0` and `t3-t0` must not be confused with file write time. No predetermined 16/33 ms claim.

**WP-03: geometry and spill**. Flat plane first; tilted exhibition wall second; polygons of 3–12 vertices with hard edges, rotated UV and feather. Fix stage units, projector/plane transforms, texture resolution, camera, exposure, sampling and color space. Unit-test degeneracy, winding/handedness, UV clipping; asymmetric corner card before homography. Compare geometry boundary error in mm to measured rendered illumination edge, report separate results in RT 2.0/PT. Capture beauty + supported **linear** DI/illuminance/GI/world-position channels (disable or characterize denoiser), Projector ON/OFF difference; test NaN/Inf and unavailable AOV. Compute 10–90% intensity edge width and direct spill outside target. DI contribution is **not automatically physical lux**. GI outside the target is not automatically a projector clipping failure.

### Traceable acceptance IDs

- **AC-01/02:** actual projected illumination, changes to CCT/intensity/rotation and saved attributes visible in controlled A/B.
- **AC-03:** deterministic rectangular/trapezoid/polygon mask generation, including invalid geometry cases.
- **AC-04:** plane inverse mapping geometry measured separately; existing **candidate** ≤10 mm only after reference scale locked.
- **AC-05:** relative direct spill observed in defined ROI; existing **candidate** ≤1% at 20 mm beyond edge is not yet a universal guarantee.
- **AC-06:** feather has a repeatable edge transition `w10-90` under pinned settings.
- **AC-07:** stage/asset portability and reopen.
- **AC-08/09:** mode comparison and explicit unsupported/AOV failures; do not fabricate success.
- **AC-10 (proposed):** repeatable dynamic mask visibility and bounded resource behavior; only freeze p95 latency after initial measurements.

**Go A:** projected illumination is real, dynamically controllable and boundaries measurable within accepted scene-local thresholds. **Conditional Go:** sound functionality but documented quality/latency constraints and transparent product labels. **No-Go A:** no controllable projected illumination or persistent/unbounded cache/latency failures; run scoped B/C comparator. Haze, 3D silhouettes, fixture calibration and 64–128 parallel render performance are outside core sign-off.

## Outstanding API/runtime assumptions and follow-up

1. Actual `isProjector` and `projection:directionTexture:file` authored type, namespace, fallbacks, metadata and renderer ingestion on resolved Kit 110.4.
2. Exact Windows ABI/config `kit-kernel` build, RTX renderer version, packaged OpenUSD version and production channel differences.
3. Grayscale versus RGB/alpha compositing, texture filtering, color space, mipmaps and emission response.
4. Mask change notification and A1/A2 update ordering; whether any supported GPU-resident update path exists.
5. Projector optical mapping versus ideal pinhole assumption; perspective limits, source size, penumbra.
6. PT versus RT 2.0 shadow/volumetric/AOV behaviors and denoiser/sample effects.
7. Linear AOV interpretation, units and repeatable separation of direct/indirect spill.

**Stop condition met for source investigation**: further renderer-specific uncertainty requires executable PoC. Author PRD/Technical Design/Handoff in a subsequent phase using this *test contract*, but do not claim physical or RTX-runtime validation from this report.

## Related records

- [OVR-INV-0002 — Requirements and PoC roadmap](OVR-INV-0002-precision-lighting-requirements-and-poc.md)
- [OVR-ADR-0001 — Virtual-First, Physical-Ready](OVR-ADR-0001-virtual-first-physical-ready.md)
