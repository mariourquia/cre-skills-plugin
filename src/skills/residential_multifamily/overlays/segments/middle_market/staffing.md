# Middle-Market Staffing Posture

Middle-market (workforce / attainable) properties operate on a lean, durable staffing
model. The posture is: staff for steady-state service delivery, flex up for seasonal
turn and rollover spikes, never run so lean that work-order SLAs slip or that tour
response times fall outside the band.

## Site team shape

A middle-market property carries a small, cross-trained site team:

- Property manager — accountable for collections, budget variance, and leasing funnel
  health.
- Assistant property manager (threshold-based by unit count) — accountable for
  receivables, ledger accuracy, and move-in/out coordination.
- Leasing manager with leasing associates per the staffing ratio referenced from
  `reference/derived/role_kpi_targets.csv#row_mm_leasing_staffing_ratio`.
- Maintenance supervisor plus maintenance technicians per
  `reference/derived/role_kpi_targets.csv#row_mm_maintenance_staffing_ratio`. Make-ready
  and preventive maintenance share the same pool; during heavy-turn windows the pool
  flexes via the porter-trainee feeder or trusted turn vendors.
- Porter / groundskeeper coverage scaled to form factor. Garden and walk-up form
  factors require more grounds coverage per unit than urban mid-rise; ratios live in
  `reference/derived/role_kpi_targets.csv`.

## Principles

1. The staffing ratios above are bands, not points. Turnover rate, work-order volume,
   and form factor shift where on the band a property sits.
2. Lease-up overlay tightens leasing ratios; stabilized overlay returns them to the
   baseline band. Seasonal turn windows temporarily tighten maintenance ratios.
3. Training and cross-coverage are mandatory; a middle-market property cannot afford
   to depend on a single tech or single agent. Succession candidates are named, not
   implied.
4. Vacancy in a site role is itself a reportable KPI; see
   `_core/metrics.md#staffing_vacancy_rate_tpm` for the TPM-side equivalent, and the
   owner-oversight overlay for how owner-side monitors apply to self-managed and
   third-party-managed properties.

## What this overlay does not do

This overlay does not embed headcount ratios in prose. Every ratio is a reference-layer
row. This overlay documents the posture; reference values move on their own change log
without rewriting skill text.
