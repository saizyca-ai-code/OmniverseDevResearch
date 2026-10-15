# GitHub Setup & Ruleset Checks

## Access and boundaries

1. 用已明確授權的 GitHub Connector 讀取研究 repository；先確認實際權限。
2. 優先從獨立 feature branch 建立 PR，不直接提交到 `main`。
3. 研究 repo 與 upstream／implementation repo 不可混淆；閱讀權限不等於有權修改其他 repository。
4. PR 的檢查結果要和本機、Kit SDK、RTX runtime 測試分開報告。

## Recommended protection for solo-maintained research repo

- Ruleset 生效於 `~DEFAULT_BRANCH`（只限制預設分支）。
- 禁止刪除受保護分支與 force push。
- Require pull request before merging。
- 單人時 Required approving reviews 設為 `0`；若確有其他審核者，可改成 `1`。
- Require status checks to pass，**必須在 Additional settings 加入** `validate`（現有 `.github/workflows/research-quality.yml` 的 job 名稱）；只勾選選項而沒有加入 Required checks 並不足以保護 CI。
- 可視情況啟用 Require conversation resolution；是否要求 branch up-to-date 依團隊合併頻率決定。
- 不以 Ruleset 名稱或文件推定設定已生效，應使用 GitHub API／PR 合併門檻實測。

**手動操作：** Repository → Settings → Rules → Rulesets → `protect` → Edit → Require status checks to pass → Additional settings → 輸入 `validate` → Add → Save。若下拉列表沒有自動出現，先確認 Actions job 已在最近的 workflow run 執行；GitHub 支援手動輸入 check 的精確名稱。Workflow 的名稱為 `Research quality`，job 的名稱才是 `validate`。

官方文件：
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/troubleshooting-rules

## Verification after changes

開一個非破壞性 feature branch + PR：確認能寫入工作分支，Actions 會執行 `validate`，Failed / Pending check 會阻止 merge，而 Success 時才可合併。不要在未確認分支保護效果前將測試 PR 合併。

> Ruleset 設定儲存在 GitHub，不屬於 repository 內的 Git commit。本文件是操作規範，不代表設定已由 CI 自動強制。
