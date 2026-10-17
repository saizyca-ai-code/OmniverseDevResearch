---
id: OVR-DES-0001
title: PoC 0 — Environment and Capability Technical Design
type: technical-design
status: planned
created: 2026-10-16
updated: 2026-10-17
domains: [omniverse-kit, rtx-lighting, openusd]
repositories:
  - https://github.com/NVIDIA-Omniverse/kit-app-template
  - https://github.com/PixarAnimationStudios/OpenUSD
tags: [precision-lighting, poc0, environment-validation]
---

> **Draft only — not published to GitHub.** 設計編寫日期：2026-10-16。依據研究庫 merge baseline `79fc7ef579239555b2b9990c21dbbf40d842cf03`。本交付並未執行 Kit / RTX / GPU 測試。
> 文件 ID 為候選（subject to repository-wide uniqueness check）；GitHub metadata status=`planned` 代表未正式發布，非技術設計未完成。

# PoC 0 — Technical Design (L3)

## Decisions and verified context
- PRD: `OVR-PRD-0001`. Investigation: `OVR-INV-0003`, architecture: `OVR-ADR-0001`。
- Kit App Template `9cc43b…` / Kit 110.4 candidate; packaged binaries not inspected. OpenUSD upstream v25.11 not asserted embedded.
- PoC 0 observes, does not require native projector success. A2 vs A1 texture update belongs PoC 1.
- Code modules added incrementally; pure probes preferred over premature product Extension layering.

## Architecture and process boundaries
```text
Pinned Template / SDK Resolution  →  EnvironmentProbe (OS/GPU/deps)
                                  →  Minimal Kit App Runner
                                          ├─ UsdBaselineProbe → stage/save/reopen
                                          ├─ RendererProbe    → RT 2.0 / PT captures
                                          ├─ ProjectorInspector → property metadata / roundtrip
                                          └─ AOVProbe         → per-mode availability/export
                                     ↓
                         EvidenceStore / ManifestWriter / ReportValidator
```
One controller process sequences probes. `pxr`/Kit-dependent calls run **inside the resolved Kit Python/runtime**, not in a possibly mismatched system Python. OS/GPU inventory can run separately. Stage authoring and extension/renderer actions on Kit-supported thread/update context; no background thread access to USD/Kit interfaces unless documented. Every probe has bounded timeout, clean shutdown and explicit command record.

## Contract: capability vs execution status
**Execution status:** `pass|fail|blocked|not-run`; `pass` is valid only when the assertion and evidence were observed.
**Capability status:** `supported|unsupported|unknown|blocked`. Capability `supported` always tagged by precise claim level:
1. `discovered` property/setting exists;
2. `authored` valid USD authoring and roundtrip;
3. `rendered` controlled visible effect;
4. `exported` valid captured AOV (not semantic/lux proof).
A capability can be supported at level 1 while 3 remains unknown. Do **not** flatten into one boolean. `unsupported` requires a **completed negative probe** on the exact resolved build, not a missing source citation.

### Manifest schema and accepted research identity contract

Canonical [expected manifest example](../handoffs/precision-lighting-poc0/expected-manifest.example.json) is **example0.2, not observed output**. The previous fragment0.1 is historical; existing implementation evidence is not automatically migrated. Detailed binary-set/environment identity schemas, canonical bytes/IDs, coverage/criticality, evidence refs, human approval fields and synthetic vectors are defined only in [ADR-0002](../research/OVR-ADR-0002-poc0-binary-identity-policy.md).

The accepted research `identity` contract (implementation adoption pending) separates declared RTX package build, internal revision/unavailable reason, binary and environment identities and their policy/coverage/pre-runtime-post/human refs. Unknown values remain null/unavailable; generic dev/Kit target hashes are not substituted for vendor revision. `result_levels` separates diagnostics, final identity acceptance, full environment Go and Gate0. An implementation may first adopt the reviewed policy and checker while B final identity acceptance stays blocked pending approved runs and independent human review.

Example0.2 adds these fields to the research example; it does not change product code or existing0.1 reports. Legacy0.1 remains usable as historical inventory/diagnostics but cannot imply B-pass. No automatic migration can fill approved/pass defaults. Actual policy SHA is recorded only after policy publication and separately reviewed implementation lock adoption. Schema/JSON checks do not establish runtime or human approval.

Every probe record should include UTC timestamp, cwd (redacted), command argv, exit code (null if not run), error class/message (sanitized), assertions and artifact hashes. No fabricated measured values.

## Probe work contracts
| Probe | Input / implementation | Output evidence | Failure classification |
|---|---|---|---|
| P0-01 SDK | pinned template, installed toolchain, license | package URLs/IDs, resolution log, resolved lock, result | download/permission/license/ABI |
| P0-02 Dependency | actual installed config + Kit version introspection | package/extension inventory (IDs, versions, hashes if available), Python, USD, RTX build | unresolved/version missing |
| P0-03 Host | Windows commands, `nvidia-smi` if available | OS build, GPU, VRAM, driver with source provenance | tool missing/unsupported hardware |
| P0-04 USD | minimal receiver plane + light, stage units, fixed camera | stage.usda, before/after dumps, render, startup/shutdown | prim mismatch, save error, black frame |
| P0-05 Modes | verified renderer selection for each of RT 2.0, PT | exact setting/mode, log, screenshots/images, nonzero light difference | mode missing/render failure |
| P0-06 RTX props | prim property introspection; compare no-texture/textured/default/projector hypothesis | full names/types, authored test, reopened prim dump, separate rendered status | property missing/type mismatch/no effect |
| P0-07 AOV | version-matched settings enumeration then controlled enable/export attempt | per-mode probes/EXR or valid supported format and metadata; explicit missing | unavailable/export/invalid pixels |

### P0-04 scene invariant
Stage units explicitly set (proposed `metersPerUnit=1`, `upAxis=Y`, to be recorded, not assumed). Single plane, RectLight, fixed camera, no changing auto-exposure; fixed resolution (proposed 512×512), light ON/OFF controls. Validate prim paths, authored type and values before/after reopening. Captures should be tested for finite pixel data, dimensions, scene visibility and **a positive light-dependent difference**, not mere file creation.

### P0-05 renderer verification
Use officially supported settings/mode-selection path discovered in resolved runtime, log **exact key/value** plus renderer confirmation. Compare different actual mode captures; no pixel-equality requirement. If renderer cannot select RT 2.0 or PT, record blocked/unsupported with config/log and do not silently substitute.

### P0-06 property safety
The upstream v25.11 `UsdLuxRectLight` schema exposes `inputs:texture:file`, but RTX `isProjector` is **renderer-specific, unknown**. Do not call assumed `CreateIsProjectorAttr()`; inspect complete attribute namespace, registered properties, types, authored metadata and vendor runtime documentation. Creating a guessed custom attribute without evidence does **not** prove capability. Capture ordinary RectLight baseline, textured non-projector comparison, orientation-card projector hypothesis; reserve LUT as optional discovery.

### P0-07 AOV safety
Test Path Tracing docs names `diAOV`,`giAOV`,`illuminanceAOV`,`worldPosAOV` individually and detect RT 2.0 separately. Settings presence ≠ exported buffer; exported buffer ≠ physically meaningful lux or DI/GI separation. Save raw data, format, channel names, finite/nonfinite counts, camera/sample/denoiser settings and ON/OFF controls. Interpret semantics in PoC 1.

## Data / persistence contract
Probe-generated USD and captures are **test artifacts**. PoC 0 does not need production sidecar/asset migration. Use relative paths under `artifacts/runs/<run-id>/`; redact sensitive machine strings before publishing. Do not delete other runs or alter upstream files. Copy or hash resolved manifests, do not silently edit vendor dependency locks.

## Runtime and performance
No arbitrary 16/33ms, FPS or memory acceptance budget for PoC 0. Record startup duration and frame timestamps where feasible, but do not use performance as Gate 0 pass criterion. Tools should have configurable timeout + meaningful cleanup on interruption. Avoid unbounded log/capture generation.

## Commands: discovery-first, not fabricated
1. `git clone https://github.com/NVIDIA-Omniverse/kit-app-template.git` and `git checkout 9cc43b764e6d4cd86cb6296a8440665c3c4f4843` (at a **separate authorized local checkout**, or the approved template acquisition equivalent).
2. Inspect pinned README/tool scripts and dependency files to identify **actual Windows** build/bootstrap/start flags; record them in `docs/development/commands.locked.md`.
3. For host inventory (PowerShell), sample candidates: `Get-ComputerInfo | Select-Object WindowsProductName, OsVersion, OsBuildNumber`; `nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv` (if present); verify tools exist and redact output.
4. Resolve the correct Kit launcher and embedded Python via the installed SDK before specifying USD/RTX probe commands.
5. `python -m pytest tests/unit -q` is only a **planned** command for pure Python validators; not assumed installed/executed. No invented Kit executable path or renderer setting keys.

## Compatibility, security and license
Assess feature vs production NGC channel and package licensing before distribution. Do not record access tokens, full user-home paths or hardware serials. No DMX/Art-Net/sACN network I/O. No modifications to upstream. Preserve vendor tool EULA and license metadata.

## Testing and evidence
Full per-test expected outcomes, evidence minimum, negative cases and decision rules in `POC0-ACCEPTANCE.md` + `POC0-VERIFICATION-PLAN.md`. Implement JSON schema validation independently of Kit; integration/runtime need target machine.

## Delivery slices
- Implementation PR-01: template bootstrap, environment inventory, minimal Kit App, USD roundtrip, RT 2.0/PT basic captures.
- Implementation PR-02: projector property/type/roundtrip and AOV capability probes, final capability manifest.
- Prioritize one PR at a time; PR-02 may be blocked until PR-01 environment succeeds.

## Known unknowns and fallback
RTX renderer/build/packaged USD version, Windows ABI resolution, projector namespace/type/ingestion, AOV availability/export semantics, RT 2.0 vs PT compatibility, license/feature-channel support, driver suitability: **U, `not-verified`**. If 110.4 cannot bootstrap, capture blocker and request version-switch decision; 110.3 is not automatically compatible with the same template commit.
## Research evidence and source pins

| 依據 | 釘選與驗證界線 |
|---|---|
| [OVR-INV-0003](https://github.com/saizyca-ai-code/OmniverseDevResearch/blob/79fc7ef579239555b2b9990c21dbbf40d842cf03/docs/research/OVR-INV-0003-rtx-projector-source-investigation-and-poc.md) | 2026-10-16 `source-inspected` for public source/config; RTX runtime `not-verified` |
| [OVR-INV-0002](https://github.com/saizyca-ai-code/OmniverseDevResearch/blob/79fc7ef579239555b2b9990c21dbbf40d842cf03/docs/research/OVR-INV-0002-precision-lighting-requirements-and-poc.md) | 已確認需求及 PoC 0/1 roadmap；非 runtime 證據 |
| [OVR-ADR-0001](https://github.com/saizyca-ai-code/OmniverseDevResearch/blob/79fc7ef579239555b2b9990c21dbbf40d842cf03/docs/research/OVR-ADR-0001-virtual-first-physical-ready.md) | Accepted Virtual-First, Physical-Ready design，不證明 RTX 行為 |
| [Kit App Template](https://github.com/NVIDIA-Omniverse/kit-app-template/tree/9cc43b764e6d4cd86cb6296a8440665c3c4f4843) | commit `9cc43b764e6d4cd86cb6296a8440665c3c4f4843`; `VERSION.md`, `tools/deps/kit-sdk.packman.xml`, `tools/deps/repo-deps.packman.xml`，聲明 `kit-kernel 110.4.0+feature.${platform_target_abi}.${config}`，不等於已取得 binary |
| [OpenUSD `schema.usda`](https://github.com/PixarAnimationStudios/OpenUSD/blob/363a7c8da8d1937072a5f0989e91faf72eb1fa76/pxr/usd/usdLux/schema.usda#L1131-L1172) | v25.11 commit `363a7c8da8d1937072a5f0989e91faf72eb1fa76`; `UsdLuxRectLight` width/height/texture，非 embedded Kit USD version |
| [NVIDIA Lighting docs](https://docs.omniverse.nvidia.com/materials-and-rendering/latest/lighting.html) | 官方文件描述 RTX `isProjector`, `projection:directionTexture:file`；`latest` 浮動文件，Kit 110.4 runtime property 名稱/型別 U |
| [NVIDIA Path Tracing docs](https://docs.omniverse.nvidia.com/materials-and-rendering/latest/rtx-renderer_pt.html) | 文件描述 `diAOV`, `giAOV`, `illuminanceAOV`, `worldPosAOV`；可用性、buffer/units U |
| [Kit 110.2 release notes](https://docs.omniverse.nvidia.com/kit/docs/kit-sdk/110.2.0/docs/overview/release-notes.html) | 曾描述貼圖變更重載，不能推論 110.4 RTX projector reload 已可用 |

**Evidence Policy:** A＝直接來源；B＝交叉查核；C＝推論；U＝未知。`source-inspected` ≠ `test-executed` ≠ `runtime-verified`。實際可用性不得由文件存在性推論。
