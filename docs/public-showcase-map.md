# RTS-01 Public Showcase Map

This page is the safe presentation layer for RTS-01.

It maps the reviewed public material into a readable path. It does not mirror the private repository's branches, raw history, Runner logs, credentials, local identities or unpublished evidence.

## Start here

```text
README
├─ Architecture & Lifecycle
│  └─ task states, evidence layers and the end-to-end contract
├─ Diagnostic Skill
│  └─ ordered checks for discovery, readiness, execution and writeback
├─ Troubleshooting Playbook
│  └─ failure classes, smallest recovery action and stopping rules
├─ Security & Governance
│  └─ secret boundaries, least privilege and human review
├─ Project Evolution
│  └─ sanitized engineering lessons and scope changes
├─ Glossary
│  └─ queue, claim, MCP, CAS and readback terminology
├─ Synthetic Task → Synthetic Result
│  └─ a non-operational example of the evidence shape
└─ src + tests + GitHub Actions
   └─ deterministic local contract: queue → claim → bounded execution
      → CAS writeback → remote readback
```

## Content mapping

| RTS-01 material | Public representation | Boundary |
| --- | --- | --- |
| Architecture and lifecycle | `docs/architecture-and-lifecycle.md` | Newly authored public explanation |
| Case study and engineering narrative | `docs/case-study-zh-hant.md` | Traditional Chinese, de-identified rewrite |
| Diagnostic and recovery method | `docs/diagnostic-skill.md`, `docs/troubleshooting-playbook.md` | No operational secrets or host identifiers |
| Security and governance | `docs/security-and-governance.md`, `docs/publication-boundary.md` | Policy and evidence rules only |
| Engineering history | `docs/project-evolution.md` | Sanitized lessons, not private commit history |
| Task and result contract | `examples/synthetic-task.md`, `examples/synthetic-result.md` | Synthetic values only |
| Executable reference | `src/`, `tests/`, `.github/workflows/` | Fixed local operation; no arbitrary shell or network |

## Branch disposition

The public repository intentionally uses one reviewed `main` line.

```text
Private RTS-01 development branches
├─ historical diagnostics       → summarized, not mirrored
├─ runner/auth investigations   → summarized, not mirrored
├─ security-response work       → sanitized policy only
└─ raw evidence and artifacts   → excluded

Public RTS-01
└─ main
   ├─ reviewed documentation
   ├─ synthetic examples
   └─ deterministic bounded contract test
```

This is deliberate. “All branches” is not a safe publication rule when a branch may contain a secret, a private path, a service identity, or raw execution evidence. The public equivalent is a reviewed content map, not a branch-for-branch copy.

## Current proof boundary

The public reference contract has fresh evidence for:

```text
queue
→ claim
→ bounded execution
→ CAS writeback
→ remote readback
```

The public repository does not claim:

- private queue access;
- production Runner access;
- ChatGPT or API authentication validity;
- unrestricted agentic execution;
- full private-history reproducibility;
- production readiness.

The current release state remains `PUBLIC_CANDIDATE` until a separate release decision accepts the security, license, documentation and maintenance checks.

## Verification pointers

- Local test: `python -m unittest discover -s tests -v`
- Local contract: `python -m src.rts01_contract --workdir .rts01-synthetic-run`
- CI workflow: `.github/workflows/synthetic-contract.yml`
- Release boundary: `docs/release-manifest.md`
