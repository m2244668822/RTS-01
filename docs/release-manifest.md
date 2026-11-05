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

