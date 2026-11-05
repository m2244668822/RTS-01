# Example: Synthetic Result and Verification

> Demonstration only. It describes what success evidence should look like; no test runner has executed this fixture in the public repository.

```yaml
task_id: demo-task-001
correlation_id: DEMO-CORRELATION-001
run_id: demo-run-001
trace_id: demo-trace-001
executor_class: demo-executor
claim_valid: true
execution_started: true
bounded_test:
  name: synthetic-text-check
  expected: "READY"
  observed: "READY"
  outcome: PASS
writeback:
  revision_expected: rev-001
  revision_published: rev-002
  cas_status: PASS
remote_readback:
  revision: rev-002
  correlation_matches: true
final:
  task_state: done
  evidence_state: VERIFIED
  scope: synthetic-demo
```

## Interpretation

This is a **made-up example**, not proof of a real GitHub Action, MCP invocation, secret scan, or production deployment. Every value above is illustrative.

If the remote revision were `rev-003` or the readback correlation did not match, the evidence status must be reduced to BLOCKED or PARTIAL even if the local process exited successfully.

Do not add authentic credentials, runner identity information, operational logs or private task IDs to this sample.
