# DMX → Omniverse USD Composer / Kit → RTX：研究啟動案例

> **用途：研究流程示例／待驗證工作計畫，不是已完成的技術報告、產品能力保證或已核准 PRD。**

## 使用者需求（保持原意）

「我想要在 Omniverse USD Composer 中開發 DMX 燈光系統，能支援即時預覽和 RTX 渲染，幫我研究可用方案和相關技術，並完成工具開發。」

## L1 — Exploration：先切出關鍵決策

1. Target 產品：現有 USD Composer 的哪一版本、如何安裝/啟動、能否新增 Kit Extension？若不可行，是否接受由 `kit-app-template` 建立相近功能的 custom Kit App？**需驗證**。
2. I/O 方向：實際是接收現場 console 的 DMX 資訊、由 Omniverse 發送 DMX，還是雙向控制？初始 PoC 可先假定接收網路燈控協定、更新虛擬燈具，但不能將此假定當作需求已核准。
3. Network 協定候選：Art-Net、sACN / E1.31；若使用物理 DMX512 介面，另需硬體 gateway/USB 支援與安全範圍。這些是**候選技術**，非已確認在目標 Composer build 原生支援。
4. 虛擬燈具模型：fixture profile、DMX universe/address、channel mapping、8/16-bit 值、RGB/色溫、強度、pan/tilt、beam、gobo（依可行 API 分階段驗證）。
5. Render：需區分 viewport 即時預覽和 RTX Real-Time / RTX Path Tracing；各燈具屬性在目標 renderer 是否真的生效，要靠版本匹配的測試。

## L2 — 必須深入驗證的問題

| Investigation | 關鍵問題 | 證據方式 |
| --- | --- | --- |
| App lifecycle | USD Composer 此 build 是否仍可配置/安裝第三方 Extension？ | 官方 lifecycle 文件 + 實機驗證 |
| USD light schema | `UsdLux` 對應哪些 attributes；版本語意有何差異？ | Kit/OpenUSD pinned 文件與 sample |
| RTX renderer | 哪些燈光類型/attribute 會在指定 renderer 產生視覺效果？ | runtime PoC（GPU） |
| Protocol ingestion | Art-Net/sACN library 與 OS 支援、封包解析與權限？ | 官方/原始碼 + unit test |
| Event scheduling | DMX 更新如何節流/coalescing，不阻塞 Kit 更新執行緒？ | Kit API 查核 + 最小整合測試 |
| Stage persistence | 燈光值更新是 session layer、persistent layer 或 time samples？ | 實機 stage 修改與保存測試 |
| Error handling | 斷線、封包逾期、多 universe、重連如何影響燈具？ | 模擬器 + fault injection |

## L3 — 方案候選（未決，不先預設勝出者）

A. Kit Extension：直接在相容的 USD Composer/Kit 環境處理 UDP 接收、fixture 映射、USD 更新與 UI。

B. External bridge + Kit Extension：獨立 process 處理舞台協定及輸入驗證，Extension 負責 Kit/UsdLux 與 UI。可能較容易分離故障、獨立測試，但會增加部署與 IPC 複雜度。

C. Custom Kit App：若指定 USD Composer build 不便安裝/維護 Extension，使用 Kit App Template 建立自訂應用；增加產品組裝與部署成本。

評估軸：Composer build 相容性、使用者工作流程、部署成本、版本遷移、效能、除錯性、擴充 fixture 能力與 RTX 視覺一致性。

## 最小可行 PoC（暫定，不視為已執行）

- 用測試環境/模擬器產生 **一組**可重現的網路 DMX 控制資料，不與實際舞台燈控設備相連。
- 以兩種虛擬燈具實驗亮度/顏色變化，記錄 Stage 屬性變化與 renderer 可見結果。
- 檢查斷線恢復、資料更新停止時的 fail-safe 行為。
- 在指定 Kit/Composer/RTX/OS/GPU 環境量測更新延遲與穩定性；由使用者同意可接受門檻，不能自行宣稱滿足「即時」。
- 將結果明確標為 source-inspected / test-executed / runtime-verified，與預期分開。

## PRD / Design 產生條件

- 確認 target 應用與可取得版本、輸入/輸出方向、fixture MVP 功能和主要使用情境。
- 完成或列出需先做的 PoC：Light attribute → RTX 行為、Kit 更新方式、network bridge 接入。
- 定義能量測的 acceptance criteria 和實作 repo。
- 再將研究轉為 PRD、Technical Design、開發工作包；不必等所有非核心細節研究結束。

## L4 — 建議交付 Codex / Claude Code 的工作切片

1. Protocol simulator / parser / fixtures mapping unit tests（無 GPU 依賴）。
2. USD/Kit Extension skeleton、lifecycle 與明確 API contract。
3. Protocol → normalized fixture state → USD attribute bridge；增加可重現 integration test。
4. Mapping UI / diagnostics / error and reconnect flows。
5. RTX 視覺測試、效能 profiling、場景保存策略。
6. Packaging、版本鎖定、交付說明與 review。

每個切片獨立 PR；Coding Agent 回報實際 commit/測試，再更新研究與 ADR。

## 官方起始參照（仍需依實際版本釘選）

- NVIDIA Kit overview: https://docs.omniverse.nvidia.com/kit/docs/kit-manual/latest/guide/kit_overview.html
- NVIDIA Omniverse compatibility matrix: https://docs.omniverse.nvidia.com/usd/latest/common/compatibility-matrix.html
- NVIDIA lighting / UsdLux & RTX: https://docs.omniverse.nvidia.com/materials-and-rendering/latest/lighting.html
- NVIDIA Kit App Template: https://github.com/NVIDIA-Omniverse/kit-app-template
- NVIDIA legacy product entry: https://docs.nvidia.com/omniverse/
- Open Lighting Architecture (candidate protocol tooling): https://www.openlighting.org/ola/

**版本敏感提醒**：NVIDIA lighting 文件指出 `UsdLux` 25.05 的語意更新以及 Kit 109.0 的預設行為改變。具體 source/runtime 版本在正式研究時必須記錄；不能把單一最新文件的行為推廣到全部 USD Composer 版本。
