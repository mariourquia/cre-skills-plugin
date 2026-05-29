# Known Limitations

What the document-to-database family deliberately does not do. These are scope boundaries, not bugs — each one is a place where the family carries the source figure faithfully but declines to synthesize a number it cannot defend. Knowing these prevents over-reading the output.

## Billed-vs-collected cash is out of scope

There is no accounts-receivable feed. The rent roll is treated as annualized CONTRACTUAL in-place income, and the T-12 as RECOGNIZED ACCRUAL income; collected cash is explicitly `not_available`. The family does not compute delinquency, bad debt, or actual collections, and it does not reconcile to a bank statement. A reconciliation difference between contractual and accrual is a legitimate, classified variance (free rent, vacancy, true-ups), not a collections signal. Do not read the tie-out as a cash-collections proof.

## Percentage-rent breakpoints are carried, not projected

A `percentage_rent` charge line is captured where present, and percentage-rent / overage descriptions are recognized and mapped. But the family does not model contingent rent: natural and artificial breakpoints, sales-based projections, co-tenancy clauses, and kick-out rights are not turned into a forward percentage-rent estimate. The current-period figure on the charge line is what is carried; the contingent upside is left to the underwriting model downstream.

## Prepaid rent and deposit timing are blind spots

Prepaid rent and security-deposit-applied-to-rent are timing items the family does not currently resolve. A deposit is carried as a lease field (`security_deposit`), but the family does not track when a deposit is applied to rent, nor does it reattribute a prepaid amount across periods. These can create a legitimate, unexplained-looking timing difference in a reconciliation; treat such a difference as a candidate timing item for review, not as a model error.

## Recoveries are combined in one canonical other-rental account

The canonical chart of accounts combines CAM, tax, and insurance recoveries together with parking, storage, percentage rent, and other recurring income into a single `revenue_other_rental` account (one-time amortized income posts to `revenue_other_non_rental`). The reconciliation keeps the rent-roll-side breakdown (recoveries vs other income) visible, but the T-12 side is the combined total because the chart does not split it. Consequently, the recoveries and other-income tie-out dimensions both report against the combined `other_rental` total — a per-recovery-type tie-out at the account grain is not available without forking the chart, which the family does not do.

## Partial-year statements are annualized with a caveat

A T-12 with fewer than twelve monthly periods (a partial year or a lease-up) is accepted, but the missing months are carried as a gap — never synthesized into invented monthly figures. Where the reconciliation needs an annual figure, it scales the months present to twelve, which is an explicit annualization, not a measured full year. The basis block on the reconciliation reports how many months were present so a reader can judge the annualization. A partial-year statement therefore supports a directional tie-out, not a precise full-year reconciliation.

## Mapping is deterministic, not semantic

Charge and account mapping resolve by known codes, known aliases, and an ordered keyword table — not by a learned semantic model. A novel charge code with an unrecognized description is `unmapped` and routed to human review rather than guessed. This is intentional (fail-closed beats a confident wrong mapping), but it means the family will queue items a human reader would map at a glance; the alias and keyword tables are the place to extend coverage. See `charge-code-account-framework.md`.

## The emitted DDL is a specification, not an applied schema

The target-model DDL and load plan are reviewable specifications for a downstream warehouse. They are not executed, they emit no DML, and they are not the prototype runtime's staging schema (which is flatter, FK-free, and session-scoped). Do not treat a successful DDL emission as a created database. See `target-model-profiles.md`.

## Escalations are captured, not stepped forward

The lease `escalation` object (type, amount, frequency, next-escalation date, and the CPI sub-fields) is captured where present and contributes to the escalation-documentation grade. But the family does not roll a lease forward: it does not apply a fixed-percent bump, resolve a CPI index against a base month, mark to fair-market value, or build a forward rent schedule. A future-dated escalation also does NOT break the current-period `annual == monthly*12` identity, so it is not allowed to skip the arithmetic check the way free rent or an in-period step does. Forward rent stepping belongs to the underwriting model downstream, not to ingestion.

## No cross-document entity resolution

The family produces entity-resolution HINTS (stable ids within a run, a property/unit/lease/tenant key per document), but it does not perform fuzzy entity resolution ACROSS documents or across runs. It will not decide that "Suite 200" in a rent roll and "Ste 200" in a different statement are the same unit, nor that two pseudonymized tenants in separate exports are the same party — and by design it cannot, because the pseudonym salt is the `run_id`, so identities are intentionally not linkable across runs without reusing that id. Cross-document and cross-run identity stitching is a downstream warehouse concern.

## Mapping is deterministic, not learned, and capex never enters NOI

The mapping and the accounting are rule-based on purpose. The chart of accounts assigns each canonical slug a `statement_section`, and a capex, debt-service, or distribution line is kept out of the NOI computation by that classification — an NOI that includes a below-the-line item is a critical failure, not a silent inclusion. There is no learned model that might quietly reclassify a capital item into operating expense; the cost of that determinism is the queue of items a human reader would map at a glance, which is the intended trade. See `charge-code-account-framework.md` and `data-quality-rules.md`.
