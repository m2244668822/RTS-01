# RTS-01 Public Release Manifest

Release state: `PUBLIC_CANDIDATE`

This manifest records the release boundary without exposing private repository content or credential material.

## Security checks

| Check | Result |
| --- | --- |
| Suspected OpenAI key | Revoked |
| GitHub Actions secret associated with the incident | Removed |
| Affected remote branches | Removed |
| Active branch refs reaching the incident commit | None observed |
| Related Actions logs scanned | 41 runs |
| Credential-shaped matches in those logs | 0 |
| Related artifacts | 0 |
| Actions cache entries | 0 |
| Public export secret-pattern scan | 0 matching files |
| Public export private-identifier scan | 0 matching files |

## Non-claims

- Revoking a key does not erase copies that may already have been observed by a third party.
- Deleting branch refs does not guarantee immediate physical removal from every provider backup or retention layer.
- This repository does not claim that the private source repository is safe to publish.
- This repository does not claim production E2E completion.

## Export rule

Only the reviewed files in this repository are public. New files require the publication-boundary review before they are added.


## Documentation expansion note (2026-11-05)

After the initial five-file clean-room export, additional **newly authored public documentation** was added to explain the previously discussed architecture, diagnostic Skill, recovery method, security policy, engineering lessons, glossary and synthetic contract examples.

Files added in this expansion:

- `docs/architecture-and-lifecycle.md`
- `docs/diagnostic-skill.md`
- `docs/troubleshooting-playbook.md`
- `docs/security-and-governance.md`
- `docs/project-evolution.md`
- `docs/glossary.md`
- `examples/synthetic-task.md`
- `examples/synthetic-result.md`

**Scope of checks:** pre-publication content-pattern screening for typical secret-shaped strings and selected private identifier patterns was applied to each successful addition. This is a limited textual preflight check, **not** a comprehensive independent secret scanner, privacy certification, license audit or proof about all Git history. All successful additions were subsequently fetched back and checked for the same limited patterns. Do not apply the earlier initial-export zero-match audit to every future addition without a new complete scan.

Three proposed long-form documents (detailed historical evaluation, a learning guide and a roadmap) were held back during publication safety review; the public copy omits their unreviewed content. The repository remains `PUBLIC_CANDIDATE` and does not claim production readiness.

## Public showcase map

The reviewed public material is presented through `docs/public-showcase-map.md`. It maps the RTS-01 concepts and content families to public files without mirroring private branches, raw history, Runner identities, local paths, logs or artifacts.

The Traditional Chinese public case study is a de-identified rewrite at `docs/case-study-zh-hant.md`. It is a learning document, not a private transcript or a claim that every historical agentic run passed.

## Synthetic contract verification

The public reference runner was verified locally and by GitHub Actions Run `42053189781` at commit `e108488abb2e1e34202be83f48515c080b01d4e5`.

The verified sequence is:

```text
queue → claim → bounded execution → CAS writeback → remote readback
```

This is a local fixture contract. It does not prove access to a private GitHub queue, a real runner, an external model, or production E2E behavior.
