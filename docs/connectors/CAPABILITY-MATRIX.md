# Connector Capability Matrix (Honest)

> Status: released (v5.1.0)
> Owner: Mario Urquia
> Last reviewed: 2026-06-04
> Source-of-truth this doc describes:
> - `src/skills/residential_multifamily/reference/connectors/` (canonical connector contracts + adapters — **every one is `status: stub`**)
> - `src/skills/residential_multifamily/reference/connectors/source_registry/source_registry.yaml` (per-source `status: stubbed | planned | active`)
> - `src/skills/residential_multifamily/reference/connectors/adapters/adapter_lifecycle.md` (the `stub → starter → production → deprecated` lifecycle)
> - `docs/plans/v5-analysis/03-data-connector.md` (the full v5 connector analysis this matrix summarizes)
> - `src/calculators/ingest/` (the document → database ingestion family — the offline, ZDR layer)

This is the **honest** connector capability matrix. Its job is to prevent any
reader from believing the plugin has a live integration it does not. **No live
adapter exists today.** Every connector contract and every vendor adapter in the
repo is `status: stub`. The only ingestion shape that is `active` is a
shared-drive / email **file drop** (Excel / manual upload) — not a live API feed.

## 1. Capability states (vocabulary)

| State | Meaning |
|-------|---------|
| **implemented** | Live adapter, operator-validated, reconciliation green ≥1 cadence (adapter `status: production`). **Count today: 0.** |
| **scaffolded** | Vendor-family adapter dir + manifest + canonical contract exist (adapter `status: stub` or `starter`). The vendor is reachable in principle; no live feed runs. **This is where almost everything sits.** |
| **planned** | Named in the roadmap / `source_registry.yaml`, no adapter dir yet. |
| **blocked-by-vendor** | Cannot reach `starter`/`production` without a paid/approved vendor program, a non-public sandbox, OR vendor terms that prohibit it. (Splits below into *sandbox-blocked*, *license-blocked*.) |
| **not-supported-live** | Vendor terms make any live connector contractually impossible; only an operator-licensed file overlay is allowed. |

The plugin's egress posture is deliberate: the ingestion family is **stdlib-only,
no-network, no-wall-clock, stateless, fail-closed** (`grep` finds zero
`requests`/`httpx`/`urllib`/`socket` imports in `src/calculators` and
`src/orchestrators/engine`). The warehouse-sink path **emits** reviewable
`CREATE TABLE` DDL + an FK-ordered load plan; it does **not** execute DML or open
a connection. Keeping it that way is correct and intended.

## 2. Per-vendor matrix (reflects the REAL repo state)

| Vendor / system | Domain | Repo artifact today | State | Why (the honest reason) |
|---|---|---|---|---|
| **Yardi (Voyager)** | pms / gl | `adapters/yardi_multi_role` (`stub`, wave_2) | **blocked-by-vendor** (sandbox) | SIPP interface partnership requires an established firm, multiple active Voyager clients, a paid per-interface annual fee, and a Data Exchange Agreement; **no public dev portal**; sandbox is post-approval only. |
| **AppFolio** | pms | `adapters/appfolio_pms` (`stub`, wave_4) | **blocked-by-vendor** (sandbox, lighter) | Stack partner program; sandbox + sample data provided **only after approval into the partner program** — not self-serve. |
| **MRI** | pms / gl | none (roadmap "blocked on vendor sandbox") | **planned** / blocked-by-vendor (sandbox) | Enterprise-only; no public self-serve API or sandbox. Treat as a stub; do not promise live. |
| **RealPage** | pms | registry `west_region_pms = realpage_family` (sftp, `stubbed`) | **blocked-by-vendor** (sandbox) | No public dev portal; enterprise contract + SFTP export. Realistic shape is a **file-drop** adapter, not a live API. |
| **Argus Enterprise** | valuation / dcf | roadmap "import/export"; no adapter dir | **planned** (file-overlay reframe) | **No public live API.** The realistic path is an exported report package (Excel) / `.gsf` file ingest — a file overlay, not a connector. The roadmap's "import/export API" framing is being corrected to file-overlay. |
| **CoStar / CommercialEdge** | market_data | `adapters/excel_market_surveys` (`stub`); registry `costar_family` (`stubbed`) | **not-supported-live** | CoStar terms **explicitly prohibit exposing CoStar Information to open AI tools** and to competing platforms; the API is contract-restricted. A live ingest is contractually impossible. Only an **operator-licensed manual file overlay** onto `reference/normalized/*_comps__*.csv` is allowed. |
| **Procore** | construction | `adapters/procore_construction` (`stub`, wave_4) | **scaffolded** (least-gated; buildable) | **Public dev portal + free self-serve sandbox with seed data, OAuth2.** Procore can legitimately advance `stub → starter` on sanitized data without vendor gating — the priority adapter when connector work resumes. Still `stub` today. |
| **Sage Intacct** | gl | `adapters/sage_intacct_gl` (`stub`, wave_4) | **blocked-by-vendor** (license) | Public REST + OAuth2 docs, but requires a **paid Web Services developer license** (sender ID); no free sandbox. Reachable for a funded customer, not self-serve. |
| **Snowflake / Databricks / Fabric** | warehouse sink | `profiles.py` emits target-warehouse DDL + load plan; no live loader | **scaffolded** (egress only) | The plugin emits a reviewable `CREATE TABLE` DDL + FK-ordered load plan; it does **not** execute DML or connect. This is a generated artifact, not a live writer — and intentionally so. |
| **SharePoint / OneDrive** | manual_uploads | `adapters/manual_*`; registry shared-drive sources `active` | **scaffolded** (file-drop; the one active path) | The only `active` ingestion shape is a shared-drive / email **file drop**. SharePoint / OneDrive is a file-drop *source variant*; no live Microsoft Graph API connector exists or is implied. |
| **Document intelligence** (OCR / extraction) | documents | ingest family + `document-to-data-room-extractor` upstream; PII boundary in `pii.py` | **scaffolded** (pluggable; no backbone bound) | Roadmap notes optional Tesseract / Textract / local-vision. **No OCR backbone is bound today;** ingestion consumes already-extracted tokens. The extractor stays pluggable and offline-capable; no cloud OCR is hard-bound. |

### Matrix takeaway

Of the 11 vendor/system rows: **0 are implemented**, **1 is genuinely buildable
without a vendor gate (Procore)**, **1 is buildable for a funded customer (Sage
Intacct)**, **1 is contractually not-supported live (CoStar)**, and the rest are
vendor-sandbox-blocked or file-drop only. The v5 "real-world data integration"
theme is therefore **re-scoped** from "build connectors" to: (a) close the
contract gaps, (b) ship the refusal / source-class layer, (c) advance Procore +
manual/Excel + document-intelligence to `starter` on sanitized real data, and (d)
reframe Argus / CoStar from live-API to file-overlay / not-supported-live.

## 3. Canonical contract schemas — version note

The plugin already has **vendor-neutral canonical connector contracts** for nine
domains under
`src/skills/residential_multifamily/reference/connectors/` (`pms, gl, crm, ap,
market_data, construction, hr_payroll, manual_uploads, deal_pipeline`), each with
a `manifest.yaml`, `schema.yaml`, `mapping.yaml`, `field_mapping.yaml`,
`dq_rules.yaml`, and `reconciliation_checks.yaml`. These are the **v5.1.0** stubs
(`status: stub`, v0.1.0).

The **four canonical contract schemas the v5 connector analysis calls for —
`debt`, `entity`, `valuation`, and the promotion of `funds` (with investor
reporting) into a connector entity contract — were authored in v5.1.0 as
vendor-neutral STUBS** (`status: stub`). They conform to
`connector_manifest.schema.yaml` + `entity_contract.schema.yaml`, declare
`vendor_neutral: true`, carry the 6-field raw-landing provenance + the
`source_class` field + `max_staleness`, declare `null_handling` per required
field, and ship `dq_rules.yaml` + `reconciliation_checks.yaml` with
round-tripping `sample_input.json` / `sample_normalized.json` payloads
(`tests/test_connector_contracts.py` validates all of this). The `entity`
contract is scoped to legal/ownership cap-structure and is explicitly distinct
from the operational `master_data` connector. **They are schema/contract only —
no adapter exists, nothing is live, and the connector runtime that emits/enforces
`source_class` + `max_staleness` at consume time remains deferred.**

The connector **`source_class`** field
(`connector_live | document_extracted | operator_supplied | connector_sample |
reference_illustrative | modeled_assumption`) is now a **schema-enforced enum**:
the canonical list lives in
`reference/connectors/_schema/source_class.yaml`, is wired into
`entity_contract.schema.yaml`, and is checked by
`tests/test_connector_source_class.py`. The `max_staleness` consume-time refusal
is **declared** on the new contracts but the connector *runtime* that emits and
enforces it at consume time is still **deferred** (see ROADMAP). No live adapter
emits `connector_live` today; **0 connectors are implemented/live.**

## 4. What this means for skills (v5.1.0)

- No skill gains a "connect to Yardi / AppFolio / CoStar" affordance in v5.1.0.
- Skills consume the **canonical normalized shape** (the connector `schema.yaml`
  entities / the ingest cash-flow spine), never a vendor-native payload, and never
  assume the source is live.
- A skill consuming any `connector_sample`-class input inherits the `PREVIEW /
  STAGING` banner (`docs/PREVIEW_MODE.md`); a final-marked path refuses
  sample-class data without a human acknowledgement (`docs/DATA_GRADES.md` §3).
- Comps sourced from a licensed provider (e.g. CoStar) are the operator's
  **licensed file overlay** (`operator_supplied`), never represented as a live
  plugin feed — `comp-snapshot` and the market skills enforce this in their
  Refusal Behavior.

This matrix, `docs/DATA_GRADES.md`, and `docs/plans/v5-analysis/03-data-connector.md`
together are the honest, single source of truth for connector capability. If a
v5 collateral piece implies a live integration, it is wrong — check this matrix.
