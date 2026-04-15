# CRM Identity Resolution

How leads, contacts, campaigns, and resident communications in the CRM connector crosswalk to canonical identifiers.

## Crosswalk pointers

- `reference/connectors/master_data/resident_crosswalk.yaml`: resident and contact identity (shared with PMS).
- `reference/connectors/master_data/campaign_registry.yaml`: canonical campaign identifiers and medium taxonomy.
- `reference/connectors/master_data/lead_dedup_rules.yaml`: rules for surfacing duplicate leads.

## Match methods

| Method | Use | Confidence |
|---|---|---|
| `exact` | CRM-native interaction_id, task_id, communication_id. | Highest. Used directly where the CRM is authoritative. |
| `composite` | (property_id, normalized_contact_hash, inquiry_window) to link a CRM interaction to a PMS lead when the CRM does not carry PMS lead_id. | High. The default bridge between CRM and PMS. |
| `fuzzy` | Normalized name + phone or name + email where a contact has multiple spellings or formats. | Medium. Always queued for operator adjudication. |
| `manual` | Operator-adjudicated lead merge recorded in resident_crosswalk with survivor lead_id. | Authoritative once recorded. |

## Confidence scoring

Every candidate match carries a `confidence_tier`. CRM interactions resolved to a PMS lead with `confidence_tier = low` are held from downstream funnel metrics until adjudicated; they still land so the operator can review.

## Hard cases

### Duplicate leads

A single prospect may create two or more leads by inquiring through separate channels (website form, ILS, walk-in). The CRM typically does not dedup automatically; the lead_dedup_rules declare the composite keys used to surface candidates. Failure mode: duplicate leads inflate top-of-funnel volume, distort cost-per-lead, and create duplicate outreach. Mitigation: `crm_lead_duplicate_detection` surfaces candidates; operator merges and records the survivor.

### Merged leads

Once leads are merged, the non-survivor lead_id must carry a `merged_into` pointer. Every subsequent CRM interaction for the prospect attaches to the survivor lead_id. Failure mode: an interaction attached to a non-survivor lead_id orphans the touch from the funnel. Mitigation: `crm_merged_lead_survivorship` blocks landing of interactions attached to un-pointed non-survivor leads.

### Same contact across multiple applications

A prospect who applies to two different properties in the portfolio, or re-applies to the same property in a later cycle, generates multiple `pms.application` rows. The resident_crosswalk groups these by canonical_resident_id; the CRM attaches each interaction to the correct lead_id via inquiry_window. Failure mode: cross-property leakage analysis (is a prospect shopping multiple properties?) breaks without the canonical grouping. Mitigation: `crm_contact_dedup_across_applications`.

### Offline communication missing from system

Walk-in conversations, in-person tours, and phone calls are prone to being captured late (or not at all). The CRM should carry an agent_id and a timestamp for every offline interaction; missing values indicate retroactive data entry at best or a coaching gap at worst. Failure mode: funnel conversion and lead-response-time metrics under-count offline-sourced leases. Mitigation: `crm_offline_interaction_flagged`.

### Campaign taxonomy drift

Operators tag inquiries with a campaign label that may or may not match the canonical medium enum. A new vendor campaign that is not registered silently buckets to `other`, distorting attribution. Mitigation: `crm_campaign_taxonomy_conformance` and `crm_source_channel_enum_conforms` require mapping before landing.

## Failure modes summary

| Failure | Symptom | Check |
|---|---|---|
| Duplicate lead not surfaced | Inflated top-of-funnel volume | `crm_lead_duplicate_detection` |
| Merged lead without survivor pointer | Orphan interactions | `crm_merged_lead_survivorship` |
| Offline interaction without agent/timestamp | Missed coaching / data-entry gap | `crm_offline_interaction_flagged` |
| Cross-property prospect shopping invisible | Weak competitive awareness | `crm_contact_dedup_across_applications` |
| Unregistered campaign | Buckets to other, distorts attribution | `crm_campaign_taxonomy_conformance` |
| Stale pipeline stage | Funnel lag invisible | `crm_stale_pipeline_stage` |
| Out-of-order event timestamps | Funnel cycle-time metrics corrupted | `crm_timestamp_monotonic` |
