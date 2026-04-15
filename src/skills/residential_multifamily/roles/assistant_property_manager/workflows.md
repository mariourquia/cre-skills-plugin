# Workflows invoked by assistant_property_manager

| Workflow | Cadence | Trigger |
|---|---|---|
| `workflows/move_in_administration` | Per move-in | move_in_event |
| `workflows/move_out_administration` | Per move-out | move_out_event |
| `workflows/delinquency_collections` | Weekly + per aging move | aging transition |
| `workflows/screening_application_processing` | Per application | new application submitted |
| `workflows/rent_roll_hygiene_check` | Weekly | pre-PM weekly review |
| `workflows/vendor_invoice_batch_prep` | Weekly | AP cycle |
| `workflows/lead_to_lease_funnel_review` | Weekly (data-prep support) | pre-PM weekly review |
| `workflows/ledger_posting_reconcile` | Daily | end of posting day |
