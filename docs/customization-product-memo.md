# Product Memo: Skill Customization & Feedback

## Recommendation Summary

Ship the customization system as a first-class feature of the CRE Skills Plugin. It addresses a fundamental product tension: skills must be opinionated enough to be useful out of the box, but every CRE team has its own terminology, approval chains, compliance requirements, and deliverable formats. This feature lets users resolve that tension themselves.

## Key Product Decisions

### 1. Full-copy overrides, not patches

Customizations are complete copies of the SKILL.md file, not diffs or patches applied at runtime.

**Why:** Non-technical users can read and edit a complete file. Patches break when the base changes. Full copies are portable, debuggable, and simple to reason about.

**Tradeoff:** Customized skills do not automatically receive upstream improvements. Users must re-customize after major base skill updates. This is acceptable because: (a) most customizations are small and targeted, (b) the base snapshot enables easy comparison, and (c) automatic merging would introduce unpredictable behavior for compliance-sensitive workflows.

### 2. Conservative privacy defaults

Default mode: `metadata_only` with `require_consent: true` and no remote endpoint.

**Why:** CRE teams handle sensitive internal process details. A single data leak from a customization payload -- even a diff showing an internal compliance step -- would destroy enterprise trust in the plugin. The default must be safe enough that an IT security review passes without objection.

**Tradeoff:** The maintainer receives less signal by default. This is acceptable because: (a) metadata alone (which skill, what category, why) answers the most important product questions, (b) users who want to share more can opt up explicitly, and (c) the structured category tags provide machine-analyzable signal without free-text content.

### 3. Structured category tags over free-text classification

The 11 change categories (terminology, approval chain, required steps, etc.) are a fixed taxonomy, not user-defined labels.

**Why:** Enables quantitative analysis at scale. "Which skills have the most compliance customizations?" is answerable with structured tags. Free-text reasons are also captured but as supplementary context, not primary classification.

**Tradeoff:** Some customizations won't fit neatly into the taxonomy. The "other" category and free-text rationale field handle this. The taxonomy can be extended in future versions based on observed "other" patterns.

### 4. Local-first architecture

All customizations work fully offline. Remote feedback is layered on top, never required.

**Why:** Enterprise deployments may prohibit outbound network calls from developer tools. Air-gapped environments exist. The feature must be valuable without any network connectivity.

### 5. Outbox-based remote delivery

Feedback payloads are queued locally and drained on next session start, not sent synchronously.

**Why:** (a) MCP tool calls are synchronous in the current architecture, (b) network failures should never block the user's workflow, (c) the existing outbox mechanism already handles retry and eviction.

## Analytics Opportunities

The feedback schema is designed to answer these product questions:

| Question | Data source |
|----------|------------|
| Which skills are most customized? | `skill_slug` frequency |
| What kind of changes are most common? | `change_categories` distribution |
| Are teams adapting terminology or process? | Category breakdown |
| Which sections of skills don't fit? | `sections_changed` field |
| How big are typical customizations? | `diff_stats` (lines added/removed) |
| Which customizations suggest a missing feature? | `wants_upstream_consideration` + rationale |
| Are customizations growing over time? | Timestamp trends |
| Platform distribution? | `platform` field |

At scale, the most valuable signal will be: "Skill X has 15 customizations across 8 organizations, 12 of which modify the Process section and are tagged 'compliance_governance'." This tells the maintainer exactly what to fix upstream.

## Privacy & Compliance Considerations

1. **No PII by design.** Payloads contain skill slugs, category tags, and hashes. Even in `metadata_and_content` mode, the content is a process description, not deal data.

2. **Explicit consent for content.** The `consented_to_content` flag is enforced at the filtering layer, not just the UI. Even if a bug sets the mode to `metadata_and_content`, content is stripped without the consent flag.

3. **Enterprise endpoint support.** Organizations can point `feedback_endpoint` to their own infrastructure, keeping all data internal.

4. **Audit trail.** `dry_run` mode shows exactly what would be sent. Every payload is saved to local `feedback-log.jsonl` regardless of remote status.

5. **No silent sends.** When `require_consent` is true (default), the user always sees a preview before any remote submission.

## Shipped Capabilities

These features are implemented and available in the current release:

- **Export/import customization bundles** (`cre_export_customization`, `cre_import_customization`). Portable JSON bundles for team sharing and backup.
- **Upstream suggestion flow** (`cre_upstream_suggestion`). Generates a structured GitHub issue body from a customization with rationale, categories, and diff.
- **Customization health check** (`cre_customization_health_check`). Detects base skill drift after plugin updates, single-skill or batch.
- **Admin-approved templates** (`cre_list_templates`, `cre_apply_template`). Pre-built customization starting points in `templates/customizations/`. Ships with FIRPTA screening, NYC transfer tax, and ESG pre-screening templates.
- **Local analytics** (`cre_customization_analytics`, `/cre-skills:customization-analytics`). Aggregates skill frequency, category distribution, upstream request rate, section patterns, and monthly trends from local feedback log.

## Future Roadmap

### Near-term

- **Team-shared customization packs.** A git repo or shared folder of approved customizations that team members can install via import.
- **Conflict detection.** When multiple customizations affect the same skill chain, detect potential conflicts in process flow or output expectations.
- **Schema versioning.** Add `schema_version` field to feedback payloads for cross-version compatibility at the telemetry endpoint.

### Medium-term

- **Server-side analytics dashboard.** Aggregate anonymized feedback data at the `cre-skills-feedback-api` endpoint into a maintainer-facing dashboard showing cross-user customization patterns.
- **Customization marketplace.** Community-contributed customization packs for specific markets (NYC, London, Hong Kong), property types (life science, data center), or regulatory regimes (FIRPTA, Opportunity Zone, EB-5).

### Long-term

- **AI-assisted customization.** "I need this skill to follow our IC review process" generates the customization automatically based on the user's description and existing customizations.
