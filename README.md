# OmniverseDevResearch

研究 NVIDIA Omniverse、Kit、OpenUSD、RTX、Extensions 與整合技術的**研究、技術決策及可重現實驗知識庫**。ChatGPT 負責探索與方案設計；GitHub 保存有長期價值的知識。產品開發預設放在另外指定的 implementation repository，不在這裡修改 upstream 原始碼。

## Start here

1. 閱讀 [`PROJECT_INSTRUCTIONS.md`](PROJECT_INSTRUCTIONS.md) 與 [`docs/governance/research-to-delivery-workflow.md`](docs/governance/research-to-delivery-workflow.md)。
2. 研究證據與版本以 [`evidence-policy.md`](docs/governance/evidence-policy.md)、[`research-methodology.md`](docs/governance/research-methodology.md)、[`versioning-policy.md`](docs/governance/versioning-policy.md) 為準。
3. 從 [`catalog/repositories.yaml`](catalog/repositories.yaml) 找研究標的，正式文件依 [`templates/`](templates/) 建立。
4. 少量 Chat 探索不必建立文件；正式調查、關鍵決策、PoC、PRD、Technical Design 與 Agent Handoff 才值得保存。
5. 變更前先參閱 [`CONTRIBUTING.md`](CONTRIBUTING.md) 和 [`docs/governance/github-setup.md`](docs/governance/github-setup.md)。

## Work modes

- **L1 Exploration** — Chat 快速探索；不強制 ID、報告或 PR。
- **L2 Investigation** — 版本釘選的正式研究；重要成果放入 `docs/research/`。
- **L3 Solution Design** — 需求、方案、ADR、PRD、Technical Design；正式規格放入 `docs/specs/`。
- **L4 Implementation Handoff** — 可交付 Coding Agent 的設計、介面和測試交接；文件放入 `docs/handoffs/`。
- **L5 Validation / Knowledge Consolidation** — 驗收、實驗觀察和有決策價值的知識回寫。

詳情與轉換判準見 [`research-to-delivery-workflow.md`](docs/governance/research-to-delivery-workflow.md)。

## Repository layout

- `docs/governance/` — 工作規範、證據、版本與 GitHub 設定。
- `docs/research/` — `OVR-REPO/INV/VER/ADR` 等正式研究。
- `docs/specs/` — `OVR-PRD`、`OVR-DES` 規格文件。
- `docs/handoffs/` — `OVR-HOF` 開發交接。
- `experiments/` — `OVR-EXP` 可重現實驗紀錄。
- `examples/` — 範例／未驗證研究構想，**不是**已完成調查。
- `catalog/` — 來源 repository 清單。
- `templates/` — 各類 artifact 範本。
- `scripts/`、`tests/`、`.github/workflows/` — Metadata / Index / Catalog 的自動檢查。

## Validate

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_research.py
python scripts/build_index.py
pytest -q
```

提交前檢查 `git diff -- docs/GENERATED-RESEARCH-INDEX.md`，Generated Index 不可手動維護。研究 repo 的 CI 成功不代表 Omniverse Kit／RTX 執行環境已驗證。
