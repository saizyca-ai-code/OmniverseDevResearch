---
id: OVR-INV-0004
title: RTX identity — Research Feedback 與 binary identity 待審候選
type: investigation
status: review
created: 2026-10-17
updated: 2026-10-17
domains: [omniverse-kit, rtx, reproducibility]
repositories:
  - https://github.com/saizyca-ai-code/ov_dmx_light_control
  - https://github.com/saizyca-ai-code/OmniverseDevResearch
tags: [poc0, research-feedback, renderer-identity]
---

# RTX identity — Research Feedback 與 binary identity 待審候選

> **待研究審查，非已接受決策。** 本 PR 只新增調查／決策輸入及生成索引；不修改現行 PRD、DES、HOF、Acceptance、Verification Plan、治理或 implementation handoff lock。方案 B 未達標、未採用；full environment Go=blocked，Full Gate0 decision=not-assessed／未簽核。合併本報告也不會自動改變判準或授權後續實作。

## 問題、範圍與摘要

檢查日期：2026-10-17。PoC 0 PR-01 的一般燈光 baseline 已執行，但 28 個 RTX plugin runtime build 仍全部為 `dev`。研究 owner 需決定：critical RTX identity 是否必須有權威 vendor build／revision 到 loaded bytes 的映射（方案 A），或可接受 human 核准、受限本機 PoC 的可驗證 binary identity（方案 B）。方案名稱 A／B 與下方 Evidence Policy 的證據類別 A／B 是不同概念。

建議僅將 B 列為待審候選，保留 A 的 provenance 目標。兩者證明目的不同，不視為等價。既有 PR 合併、SDK 使用授權、hash 一致與成功 baseline 都不等於 B 的信任根或 binary 集合已批准；不得由執行 agent 自我批准形成循環論證。

本次僅整理既有公開且已清理的實作證據，以及經本機 review 修正的決策輸入。沒有新增 Kit／RTX runtime、重跑官方搜尋、下載 SDK archive、實作 projector／AOV／PR-02、修改現行判準或對外送出 NVIDIA 詢問。私人取得紀錄與 raw logs 不上傳；既有公開摘要保留其 hashes，但外部 reviewer 未必能獨立取得 raw bytes，採用前須安排授權範圍內的證據檢視。

## 固定版本與研究依據

- 研究／本 PR 起點：`27ab5add5c62692d47662e32401df860a82136cf`；implementation 仍以此作唯一 handoff 基線。
- Implementation 證據版本：`92abd6c4c4cf819395afaac667794914b71ccda5`，以下連結均釘此版本；不引用浮動 main 作技術證據。
- [AC-02](https://github.com/saizyca-ai-code/OmniverseDevResearch/blob/27ab5add5c62692d47662e32401df860a82136cf/docs/handoffs/precision-lighting-poc0/POC0-ACCEPTANCE.md)、[Verification Plan](https://github.com/saizyca-ai-code/OmniverseDevResearch/blob/27ab5add5c62692d47662e32401df860a82136cf/docs/handoffs/precision-lighting-poc0/POC0-VERIFICATION-PLAN.md)、[DES](https://github.com/saizyca-ai-code/OmniverseDevResearch/blob/27ab5add5c62692d47662e32401df860a82136cf/docs/specs/OVR-DES-0001-poc0.md)、[HOF](https://github.com/saizyca-ai-code/OmniverseDevResearch/blob/27ab5add5c62692d47662e32401df860a82136cf/docs/handoffs/OVR-HOF-0001-poc0.md)與[Handoff Protocol](https://github.com/saizyca-ai-code/OmniverseDevResearch/blob/27ab5add5c62692d47662e32401df860a82136cf/docs/governance/research-to-implementation-handoff-protocol.md)是判準及採用程序的固定來源。

AC-02要求 exact RTX build／critical identity resolved，**沒有明訂 renderer 必須取得完整 Git SHA**。目前「唯一 internal revision」是阻擋缺口的具體解讀，不能偽稱原文要求 40 字元 renderer source SHA。可接受 vendor build ID 的粒度、是否必須證明 vendor provenance，以及 B 是澄清或門檻變更，都待研究 owner 決定。原文件中的歷史 draft／未執行文字與 publication SHA、後續實測分開解讀，不藉本報告改寫原文。

| 已記錄環境 | 實際版本／值 |
|---|---|
| OS／GPU／driver | Windows 11 Pro 10.0.22631 x64；RTX 5080／16303 MiB；616.92；D3D12 |
| Kit app build | `110.4.0+feature.386251.187cf21b.gl` |
| kernel | `210.4.11+release.15522.174283e4.gl` |
| RTX extension | `omni.hydra.rtx-1.0.5+187cf21b.wx64.r` |
| 宣告 renderer dependency | `110.4.0+feature.385994.1ea54838.gl.windows-x86_64-rendering-usd_25.11_3.12-1ea548386c` |
| OpenUSD／Python | 0.25.11／embedded 3.12.14；host Python 3.12.11 |
| renderer／fixture | RTX Real-Time 2.0／Path Tracing；固定 512×512 一般燈光 ON／OFF baseline |

## 已有證據與可支持的主張

下列為既有實作證據，檢查日期2026-10-17；本次未重跑runtime或搜尋。

| 證據 | 已支持的主張 | 不能支持的主張 |
|---|---|---|
| [baseline report／summary](https://github.com/saizyca-ai-code/ov_dmx_light_control/blob/92abd6c4c4cf819395afaac667794914b71ccda5/docs/development/pr01-report.md)，run `20261016-review-final01` | 目標Windows／RTX5080／driver616.92上，USD／RT2／PT各兩次，六次退出及baseline assertions通過 | 相同hash以外的SDK、其他GPU／driver、precision投影、AOV語意或物理lux |
| [T004／T005 identity report](https://github.com/saizyca-ai-code/ov_dmx_light_control/blob/92abd6c4c4cf819395afaac667794914b71ccda5/docs/development/t004-rtx-identity-report.md)，run `20261017-t004-review-runtime` | 28個loaded RTX plugin path／SHA256與lock吻合，11項identity checks通過，build全為dev | 唯一vendor revision已解析、磁碟hash是vendor簽章、所有依賴或resident memory均已認證 |
| [resolution.lock.json](https://github.com/saizyca-ai-code/ov_dmx_light_control/blob/92abd6c4c4cf819395afaac667794914b71ccda5/tools/bootstrap/resolution.lock.json) | 35份已檢視SDK／RTX檔案固定，含28個plugin與兩個support DLL | 完整SDK SBOM或所有transitive GPU依賴／driver binaries的完整digest集合 |
| SDK manifest、registry與generated config | Kit `110.4.0+feature.386251.187cf21b.gl`、kernel `210.4.11+release.15522.174283e4.gl`、RTX extension package `omni.hydra.rtx-1.0.5+187cf21b.wx64.r`；SDK宣告renderer dependency含`385994.1ea54838`／`1ea548386c` | 該dependency宣告必定等於目前loaded DLL的source revision |
| [T007官方搜尋報告](https://github.com/saizyca-ai-code/ov_dmx_light_control/blob/92abd6c4c4cf819395afaac667794914b71ccda5/docs/development/t007-official-provenance-search.md) | 187cf21b為Kit target／publication角色；24queries及官方metadata範圍內未找到exact mapping | 全網或NVIDIA私有系統不存在manifest；187cf21b與1ea54838為等價或祖先關係 |
| 原始失敗與證據索引 | sandbox readonly／timeout與授權環境成功重試分開保留，raw檔案可核對hash | sandbox權限已修復或完整descendant cleanup已盤點 |

來源缺口：既有調查未取得當初RTX ZIP bytes／checksum；搜尋僅涵蓋repository內的.cache/registry、.cache/packman與.cache/kit-runtime，未查system temporary或external/global caches，不能推論整台主機或vendor端都不存在原archive。vendor folder hash `6f84576881594a1d`與archive-name後綴`fcf7d3edfc3a1aee`不同。列舉順序、文字正規化、發布處理與截短hash等限制已記錄。不能把差異當integrity pass，也沒有證據可直接判為corruption；這些缺口不因採B而消失。

## Evidence matrix 與可重定位來源

| 主張 | 證據類別 | Validation state／結果 | 固定來源與定位 |
|---|---|---|---|
| AC-02 分開 inventory 與 critical identity；缺 critical identity 阻擋 full environment Go | A（直接） | source-inspected | 上列 Acceptance／AC-02 及 Gate 說明 |
| 28 個 loaded plugin path／hash 符合 lock，build 全 dev | A（直接、歷史 run） | runtime-verified（診斷成功；revision 未解析） | T004 report「Pre-merge review and corrections (T005)」；run `20261017-t004-review-runtime`：exit0、19.36s、11 checks |
| 35-file lock、30 DLL 包含28 plugins及2 support DLL | B（lock 與診斷交叉核對） | static-checked／歷史 test-executed | resolution lock 與 T004 report／summary；25 plugins屬omni.hydra.rtx，其餘3屬omni.index、omni.mdl.neuraylib、omni.kit.usd.mdl |
| USD／RT2／PT各兩次baseline成功 | A（直接、歷史 run） | runtime-verified（受限 baseline） | baseline report，run `20261016-review-final01`：六次exit0；不是B驗收結果 |
| 187cf21b 是 Kit target／publication；1ea54838 是 SDK dependency 宣告 | B（metadata 與官方語意交叉核對） | source-inspected | T007 report「What the two identifiers establish」；取得SDK的 `dev/all-deps.packman.xml`、registry `package.target.kitHash` |
| 識別字串不同不直接證明不相容或損壞 | C（推論） | source-inspected，非 integrity pass | T007 report「What the two identifiers establish」 |
| 原始 RTX archive checksum、declared revision 到 loaded bytes 的權威映射 | U（未知） | not-verified／blocked | T004 provenance、T007 bounded search；24 queries 無 exact mapping，不證明 NVIDIA 不存在資料 |

Fresh review證據：[T005 runtime／11 checks／28 dev](https://github.com/saizyca-ai-code/ov_dmx_light_control/blob/92abd6c4c4cf819395afaac667794914b71ccda5/docs/development/evidence/t004-review-observed.json)與[T008 evidence review／24 unit tests](https://github.com/saizyca-ai-code/ov_dmx_light_control/blob/92abd6c4c4cf819395afaac667794914b71ccda5/docs/development/evidence/t007-review-observed.json)。原T004／T007摘要是歷史調查，fresh review結果以各自review JSON與report review章節核對，不將兩次執行混為同一run。

公開證據摘要：[baseline](https://github.com/saizyca-ai-code/ov_dmx_light_control/blob/92abd6c4c4cf819395afaac667794914b71ccda5/docs/development/evidence/pr01-observed.json)、[T004](https://github.com/saizyca-ai-code/ov_dmx_light_control/blob/92abd6c4c4cf819395afaac667794914b71ccda5/docs/development/evidence/t004-rtx-identity.json)、[T007](https://github.com/saizyca-ai-code/ov_dmx_light_control/blob/92abd6c4c4cf819395afaac667794914b71ccda5/docs/development/evidence/t007-official-provenance-search.json)。摘要、report及resolution lock互相引用；此處不複製 vendor source、binary 或私人 raw logs。

## 方案比較

| 面向 | A：要求權威、唯一RTX build／internal revision映射 | B：接受核准範圍的可驗證binary identity |
|---|---|---|
| 核心證明 | 此次loaded bytes可連到哪個vendor建置／revision | 此次使用的關鍵files與reviewer核准的baseline集合完全相同 |
| 最低證據候選 | 官方manifest／attestation或可保存來源的vendor書面映射，連結精確package／DLL digests與唯一build/revision；reviewer指定可接受識別粒度 | 明確界定module coverage、canonical digest manifest、documented loaded paths、版本／環境／命令／source fingerprints、drift checks、對應實測與明確接受的來源限制 |
| 現有充足度 | **不足**：有declared build、實際paths/hashes與dev，但無權威連結 | **足以提出候選，尚不等於通過候選門檻**：主要資料已存在，但coverage、可信baseline來源、fresh reacquisition限制、post-run checks及正式採用尚待review |
| 優點 | 有助vendor debug／release差異追溯、來源血統及精確建置識別 | 不依賴vendor公開內部commit；可對受控本機baseline做精確漂移偵測與行為重現 |
| 核心風險 | 找到revision label但沒有綁到loaded bytes仍會誤判；同source commit也可能有不同compiler／flags／依賴的binaries | 同一個錯誤或來源未認證的binary也能有穩定hash；file hash不能證明vendor身份、source lineage、安全性或功能正確 |
| 殘留不確定性 | 即使revision已知，仍需package／loaded-file鏈與實測；單靠revision不保證行為 | vendor bug對照與source-level回溯受限；未知transitive modules、取得渠道及原始ZIP缺口仍需列為限制 |
| 外部依賴與時間 | 可能需要未公開資料或vendor回覆；取得時間未知，不能承諾 | 可先用已有資料形成可審查bundle；仍需研究review、判準定義與可能的implementation follow-up，並非零成本 |
| 維護代價 | 每次SDK／renderer更新需重新取得mapping，且仍要保存hash與runtime證據 | 必須維護manifest coverage與留存政策；hash／環境變動需新baseline、重新驗證及review，不能延用舊pass |
| 對可重現性的限制 | 需要保存對應binaries或可重新取得來源，source ID本身不夠 | 現有local cache重跑已有證據；從乾淨新主機重新取得相同binaries尚未證明，不能宣稱完整fresh-bootstrap重現 |
| 適用範圍 | reviewer要求來源血統／唯一vendor建置識別時 | reviewer將本機PoC baseline重現與漂移控制視為足夠，並接受來源血統未知時 |
| 當前Go | blocked | **仍blocked**；目前只是草案，不能直接把hash填成已解析internal revision |

## 方案A候選驗收條件（待審查）

1. Reviewer明定唯一識別是vendor build ID、source revision或二者；不得臨時以另一個未定義欄位替換。完整Git SHA不是本草案擅自新增的必備條件。
2. 權威來源明確對應目前package及核心DLL SHA256，並區分Kit／kernel／RTX與另三個extension packages；不能只回覆「Kit110.4」或extension1.0.5。
3. 與documented loaded library paths、preflight／runtime hash證據互相核對；revision mapping與實際行為測試均保留。
4. 查無mapping時保持unavailable＋原因。搜尋無結果不能轉成unsupported；無新增資訊時不反覆重跑相同dev欄位。

## 方案B候選驗收條件（待審查，未實作）

以下是**本草案提議的不可略過最低條件**；研究review可修改提案，但不能在未記錄的情況下將必要條件當成可選限制。條件尚未完成不妨礙「送研究審查提案」，但會阻擋「宣稱B驗證通過」。

1. **先核准信任根與coverage。** 由具名human reviewer審查官方取得紀錄、授權、package refs及source/config snapshots，明確接受其證據強度；將信任層級描述為「reviewer核准的本機baseline」，不能改稱vendor-authenticated。明列至少現有35檔、28個plugins的四package歸屬、兩個support DLL及metadata，並列出未涵蓋的動態／GPU／driver依賴及排除理由。35檔是起點，不是自動足夠的coverage；新增未知或critical依賴無法分類、來源完整性有具體疑點未解，或vendor authenticity屬不可妥協門檻時，B不得通過。執行agent的hash工具或自己的baseline批准不能替代human接受。候選驗收run開始前，必須已有針對該集合ID／coverage／信任限制的具名批准；run完成後的結果簽核不能追認未經批准的輸入集合。
2. **定義且測試可重算的集合識別。** 研究review需先固定versioned manifest schema、精確file集合、原始檔案bytes的SHA256與canonical序列化規則；至少明定path根目錄／分隔符／大小寫碰撞／重複path／link解析與拒絕規則、排序、文字編碼／換行及集合ID排除自身欄位，並有跨平台test vectors。binary集合ID與OS／driver／settings／scene等run-environment描述分開記錄、互相引用，避免相同binary在不同環境被當成相同行為保證。不要拿任意commit或archive名稱當集合digest。這些是待研究review定義、待實作測試的要求，**目前集合ID／schema尚未建立**。
3. **綁定執行並以缺漏／漂移為阻擋。** 每次候選驗收run前及clean退出後，檢查完整已核准file集合與digest；run內保留documented loaded paths/hash、已核准plugin集合、版本／enabled metadata及執行前後source fingerprints，拒絕missing／extra／duplicate／unknown／hash mismatch。執行期間禁止in-place SDK／registry更新，需有可檢視的受控執行安排與紀錄；缺任一必要輸出即不得給該run pass。現有preflight及runtime hash可沿用，**完整post-run集合檢查及此流程尚未驗證**。即使pre/post一致也不能排除惡意替換後還原、未涵蓋modules或記憶體修改；B僅針對可信本機的重現與非惡意漂移，不適用host遭入侵或memory attestation需求。
4. **行為證據不能省略。** 固定Windows／GPU／driver／Kit／kernel／embeddedUSD／Python、scene、renderer settings、sampling／denoising／曝光與完整命令，對應USD roundtrip與RT2／PT各兩次執行的baseline。CI的hash／schema pass不構成新GPU驗證。
5. **誠實保留未知欄位。** internal revision保持null／unavailable及missing reason；如新增identity-method欄位，需明確標為binary digest方法，不能將dev／Kit hash改填為唯一internal revision。此資料欄位變更屬後續候選，不修改目前report或lock。
6. **限定用途與變更觸發。** 只對reviewer核准的該組files、該環境及PoC0 baseline有效；不證明投影、AOV、lux、效能、其他版本或產品安全。任何critical binary／loaded set變更都需新集合核准；OS／driver／GPU／embedded runtime等重要環境變更須經影響評估與必要重跑，不能自動沿用pass。必要輸出缺失或發生未解漂移時，保持identity驗收blocked並保留失敗紀錄，不能先改lock來接受新hash，也不能只重算manifest消除mismatch。
7. **留存責任與復原邊界。** 具名baseline custodian確認evidence／核准manifest可恢復，並在授權允許範圍內記錄現有cache／package的保管及停止清理安排；此處不授權複製／重新散布binary。cache清除或bytes遺失後若無法取得相同集合，停止將原B結論套用於新執行，原pass只能作歷史紀錄。不得宣稱原ZIP checksum已補齊或已驗證乾淨主機reacquisition；若獨立新主機重建是必要目標，現有資料不足，B在該目標下不得通過。
8. **逐項human signoff。** 研究owner批准政策／目的／限制，implementation verifier提供每條候選條件的證據及未解gap，再由獨立於coding agent的human reviewer簽核實際run與scope；同一maintainer可承擔多個human角色，但需分開記錄政策決定與執行結果核准。vendor revision未知、來源信任、非完整dependency coverage、archive及memory限制須逐項接受；不能用一句「接受風險」跳過上述最低條件。任何critical requirement不可接受時，B不通過。必要補測未獲授權時只能保持gap，不自行執行。

### B 的現有證據／待補項目對照

| 必要項目 | 目前狀態 | 採用前的差距 |
|---|---|---|
| human批准的信任根與coverage | 未完成 | 既有取得logs／metadata／lock可供review，但沒有B的baseline批准；未知依賴的排除理由與風險界線需定義 |
| canonical binary集合schema／ID及test vectors | 尚未定義／未實作 | 已有逐檔SHA256不等於已存在可重算且經測試的集合ID |
| preflight／runtime path/hash與版本 | 有既有證據 | 35-file preflight及28個plugin結果可引用；如coverage變更需重驗 |
| full covered-set post-run檢查與受控執行安排 | 尚未證明 | 需後續實作／執行證據；不從clean exit推論已完成，也不聲稱memory安全 |
| USD／RT2／PT baseline重複實測 | 已有歷史證據 | 是否可用於新判準須逐條確認；不能改寫歷史run為B-pass。未被舊證據覆蓋的新增條件需新run |
| private evidence／CI／負例 | 已有完整性checks及24個既有unit tests | 尚無B集合schema／pre/post／新scope的checker與負例；現有assessor仍維持Go=blocked |
| 留存／復原負責人及可接受重建限制 | 待明列 | 既有ignored cache／evidence存在，不等於已核准保管方案或fresh-bootstrap重建能力 |
| 研究政策採用、implementation採用及human run signoff | 均未執行 | 新研究版本、lock採用、實作驗證與獨立簽核缺一不可；本草案review不能代替 |

所有「未完成／未證明／待明列」項目是**B啟用阻擋**，不是文字修正後即自動滿足。本 PR 只整理提案，未補做實作或runtime驗證。

## Go、Conditional Go與Full Gate0的分離

目前`full_environment_go=blocked`表示critical RTX identity阻礙仍在；不能直接等同鎖定文件中整個Gate0枚舉的BLOCKED理由。**Full Gate0 decision維持not-assessed／未簽核。** 研究文件另有Conditional Go，可在明確缺口下允許有限Pure Core工作，但這不是本次選擇，也不構成PR-02或RTX Adapter假設授權。

即使未來A取得mapping或B獲批准並完成候選驗證，也只可能解除identity這一項阻礙；仍需review其他AC、PR-02 capability／完整性證據及正式Gate0 signoff。本次沒有把AC06–09、PR-02或PoC1視為完成。

## 待研究 owner 審查的 Research Feedback

| 提案 | 建議內容 | 分類待owner確認 |
|---|---|---|
| RF-1：身分術語 | 分開SDK-declared dependency、Kit target／publication、runtime plugin build、ABI version、loaded-file digest與vendor provenance；說明187cf21b與1ea54838不能互換 | 證據補充／術語澄清 |
| RF-2：AC-02 critical identity | 明定A必需的唯一識別粒度及digest mapping；或明確列出B在限定PoC0的coverage、信任與重驗條件，以及仍保留的unknown欄位 | 可能為驗收澄清或規範變更，不預先判定 |
| RF-3：Go vocabulary | 分清inventory pass、identity blocker、full environment Go與正式Gate0 decision；保留Conditional Go的原始限制 | 判定與報告澄清 |
| RF-4：證據／驗證計畫 | 如採B，增加明確module coverage、來源信任、post-run／漂移／留存／fresh-bootstrap限制的檢查，不以hash-only替代behavior | 驗證計畫／design影響 |

候選影響範圍：AC-02及其Gate說明、verification plan的identity證據欄位；DES的inventory／驗證界線與HOF reviewer要求視owner review結果同步。這不是要求直接更動全部文件，也不在此複製整份研究規格。

### 採用程序與停止條件（待研究審查）

Handoff Protocol要求判準／設計變更經研究review，並由implementation另行review版本採用與影響；下列是將該要求落到B的**候選程序**，不是本次後續操作授權。

| 階段 | 必須交付與批准的內容 | 不能推導的結論 |
|---|---|---|
| S0：提案送審 | 本報告清楚區分A／B的證明目的、既有證據、必要gap及風險；本 PR 僅提交待審提案 | 送審或合併提案不等於B已通過或政策已接受 |
| S1：研究政策決定 | 具名研究owner／human reviewer選擇A或B，判定澄清或變更，定義不可略過門檻、coverage、信任模型與可接受用途 | 批准政策不等於批准實際binary集合、完成補測或解除Go |
| S2：實質政策發布 | S1決定後，另經明確授權與review的研究變更PR，修改必要判準／驗證計畫，完成研究validation與human merge，保存實際40字元merged政策研究SHA | 本提案PR不含政策變更；不得以其merge取代實質政策發布，未merge分支亦不是已發布基線 |
| S3：implementation採用 | 另經授權與review的adoption PR，含新研究lock、影響評估、manifest／checker／pre-post流程及負例測試、report語意；維持fail-closed，不能只改Go字串。SDK pins變更若有需要須另行評估，不由判準變更隱含授權 | 政策與lock合併不等於runtime通過；未完成驗證仍blocked |
| S4：執行證據與簽核 | 依已採用判準逐條確認證據；候選驗收run前先由具名human批准信任根／集合ID／排除項，implementation verifier依已批准輸入執行並提供實際run IDs／hashes／結果，獨立於coding agent的human reviewer簽核適用範圍及限制。舊證據可引用的條件需逐項說明，新增條件缺證據需後續授權補測 | 只可能解除已驗證的identity阻礙，不代替其他AC或Full Gate0；不回寫歷史run為B-pass，也不授權PR-02 |

任一必要條件失敗、缺證據或未獲批准，就停在該階段並保留blocked與失敗證據，不能以未來承諾先給pass。採用後若發現未知critical module、來源信任問題或hash漂移，停止將該接受結論用於新run，重新開啟缺口／影響評估；保留歷史判定與其當時判準。這不是自動改寫lock或回退Git版本的授權。任何需下載archive、對外詢問、擴大scope或取得研究寫入權限的工作，都需另行明確授權。

目前implementation assessor／checker與resolution lock保留Go=blocked的既有行為。若後續採B，需另做implementation change review並更新相應tests／report semantics；**不是直接修改現有Go字串**，也不應回寫歷史run為新版驗收pass。

## 決定（待填，不是已接受方案）

| 欄位 | 草案狀態 |
|---|---|
| 決策owner／reviewer | 待指定 |
| 方案選擇A／B | 未決定 |
| 接受的證據目的／coverage／來源信任強度 | 待明列 |
| 信任根與binary集合human批准者／baseline custodian | 待具名；尚無批准 |
| 已批准manifest schema／集合ID／排除項 | 未定義／未批准 |
| classification：澄清或驗收變更 | 待研究owner review |
| 接受限制、必補gap與重新驗證項目 | 待逐項記錄 |
| Research PR／新merged政策SHA | 本 PR 僅提案，尚無實質政策發布SHA；merge本提案亦不構成政策接受 |
| Implementation adoption PR／新lock | 未建立／未修改 |
| 必要gap closure／驗證run IDs與evidence digests | 未完成；不能用既有CI或clean exit代替 |
| 生效時間／Gate reviewer signoff | 未生效／未簽核 |

## 驗證範圍與現行判定

- source-inspected／static-checked：固定研究條文、實作 reports／摘要／lock及本候選文字的一致性。
- test-executed：本 PR 的研究 metadata、generated index及repository tests，實際命令／結果列於PR描述；不把它們當作產品或GPU驗證。
- runtime-verified：只引用上述歷史run。**本次 Kit／RTX not-run；B not-verified，必要gap仍blocked。**
- inventory completeness pass可含明確missing reason；它不代表critical identity已解。28個plugins仍dev，原archive與權威mapping缺口仍在。Full environment Go=blocked；Full Gate0 not-assessed。
- 研究owner需先回答：驗收目的與可接受粒度是什麼？選A或B？B屬澄清還是變更？誰批准信任根／coverage、保管證據並獨立簽核run？未填欄位是待決，不是默認批准。
- 後續如採B，需另行明確review判準／驗證計畫的實質變更與implementation版本採用。本PR只合併調查輸入，**不能以本PR的merged SHA直接宣稱B政策已發布**；需先完成實質政策決定及相應研究變更。

## 重新檢討條件

官方mapping或可驗證attestation出現；需要vendor source-level支援；更換SDK／extension／GPU／driver或hash集合；fresh-bootstrap不能取得相同bytes；baseline來源信任被質疑；新增產品／precision／物理照明要求。上述任一出現都應重審方案及適用邊界，不能把本機PoC暫定接受永久擴張為產品保證。


## 2026-10-17 direction update — policy remains review

Human owner explicitly approved B as the restricted PoC candidate direction, retaining A provenance goals and L01–L05 principle acceptance, with B eight conditions/E01–E08 mandatory. This does not approve the actual binary baseline, concrete integrity-issue disposition, B acceptance or policy activation. [ADR-0002](OVR-ADR-0002-poc0-binary-identity-policy.md) is a separate proposed policy change with the detailed contract; if accepted and adopted, its contract is used prospectively. It is not evidence that the original AC-02 already accepted B.

Earlier undecided-direction statements in this report are historical investigation context. Original 28dev results, archive gaps, bounded search, all fixed evidence links and implementation lock remain unchanged. The report stays review, not runtime-verified policy. Current full environment Go=blocked; no new runtime, archive download, PR-02 or NVIDIA inquiry.


## 2026-10-17 policy acceptance update — implementation adoption pending

After full PR #7 review and fixes, the human owner explicitly accepted the ADR-0002 research policy contract and authorized its merge. The preceding direction-only/policy-review statements remain dated investigation history; the accepted policy contract is authoritative in [ADR-0002](OVR-ADR-0002-poc0-binary-identity-policy.md) once published. This investigation report itself remains review, not a verified baseline. No B01–B08/L01–L05/E01–E08 requirement is waived, no binary baseline or B result is approved, and the implementation handoff lock is unchanged. Full environment Go=blocked; no runtime, archive download, PR-02 or NVIDIA inquiry. Implementation adoption requires a separate authorized and reviewed PR using the actual merged research SHA.
