# Taxonomy

Every request into this subsystem is classified along these axes. The routing layer uses this taxonomy to select packs, overlays, and references. Skills and overlays declare the axes they apply to in their frontmatter.

## Axis 1 — Asset class

- `residential_multifamily` — the only value in this subsystem.

Reserved for future extension: `residential_btr`, `residential_senior`, `residential_student`, `residential_mixed_use`. Not implemented.

## Axis 2 — Segment

| Slug | Human name | Depth in Phase 1 |
|---|---|---|
| `middle_market` | Middle-market / workforce / attainable conventional rental | **Full depth.** |
| `affordable` | Lower-rent, affordable, LIHTC, HUD-related | Stub with divergence notes. |
| `luxury` | Class-A / luxury / lifestyle | Stub with divergence notes. |

Affordable and luxury stubs exist so overlays can diverge without touching canonical core. Do not deepen them in Phase 1.

## Axis 3 — Form factor

| Slug | Human name |
|---|---|
| `garden` | Garden-style (typically 2–3 story walk-up, surface parking). |
| `walk_up` | Walk-up (no elevator, small footprint). |
| `wrap` | Wrap (apartments wrapping a structured parking deck). |
| `suburban_mid_rise` | Suburban mid-rise (typically 4–6 stories, structured parking). |
| `urban_mid_rise` | Urban mid-rise (typically 5–8 stories, vertical mixed-use common). |
| `high_rise` | High-rise (9+ stories). Stub only. |

## Axis 4 — Lifecycle stage

| Slug | Human name |
|---|---|
| `development` | Pre-construction: entitlements, permitting, design, bidding. |
| `construction` | Under construction through substantial completion. |
| `lease_up` | From TCO through stabilized occupancy. |
| `stabilized` | Steady-state operations. |
| `renovation` | In-place value-add interior or common-area renovation. |
| `recap_support` | Preparing for refinance, disposition, partnership buyout, or recapitalization. |

## Axis 5 — Management mode

| Slug | Human name |
|---|---|
| `self_managed` | Owner operates the property directly. |
| `third_party_managed` | A third-party property manager operates on the owner's behalf. |
| `owner_oversight` | The owner-side oversight layer over a third-party manager. Used in conjunction with `third_party_managed`. |

A property in `third_party_managed` mode typically has both `third_party_managed` (site) and `owner_oversight` (owner-side) packs active simultaneously; the router loads the appropriate pack for the asking user's role.

## Axis 6 — Role

Roles map to who is asking. Packs live under `roles/<role_slug>/`.

### Site

- `property_manager`
- `assistant_property_manager`
- `leasing_manager` (covers leasing agents and leasing directors at property level)
- `maintenance_supervisor`

### Regional / corporate

- `regional_manager`
- `director_of_operations`
- `training_compliance_lead` (future — not in Phase 1)

### Ownership side

- `asset_manager`
- `portfolio_manager`
- `third_party_manager_oversight_lead`

### Development / construction / estimating

- `development_manager`
- `construction_manager`
- `estimator_preconstruction_lead`

### Finance / reporting

- `reporting_finance_ops_lead`

### Executive

- `coo_operations_leader`
- `cfo_finance_leader`
- `ceo_executive_leader`

## Axis 7 — Workflow / task

Workflows live under `workflows/<workflow_slug>/`. Routing may select a workflow directly, or a role pack may select one. The canonical list is in `workflows/INDEX.md`.

## Axis 8 — Geography

Geography is expressed through `reference/normalized/markets/`. A request may pin a single market (`market=Charlotte, submarket=South End`) or be portfolio-wide. If a role pack needs a market-scoped reference and no market is resolved, routing asks.

## Axis 9 — Output type

| Slug | Human name |
|---|---|
| `memo` | Narrative document with analysis and recommendation. |
| `kpi_review` | Tabular summary of KPIs vs. benchmarks and targets. |
| `checklist` | Actionable task list, often with owners and due dates. |
| `estimate` | Dollar estimate for a scope (capex, turn, bid, budget line). |
| `operating_review` | Structured operating review (weekly / monthly / quarterly). |
| `scorecard` | Rubric-scored evaluation (TPM scorecard, vendor scorecard). |
| `dashboard` | Metric grid with thresholds and drill-downs. |
| `email_draft` | Draft outbound communication (resident, vendor, owner, LP). |

## Axis 10 — Decision severity

| Slug | Meaning |
|---|---|
| `informational` | Describes state. No action recommended. No approval implied. |
| `recommendation` | Proposes an action. Human reads and decides. |
| `action_routable` | System may execute autonomously inside policy thresholds. |
| `action_requires_approval` | System must not execute without an approved `approval_request`. |

See `approval_matrix.md` for how severity maps to gates.

## Reserved expansion slots

The taxonomy reserves space for future segments, form factors, and roles without renaming anything today. Examples:

- Segment extensions: `senior`, `student`, `btr`, `mixed_use_residential`.
- Form factor extensions: `podium`, `cottage_court`.
- Role extensions: `training_compliance_lead`, `sustainability_lead`.

Reserved slots are documented here so overlays and manifests know what namespace is legal.
