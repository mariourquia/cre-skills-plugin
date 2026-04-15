# _core

The canonical substrate every role pack, workflow pack, overlay, and template in this subsystem builds on. If you change a file in `_core/`, expect ripple effects across the system — every pack reads from here.

## Files in this directory

| File | Purpose |
|---|---|
| `DESIGN_RULES.md` | The non-negotiable rules that all skill authors must follow. |
| `taxonomy.md` | Canonical segment / form / stage / management-mode / role / market / output taxonomy. |
| `ontology.md` | Canonical object definitions (Property, Unit, Lease, Work Order, etc.). |
| `metrics.md` | Canonical metric definitions using the metric contract schema. |
| `skill_conventions.md` | File-set and frontmatter conventions every pack must follow. |
| `approval_matrix.md` | Default autonomy thresholds and approval gates. |
| `guardrails.md` | Fair housing, legal, safety, and compliance rails. |
| `change_log_conventions.md` | How reference updates are logged, diffed, and approved. |
| `naming_conventions.md` | Metric naming rules, alias policy, and conflict detection. |
| `alias_registry.yaml` | The canonical metric alias registry. Humans and agents must check before naming. |
| `routing/` | Progressive-disclosure routing rules. |
| `schemas/` | YAML schemas for metric contract, reference record, skill manifest, overlay manifest, approval request, change log entry. |

## Dependency order

1. `taxonomy.md` — what categories exist.
2. `ontology.md` — what objects exist within those categories.
3. `schemas/metric_contract.yaml` + `metrics.md` — what we measure about those objects.
4. `schemas/reference_record.yaml` — how mutable figures are stored.
5. `routing/` — how a request is mapped to the right pack + overlays + references.
6. `skill_conventions.md` — how packs are structured so routing can find them.
7. `approval_matrix.md` + `guardrails.md` — when autonomy stops.
8. `change_log_conventions.md` + `naming_conventions.md` + `alias_registry.yaml` — how we stay coherent over time.

New contributors read in this order.
