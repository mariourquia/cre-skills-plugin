# Templates

Starter templates for operating, reporting, construction, TPM oversight, and resident communications. Every template is Markdown with optional YAML frontmatter capturing scope and legal-review requirements.

## Frontmatter

```yaml
---
template_slug: <kebab-case-slug>
title: <Human-readable title>
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized]
  management_mode: [self_managed, third_party_managed]
  role: [property_manager]
  output_type: operating_review
legal_review_required: false          # true = do not send before legal review
jurisdiction_sensitive: false         # true = state/city-specific content
status: starter | sample | placeholder | approved
references_used:
  - reference/normalized/...
produced_by: roles/property_manager | workflows/<slug>
---
```

## Legal-review banner

Every template that could constitute a statutory notice in some jurisdiction (rent increase, non-renewal, pay-or-quit, entry notice, lease violation, eviction-preceding notice, reasonable accommodation response) carries:

- `legal_review_required: true` in frontmatter.
- A prominent "LEGAL REVIEW REQUIRED BEFORE SEND" banner at the top of the body.
- A footer listing the jurisdictional dimensions that must be reviewed (state, city, operator policy).

## Placeholder fields

Template placeholders use `{{field_name}}` or `<field_name>` style. The rendering layer fills from the invoking pack's inputs. Unfilled placeholders in rendered output fail validation.

## Source data tagging

When a template renders with sample-tagged reference data, the rendered output surfaces the tag (typically in a footer).

## Directory layout

```
templates/
  README.md                         # this file
  site_ops/                         # PM weekly / daily templates
  monthly_reviews/                  # scorecards, memos
  quarterly_portfolio/              # AM / PM / exec quarterly
  budget_forecast/                  # budget build, forecast refresh, variance
  capex/                            # capex request, bid leveling, CO log
  construction/                     # meeting agenda, draw package, risk register
  development/                      # milestone tracker, executive summary
  tpm_oversight/                    # scorecard, audit log, approval routing
  resident_comms/                   # resident-facing drafts (legal-review banners where needed)
  vendor_comms/                     # vendor-facing drafts
  executive/                        # exec summary pack
  market_survey/                    # market survey intake / summary
```

All templates are `status: starter` or `status: sample` on first commit. Operators tailor through the tailoring skill and the org overlay.
