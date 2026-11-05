# RTS-01｜Troubleshooting & Recovery Playbook

> Use for diagnosis and safe recovery; not a recipe for privileged service manipulation.

## 1. Find the first failing gate

| Symptom | Candidate layer | Safe first check |
| --- | --- | --- |
| No task at authoritative source | Retrieval | Check expected task identifier and source |
| Task exists, selector misses it | Queue contract | Validate parser / schema using synthetic fixture |
| Selector sees task, not runnable | Router / readiness | Check route, capacity and readiness under actual identity |
| Runnable without claim | Claim | Inspect lease / ownership / contention |
| Claimed without execution | Executor / host policy | Inspect step state and service context |
| Process starts, tool call fails | MCP / policy | Inspect allowlist and non-secret error category |
| Tool call succeeds, test fails | Validation | Compare assertion and observed result |
| Validation passes, no Result | Writeback | Examine CAS conflict / publication status |
| Result exists, remote differs | Readback / sync | Compare revision and fetched Result |

Stop at the earliest unproven gate. Do not rebuild the entire queue to fix a single readiness failure.

## 2. Blocker taxonomy

| Code | Area |
| --- | --- |
| B-TRANSPORT | Queue / runner / network transport |
| B-DISCOVERY | Executable discovery / PATH |
| B-AUTH | Authentication class, session or identity mismatch |
| B-ROUTER | Route, readiness or capacity |
| B-CLAIM | Ownership, lease or claim conflicts |
| B-MCP | MCP initialize, tools/list or tools/call |
| B-HOST-POLICY | Execution policy / approval boundaries |
| B-VALIDATION | Bounded tests and workspace policy |
| B-WRITEBACK | CAS publication or remote readback |
| B-INTEGRATION | Conversation-event ingestion adapter |
| B-GOVERNANCE | Conflicting authority, legacy contract or permissions |

These are diagnostic categories, not claims of a specific root cause.

## 3. Bounded executor discovery

Allowed order: explicitly approved executable location → service PATH lookup → approved common locations → stop. A user desktop and a service runner may use different profiles. Do not scan an entire drive, search arbitrary user directories, inspect credential stores or transplant another identity's login artifacts.

Only collect safe status indicators: executable exists, version probe result, authentication state (no secret material), service-class identity match, and headless readiness.

## 4. Prediction before repair

Example hypothesis: 'The runner cannot route because executor discovery failed.'

- **Prediction:** a bounded executable lookup under the runner identity will fail.
- **Disconfirmation:** executable is found and headless readiness is true, yet route still rejects the task.
- **Next hypothesis:** router project contract or capacity decision is wrong.

Record the difference between predicted and observed behavior. A repair is not verified until a new bounded test proves its intended effect.

## 5. Recover without destroying evidence

1. Freeze the current observation and capture a sanitized snapshot.
2. Identify last-known-good state, its age and its environment.
3. Apply the least privileged change that addresses the proven gate.
4. Check local regression and remote readback.
5. Preserve failed attempts and link successor attempts rather than mutating completed history.
6. Stop if a repair requires unknown credentials, unexpected privilege, destructive workspace cleanup or publication of private logs.

## 6. Handoff template

```yaml
task: "example-task"
scope: "bounded-demo"
verified_fact: "task visible in durable queue"
current_blocker: "B-ROUTER"
last_successful_gate: "retrieval"
next_probe: "readiness and route decision, non-secret only"
hypothesis: "executor readiness mismatch"
prediction: "readiness probe will not pass"
counterexample: "probe passes while router rejects"
rollback: "restore previous approved configuration"
stop_if: "unexpected privileges or credential request"
outcome: "NOT_VERIFIED"
```

Do not label a recovery complete solely because a workflow became green. See [Architecture](architecture-and-lifecycle.md) and [Diagnostic Skill](diagnostic-skill.md).
