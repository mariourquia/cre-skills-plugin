# Update Flow Walk-Through — `concession_benchmark` (Market Survey → New Benchmark)

Scenario: the regional manager circulates a Charlotte market shop survey conducted 2026-03-28 to 2026-04-02 covering 24 comp properties in the South End, Uptown, and Ballantyne submarkets. The survey shows Uptown stabilized concessions jumping from 1.0 months to 1.5 months on a 12-month lease as a new lease-up ramp crowds pricing.

## 1. Inbound

Raw survey file lands:

```
reference/raw/concession_benchmark/2026/04/regional_shop_survey__2026-04-02.csv
```

| source_row_id | market | submarket | lifecycle_stage | lease_term_months | concession_months_offered | pct_comps_offering | avg_concession_dollars |
|---------------|--------|-----------|-----------------|-------------------|---------------------------|--------------------|------------------------|
| RS-2026Q2-CLT-UPT-STAB | Charlotte | Uptown | stabilized | 12 | 1.5 | 0.82 | 2775 |
| RS-2026Q2-CLT-SOU-STAB | Charlotte | South End | stabilized | 12 | 0.75 | 0.55 | 1125 |

Status at ingest: `proposed`, confidence `medium` (regional survey; not a vendor aggregate).

## 2. Validation

- Schema check: Uptown row's `concession_months_offered = 1.5` is within plausible band (0-3 months for stabilized) but the Uptown delta from 1.0 to 1.5 months is +50% - triggers the implausible-jump warning threshold.
- The row is routed to the approval queue automatically; the human approver (in this walk-through, `regional_manager`) has context from the shop survey itself.

## 3. Normalization

New row written to:

```
reference/normalized/concession_benchmarks__charlotte_mf.csv
```

With `prior_reference_id: cb-charlotte-uptown-mm-urbanmidrise-stabilized-20260331`.

South End row passes auto-approval (delta small); lands immediately.

## 4. Approval

Uptown row: `approval_request` opened with `policy_owner_role: regional_manager`. Request body summarizes:

- 24 comps surveyed
- 20 offering concessions (82%)
- median 1.5 months off on a 12-month lease
- shop survey window: 2026-03-28 to 2026-04-02
- context: new ~285-unit mid-rise delivered in Uptown Q1 2026 pushing effective rents down

Regional manager approves. Row transitions to `status: approved`, `approved_by: human:regional_manager`.

## 5. Change Log Entry

```yaml
change_log_id: chg_2026_04_02_0001
change_type: update
target_kind: reference_record
target_ref: reference/normalized/concession_benchmarks__charlotte_mf.csv#cb-charlotte-uptown-mm-urbanmidrise-stabilized-20260331
old_value:
  concession_months_offered: 1.0
  pct_comps_offering: 0.65
  avg_concession_dollars: 1850
new_value:
  concession_months_offered: 1.5
  pct_comps_offering: 0.82
  avg_concession_dollars: 2775
source_name: "Regional shop survey 2026-03-28 to 2026-04-02 (illustrative)"
source_type: local_survey
source_date: 2026-04-02
as_of_date: 2026-04-02
proposed_by: agent:concession_survey_agent
approved_by: human:regional_manager
proposed_at: 2026-04-02T17:00:00Z
approved_at: 2026-04-03T10:30:00Z
confidence: medium
reason_for_change: |
  Regional shop survey indicates Uptown Charlotte stabilized concessions widened from
  ~1.0 months to ~1.5 months on a 12-month lease following delivery of a new ~285-unit
  mid-rise and a concurrent easing of absorption. 24 comps surveyed, 20 offering concessions.
affected_skills:
  - roles/property_manager
  - roles/leasing_manager
  - roles/asset_manager
  - workflows/lead_to_lease_funnel_review
  - workflows/renewal_retention
  - workflows/rent_optimization
affected_overlays:
  - segments/middle_market
```

## 6. Derived Recomputation

No automatic derived recomputation is wired for concession benchmarks today (the peer_median is read directly by role_kpi_targets). However, a soft signal is emitted to:

- `roles/leasing_manager` — suggests revisiting `concession_policy_max` effective rate given widening comp-set concessions.
- `workflows/rent_optimization` — flags Uptown-located properties with a stale market-to-lease gap assumption.

Neither triggers an automatic change to the derived file; both trigger a queued review for the human owner.

## 7. Skill Notification

Packs logged as affected:

- `roles/property_manager`
- `roles/leasing_manager`
- `roles/asset_manager`
- `workflows/lead_to_lease_funnel_review`
- `workflows/renewal_retention`
- `workflows/rent_optimization`

Outputs produced by these packs after 2026-04-03 surface the concession freshness banner.

## 8. Archival

Prior Uptown row copied to `reference/archives/concession_benchmark/2026/03/concession_benchmarks__charlotte_mf__2026-03-31.csv` with `status: deprecated`.

## Confidence banner the skill surfaces

```
References: concession_benchmarks__charlotte_mf.csv@2026-04-02 (medium confidence, regional shop survey; Uptown stabilized concessions widened +50% MoM).
```
