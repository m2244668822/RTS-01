# RTS-01

RTS-01 is a bounded integration contract for a planner, durable task queue, unattended runner, executor, and result writeback path.

This repository is a clean public export. It does not contain the source private repository, private Git history, credentials, API keys, runner identities, local paths, or raw execution logs.

## Scope

```text
planner
  -> durable queue
  -> isolated runner
  -> bounded executor
  -> validation
  -> result writeback
```

The contract separates:

- mechanical delivery and result persistence;
- agentic executor readiness and bounded execution;
- evidence review and publication readiness.

`visible` is not the same as `runnable`, `claimed`, `executed`, or `verified`.

## Safety boundary

- Secrets are never committed or copied into this repository.
- Logs and results must redact credential-shaped values before persistence.
- Public evidence must be synthetic or aggregate and must not identify private hosts, users, paths, or tokens.
- A historical private repository is not rewritten into this repository.

## Verification model

Each test records only non-secret metadata:

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

See [the public integration contract](docs/RTS-01-integration-contract.md) and [the publication boundary](docs/publication-boundary.md).

## Status vocabulary

`PROPOSED` → `RUNNING` → `VERIFIED` | `BLOCKED` | `FAILED`

Historical results are not current runtime truth. A passing mechanical smoke test does not prove production agentic E2E.

