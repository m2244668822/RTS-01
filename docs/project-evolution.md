# RTS-01｜Project Evolution & Engineering Lessons

This is a synthesized engineering narrative from earlier discussions and private test work. It deliberately excludes original transcript text, private repository links, host identities, credentials, raw logs and private commit references.

## Stage A — A task can be visible yet never execute

**Observation:** a durable queue and a green workflow do not necessarily imply a task was claimed or executed.

**Initial hypothesis:** some global connection might be broken.

**Better model:** divide the path into retrieval, routability, claim, execution, validation and writeback. Test one gate at a time.

**Reusable rule:** diagnose the earliest failed gate; do not rebuild every subsystem based on a vague symptom.

## Stage B — Interactive availability is not unattended readiness

**Observation:** an editor or desktop session may locate an executable while the service runner cannot.

**Revised hypothesis:** service identity, environment discovery, authentication class and headless readiness are independent.

**Prediction:** if the mismatch is real, probing under the actual runner identity will reproduce it.

**Reusable rule:** report the actual identity class and non-secret readiness status, without moving credentials or expanding permissions.

## Stage C — Execution is not durable completion

**Observation:** code can execute and a tool test can pass while Result publication or remote synchronization fails.

**Revised model:** the task's terminal verdict requires revision-aware Result persistence and readback, not a process exit code alone.

**Reusable rule:** claim success only when the entire declared same-run acceptance contract is satisfied.

## Stage D — Safe synthetic end-to-end verification

A later disposable test fixture was recorded as satisfying its bounded Agentic E2E acceptance path after several historical blocked attempts. This establishes a **specific fixture result**, not production portability or unbounded autonomy.

The existence of many failed attempts is useful: their causes were not all the same and the sequence should not be presented as a representative sample of live user workloads.

## Stage E — Public documentation without exporting the work environment

The project then separated its public contract, architecture and sanitized teaching material from private execution evidence. The public repository uses a fresh history. This boundary is a deliberate feature, not missing documentation.

## What RTS-01 teaches

1. Separate observation from inference.
2. Define acceptance before repeating work.
3. Keep each attempt's scope and provenance.
4. Retain failed tests and prediction error.
5. Prefer a small reversible probe to a large speculative repair.
6. Preserve human approval and security controls.
7. Publish reusable methods rather than private raw evidence.

See [Architecture](architecture-and-lifecycle.md), [Skill](diagnostic-skill.md) and [Troubleshooting](troubleshooting-playbook.md).
