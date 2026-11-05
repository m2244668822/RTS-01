# RTS-01｜Diagnostic Skill (Public Adaptation)

**Status:** documented reusable diagnostic procedure. This file is **not** proof that any third-party agent, IDE or runtime automatically loads the skill.

## Purpose

Enable an assistant to diagnose the path from user intent to durable task Result without confusing a UI indication, configuration, execution attempt or verified completion.

## When to apply

- A task exists but is not runnable or claimed.
- The workflow is green but the requested work is not done.
- An editor can use a tool but the unattended runner cannot.
- MCP is configured but no bounded tool call has been proven.
- The queue, claim, test and Result disagree.
- A previous blocked attempt needs evidence-based recovery.

## Inputs required

- Declared task goal, scope, identity and acceptance criteria.
- Current durable task / Result, current job-step conclusions and runner readiness evidence.
- Evidence for tool invocation, validation, publication and readback.
- Relevant last-known-good evidence, explicitly labeled historical.

Do not request passwords, authentication exports, raw authorization headers, complete user directories, personal conversation histories or unbounded system access.

## Eight-stage diagnostic procedure

1. **Identity:** distinguish task identifier, correlation grouping and execution attempt.
2. **Retrieval:** prove the durable task exists and the selector can parse it.
3. **Routability:** test route, project contract, capacity and headless readiness.
4. **Claim:** prove a compatible executor accepted ownership.
5. **Execution:** prove the intended process started, not merely that a job was scheduled.
6. **Validation:** inspect bounded tests, allowlisted tool-call evidence and errors.
7. **Writeback:** inspect the revision-aware Result and independently read it from the remote source.
8. **Recovery:** classify the earliest failing gate, predict the minimal fix, test it and preserve negative evidence.

## Evidence precedence and conflict handling

Task contract / durable Result, workflow steps, runtime capabilities, MCP audit, user observation and historical reports have different functions. Prioritize evidence with a direct link to the specific gate being claimed. **A persisted Result is not immune to error**: if it contradicts a test or readback, investigate the inconsistency instead of declaring victory.

## Strict distinctions

- Visible ≠ runnable ≠ claimed ≠ executed ≠ verified.
- Installed on an interactive desktop ≠ usable by an unattended service identity.
- Configured MCP ≠ a successful bounded tools/call.
- Historical PASS ≠ current PASS.
- Agent narrative ≠ independent task verification.
- A single successful fixture ≠ generalized or production reliability.

## Minimum response contract

```yaml
task_id: "example-task"
scope: "synthetic-only"
observed_at: "example-timestamp"
current_gate: "routability"
status: "BLOCKED"
observed: "selector sees task; no compatible headless executor"
inference: "readiness mismatch is a candidate explanation"
blocker_code: "B-ROUTER"
next_minimal_probe: "inspect runtime capability flags under runner identity"
expected_if_hypothesis_true: "readiness remains false for the configured executor"
disconfirming_result: "executor is ready, but selector still rejects the task"
next_action: "no mutation until the cause is isolated"
evidence: "sanitized reference only"
```

Fields are illustrative and must be populated with real evidence before making a verified claim.

## Safety and human-context limits

Use least privilege and bounded discovery. Never copy credentials between accounts or bypass approval. If the user corrects an inferred intention or feeling, update the interaction hypothesis; do not transform it into a permanent personality claim. Human context is valuable input, but neither AI inference nor human intuition overrides independent external execution evidence.

## Deployment note

The original internal skill specification was a draft. This document publishes the reusable method only, not its private source, installation metadata or local execution configuration. For recovery steps see [Troubleshooting](troubleshooting-playbook.md).
