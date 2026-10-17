---
id: OVR-PRD-0001
title: PoC 0 — Environment Validation Product Requirements
type: prd
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

# PoC 0 — Product Requirements (L3)

## Product goal
在 Windows 11 + GeForce RTX 5080 16GB + 64GB RAM 上，建立**可重現啟動、可測試、可查核版本**的最小自建 USD Composer-style Kit App 環境，作為單一 Virtual Precision Projector 的 PoC 1 前置 gate。主要使用者是開發者、技術審查者及 Coding Agent，不是終端燈光設計師。

成功定義：另一位有授權的開發者能依產生的文件重建環境，得到真實解析出的 Kit/RTX/OpenUSD 版本資訊、USD roundtrip、兩種 renderer 的測試紀錄、projector property/AOV 探測結果，並可作出 Go/Conditional Go/Blocked/No-Go 決策。

> **2026-10-17 accepted research policy boundary (implementation adoption pending):** [ADR-0002](../research/OVR-ADR-0002-poc0-binary-identity-policy.md) defines an explicitly restricted local binary-identity alternative for AC-02 after policy acceptance and implementation adoption. It does not waive the overall reconstruction goal above, fabricate an unavailable vendor revision, satisfy projector/AOV requirements or prove full PoC readiness. A B local-identity acceptance cannot be used as proof of another developer/fresh-host reconstruction; if that required evidence is unavailable, keep the overall success claim incomplete and record it for human Gate review. Current implementation lock and Go=blocked remain unchanged; this PR supplies no new runtime or PR-02 execution.

## Context and accepted decisions
- Research baseline `OVR-INV-0002`, `OVR-INV-0003`; architecture `OVR-ADR-0001`。
- Kit 110.4.0 **candidate**；110.3.0 僅在已記錄 110.4 blocker 且審核後 fallback。
- D1 USD + versioned JSON sidecar + assets、D2 A2 primary/A1 mandatory comparator、D3 Virtual Focus/Zoom、D4 one independent implementation repo with incremental Extensions **為 PoC 1 的預定契約**；PoC 0 不需要先實作這些功能。
- 不以 Light Linking / material edits 假裝物理截光；不預設 custom renderer。

## Target environment
- Windows 11; RTX 5080 16GB VRAM; RAM 64GB; driver/version at runtime TBD。
- [Kit App Template pinned SHA](https://github.com/NVIDIA-Omniverse/kit-app-template/tree/9cc43b764e6d4cd86cb6296a8440665c3c4f4843); resolved SDK/renderer/extensions/embedded OpenUSD/Python/build **all TBD by probe**。
- 使用者未授權本輪建立 implementation repo；實作必須在後續授權的獨立 repository。
- 最小 App 不等於現成 USD Composer binary；不得假定 Composer proprietary features 可用。

## Scope
**In:** SDK acquisition/license feasibility; dependency/build inventory; GPU/driver fingerprint; minimal Kit startup/shutdown; ordinary USD RectLight/Stage save-reopen; independent RTX Real-Time 2.0 and Path Tracing captures; projector property/name/type inspection; AOV probe/export attempt; machine-readable manifest; evidence bundle; reproducible commands.
**Out:** Production Extension/UI, DMX, Mask Editor, dynamic A1/A2 latency (PoC 1), geometry solver, physical lights and lux calibration, 64–128 simultaneous fixtures, source modification to upstream, releasing a product.

## Functional requirements
| ID | Must | Requirement | Acceptance |
|---|---|---|---|
| FR-P0-01 | Yes | 確認 pinned template 與 SDK 取得流程；保留工具/權限/授權判斷 | P0-AC-01 |
| FR-P0-02 | Yes | 收集實際解析的 SDK/Kit/RTX/embedded USD/Python/extensions 和版本來源 | P0-AC-02 |
| FR-P0-03 | Yes | GPU、driver、Windows fingerprint，敏感資訊遮蔽 | P0-AC-03 |
| FR-P0-04 | Yes | minimal app 可啟動/退出；Stage/RectLight save-close-reopen | P0-AC-04 |
| FR-P0-05 | Yes | RT 2.0 與 Path Tracing 獨立渲染與記錄 settings | P0-AC-05 |
| FR-P0-06 | Yes | 逐一 inspect  `isProjector`, `inputs:texture:file`, `projection:directionTexture:file`，保留未發現/未支援結果 | P0-AC-06 |
| FR-P0-07 | Yes | 嘗試 AOV enable/export，區分 property exists/render actually exported | P0-AC-07 |
| FR-P0-08 | Yes | 完整保存 test status/error/evidence/command/report | P0-AC-08 |
| FR-P0-09 | Yes | 分析 110.4 feature channel 遷移風險；只有實證 blocker 才提 110.3 fallback | P0-AC-09 |

## Non-functional requirements
| ID | Target | 方法 |
|---|---|---|
| NFR-P0-01 Reproducibility | 記錄 exact commands + cwd + arguments + pin + resolved package versions；重跑一次起動/roundtrip/每模式渲染（若 target HW available） | Logs / artifacts compare |
| NFR-P0-02 Traceability | 每 probe 有 ID/status/evidence, observed/expected 與環境 ref | JSON validator |
| NFR-P0-03 Failure honesty | 失敗不補值，不用 fake renderer frames；`not-run` 與 `blocked` 分清楚 | Negative tests |
| NFR-P0-04 Data safety | 公開輸出不含 token、主機名稱、個人路徑；不得破壞 upstream | Secret/redaction review |
| NFR-P0-05 Deterministic baseline | 固定 camera/scene/light settings，存原始 USD 與圖像設定 | Check fixtures |
| NFR-P0-06 Timing | 初期無 FPS/latency 門檻；timeout 需可設定並記錄 | Report |

## UX / operations
CLI / developer workflow: `bootstrap → environment inventory → USD sanity → renderer probes → property probe → AOV probe → report`。每個步驟可單獨重跑。失敗必須顯示最短有效診斷、相關 log 位置及可行下一步，並結束已啟動資源。

## Dependencies and risks
| Risk | Evidence | Consequence | Mitigation |
|---|---|---|---|
| 110.4 feature binary unavailable | U | blocked | record Packman/download + license, do not swap silently |
| RTX RT 2.0 or PT unsupported | U | no full environment Go | capture exact settings/errors; review compatibility |
| Projector property absent/different | U | PoC 1 implementation delay | inspect authored property metadata; no fabricated API |
| AOV not exportable / wrong units | U | measurement limits | separate discovery and semantic validation in PoC 1 |
| Image black/noisy vs light absent | U | false negative | ordinary RectLight ON/OFF baseline and fixed camera |
| Driver/GPU mismatch | U | startup failure | inventory before renderer run |

## Milestones and signoff
P0-01…P0-07 map to the research investigation; implementation PR-01 bootstrap + baseline, PR-02 property/AOV capability diagnostics. Gate 0 is **environment-ready**, not proof of working precision projector. `OVR-HOF-0001` owns delivery; `POC0-ACCEPTANCE.md` owns machine-checkable acceptance rules.

Review owner: user/project maintainer; technical execution owner: authorized Coding Agent. Review requires artifact/evidence inspection, not just README assertions.
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
