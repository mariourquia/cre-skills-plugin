# Update Flow Walk-Through — `unit_turn_cost` (Vendor Bid → Updated Turn Cost)

Scenario: Queen City Painters, the Charlotte region's primary turn-paint vendor, submits a refreshed bid card on 2026-04-08 lowering the `paint_full_unit` line from $785/unit to $725/unit. The inbound vendor bid triggers both a `vendor_rate` record and a downstream `unit_turn_cost` derivation.

## 1. Inbound

Vendor rate sheet lands:

```
reference/raw/vendor_rate/2026/04/queencitypainters_bid__2026-04-08.csv
```

| source_row_id | market | vendor_name | service_slug | service_category | price_amount | unit |
|---------------|--------|-------------|--------------|------------------|-------------|------|
| VR-2026Q2-CLT-QCPAINT-FULL | Charlotte | Queen City Painters (illustrative vendor) | paint_full_unit | turn_paint | 725 | dollars_per_unit |

Contract term: 12 months. Effective 2026-05-01.

Status at ingest: `proposed`.

## 2. Validation

- Row passes schema validation against `reference/normalized/schemas/vendor_rate.yaml`.
- Delta vs prior Queen City Painters rate is -7.6%, within plausible-band auto-approval.
- Concurrent-quotes check: at least one alternate bid on file? A quick search confirms a second painter bid is in the archive with a 5-way spread. Record passes triangulation check.

## 3. Normalization

Write the new `vendor_rate` row to:

```
reference/normalized/vendor_rates__charlotte_mf.csv
```

With `prior_reference_id: vr-charlotte-painters-union-paint-full` (superseding).

## 4. Approval

Within auto-approval band for a vendor rate (vendor rate card changes under 10% with an effective_start < 60 days out are auto-approvable for the `contract_award` gate below the `threshold_contract_award` threshold). Row moves to `status: approved`.

## 5. Change Log Entry

Primary vendor_rate update:

```yaml
change_log_id: chg_2026_04_08_0001
change_type: update
target_kind: reference_record
target_ref: reference/normalized/vendor_rates__charlotte_mf.csv#vr-charlotte-painters-union-paint-full
old_value:
  value: 785
  as_of_date: 2026-02-28
new_value:
  value: 725
  as_of_date: 2026-04-08
source_name: "Queen City Painters 2026-Q2 bid card (illustrative)"
source_type: vendor_bid
source_date: 2026-04-08
as_of_date: 2026-04-08
effective_start: 2026-05-01
proposed_by: agent:vendor_rate_agent
approved_by: human:mu_owner
proposed_at: 2026-04-08T12:00:00Z
approved_at: 2026-04-08T13:15:00Z
confidence: verified
reason_for_change: |
  Queen City Painters Q2 bid card: paint_full_unit rate drops from $785/unit to $725/unit
  effective 2026-05-01. Incumbent vendor re-bid for volume.
affected_skills:
  - workflows/unit_turn_make_ready
  - workflows/capex_prioritization
  - roles/property_manager
  - roles/maintenance_supervisor
affected_overlays:
  - segments/middle_market
```

## 6. Derived Recomputation

The `turn_cost_derivation_agent` re-prices each `unit_turn_cost` row whose `included_scope_items` contains `paint_full_unit`:

- `utc-se-mm-garden-standard-a1` (standard turn: paint included, contains `paint_full_unit`)
- `utc-se-mm-garden-heavy-a1`
- `utc-se-mm-garden-classic-a1`
- `utc-se-mm-garden-premium-a1`
- Same for B1 variants.

For each, subtract the old line amount and add the new (`785 -> 725`, delta -60 per unit). Write a new row to:

```
reference/normalized/unit_turn_cost_library__middle_market.csv
```

with `prior_reference_id` pointing to the superseded row. The five rows become 10 change_log entries (old deprecated + new added), OR the existing rows are updated in place with a single `change_log_entry` per row of `change_type: update`.

Derived update example:

```yaml
change_log_id: chg_2026_04_08_0002
change_type: update
target_kind: reference_record
target_ref: reference/normalized/unit_turn_cost_library__middle_market.csv#utc-se-mm-garden-standard-a1
old_value:
  value: 1285
new_value:
  value: 1225
source_name: "Derived from vendor_rate chg_2026_04_08_0001"
source_type: internal_record
source_date: 2026-04-08
as_of_date: 2026-04-08
proposed_by: agent:turn_cost_derivation_agent
approved_by: human:mu_owner
proposed_at: 2026-04-08T13:30:00Z
approved_at: 2026-04-08T13:45:00Z
confidence: verified
reason_for_change: |
  Derived recomputation. paint_full_unit line dropped from $785 to $725 (chg_2026_04_08_0001).
  Standard turn A1 cost drops by $60.
affected_skills:
  - workflows/unit_turn_make_ready
  - workflows/capex_prioritization
  - roles/property_manager
  - roles/maintenance_supervisor
```

## 7. Skill Notification

Packs whose `reference_manifest.yaml` lists the turn-cost library are logged as affected:

- `workflows/unit_turn_make_ready`
- `workflows/capex_prioritization`
- `roles/property_manager`
- `roles/maintenance_supervisor`

The skill layer surfaces a "turn cost library refreshed 2026-04-08" banner on subsequent turn-projection outputs.

## 8. Archival

Prior `vr-charlotte-painters-union-paint-full` row copy moved to `reference/archives/vendor_rate/2026/02/` with `status: deprecated`.

## Confidence banner the skill surfaces

```
References: vendor_rates__charlotte_mf.csv@2026-04-08 (verified: Queen City Painters 2026-Q2 bid, -7.6% on paint_full_unit), unit_turn_cost_library__middle_market.csv@2026-04-08 (verified: derived recomputation).
```
