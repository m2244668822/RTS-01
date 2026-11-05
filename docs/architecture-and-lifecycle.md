# RTS-01｜Architecture and Task Lifecycle

> Public design reference · sanitized conceptual derivation · not a production deployment guide.

## 1. Problem statement
A conversational assistant can say a job is complete while the queue only received it, the runner never claimed it, a tool failed, or the durable Result was never published. RTS-01 turns these distinct conditions into observable gates.

**Goal:** Evidence-before-success. Share verifiable task state among the planner, durable queue and runner; do **not** claim they share internal AI memory.

## 2. Logical architecture

```text
Human request / Planner
  -> ConversationEvent (proposed ingestion adapter)
  -> Durable Queue (persisted task contract)
  -> Selector + Router (compatible task and readiness)
  -> Executor Claim (owner / lease)
  -> Bounded Executor (mechanical or agentic)
  -> Allowlisted MCP tools / bounded tests
  -> Validation
  -> Compare-and-Swap Result publication
  -> Remote readback + audit
  -> Human-facing status
```

This is a **logical target flow**. A diagram edge is not a claim that the corresponding product integration is deployed. In particular, conversational ingestion needs separate acceptance evidence.

## 3. Component responsibilities

| Component | Responsibility | Proof needed |
| --- | --- | --- |
| Planner | Define task goal, boundaries and acceptance criteria | Explicit task contract |
| Durable Queue | Persist an addressable task | Task retrievable from authoritative source |
| Selector / Router | Check project, route, executor, capacity and readiness | Structured decision or reason code |
| Claim | Record exclusive execution ownership | Durable claim with matching execution identity |
| Runner / Executor | Execute using the actual service identity | Actual start and exit evidence |
| MCP adapter | Invoke only approved tools under declared scope | Initialize / list / call evidence when required |
| Validator | Run bounded contract checks | Named test results and expected/observed |
| Result writer | Publish terminal result safely | CAS / revision-aware write, failure handling |
| Remote reader | Verify source-of-truth Result | Readback of same task and expected correlation |

## 4. State separation

Two independent dimensions must never be conflated:

**Task lifecycle:** `queued`, `running`, `done`, `blocked`, `failed`.

**Engineering evidence maturity:** `DESIGNED`, `IMPLEMENTED`, `EXECUTED`, `VERIFIED`, `PARTIAL`, `BLOCKED`.

For example, a task may be `blocked` while its executor discovery fix is `IMPLEMENTED`; a workflow can be green while no task transitioned to `done`.

## 5. Correlation, idempotency and concurrency

- `task_id` identifies one task; a correlation key joins related attempts and stages without becoming a unique attempt ID.
- `run_id` and `trace_id` identify a specific observed run and trace. Never equate repeated correlation IDs with identifier collision by default.
- Terminal tasks are not silently requeued. Use an explicit new attempt or successor task with provenance.
- A claim needs ownership / lease rules. Conflicting claims or stale leases must fail safely.
- Compare-and-swap publication prevents a stale writer from overwriting a newer result; remote readback confirms the durable state.
- A green publishing step does not prove the published Result says `done`.

## 6. Acceptance as a conjunction

```text
task_found
AND runnable
AND claim_written
AND executor_identity_matches
AND execution_started
AND bounded_validation_passed
AND result_published
AND remote_readback_matches
=> VERIFIED for that run's declared scope
```

If a required condition is unknown, the conclusion is not VERIFIED. Results from a disposable fixture must not be extended to production, a different host, or all possible tasks.

## 7. Design decisions and limitations

The project deliberately prefers the smallest proven repair over a broad redesign. Missing PATH lookup is not evidence that the queue needs replacement. Current evidence outranks stale reports, but contradictory sources must be reconciled rather than ignored.

This repository is an architectural/documentation export, not a turnkey runnable agent platform. See [Integration Contract](RTS-01-integration-contract.md) and [Evidence & Evaluation](evidence-and-evaluation.md).
