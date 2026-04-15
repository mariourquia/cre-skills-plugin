# Sample run — Acme Multifamily

A walk-through of a first tailoring interview for a fictitious operator, Acme Multifamily. All numbers below are illustrative answers entered by the operator during the interview; none are canonical or hardcoded.

**Operator profile.** Acme Multifamily operates 22 middle-market garden and wrap properties across the Southeast. They are self-managed. Their COO is onboarding the org onto this subsystem for the first time.

## Session invocation

```shell
$ python3 tailoring/tools/tailoring_tui.py --org-id acme_mf
```

## Screen 1 — session bootstrap

```
+============================================================================+
| Tailoring Interview - acme_mf                                              |
| session 20260415_164301_coo_a3f1  audience coo_operations_leader           |
+============================================================================+
```

Output lines printed by the TUI:

```
Created new session 20260415_164301_coo_a3f1 for acme_mf.
```

## Screen 2 — first question

```
+----------------------------------------------------------------------------+
| [coo / coo_operations_leader] coo_001                                      |
|                                                                            |
| What is the organization's primary operating model across the portfolio?   |
|                                                                            |
| why: Determines whether role packs load self_managed, third_party_managed, |
|      or both; gates downstream audiences.                                  |
|                                                                            |
| choices:                                                                   |
|   1. self_managed                                                          |
|   2. third_party_managed                                                   |
|   3. hybrid                                                                |
|   4. unknown                                                               |
|                                                                            |
| progress: [.........................................] 0/30 (0%)           |
| [:b back] [:s skip] [:w where] [:p preview] [:q quit] [:h help]            |
+----------------------------------------------------------------------------+

answer [single_choice] > 1
```

Operator answers `1` (self_managed). The session is persisted.

## Screens 3–12 — further COO answers (selected highlights)

The operator answers through coo_002 (hybrid mix — skipped with `:s` because Acme is fully self-managed), coo_003 (org chart — operator uploads org_chart.pdf). The TUI confirms:

```
answer [document_request] > /Users/acme/Documents/org_chart_apr2026.pdf
```

On coo_004 the operator enters `35` (regional manager span of control in units times ten? no, they mean 35 properties — operator corrects; the question actually asks units, so they enter `900`).

On coo_007 the operator enters PM autonomous disbursement threshold:

```
answer [numeric] > 25000
```

On coo_008 the operator enters regional threshold:

```
answer [numeric] > 100000
```

On coo_010 the operator picks the lead response SLA:

```
choices:
  1. within_15_minutes
  2. within_1_hour
  3. same_business_day
  4. next_business_day
  5. no_standard

answer [single_choice] > 3
```

On coo_013 the operator enters concession policy ceiling:

```
answer [numeric] > 4
```

(four weeks of rent equivalent, above which escalation is required).

On coo_019 the operator does not have the property list ready:

```
answer [document_request] > missing
  + missing_doc queued: property_list (p1) for role coo_operations_leader
```

On coo_021 the operator enters leasing-agent staffing ratio:

```
answer [numeric] > 95
```

(95 units per leasing agent).

On coo_028 the operator uploads the SOPs library:

```
answer [document_request] > /Users/acme/Documents/sops_library_2026.zip
```

## Final screen — diff preview

After coo_030 the TUI renders the diff:

```
Diff preview

@@ approval_matrix.threshold_disbursement_1  ~~ approval_matrix row 6
-  approval_matrix.threshold_disbursement_1: None
+  approval_matrix.threshold_disbursement_1: 25000
   ^ approver_role: coo_operations_leader
   ^ rationale: Approval matrix row 6 (financial disbursement tier 1) threshold;
     sourced from coo interview coo_007.
   ^ source: {'bank_slug': 'coo', 'question_id': 'coo_007'}

@@ approval_matrix.threshold_disbursement_2  ~~ approval_matrix row 7
-  approval_matrix.threshold_disbursement_2: None
+  approval_matrix.threshold_disbursement_2: 100000
   ^ approver_role: coo_operations_leader
   ^ rationale: Approval matrix row 7 (financial disbursement tier 2) threshold;
     sourced from coo interview coo_008.
   ^ source: {'bank_slug': 'coo', 'question_id': 'coo_008'}

@@ approval_matrix.threshold_vendor_contract  ~~ approval_matrix row 19
-  approval_matrix.threshold_vendor_contract: None
+  approval_matrix.threshold_vendor_contract: 50000
   ^ approver_role: portfolio_manager
   ^ rationale: Approval matrix row 19 (vendor contract signature) threshold;
     sourced from coo interview coo_009.
   ^ source: {'bank_slug': 'coo', 'question_id': 'coo_009'}

@@ concession_policy.pm_max_weeks
-  concession_policy.pm_max_weeks: None
+  concession_policy.pm_max_weeks: 4
   ^ approver_role: coo_operations_leader
   ^ rationale: Concession policy change; approval matrix row 13 applies.
     Sourced from coo interview coo_013.
   ^ source: {'bank_slug': 'coo', 'question_id': 'coo_013'}

@@ operating_model
-  operating_model: None
+  operating_model: self_managed
   ^ approver_role: unspecified
   ^ rationale: From coo interview question coo_001.
   ^ source: {'bank_slug': 'coo', 'question_id': 'coo_001'}

@@ renewal_strategy.renewal_offer_lead_time_days
-  renewal_strategy.renewal_offer_lead_time_days: None
+  renewal_strategy.renewal_offer_lead_time_days: 90
   ^ approver_role: unspecified
   ^ rationale: From coo interview question coo_014.
   ^ source: {'bank_slug': 'coo', 'question_id': 'coo_014'}

@@ service_standards.lead_response_target
-  service_standards.lead_response_target: None
+  service_standards.lead_response_target: same_business_day
   ^ approver_role: unspecified
   ^ rationale: From coo interview question coo_010.
   ^ source: {'bank_slug': 'coo', 'question_id': 'coo_010'}

@@ service_standards.make_ready_days_target
-  service_standards.make_ready_days_target: None
+  service_standards.make_ready_days_target: 7
   ^ approver_role: unspecified
   ^ rationale: From coo interview question coo_012.
   ^ source: {'bank_slug': 'coo', 'question_id': 'coo_012'}

@@ staffing_ratios.leasing_units_per_agent
-  staffing_ratios.leasing_units_per_agent: None
+  staffing_ratios.leasing_units_per_agent: 95
   ^ approver_role: unspecified
   ^ rationale: From coo interview question coo_021.
   ^ source: {'bank_slug': 'coo', 'question_id': 'coo_021'}

@@ vendor_policy.centrally_approved_categories
-  vendor_policy.centrally_approved_categories: None
+  vendor_policy.centrally_approved_categories: 'hvac, plumbing, roofing, landscaping'
   ^ approver_role: portfolio_manager
   ^ rationale: Vendor policy change; approval matrix row 19 applies.
     Sourced from coo interview coo_024.
   ^ source: {'bank_slug': 'coo', 'question_id': 'coo_024'}

... (additional entries elided for brevity) ...

14 sign-off queue entries opened. Nothing was written to overlays/org/acme_mf/.
```

## Sign-off queue entries (excerpt)

`tailoring/sign_off_queue.yaml` gains entries of the form:

```yaml
- queue_entry_id: 3f9b1ac7c4a24...
  org_id: acme_mf
  session_id: 20260415_164301_coo_a3f1
  overlay_key: approval_matrix.threshold_disbursement_1
  prior_value: null
  proposed_value: 25000
  rationale: |
    Approval matrix row 6 (financial disbursement tier 1) threshold;
    sourced from coo interview coo_007.
  interview_source:
    bank_slug: coo
    question_id: coo_007
  approver_role: coo_operations_leader
  approval_matrix_row: 6
  created_at: 2026-04-15T16:52:14Z
  expires_at: 2026-05-15T16:52:14Z
  status: pending
  approver_note: null
```

## Missing docs queue entries (excerpt)

`tailoring/missing_docs_queue.yaml` gains:

```yaml
- doc_slug: property_list
  doc_title: Property list (segment, form factor, lifecycle, market per property)
  requested_from_role: coo_operations_leader
  requested_at: 2026-04-15T16:47:22Z
  priority: p1
  used_by_overlay_keys:
    - overlay.yaml#property_list_ref
  substitute_behavior: use_defaults
  status: open
  org_id: acme_mf
  session_id: 20260415_164301_coo_a3f1
  notes: |
    Opened from question coo_019 in the coo bank.
    Target overlay key: overlay.yaml#property_list_ref.
```

## Session summary (excerpt)

`tailoring/sessions/acme_mf/20260415_164301_coo_a3f1__summary.md`:

```markdown
# Tailoring session summary — acme_mf

- session_id: `20260415_164301_coo_a3f1`
- created_at: 2026-04-15T16:43:01Z
- updated_at: 2026-04-15T16:52:14Z
- audiences_scheduled: coo, cfo, regional_ops, asset_mgmt, development, construction, reporting
- audiences_completed: coo

## Completeness by audience

| Audience | Total | Answered | Pending doc | Score |
|---|---|---|---|---|
| coo | 30 | 23 | 1 | 79% |
| cfo | 28 | 0 | 0 | 0% |
| regional_ops | 15 | 0 | 0 | 0% |
| asset_mgmt | 15 | 0 | 0 | 0% |
| development | 12 | 0 | 0 | 0% |
| construction | 12 | 0 | 0 | 0% |
| reporting | 12 | 0 | 0 | 0% |

## Missing docs opened this session

- property_list

## Proposed diff

| Overlay key | Prior | Proposed | Approver | Row |
|---|---|---|---|---|
| `approval_matrix.threshold_disbursement_1` | `None` | `25000` | coo_operations_leader | 6 |
| `approval_matrix.threshold_disbursement_2` | `None` | `100000` | coo_operations_leader | 7 |
| `approval_matrix.threshold_vendor_contract` | `None` | `50000` | portfolio_manager | 19 |
| `concession_policy.pm_max_weeks` | `None` | `4` | coo_operations_leader | 13 |
| `operating_model` | `None` | `self_managed` | - | - |
| `renewal_strategy.renewal_offer_lead_time_days` | `None` | `90` | - | - |
| `service_standards.lead_response_target` | `None` | `same_business_day` | - | - |
| `service_standards.make_ready_days_target` | `None` | `7` | - | - |
| `staffing_ratios.leasing_units_per_agent` | `None` | `95` | - | - |
| `staffing_ratios.maintenance_units_per_tech` | `None` | `120` | - | - |
| `staffing_ratios.regional_span_of_control_units` | `None` | `900` | - | - |
| `vendor_policy.centrally_approved_categories` | `None` | `'hvac, plumbing, roofing, landscaping'` | portfolio_manager | 19 |

Sign-off queue entries were opened for each diff row. The commit of approved
entries to `overlays/org/{org_id}/overlay.yaml` is handled by a separate tool.
```

## What happens next

1. The approvers (COO and portfolio manager) review `sign_off_queue.yaml`, mark entries `approved` or `rejected`, and annotate `approver_note` where useful.
2. An external commit tool reads the approved entries and writes them to `overlays/org/acme_mf/overlay.yaml`, creating the directory if needed, and appends a corresponding entry to `overlays/org/acme_mf/change_log.md` per approved change.
3. The COO uploads `property_list.xlsx` the next business day. A future session runs the `process_missing_docs_queue` workflow to parse it and propose the dependent overlay keys. Those keys go back through the sign-off queue before being committed.
4. The operator resumes the interview the following day to run the CFO, regional_ops, and other audiences in separate sessions.
