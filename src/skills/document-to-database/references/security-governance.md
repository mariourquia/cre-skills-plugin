# Security and Governance

The document-to-database family handles rent rolls and operating statements, which carry personally identifiable and commercially sensitive information. The executable layer is built to be no weaker than the prose layer it sits beneath, and to be safe to run inside a stateless, zero-data-retention boundary. PII handling is implemented in `src/calculators/ingest/pii.py`, provenance in `src/calculators/ingest/provenance.py`, and determinism in `src/calculators/ingest/determinism.py`.

## The PII boundary

The boundary mirrors `src/skills/document-to-data-room-extractor/references/pii-redaction-policy.yaml` exactly, and parity is enforced by a sync test. Certain values are NEVER emitted as values:

- **Natural-person identity** — tenant individual names, guarantor names, signatory names, occupant names, emergency contacts.
- **Per-unit identity** — per-unit tenant name, per-unit actual rent tied to a named person, per-unit lease dates tied to a named person, named delinquencies.
- **Personal identifiers** — SSN, EIN of a natural person, driver's license, passport.
- **Personal contact** — personal phone, personal email, an individual's notice address.
- **Sensitive financial** — bank routing and account numbers, credit scores, guarantor personal balance-sheet detail, personal tax-return figures.

The unit and tenant grains are still preserved — the family does not throw away the spine — but identity is held under a different trust tier.

## Pseudonymization

A natural-person tenant name is consumed on ingest and replaced with a deterministic, salted pseudonym (`Tenant XXXXXX`). The salt is the `run_id`, so the same name maps to a stable token within one run, but the tokens are not trivially linkable across exports unless a consumer reuses the `run_id`. The raw name is never written to any output.

## The locator-not-value rule

For any field classified as PII, the cell ADDRESS (the locator — page / section / table / row / column / cell) is retained so a reviewer can find the source, but the verbatim value is never stored: `source_text_span` is dropped and `redaction_status` becomes `redacted`. A verbatim span is retained only for aggregate-safe fields. This is how the family keeps a complete audit trail without ever exposing sensitive text. The only thing allowed to cross into a prompt, a deck, or any downstream LLM context is a one-way reduction to an aggregate-safe view.

## Stdout and log discipline

The PII helpers never print a value. The leak scanner walks the entire emittable structure and, on a hit, returns the field PATHS only — never the offending value — mirroring the policy's hard-stop semantics. When a leak is detected, the directive is to halt emission and report the field paths; a partially redacted payload is never delivered. Diagnostics emit counts and locators (how many rows, which field path), never the sensitive content itself.

## `tenant_id` is a label, not an authentication token

The tenancy / workspace label is path-validated, not an auth credential. It must be present, must not contain `/`, `\`, or `..` (no path components), and must be at most 128 characters. It scopes a run and stamps the provenance; it does not grant access. Do not gate any sensitive operation on it. A missing or malformed label fails closed.

## Determinism and the zero-data-retention guarantee

The calculators are pure and stateless by construction, and that IS the zero-data-retention / stateless story:

- They are **stdlib-only** — no third-party dependencies.
- They **write only to stdout** — no files, no database, no network call, no side effects.
- They **hold no state** between runs.
- They **read no wall clock** — nothing in the support package imports `datetime` or `time`. Every timestamp (`created_at`, `updated_at`, `extracted_at`) comes from a caller-supplied `as_of`, and `run_id` is injected. A payload/graded run rejects a missing `as_of`, because a wall-clock fallback would break reproducibility.

The consequence is that the same input dict produces byte-identical JSON. There is no retained data, no hidden timestamp, and nothing to leak between runs.

## Audit trail without exposing sensitive text

The provenance bundle (the superset of the 8-column warehouse contract, plus granular locators, run/skill/parser identity, `pii_class`, and `redaction_status`) lets any emitted number be traced back to a `data-room/<doc>#<anchor>` source and a cell address — fully auditable — while the locator-not-value rule guarantees the sensitive value itself was never stored. The audit trail proves where a number came from without reproducing the PII it was derived near.

## Synthetic-only fixtures

The evaluation loop runs against synthetic-only fixtures. No real tenant, lease, or operating data is committed to the repository. When a fixture exercises the leak scanner, it uses synthetic banned values (e.g. a made-up name) so the guard can be proven to fire without any real PII ever being present. See `self-iteration-loop.md` for how the loop uses these fixtures and `data-quality-rules.md` for the non-overridable PII gate.
