# RTS-01｜Glossary / 術語表

| Term | 中文 | Plain-language meaning |
| --- | --- | --- |
| Planner | 規劃端 | Defines the goal, scope, and acceptance criteria |
| Durable Queue | 持久化任務佇列 | Keeps a task retrievable after a chat or worker restarts |
| Task Contract | 任務契約 | Declares what to do and what qualifies as completion |
| Correlation | 關聯追蹤 | Joins related events; not necessarily a unique attempt ID |
| Selector | 任務選取器 | Finds eligible tasks |
| Router | 路由決策器 | Decides whether a compatible executor is ready |
| Claim / Lease | 接單／租約 | Controls who may run a task and for how long |
| Headless Readiness | 無人值守準備狀態 | Whether an executor works in the actual unattended context |
| MCP | 模型上下文協定 | Interface through which approved tool calls may be made |
| Bounded Validation | 受限驗證 | A test with a defined scope and stop conditions |
| CAS | 比較後更新 | Prevents stale writes from silently overwriting newer state |
| Readback | 遠端讀回 | Independently retrieves the authoritative stored Result |
| Evidence Gate | 證據關卡 | A required check before promoting a state |
| Prediction Error | 預測誤差 | Difference between expected and observed outcomes |
| Regression | 退化 | A capability that worked previously but fails under current conditions |
| Fixture | 測試樣本 | A controlled input designed for an explicit test |
| Synthetic | 合成資料 | Invented safe data, not exported from private operations |
| Agentic E2E | 代理式端到端 | Verifies the declared agent task path including tools and durable Result |

## Key equivalences that do *not* hold

- A configured tool is not a successfully invoked tool.
- A running workflow is not a completed task.
- A completed task in a synthetic fixture is not production certification.
- A written Skill is not necessarily installed in an agent.
- An aggregate result is not a full experimental dataset.

For the complete workflow see [Architecture](architecture-and-lifecycle.md).
