# Example: Synthetic Task Contract

> Demonstration only. This file is not a queued task, runnable job or reference to any real environment.

```yaml
task_id: demo-task-001
correlation_id: DEMO-CORRELATION-001
status: queued
route: mechanical
project: synthetic-demo
executor: demo-executor
scope: read-only
objective: "Validate a small synthetic text payload"
acceptance:
  - "The fixture contains the word READY"
  - "The validator returns PASS"
  - "Result is persisted using an expected revision"
  - "Remote readback matches the persisted result"
publication: synthetic-only
```

## Expected control flow

1. Selector finds this **example** task.
2. Router checks whether a compatible demo executor exists.
3. Executor acquires an unexpired claim.
4. A bounded validator checks a fixed, non-sensitive text string.
5. The result writer publishes a terminal verdict through a revision check.
6. A separate readback checks the stored value.

## Distinct negative cases

- No compatible executor: mark route blocked; do not claim.
- Duplicate claim: reject the second owner without executing twice.
- Failed validation: report failed assertion, not done.
- Stale expected revision: CAS conflict; do not overwrite newer Result.
- Readback mismatch: do not report VERIFIED.

No real host, network, account or private content is required. See [Result example](synthetic-result.md).
