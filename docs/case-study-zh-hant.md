# RTS-01｜跨系統任務閉環工程案例

## 案例標題

**RTS-01：跨 ChatGPT、durable queue、unattended Runner 與本機 executor 的可驗證任務診斷**

## 公開版本說明

這是一份根據私人工作紀錄重新撰寫的繁體中文公開案例。它保留問題拆解、證據規則、失敗校準與可重用方法；不包含私人聊天逐字稿、主機身份、實際路徑、私有分支、認證材料或 raw logs。

公開 repo 可重跑的部分是固定、無秘密、無外部網路的 synthetic contract。私人環境中的歷史結果不能直接當成這個公開 demo 的現況，也不能反向宣稱 production E2E 已完成。

## 一、問題背景

一個自然語言任務通常會經過多個上下文：

```text
Planner / ChatGPT
    ↓
GitHub durable queue
    ↓
isolated Runner
    ↓
bounded executor
    ↓
validation
    ↓
Result writeback / remote readback
```

最初的問題不是「某個指令怎麼下」，而是：

> ChatGPT 能不能把任務交給一條可驗證的執行鏈，而不是只產生一段看似合理的回答？

### 觀察 Observation

任務可以出現在 queue，workflow 也可以顯示綠燈，但任務仍可能沒有被 claim、沒有執行，或沒有留下可讀回的 Result。

### 當時推論 Hypothesis

早期容易把「任務可見」或「workflow 成功」當成「任務已完成」。也容易認為重跑同一任務就能解決所有問題。

### 驗證結果 Verification

RTS-01 將狀態拆開：

```text
visible
→ runnable
→ claimed
→ running
→ validated
→ verified
```

### 可重用規則 Reusable rule

每一個狀態都要有自己的證據。先找最早失敗的 gate，再做最小、可回復的修復。

## 二、診斷模型

RTS-01 使用 correlation trace 將任務路徑分成六層：

| 層級 | 要回答的問題 | 不能直接推論的事情 |
| --- | --- | --- |
| Retrieval | queue 是否保存任務？ | 任務已被接單 |
| Routability | 目前 executor 是否符合路由條件？ | executor 已開始工作 |
| Claim | 是否建立正式 claim？ | claim 一定會完成 |
| Execution | bounded executor 是否啟動？ | Result 已寫回 |
| Validation | 工具與測試是否符合限制？ | production 已驗收 |
| Writeback / Readback | Result 是否 CAS 寫入並能遠端讀回？ | 所有未來執行都可靠 |

這個分層阻止一個常見錯誤：把單一成功訊號擴大解讀成整條鏈已完成。

## 三、代表性故障：任務可見但沒有 claim

### 觀察 Observation

某次 agentic 任務能被 durable queue 找到，但沒有建立 claim。

### 當時推論 Hypothesis

初步可能懷疑 queue transport、GitHub 或 MCP 壞掉；也可能把問題誤判成任務不存在。

### 驗證結果 Verification

分層 probe 將問題收斂到 executor readiness：

```text
route = agentic
+ executor = auto
+ no executor satisfied headless readiness
→ executor unavailable
→ task visible but not runnable
→ no agentic claim
```

這證明「任務存在」與「任務可被接單」是兩個不同命題。

### 可重用規則 Reusable rule

不要用 queue 的存在性代替 executor 的可用性。`task visible ≠ runnable ≠ claimed`。

## 四、Runner identity 與 headless readiness

### 觀察 Observation

互動式桌面視窗可能找得到 CLI，服務程序卻可能使用不同的 profile、環境變數、PATH 或 authentication state。

### 當時推論 Hypothesis

最初容易把問題單獨歸因於 PATH、網路或登入畫面。但真正需要比較的是：

```text
execution identity
+ profile
+ CODEX_HOME access
+ executable discovery
+ auth parser
+ headless readiness
```

### 驗證結果 Verification

只有在實際 Runner service identity 下取得一致的 `version`、`login status`、`exit` 與 readiness probe，才能判定 unattended executor 可用。互動視窗顯示登入成功，不足以證明服務程序可執行。

### 可重用規則 Reusable rule

不搬移認證秘密，不擴大權限；只在同一執行身份下做 bounded discovery 與非秘密 probe。

## 五、Parser 回歸：登入文字不等於認證狀態

### 觀察 Observation

CLI 可能輸出類似 `Logged in using ChatGPT`，但 Runner 的認證解析器仍回報 `unknown`。

### 當時推論 Hypothesis

這可能被誤判成登入失敗，並導致重複進行 device login。另一個可能性是成功 probe 與 `execute-inbox` 使用了不同 parser、不同輸出通道或不同退出碼規則。

### 驗證結果 Verification

auth gate 必須在同一次 probe 中得到：

```text
auth_class = chatgpt
exit = 0
headless_ready = true
```

只有這三項同時成立，才可以進入後續 agentic contract。

### 可重用規則 Reusable rule

成功 probe 與實際執行器必須共用同一個 auth parser、欄位名稱與退出碼契約。UI 成功不得直接等同於 Agentic E2E 成功。

## 六、MCP、bounded execution 與 Result 回寫

### 觀察 Observation

Codex 或 MCP 可能已經啟動，但 tool call、bounded validation、CAS writeback 或 remote readback 仍可能失敗。

### 當時推論 Hypothesis

只看 process exit code，或只看一次 `tools/call`，就把任務標成完成，是常見的假陽性來源。

### 驗證結果 Verification

完整 acceptance path 應在同一次受控執行留下：

```text
auth
→ runtime.capabilities
→ MCP initialize
→ tools/list
→ bounded tools/call
→ validation
→ claim
→ execution
→ CAS Result writeback
→ remote readback
```

公開 repo 的 synthetic contract 已提供以下固定流程的可重跑示範：

```text
queue
→ claim
→ bounded execution
→ CAS writeback
→ remote readback
```

它不使用私人 queue、外部模型、認證或 production MCP host。

### 可重用規則 Reusable rule

完成判定必須綁定同一個 `task_id`、`trace_id` 與 run。缺少任何 gate，就維持 `PARTIAL`、`BLOCKED` 或 `NOT VERIFIED`。

## 七、失敗與 Prediction Error 的價值

### 觀察 Observation

多次失敗表面上都像「登入問題」，實際上可能分別來自 parser、身份、profile、權限、工具呼叫或回寫層。

### 當時推論 Hypothesis

如果只保留最後一次成功，系統會遺失哪些假設被推翻的資訊。

### 驗證結果 Verification

保留有界的失敗資料，可以區分：

```text
不可見
→ 可見但不可執行
→ 已 claim 但執行失敗
→ 執行成功但未回寫
```

### 可重用規則 Reusable rule

失敗不是成功的反面資料，而是模型校準資料。保留原因碼、範圍與證據邊界，但不公開秘密或私人環境細節。

## 八、人與 AI 的分工

RTS-01 的重要收穫不是「把所有工作交給 AI」，而是建立共同校準：

```text
Human
├─ 提供目標、現場觀察與接受標準
└─ 辨識異常並決定是否擴大範圍

ChatGPT
├─ 拆分問題與提出可證偽假設
└─ 整理證據與下一步

Runner / Executor
├─ 執行 bounded operation
└─ 暴露真實身份與 runtime 限制

GitHub / RTS-01
├─ 保存 durable evidence
├─ 記錄狀態轉換
└─ 蒸餾 reusable rule
```

自然語言可以成為複雜系統的問題描述與決策介面；但它不能取代實際執行、證據與驗收。

## 九、公開案例的結果邊界

公開版本可以合理展示：

- 如何把模糊問題拆成可驗證 gate。
- 如何區分 observation、hypothesis 與 verification。
- 如何診斷 queue、Runner、executor、MCP 與 writeback 的不同失敗。
- 如何把 Prediction Error 轉成 SOP、Skill 與 bounded contract。
- 如何用 synthetic test 呈現安全的 queue-to-readback 流程。

公開版本不能直接宣稱：

- 私人 ChatGPT 帳號永久有效。
- 任一 Windows Runner 都可自動接單。
- 所有歷史 blocked task 都可恢復。
- 公開 synthetic contract 等於 production Agentic E2E。
- 使用者或 AI 單方面完成整套底層工程。

## 十、對外讀者的學習路徑

```text
先讀本案例
→ 再讀 Architecture & Lifecycle
→ 用 Diagnostic Skill 對照 gate
→ 閱讀 Troubleshooting Playbook
→ 執行 synthetic contract
→ 最後查看 Security & Governance
```

## 結論

RTS-01 的核心不是「讓 AI 看起來像完成了工作」，而是讓任務的可見性、可執行性、接單、執行、驗證與結果回寫都能被分別證明。

這是一個可靠性診斷案例，也是一個人機共同工作的研究紀錄。它的公開價值來自可重用的方法，而不是來自暴露私人環境的細節。
