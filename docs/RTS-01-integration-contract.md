# RTS-01 Public Integration Contract

## Objective

Verify a bounded, auditable path from task planning to remote result readback without exposing private execution data.

## Required stages

1. Queue contract is durable.
2. Runner claims only a compatible task.
3. Runtime capabilities are reported under the actual executor identity.
4. Authentication class is reported without secret material.
5. Bounded execution uses a fixed test profile.
6. Tool calls stay inside the declared read-only or bounded-write boundary.
7. Result writeback is content-addressed and idempotent.
8. Remote readback confirms the same correlation identifier.

## Anti-cheating rules

```text
task visible != runnable
runnable != claimed
claimed != executed
executed != verified
historical PASS != current PASS
```

## Credential handling

The executor may use an approved authentication mechanism, but evidence must contain only:

- authentication class;
- exit status;
- readiness result;
- non-secret error code;
- correlation and run identifiers.

It must never contain a secret value, a copyable token, or an unredacted authorization header.

## Acceptance

The contract is verified only when all required stages have evidence from the same bounded run. A partial stage remains partial; it is not promoted by inference.

