# RTS-01｜探索歷程與工程學習（繁體中文）

這是一份去識別化的工程研究紀錄。它整理問題如何被拆開、假設如何被修正，以及哪些方法可以重用。

本文不是私人聊天逐字稿，也不是完整的 production incident report。技術識別字、命令、API 欄位與狀態名稱保留英文，避免翻譯造成操作歧義。

## 閱讀方法

每一段都分成四層：

1. **觀察 Observation**：當時實際看到的現象。
2. **當時推論 Hypothesis**：在證據有限時提出的解釋。
3. **驗證結果 Verification**：後續 probe 或測試真正證明了什麼。
4. **可重用規則 Reusable rule**：下次可以直接套用的判斷方式。

這種分層可以避免事後把結果說成「一開始就知道」。

## 1. 最初問題：任務能不能真的走完？

### 觀察 Observation

一個任務可能已經出現在 durable queue，也可能有綠色的 workflow，但仍然沒有完成實際工作。

### 當時推論 Hypothesis

早期容易把「流程綠燈」理解成「任務已被接單並完成」。另一個常見猜測是：只要再重跑一次，任務就會繼續。

### 驗證結果 Verification

測試顯示，以下狀態不是同一件事：

```text
visible → runnable → claimed → running → validated → verified
```

queue 存在、Runner 看得到任務、executor 可以執行，以及 Result 已遠端讀回，必須分開留下證據。

### 可重用規則 Reusable rule

先找最早失敗的 gate，再修最小範圍。不要把 queue、MCP、Runner 與 executor 一次全部重建。

## 2. Runner 身份：互動式成功不等於 unattended ready

### 觀察 Observation

同一台 Windows 電腦上，互動式 PowerShell 可能找得到 CLI；service Runner 卻可能看不到同一個 executable、profile 或 authentication state。

### 當時推論 Hypothesis

最初可能把問題歸類成 PATH 或網路故障。但真正需要比較的是執行身份、profile、`CODEX_HOME`、認證模式與 headless readiness。

### 驗證結果 Verification

只有在實際 Runner service identity 下取得一致的 probe，才能把 `auth_class`、`exit` 與 `headless_ready` 當成該 Runner 的證據。互動式視窗的 `Logged in` 不足以證明 unattended executor 可以工作。

### 可重用規則 Reusable rule

每次報告都要帶非秘密的身份類別、profile 狀態、CLI version、auth parser 結果與 readiness 結果；不搬移或複製認證秘密。

## 3. Parser：CLI 輸出文字不是穩定的狀態契約

### 觀察 Observation

CLI 可能回報類似 `Logged in using ChatGPT` 的文字，但 Runner parser 仍判定為 `unknown`，導致後續 agentic gate 不啟動。

### 當時推論 Hypothesis

早期容易把這視為登入本身失敗，或直接再做一次 device login。另一個可能性是：登入成功了，但 `execute-inbox` 與 success probe 使用不同的 parser 或不同的輸出通道。

### 驗證結果 Verification

這類問題必須比較同一次執行的 raw exit code、stdout、stderr 與 parser output。只有 parser 明確產生 `auth_class=chatgpt`，且 `exit=0`、`headless_ready=true`，才可以通過 auth gate。

### 可重用規則 Reusable rule

成功 probe 與實際 `execute-inbox` 必須共用同一個 auth parser、同一套欄位名稱與同一個退出碼規則。登入 UI 成功不得直接等同於 Agentic E2E 成功。

## 4. Execution：工具呼叫與 Result 回寫是不同 gate

### 觀察 Observation

Codex 或 MCP 可能已經啟動，但 tool call、bounded validation、CAS writeback 或 remote readback 仍可能失敗。

### 當時推論 Hypothesis

容易只看 process exit code，或只看一次 MCP 呼叫，就把整個任務標成完成。

### 驗證結果 Verification

完整 acceptance path 必須在同一次受控執行中留下：

```text
auth
→ runtime.capabilities
→ MCP initialize / tools/list / bounded tools/call
→ bounded validation
→ claim
→ execution
→ CAS Result writeback
→ remote readback
```

公開 repo 的 synthetic contract 只驗證固定、無網路、無秘密的合成流程；它不宣稱可以代替私人 production E2E。

### 可重用規則 Reusable rule

宣稱完成時，列出同一個 `task_id`、`trace_id` 與 run 的證據。缺少其中一個 gate，就保持 `PARTIAL`、`BLOCKED` 或 `NOT VERIFIED`。

## 5. 意外收穫：失敗本身可以成為診斷資料

### 觀察 Observation

多次失敗看起來像同一個問題，但實際上可能分別來自 parser、身份、profile、權限、工具呼叫或回寫層。

### 當時推論 Hypothesis

如果只保留最後一次成功，系統會失去 prediction error，也無法知道哪個假設被推翻。

### 驗證結果 Verification

把失敗保留為有界的歷史紀錄，可以區分「任務不可見」、「可見但不可執行」、「已 claim 但執行失敗」與「執行成功但未回寫」。這讓下一次修復能從正確的 gate 開始。

### 可重用規則 Reusable rule

失敗不是成功的反面資料；它是模型校準資料。保留狀態、原因碼、範圍與證據連結，但不公開秘密或私人環境細節。

## 6. 公開化：展示方法，不搬運工作環境

### 觀察 Observation

外部讀者需要看到架構、狀態機、測試契約與錯誤分類，才能理解 RTS-01；但私人聊天、Runner 身份、原始 logs 與憑證不能一起公開。

### 當時推論 Hypothesis

「全部分支與全部歷史都上傳」看似完整，實際上會擴大秘密、隱私、授權與不可重現證據的風險。

### 驗證結果 Verification

安全的公開形式是 clean-history、reviewed `main`、去識別化文件、synthetic examples、固定 bounded test，以及明確的 publication boundary。

### 可重用規則 Reusable rule

公開完整性不是資料量最大化，而是讓外部讀者能理解、檢查與重現安全部分，同時知道哪些證據被刻意排除以及原因。

## 一頁式收束

```text
問題
└─ workflow 綠燈不等於任務完成
   ├─ 拆分 visible / runnable / claimed / executed / verified
   ├─ 在實際 Runner identity 下驗證 readiness
   ├─ 統一 parser 與 exit-code contract
   ├─ 把 MCP、bounded test、CAS、readback 分開驗收
   └─ 公開可重現方法，不公開私人工作環境
```

## 對外讀者的限制聲明

RTS-01 的公開資料展示可靠性診斷方法與合成契約。它不保證任何特定 ChatGPT 帳號、Windows Runner、MCP host、模型或 production environment 永久可用，也不把歷史成功直接推論成目前 runtime truth。

延伸閱讀：[Project Evolution](project-evolution.md)、[Diagnostic Skill](diagnostic-skill.md)、[Publication Boundary](publication-boundary.md)。
