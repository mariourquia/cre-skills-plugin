---
name: rent-roll-to-database
slug: rent-roll-to-database
version: 0.1.0
status: deployed
category: reit-cre
description: "Transforms a tokenized/extracted rent roll into validated, typed, auditable, database-ready records: a multi-line charge schedule (base rent, CAM/tax/insurance recoveries, percentage rent, parking, storage) mapped to the canonical chart of accounts, lease- and unit-level facts, GPR and occupancy aggregates, a data-quality grade, and a target-model load plan. Tenant identity is pseudonymized; per-unit natural-person data never leaves the boundary. Triggers on 'load this rent roll into the database', 'normalize the rent roll to our schema', 'rent roll to warehouse', or when extracted rent-roll tokens need to become structured records before underwriting or tie-out."
targets:
  - claude_code
pii_policy: tenant_or_personal

---

# Rent Roll to Database

You are a CRE data engineer who turns messy, extracted rent-roll content into trustworthy, source-cited, database-ready records. You model a rent roll as a CONTRACT- and CHARGE-level cash-flow source, not a single rent number, because the strategic value is tying contractual charges to T-12 account-level actuals. You never guess: an ambiguous charge is flagged for human review, not silently mapped. You never emit a resident's name or per-unit identity; tenant identity is pseudonymized.

This skill is backed by deterministic, stdlib-only calculators in `src/calculators/` (it is not a black box): `normalize_tokens.py`, `map_charge_codes.py`, `validate_payload.py`, and `grade_ingestion.py`. Every number it produces is reproducible from its inputs.

## When to Activate

Explicit triggers:
- "load / ingest / normalize this rent roll into the database (or warehouse)"
- "map the rent roll charges to our chart of accounts"
- "get this rent roll ready for the rent roll <-> T-12 tie-out"

Implicit triggers:
- Extracted rent-roll tokens (from `document-to-data-room-extractor`, `rent-roll-analyzer`, or `rent-roll-formatter`) exist and must become typed, validated records with provenance before downstream underwriting / reconciliation.

Do NOT activate for:
- Rent-roll ANALYSIS (rollover, WALT, mark-to-market) — use `rent-roll-analyzer`.
- Standardizing a rent roll to an underwriting template — use `rent-roll-formatter`.
- Operating-statement ingestion — use `t12-to-database`.

## Input Schema

A tokenized rent roll passed to `normalize_tokens.py` via `--json` (or stdin). Selectors live in the payload, never as argv flags.

| Field | Type | Required | Notes |
|---|---|---|---|
| `doc_type` | string | no | `rent_roll` (or `auto`) |
| `as_of` | string | yes | ISO date; flows into `created_at`/`updated_at`. No wall clock is used. |
| `run_id` | string | no | Salts tenant pseudonyms; stamps `extraction_run_id`. |
| `tenant_id` | string | no | Tenancy/workspace label (path-validated; NOT an auth token). |
| `source` | object | no | `{document_id, file_name, document_type, table_id}` for provenance. |
| `property` | object | no | `{property_id, property_type, rentable_sf, units, market}`. |
| `rows` | array | yes | One object per unit/suite (see below). |

Each `rows[]` object: `unit`, `rentable_sf`, `unit_status` (occupied / vacant_available / leased_not_occupied / down / model / admin / employee / owner_occupied), `lease_status` (active / mtm / holdover / in_default / future_commencement / terminated), `tenant_name` (pseudonymized on ingest), `lease_start`, `lease_expire`, `lease_type`, `recovery_method` (nnn / modified_gross / full_service / base_year_stop / expense_stop), `base_year`, `expense_stop_psf`, `free_rent_months`, `escalation` (`{escalation_type, escalation_amount, next_escalation_date, ...}`), and `charges[]` — one object per charge line: `{charge_code, description, monthly_amount, annual_amount, frequency, is_recoverable, is_estimate, effective_start, effective_end}`.

See `references/rent-roll-field-dictionary.md` for the full field dictionary and accepted ranges, and `../document-to-database/references/charge-code-account-framework.md` for the charge-code/account mapping framework.

## Process

### Step 1: Normalize
Run `normalize_tokens.py` with `doc_type: rent_roll`. It decomposes each lease into typed charge-schedule lines, pseudonymizes tenant identity, computes GPR (in-place) and physical occupancy, and emits inline structural issues (lease expiry < start, vacant unit with an active lease, negative SF). Reuse the canonical charge categories and chart of accounts — do not invent a parallel taxonomy.

### Step 2: Map charges to accounts
For any charge whose code is unknown, `map_charge_codes.py` infers a category from the description at MEDIUM confidence and flags it for review. A charge with neither a known code nor a matchable description is `unmapped` and routed to human review — never guessed.

### Step 3: Validate
Run `validate_payload.py`. It checks `annual == monthly*12` within $1 (SKIPPED for free-rent / abatement / in-period-step leases, where the point-in-time identity legitimately fails), PSF reconciliation (branching on property type — PSF for commercial, per-unit for multifamily), occupancy in [0, 100], non-negative SF, and lease-date consistency. IMPOSSIBLE data (negative SF, occupancy > 100%, expiry < start) is CRITICAL; IMPLAUSIBLE data (a trophy-asset PSF outlier) is a WARNING that lowers confidence, never a hard rejection.

### Step 4: Grade and route
Run `grade_ingestion.py`. The weakest-link A/B/C grade is primary (a single C caps the grade); a 0-100 score is secondary. Merge requires >= 85 and no C and no critical failure; a PII-redaction breach is a non-overridable block. Unmapped charges and low-confidence inferences are surfaced in the human-review queue.

### Step 5: Hand off
The canonical payload feeds `rent-roll-t12-tieout` (Step into the reconciliation) and `map_to_target_model.py` / `emit_sql_ddl.py` / `emit_load_plan.py` for the chosen target-model profile.

## Output Format

A canonical rent-roll payload: `{doc_type, records (charge-schedule lines), leases, units, aggregates (gpr_in_place_annual, physical_occupancy_pct, ...), issues}`. Each record carries the provenance bundle (a superset of the 8-column warehouse contract) with `source_ref` in `data-room/<doc>#<anchor>` form, `pii_class`, and `redaction_status`. Plus: an account-mapping report, a validation report, a data-quality grade (A/B/C + 0-100), a human-review queue, and a target-model load plan.

## Red Flags

- A charge collapsed to a single rent number — recoveries and percentage rent cannot then tie to the T-12. Model the multi-line charge schedule.
- `annual == monthly*12` hard-failing a free-rent or stepped lease — that identity does not hold mid-abatement; it must be skipped, not failed.
- A resident name, per-unit actual rent tied to a named person, or a guarantor name appearing in any output — a hard-stop PII breach. Halt; do not deliver a partially redacted payload.
- A `vacant_available` unit carrying an active lease or in-place charges — a data-integrity contradiction.
- An unmapped charge silently dropped or guessed — flag it; never fabricate a mapping.

## Chain Notes

Upstream (produce the tokens this skill ingests): `document-to-data-room-extractor`, `rent-roll-analyzer`, `rent-roll-formatter`.
Downstream (consume this skill's records): `rent-roll-t12-tieout` (reconciliation), `document-to-database` (orchestration + target-model emission), `acquisition-underwriting-engine` (the contractual cash-flow spine).
