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

**Scope of checks:** pre-publication content-pattern screening for typical secret-shaped strings and selected private identifier patterns was applied to each successful addition. This is a limited textual preflight check, **not** a comprehensive independent secret scanner, privacy certification, license audit or proof about all Git history. Remote contents are subject to a subsequent readback check. Do not apply the earlier initial-export zero-match audit to every future addition without a new complete scan.

Two fuller candidate documents were held back during publication safety review; the public copy omits their unreviewed content. The repository remains `PUBLIC_CANDIDATE` and does not claim production readiness.
