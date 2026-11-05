# Publication Boundary

## Included

- architecture and contract descriptions;
- generic state machines;
- synthetic redaction examples;
- aggregate test outcomes without private identifiers;
- reproducible bounded-test guidance.

## Excluded

- private repository history;
- raw Actions logs or artifacts;
- runner hostnames, usernames, local paths, or service identities;
- API keys, device codes, OAuth tokens, authorization headers, and secret names;
- private inbox contents and personal knowledge-base material.

## Release gate

Before adding a file, scan the complete file and its history for credential-shaped values and private identifiers. Keep the release `PUBLIC_READY` only after the scan, review, and repository readback all pass.

