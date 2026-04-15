# Compliance Calendar

Status: stub. Placeholder for the compliance-calendar concept that
aggregates every time-bound regulated obligation for a property.

## Concept

The compliance calendar is the merged view of every time-bound regulatory
event for a property: recertifications due, agency inspections scheduled,
rent-limit and UA refreshes published or expected, agency reports due,
audit windows open, REAC / NSPIRE inspection windows, extended-use
covenant milestones, qualified-contract windows. The calendar is PRODUCED
from the overlay's declared event types plus the reference state of
schedules and compliance-event ledgers.

## Target keys the overlay will populate

- `reporting_emphasis` -> surfaces the 30 / 60 / 90-day compliance
  horizon in the standard reporting emphasis for regulated properties.
- Adds:
  - `compliance_calendar_event`
  - `compliance_calendar_horizon_30d`
  - `compliance_calendar_horizon_60d`
  - `compliance_calendar_horizon_90d`

## Calendar event types

- recert_due (annual or interim)
- agency_inspection (REAC, NSPIRE, state-HFA, PHA)
- rent_limit_refresh (HUD / state publishes new limits)
- ua_refresh (publisher issues new UA)
- agency_report_due (see `agency_reporting.md`)
- audit_window (state HFA or HUD compliance audit)
- covenant_milestone (LIHTC extended-use, qualified-contract window open)

## Production rule

The calendar is not hand-edited. It is produced as the union of:

1. Recertification schedule (from `recertification.md`'s ledger).
2. Agency-reporting schedule (from `agency_reporting.md`'s cadence table).
3. Rent-limit and UA publisher schedules (from `rent_limits.md` and
   `utility_allowance.md`).
4. Covenant milestones (from the program overlay's covenant table).
5. Inspection windows (from the PHA / HFA / HUD scheduling feed).

## Phase 1 does not implement

- Event-production logic.
- Calendar UI or report layout.
- SLA bands for each event type.
- Escalation hooks (see `escalation_sensitivity.md`).
