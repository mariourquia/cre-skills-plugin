# Boundary Rules

Authoritative answer to the question "what lives where". Enforced mechanically by
`tests/test_boundary_rules.py`. Any PR that leaks content across a boundary is rejected.

The residential multifamily subsystem is organized so that conventional market-positioning,
regulated affordable-housing compliance, and operator-specific policy never cross-contaminate.
This document is the contract.

## Composition order

Overlays compose in this order. Later overlays override earlier ones on the same
`target_ref`. Overlays never redefine canonical metrics; they override target bands
and thresholds.

```
canonical core  (_core/)
   │
   ├── segment overlay        (overlays/segments/{middle_market | luxury})
   │
   ├── regulatory overlay     (overlays/regulatory/affordable/, loaded only when
   │                           regulatory_program != none)
   │                           + program overlay
   │                           (overlays/regulatory/affordable/programs/{program})
   │
   ├── form_factor overlay    (overlays/form_factor/{garden | walk_up | wrap |
   │                           suburban_mid_rise | urban_mid_rise | high_rise})
   │
   ├── lifecycle overlay      (overlays/lifecycle/{development | construction |
   │                           lease_up | stabilized | renovation | recap_support})
   │
   ├── management_mode overlay (overlays/management_mode/{self_managed |
   │                             third_party_managed | owner_oversight})
   │
   ├── market overlay         (overlays/market/ — placeholder; not populated yet)
   │
   └── org overlay            (overlays/org/{org_id}/ — populated by tailoring)
```

## Layer rules

### conventional middle-market core (`_core/`)

MAY CONTAIN:

- Canonical ontology (property, unit, lease, resident, work order, approval request,
  vendor, change order, capex project, etc.).
- Canonical metric contracts with full numerator / denominator / filters / rollup.
- Canonical taxonomy and routing (axes, rules, priority, defaults).
- Canonical approval floor and guardrails (fair housing, safety, legal review).
- Alias registry.
- Naming conventions, design rules, change-log conventions.
- Schemas (metric_contract, skill_manifest, overlay_manifest, reference_manifest,
  reference_record, approval_request, change_log_entry).

MUST NOT CONTAIN:

- Market-positioning posture (luxury hospitality tone, middle-market value posture).
- Regulated-program compliance content (LIHTC, HUD Section 8, REAC / NSPIRE, TRACS,
  HAP contract, voucher eligibility, AMI band, rent limit, income limit,
  utility allowance schedule, extended use covenant, 8609).
- Org-specific thresholds, approver names, reporting preferences, vendor lists.
- Numeric dollar thresholds or percentages in prose.
- Hardcoded market or submarket names in prose.

### middle-market segment overlay (`overlays/segments/middle_market/`)

MAY CONTAIN:

- Target bands for canonical metrics (occupancy, delinquency, trade-out, turnover,
  controllable opex, renewal offer rate) expressed as overrides referencing
  `reference/derived/role_kpi_targets.csv` rows.
- Concession policy posture (close market gaps before discounting; cap months free).
- Finish standards (classic, value-add; refer to `reference/` for dollar costs).
- Renewal strategy posture.
- Reporting emphasis (which metrics matter most in middle-market reporting).
- Resident communication tone (plain, respectful, friendly).
- Screening policy posture.
- Service standards (lead-response time targets, work-order SLA posture).
- Staffing posture.

MUST NOT CONTAIN:

- LIHTC, HUD, voucher, AMI, rent-limit, income-limit, utility-allowance,
  recertification, REAC / NSPIRE, TRACS, 8609, extended-use-covenant content. These
  belong in the regulatory overlay family.
- Luxury brand-standard posture.
- Org-specific thresholds or approver names.

### affordable overlay family (`overlays/regulatory/affordable/`)

MAY CONTAIN:

- Eligibility and certification posture.
- Income limit, rent limit, utility allowance structural definitions and schedule
  references (schedules themselves live in `reference/normalized/`).
- Recertification cadence and documentation posture.
- Compliance calendar event types.
- Agency reporting event types (submission cadences, dependent inputs).
- File audit preparedness structure.
- Escalation sensitivity flags (REAC / NSPIRE, noncompliance notice, recapture,
  VAWA, qualified contract).
- Program-specific sub-overlays under `programs/{program}/` for LIHTC, HUD Section 8,
  HUD 202/811, USDA RD, state programs, mixed-income.

MUST NOT CONTAIN:

- Market-positioning posture (middle-market vs luxury).
- Conventional concession benchmarks, renewal strategy posture, finish standards.
- Org-specific policy (those live in `overlays/org/{org_id}/`).
- Market-rent benchmarks (those live in `reference/normalized/` under non-regulatory
  categories).

Programs under `programs/{program}/` additionally MAY NOT:

- Redefine a canonical metric. They may add program-specific metrics (e.g.
  `rent_limit_compliance_rate`, `income_certification_timeliness`).
- Override posture that lives in a different family (e.g. change a concession
  policy set by the segment overlay — that target is out of scope for regulatory).

### luxury segment overlay (`overlays/segments/luxury/`)

MAY CONTAIN:

- Brand-standard posture.
- Hospitality / concierge tone.
- Compressed lead-response SLAs.
- Amenity-density posture.
- Finish-standard posture (premium).
- Vendor-mix posture (premium finishes, event programming).

MUST NOT CONTAIN:

- Regulatory program content.
- Middle-market value posture.

### market overlays (`overlays/market/`)

Placeholder family. When populated, MAY CONTAIN:

- Market-specific adjustments that cross market-rent benchmarks (e.g. a submarket
  with persistent concession pressure).
- Market-specific approval bias (a market with higher vacancy tolerance).

MUST NOT CONTAIN:

- Regulatory program content (that axis is regulatory_program, not market).
- Segment posture (that is segment, not market).

### org overlays (`overlays/org/{org_id}/`)

MAY CONTAIN:

- Operator-specific thresholds (approval matrix tier values, concession ceilings,
  vendor award thresholds).
- Named approver roles (who at this org signs a concession over policy).
- Reporting preferences (cadences, distribution list, format).
- Vendor lists and preferred partners.
- Jurisdiction scope (states and metros the operator is in — affects which
  regulatory overlays are candidates).
- Reviewed-and-endorsed posture decisions derived from the tailoring interview.

MUST NOT CONTAIN:

- Canonical metric redefinitions.
- Program rule overrides that would loosen regulatory compliance below statute.
- Any override that would drop an approval floor below the canonical minimum.

## What tailoring may write

The tailoring skill under `tailoring/` may write to:

- `tailoring/sessions/{org_id}/` (per-session state, ignored by git by default).
- `tailoring/missing_docs_queue.yaml` (committed — a queue of operator-requested docs).
- `tailoring/sign_off_queue.yaml` (committed — a queue of proposed org overlay changes).
- `overlays/org/{org_id}/overlay.yaml` and related files (ONLY after an approved
  sign-off queue entry is applied by an external commit tool; tailoring stops at the
  sign-off queue).

Tailoring MUST NOT write to:

- `_core/` (any path).
- `overlays/segments/` (any path).
- `overlays/regulatory/` (any path).
- `reference/raw/`, `reference/normalized/`, `reference/derived/` (any path).
- `reference/connectors/` (any path — connector content is authored, not
  interview-derived).

Enforced by `tests/test_tailoring_canonical_immutability.py`.

## Summary heuristic

If you are writing content about **how this property competes in the rental market**, it
belongs under `overlays/segments/`.

If you are writing content about **program rules the property must satisfy to remain
compliant with a regulator**, it belongs under `overlays/regulatory/`.

If you are writing content about **what this specific operator has decided is their
policy**, it belongs under `overlays/org/{org_id}/`.

If you are writing a **metric**, an **object**, a **routing rule**, or a **schema**,
it belongs under `_core/`.

If you are writing a **CSV of actual numbers**, it belongs under `reference/`.

If you are writing a **specification for how we pull numbers out of an external
system**, it belongs under `reference/connectors/`.
