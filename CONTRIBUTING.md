# Contributing Research and Delivery Artifacts

## Working model

先在 Chat 做 L1 探索，再依風險與重現需求升級至 L2–L5；不要求為每次問答建立文件。只保存會影響後續決策的來源證據、版本差異、可重現實驗、ADR、規格或交接成果。編輯前搜尋相關 artifact 並更新現有文件，避免重複報告。

## Git / PR policy

- 研究 repo 使用 `research/<topic>` 或 `docs/<topic>` 工作分支，透過 PR 合併到 `main`。
- upstream repositories 僅供研究；產品程式碼應在明確指定的 implementation repo。
- PR 描述應包含：研究問題、變更檔案、版本/證據、執行過的檢查與阻礙。
- 不將 ChatGPT 或 GitHub Connector 的唯讀權限誤認為可執行 Kit SDK。
- GitHub Ruleset 的實際設定見 GitHub UI；設定指引見 [`docs/governance/github-setup.md`](docs/governance/github-setup.md)。

## Artifacts and metadata

- 正式 artifact 從 `templates/` 開始，ID、type、status、日期等依 `scripts/validate_research.py`。
- `docs/research/`：`OVR-REPO`、`OVR-INV`、`OVR-VER`、`OVR-ADR`；`experiments/`：`OVR-EXP`。
- `docs/specs/`：`OVR-PRD`（`prd`）、`OVR-DES`（`technical-design`）。
- `docs/handoffs/`：`OVR-HOF`（`handoff`）。
- 對實質技術主張記錄 upstream URL、固定 commit/tag、path/symbol、檢查日期、證據 A/B/C/U 與 validation state。
- `examples/` 用來保存示例或未證實方案，不視為正式研究成果。

## Checks

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_research.py
python scripts/build_index.py
pytest -q
git diff -- docs/GENERATED-RESEARCH-INDEX.md
```

`build_index.py` 是產生索引的唯一途徑；提交生成後的變化。不要提交存取憑證、大量 upstream source、暫存輸出或不具授權的內容。

## Experiments

記錄確切目標 App/Kit build、OpenUSD、Extensions、OS/Python/GPU/driver/renderer、前置條件、命令、觀察結果與未驗證部分。動態 DMX／Art-Net／sACN 實驗預設使用隔離環境，不連接現場設備。
