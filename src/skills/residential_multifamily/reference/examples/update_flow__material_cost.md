# Update Flow Walk-Through — `material_cost` (Lumber Spike + Flooring Vendor Change)

Scenario: in early 2026-Q2, a commodity index pull reports a 14% month-over-month jump in SPF 2x4 lumber. In the same window, our primary flooring distributor rebases LVP pricing. Two events trigger parallel material_cost updates; both affect downstream unit_turn_cost and capex_line_item derivations.

## 1. Inbound

Two inbound files land:

```
reference/raw/material_cost/2026/03/purchasing_aggregate__2026-03-31.csv
reference/raw/material_cost/2026/04/lumber_commodity_spike__2026-04-10.csv  (follow-on)
```

Example row (lumber):

| source_row_id | region | material_slug | material_category | price_amount | unit | trailing_12mo_change_pct |
|---------------|--------|---------------|-------------------|-------------|------|-------------------------|
| MC-2026Q2-SE-LUMB-2X4-SPIKE | southeast | lumber_2x4x8_spf | lumber | 4.85 | dollars_per_board_foot | 11.2 |

Example row (LVP vendor change):

| source_row_id | region | material_slug | material_category | price_amount | unit |
|---------------|--------|---------------|-------------------|-------------|------|
| MC-2026Q2-SE-LVP-6MM-VENDOR | southeast | lvp_flooring_6mm | flooring | 3.05 | dollars_per_sf |

Status at ingest: `proposed`.

## 2. Validation

- Lumber row: plausible-band check on `value` against prior. Change magnitude triggers the "implausible jump" warning (|delta| > 10% MoM).
- LVP row: same check. LVP delta is -9% vs prior (within band; passes auto-approval magnitude check).

Both rows pass schema validation.

## 3. Normalization

Write to:

```
reference/normalized/material_costs__southeast_residential.csv
```

Lumber row carries `prior_reference_id: mc-se-lumber-2x4x8`. LVP row carries `prior_reference_id: mc-se-lvp-6mm-mm`. Both set `notes` explaining the driver (commodity index spike, vendor rebase).

## 4. Approval

- Lumber row (`+11.2%` delta) triggers an `approval_request` with `policy_owner_role: asset_manager`. The record sits in `status: proposed` until approved.
- LVP row (`-9%` delta) is within auto-approval band and moves to `status: approved`.

## 5. Change Log Entries

Approved LVP entry:

```yaml
change_log_id: chg_2026_04_10_0002
change_type: update
target_kind: reference_record
target_ref: reference/normalized/material_costs__southeast_residential.csv#mc-se-lvp-6mm-mm
old_value:
  value: 3.35
  as_of_date: 2026-02-28
new_value:
  value: 3.05
  as_of_date: 2026-04-10
source_name: "Primary distributor Q2 2026 rebase notice (illustrative)"
source_type: internal_record
source_date: 2026-04-10
as_of_date: 2026-04-10
proposed_by: agent:material_cost_agent
approved_by: human:mu_owner
proposed_at: 2026-04-10T09:00:00Z
approved_at: 2026-04-10T09:45:00Z
confidence: high
reason_for_change: |
  Primary LVP distributor rebased 6mm plank pricing following annual contract renegotiation
  effective 2026-04-01. Change captured at property-level turn-cost and unit-interior capex
  line-item derivations.
affected_skills:
  - workflows/unit_turn_make_ready
  - workflows/capex_prioritization
  - roles/construction_manager
affected_overlays:
  - segments/middle_market
```

Lumber entry (pending approval) stays in `proposed` until a human or an authorized agent approves:

```yaml
change_log_id: chg_2026_04_12_0003
change_type: update
target_kind: reference_record
target_ref: reference/normalized/material_costs__southeast_residential.csv#mc-se-lumber-2x4x8
old_value:
  value: 4.25
new_value:
  value: 4.85
source_name: "Commodity index aggregate spike alert (illustrative)"
source_type: commodity_index
source_date: 2026-04-10
as_of_date: 2026-04-10
proposed_by: agent:material_cost_agent
approved_by: null
proposed_at: 2026-04-12T10:00:00Z
approved_at: null
confidence: medium
reason_for_change: |
  SPF 2x4 lumber index up +14% MoM. Beyond auto-approval band. Routed to asset_manager
  approval because dev pro forma hard_cost lines will shift. Awaiting approval.
affected_skills:
  - workflows/dev_proforma
  - workflows/capex_prioritization
  - roles/development_manager
  - roles/construction_manager
```

Both entries append to `reference/archives/change_log.jsonl` and `reference/archives/material_cost/CHANGELOG.md`.

## 6. Derived Recomputation

When the LVP change lands in `approved`, `reference/normalized/unit_turn_cost_library__middle_market.csv` rows with `included_scope_items` containing `lvp_replace_unit` are flagged for recompute. The `turn_cost_derivation_agent` re-prices:

- `utc-se-mm-garden-classic-a1` (contains `lvp_replace_unit`)
- `utc-se-mm-garden-premium-a1`
- `utc-se-mm-garden-classic-b1`
- `utc-se-mm-garden-premium-b1`
- `utc-w-mm-garden-classic-a1`

Similarly, `reference/normalized/capex_line_items__middle_market_value_add.csv` rows that reference `lvp_flooring_6mm` (e.g., `capex-se-mm-garden-unitfloor-lvp`) are flagged.

Each derived change produces its own `change_log_entry` with `change_type: update` and a `derived_from` note naming the upstream change_log_id.

The lumber update is **not** propagated to derived layers until the underlying material_cost row transitions to `status: approved`. The tailoring skill surfaces a pending-approval banner on dev pro forma skills in the meantime.

## 7. Skill Notification

Packs logged as affected by the (eventually approved) lumber update:

- `workflows/dev_proforma` (reads dev budget assumptions built off lumber)
- `roles/development_manager`
- `roles/construction_manager`

Packs logged as affected by the LVP update:

- `workflows/unit_turn_make_ready`
- `workflows/capex_prioritization`

## 8. Archival

Prior rows moved to `reference/archives/material_cost/2026/02/` with `status: deprecated`.

## Confidence banner the skill surfaces

```
References: material_costs__southeast_residential.csv@2026-04-10 (lvp_flooring_6mm updated, approved; lumber_2x4x8_spf pending approval - banner suppressed in pro forma outputs).
```
