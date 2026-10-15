# Research-to-Delivery Workflow v2

## 核心概念

Chat 是探索、思考與決策工作空間；Research repo 是可追溯的長期知識；Implementation repo 是可編譯/可測試的產品原始碼。不要把聊天記錄直接當作證據，也不要把開發 repo 與研究庫混在一起。

## 工作模式與保存原則

| 等級 | 問題類型 | 建議輸出 | 必須保存到 GitHub？ | 主要判準 |
| --- | --- | --- | --- | --- |
| L1 Exploration | 查 API、技術可行性初判 | Chat 回答，來源與未知 | 否 | 已回答當下問題 |
| L2 Investigation | 跨 repo、版本衝突、行為追蹤 | 既有 `OVR-INV` / `OVR-REPO` / `OVR-VER` | 有長期價值時 | 重要主張有 pinned evidence |
| L3 Solution Design | 需要選擇路線或可開發規格 | ADR + PRD + Technical Design（視需要） | 有具體決策時 | 可量測驗收、有風險處置 |
| L4 Handoff | 開發工作較大 | 開發工作包、tasks、介面與測試 | 正式交接時 | Agent 無需猜測核心契約 |
| L5 Validation | 測試、整合、效能或視覺品質 | PR/CI 證據 + `OVR-EXP` / 決策更新 | 只有可重用結論 | 結果可重現且限制明確 |

自動轉換時機：發現跨 repository 依賴或版本差異、需承擔效能/安全風險、有多個可行方案需要取捨、有明確交付物及驗收門檻，才升級深度。無風險的問答不需生成正式 artifact。

## 知識保留的判斷

保留：實際版本的 API/內部流程、跨 repo 邊界、被驗證的限制、PoC 的成功/失敗原因、相容性矩陣、已接受的設計決策、可重用測試流程。

不保留：已經回答的簡短概念問題、未整理的搜尋紀錄、重複文檔內容、聊天逐字稿、缺少來源的推測或不再相關的暫時想法。

高價值的 Chat 結論提升為 GitHub artifact 時：
1. 搜尋現有報告，決定更新或新增。
2. 拆分「證據已確認」與「推論／待測假設」。
3. 附 upstream pinned ref、環境、日期、範圍與相關研究 ID。
4. 通過適用的驗證，經 PR 合併到研究庫。

## 從研究轉為開發規格

- Problem/Outcome：使用者真正要達成的使用情境與使用者價值。
- Requirements：功能、非功能、平台與版本、禁止事項。
- Candidate Solutions：至少包含採用理由、取捨、證據狀態和替代方案。
- Architecture & Contracts：模組、資料流、protocol/attribute mapping、生命週期、錯誤與同步策略。
- Acceptance Criteria：具體測試條件、可測量目標；無法事先決定的量化門檻先標為 TBD，切勿造數值。
- Delivery Plan：可小步 PR 的工作範圍，未決風險先以 PoC 驗證。

## 推薦 artifact 選擇（與既有制度相容）

目前既有正式 type：`repository-analysis`、`investigation`、`version-comparison`、`experiment`、`decision`；prefix `REPO/INV/VER/EXP/ADR`。研究主張歸於這些類型。

規格書與 Agent 交接文件可以先在 Chat 產出；有長期價值時，將 `prd`、`technical-design`、`handoff` 使用對應模板存入 `docs/specs/` 或 `docs/handoffs/`。這些類型已與 validator、index 和 tests 同步納入，不要放在不相容的舊類型目錄。

正式發展建議：
- `docs/research/`：研究與證據，沿用既有 IDs。
- `experiments/`：可重現實驗，沿用既有 `OVR-EXP`。
- `docs/specs/`：PRD、Technical Design。
- `docs/handoffs/`：分期的開發交接封包與結果索引。
- implementation repo：產品 source、CI 與測試、issue、PR；不要複製大量程式碼進研究 repo。

## Coding Agent 交接與回寫

一份交接包要提供：

1. `objective`：使用者故事／範圍／non-goals。
2. `repositories`：研究庫與目標實作庫的 GitHub URL、base branch、pinned ref。
3. `requirements`：PRD 與 Technical Design 的版本/連結。
4. `interfaces`：跨服務資料契約、Extension 啟動/結束流程、錯誤處理。
5. `tasks`：最小 PR 拆分、各自 acceptance criteria。
6. `verification`：可執行測試、環境要求、哪些測試需要 RTX GPU/manual observation。
7. `evidence_map`：規格依據的研究報告與 pinned source，而不是用虛構程式碼填空。
8. `handoff_rules`：不得越權修改 repo、不得擅自聲稱 runtime 測試成功；問題回報格式。

Coding Agent 結束一階段要回報：commit/PR、changed files、實際執行的檢查、結果、與設計偏差、blockers、尚未驗證之事。Chat 將重要意外回寫到調查/實驗/ADR，不複製 commit log。

## 停止條件與資源控制

- 初步答案已可支持下一步時，不再機械式搜尋其他 repo。
- 搜索從 target repo+version+symbol 開始，逐步擴張，避免一開始全庫抓取。
- 需決策但缺 runtime 證據時，安排一個最小 PoC，而不是追加無限靜態研究。
- 不需保存就不分配 ID；未實作就不輸出「完成」標記。
- 文件需更新時，優先小修改既有報告而非另建重複報告。
