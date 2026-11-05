# RTS-01｜智能體任務驗證系統

> 一份以繁體中文導覽、英文技術識別字為主的 bounded integration contract。

**中文入口：** [探索歷程與工程學習](docs/project-history-zh-hant.md) · [公開展示索引](docs/public-showcase-map.md) · [安全公開邊界](docs/publication-boundary.md)

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

## Run the synthetic contract

Requirements: Python 3.10 or newer. No package installation, credentials, or network access is required.

```bash
python -m unittest discover -s tests -v
python -m src.rts01_contract --workdir .rts01-synthetic-run
```

The command creates a disposable local queue, claims one fixture task, runs the fixed `fixture.transform` operation, writes a content-addressed result twice, and reads the same result back from a local remote mirror.

## Status vocabulary

`PROPOSED` → `RUNNING` → `VERIFIED` | `BLOCKED` | `FAILED`

Historical results are not current runtime truth. A passing mechanical smoke test does not prove production agentic E2E.


## Documentation map / 文件導覽

The following documents are **sanitized public adaptations** of the project's earlier engineering discussions, not exported chat transcripts or operational logs.

| Topic | Document |
| --- | --- |
| Full architecture and task states | [Architecture & Lifecycle](docs/architecture-and-lifecycle.md) |
| Reusable diagnosis rules | [Diagnostic Skill (public adaptation)](docs/diagnostic-skill.md) |
| Troubleshooting and recovery | [Troubleshooting Playbook](docs/troubleshooting-playbook.md) |
| Security, permissions and human review boundaries | [Security & Governance](docs/security-and-governance.md) |
| Engineering lessons and historical decisions | [Project Evolution](docs/project-evolution.md) |
| 繁體中文歷程與學習 | [探索歷程與工程學習](docs/project-history-zh-hant.md) |
| Terminology | [Glossary / 術語表](docs/glossary.md) |
| Non-operational demonstration | [Synthetic Task](examples/synthetic-task.md) → [Synthetic Result](examples/synthetic-result.md) |
| Original contract | [Public Integration Contract](docs/RTS-01-integration-contract.md) |
| Publication safety | [Publication Boundary](docs/publication-boundary.md) · [Release Manifest](docs/release-manifest.md) |
| Public presentation | [Public Showcase Map](docs/public-showcase-map.md) |

## How to use this material

Start with **Architecture**, then read **Diagnostic Skill** to learn the eight diagnostic gates. The **Troubleshooting Playbook** gives a failure classification and recovery method. The two **synthetic examples** describe a hypothetical task and result, not a working executor or a successfully executed CI test.

A documented Skill is not necessarily installed in any assistant. The repository currently publishes a **contract and teaching material**, not a general-purpose unattended agent runtime or production certification.

## Current publication state

The repository exists publicly as a curated documentation export. The release manifest still identifies its release state as `PUBLIC_CANDIDATE`; these newer documentation additions do not imply that a versioned software release has been issued or that earlier private test evidence can be independently reproduced from these files.
