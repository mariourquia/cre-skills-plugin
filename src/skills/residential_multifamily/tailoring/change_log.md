# Change Log — tailoring

## 0.1.0 — 2026-04-15
- Pack initialized.
- Frontmatter, body, metrics, workflows, routing, reference manifest complete.
- Audience question banks created: coo, cfo, regional_ops, asset_mgmt, development, construction, reporting.
- Missing-docs queue, sign-off queue, doc catalog schemas initialized.
- Preview protocol and interview flow specifications complete.
- Terminal UI reference implementation (`tools/tailoring_tui.py`) ships with stdlib-only ANSI rendering and PyYAML for parsing.
- Non-interactive unit tests (`tools/test_tailoring_tui.py`) cover question-bank loading, diff computation, and queue append.
- Example walk-through for a fictitious operator "Acme Multifamily" added under `examples/`.
- Pack explicitly forbids mutation of `_core/` and writing to `overlays/org/{org_id}/`. Sign-off queue is the stop-point for all proposed changes.
