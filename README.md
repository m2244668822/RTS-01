# RTS-01｜智能體任務驗證系統

> 以繁體中文說明工程方法，以英文保留技術識別字、命令與 API 欄位。

## 專案簡介

RTS-01 是一套 bounded integration contract，用來驗證 Planner、durable queue、unattended Runner、bounded executor 與 Result writeback 是否真的形成可追蹤的任務閉環。

```text
Planner / ChatGPT
    ↓
durable queue
    ↓
isolated Runner
    ↓
bounded executor
    ↓
validation
    ↓
CAS Result writeback
    ↓
remote readback
```

核心問題是：任務被看見，不代表任務可執行；任務可執行，也不代表已接單、已執行或已驗證。

```text
visible ≠ runnable ≠ claimed ≠ executed ≠ verified
```

## 中文閱讀入口

| 入口 | 內容 |
| --- | --- |
| [工程案例研究](docs/case-study-zh-hant.md) | 問題、診斷、失敗校準與人機分工 |
| [探索歷程與工程學習](docs/project-history-zh-hant.md) | 觀察、推論、驗證結果與可重用規則 |
| [公開展示索引](docs/public-showcase-map.md) | 所有公開內容的閱讀地圖 |
| [安全公開邊界](docs/publication-boundary.md) | 哪些內容可以公開、哪些必須排除 |

## 系統架構與方法

| 主題 | 文件 |
| --- | --- |
| 架構與任務生命週期 | [Architecture & Lifecycle](docs/architecture-and-lifecycle.md) |
| 診斷 Skill | [Diagnostic Skill](docs/diagnostic-skill.md) |
| 故障分類與復原 | [Troubleshooting Playbook](docs/troubleshooting-playbook.md) |
| 安全治理與人工覆核 | [Security & Governance](docs/security-and-governance.md) |
| 工程演進 | [Project Evolution](docs/project-evolution.md) |
| 術語表 | [Glossary](docs/glossary.md) |
| 原始公開契約 | [Integration Contract](docs/RTS-01-integration-contract.md) |
| 發布狀態 | [Release Manifest](docs/release-manifest.md) |

## 公開版本保留什麼？

保留：

- 去識別化的架構與診斷方法。
- 通用狀態機與 evidence boundary。
- synthetic task / result 範例。
- 固定、無秘密、無外部網路的 bounded contract。
- 可重跑的測試與 GitHub Actions workflow。

排除：

- 私人 repository history 與分支。
- Runner 主機身份、使用者名稱與本機路徑。
- API keys、device codes、OAuth tokens 與 authorization headers。
- 原始 Actions logs、artifacts 與私人聊天。

## 執行公開 synthetic contract

需求：Python 3.10 或更新版本。不需要安裝套件、認證或網路連線。

```bash
python -m unittest discover -s tests -v
python -m src.rts01_contract --workdir .rts01-synthetic-run
```

這會在本機建立可丟棄的 queue，claim 一個 fixture task，執行固定的 `fixture.transform`，將結果以 content-addressed 方式寫入兩次，再從 local remote mirror 讀回相同結果。

## 狀態詞彙

```text
PROPOSED → RUNNING → VERIFIED | BLOCKED | FAILED
```

歷史結果不是目前 runtime truth。一次通過的 mechanical smoke test，也不等於 production Agentic E2E 已完成。

## 公開驗證模型

每個測試只記錄非秘密 metadata：

```text
task_id
run_id
trace_id
executor_class
capability_result
bounded_test_result
writeback_result
review_status
```

公開 reference contract 驗證：

```text
queue
→ claim
→ bounded execution
→ CAS writeback
→ remote readback
```

這是公開的 synthetic proof，不代表私人 queue、外部模型、特定帳號或 production environment 已被驗證。

## 目前發布狀態

`PUBLIC_CANDIDATE`

此 repository 是經過整理的公開技術文件與合成測試展示。它不是 general-purpose unattended agent runtime，也不是 production certification。
