# RTS-01｜Security and Governance Principles

> Public guidance, not a certification or an authorization to modify a host.

## 1. Security invariants

- Minimum necessary privilege and explicit task scope.
- The unattended executor must be evaluated under its **actual execution identity**, not an interactive desktop session.
- Never copy login material across identities merely to satisfy a readiness check.
- No unbounded disk discovery, recursive inspection of unrelated user directories, credential-store access, remote tunnels or silent privilege expansion.
- Prefer allowlisted read-only probes; a bounded write requires explicit target, test profile, approval and rollback.
- Prevent credential-like strings from entering exceptions, standard output, results or artifacts **before persistence**.
- Preserve evidence of failure without preserving confidential values.

## 2. Separate three kinds of truth

| Kind | Example | Permitted conclusion |
| --- | --- | --- |
| Direct observation | Queue contains a task | 'Task is visible' |
| Inference | Executor may lack readiness | 'Candidate hypothesis' |
| Independently checked evidence | Claim, bounded test and Result readback match | 'Verified for this exact run/scope' |

A successful action in one environment does not make it universally safe or reproducible.

## 3. Human–AI collaboration

Humans supply explicit intent, context, constraints and approval. An AI helps formalize hypotheses, identify contradictions and test evidence. Neither a model's guess about a person's feelings nor a human's informal impression about an external system is proof of the corresponding fact.

When the user clarifies intent, update the interaction model and keep a correction record without turning a single interaction into a fixed description of the person.

## 4. Publication classes

| Class | Default handling |
| --- | --- |
| General architecture / abstract contracts | Public candidate after review |
| Synthetic fixtures / aggregate non-identifying statistics | Public candidate after testing and review |
| Operational tasks / trace details / raw logs | Private by default |
| Credentials / authentication payloads | Never export |
| Personal or third-party information | Excluded unless independently authorized and minimized |
| Third-party source code | Separate license and provenance review |

A Git ignore file reduces accidental inclusion; it is **not** a security scanner or a guarantee that files never entered history.

## 5. Incident containment vs deletion claims

A key can be revoked and exposed active references removed while a provider may retain inaccessible backups or historical copies. Therefore reports should distinguish: containment done, active reference scan passed, scope reviewed, and physical destruction not independently proven. Do not equate a zero-match search with universal absence.

The public [Release Manifest](release-manifest.md) contains the bounded release-audit claims. Do not infer more than that document states.

## 6. What 'production-ready' would require

Separate security design, automated negative tests, review approvals, credential controls, reproducible deployment, incident response and independent penetration testing as appropriate. Current public documentation is **not** a production safety certification.
