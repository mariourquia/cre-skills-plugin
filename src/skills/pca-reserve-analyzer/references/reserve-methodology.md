# Replacement-Reserve and PCA Conversion Methodology

This reference documents the methodology the `pca-reserve-analyzer` skill applies when
converting a Property Condition Assessment (PCA) / Physical Needs Assessment (PNA) into a
capital plan. All numeric tables below are **illustrative industry-standard reference
ranges**, not property-specific truth. The skill must always prefer quantities, unit costs,
EULs, and RULs stated in the actual PCA; these tables are fallbacks used only when the
report omits a value, and every substitution must be flagged in the output.

---

## 1. Core definitions

- **EUL (Estimated Useful Life)**: Total expected service life of a component when new, in years.
- **RUL (Remaining Useful Life)**: Years of service remaining as of the PCA report date.
- **Effective age** = EUL - RUL.
- **Immediate repair**: Life-safety, code, or critical-deferred item the consultant recommends
  addressing within roughly 0-12 months. Funded as Year 0 capital (Sources & Uses), not reserve.
- **Replacement reserve**: Annual set-aside (sinking fund) sized to fund cyclical replacement of
  components over their EUL. Expressed as per-unit-per-year (PUPY) for residential or $/SF/yr for
  commercial.
- **PNA**: HUD/FHA's term for the 20-year physical needs assessment that drives the reserve for
  replacement (R4R) deposit on agency-insured multifamily loans.

---

## 2. Triage rule (which bucket a line item lands in)

| PCA characteristic | Bucket | Model destination |
|---|---|---|
| Life-safety / code / "immediate" / 0-12 mo | Immediate (Year 0) | Sources & Uses; lender escrow |
| Recommended Yr 1-2, non-critical | Short-term deferred | Year 1-2 capital |
| Has EUL/RUL, replaced cyclically | Replacement reserve | 10-yr reserve schedule |
| Noted, no near-term cost | Informational / monitor | Diligence watchlist |

Override rule: if buyer field notes or recent-capital evidence contradicts the PCA (e.g., roof
replaced last year), reset RUL to full EUL and document the override.

---

## 3. Illustrative EUL reference ranges

Use only when the PCA omits an EUL. Ranges are typical for institutional CRE; actual EUL depends
on original quality, climate, and maintenance. **Illustrative.**

| Component | Typical EUL (yrs) |
|---|---|
| Built-up / modified-bitumen flat roof | 15 - 20 |
| Pitched shingle roof (architectural) | 20 - 30 |
| Asphalt parking lot (overlay / resurface) | 15 - 20 |
| Parking lot full reconstruction | 25 - 30 |
| Packaged rooftop HVAC unit | 15 - 20 |
| Split-system / through-wall AC | 12 - 15 |
| Central chiller | 20 - 25 |
| Boiler (commercial) | 25 - 30 |
| Domestic water heater (commercial) | 10 - 15 |
| Elevator modernization | 20 - 30 |
| Exterior paint / sealant | 7 - 10 |
| EIFS / stucco facade | 25 - 40 |
| Windows (commercial-grade) | 25 - 40 |
| Unit appliances (residential) | 10 - 15 |
| Unit flooring (carpet / LVT) | 7 - 12 |
| Site lighting / pole fixtures | 15 - 25 |
| Fire alarm / sprinkler components | 20 - 30 |

---

## 4. 10-year reserve schedule construction

1. For each reserve component, replacement year = report year + RUL.
2. Place the replacement cost in that year. If EUL is short enough that a second cycle falls inside
   the hold, place the second replacement at (first replacement year + EUL).
3. Escalate each placed cost from the report date to its replacement year at the inflation rate,
   compounded: `cost_infl = cost_current * (1 + i) ^ (replacement_year - report_year)`.
4. Sum per year; carry a cumulative total.

Worked micro-example (illustrative, 3% inflation, report year 0):

| Component | RUL | Repl yr | Cost (cur) | Cost (infl) |
|---|---|---|---|---|
| Flat roof, 30,000 SF @ $9/SF | 4 | 4 | $270,000 | $303,866 |
| Two RTUs @ $18,000 | 1 | 1 | $36,000 | $37,080 |
| Parking overlay, 60,000 SF @ $3/SF | 6 | 6 | $180,000 | $214,910 |

Year totals (current $): Y1 $36,000; Y4 $270,000; Y6 $180,000. Cumulative over hold = $486,000
current / ~$555,856 inflated. Figures are illustrative arithmetic to show method, not a real asset.

---

## 5. Implied reserve: two views

- **Levelized reserve** = (sum of all scheduled replacements over the hold) / hold years / (units or SF).
  Fully-funded sinking-fund view; smooths the capital cliff.
- **In-hold cash reserve** = same calc but only replacements landing inside the hold. Reflects cash you
  must actually fund as owner. For a newer asset, in-hold < levelized (few replacements hit yet); for an
  older asset with stacked RULs, in-hold can exceed a flat levelized figure.

Always present both, in current and inflated dollars, and benchmark against Section 6.

---

## 6. Illustrative PUPY / $-per-SF benchmark ranges

Order-of-magnitude reserve intensity by property type and vintage. Lender floors override these for
agency loans. **Illustrative.**

| Property type | Vintage | Typical reserve |
|---|---|---|
| Multifamily, garden | Pre-1990 | $300 - $600 / unit / yr |
| Multifamily, garden | 1990 - 2010 | $250 - $400 / unit / yr |
| Multifamily, mid/high-rise | Any | $350 - $700 / unit / yr |
| Office, suburban | Any | $0.20 - $0.40 / SF / yr (reserve only, excl. TI/LC) |
| Office, CBD high-rise | Any | $0.30 - $0.60 / SF / yr |
| Retail, neighborhood/strip | Any | $0.15 - $0.30 / SF / yr |
| Industrial / warehouse | Any | $0.10 - $0.20 / SF / yr |

Note: reserve intensity excludes tenant improvements and leasing commissions, which are modeled
separately in the proforma. Do not blend them into the PUPY figure.

---

## 7. Lender reserve conventions (for the adequacy gap)

Used in Step 5 to normalize the lender-underwritten reserve before comparing. **Illustrative of common
program practice; confirm against the actual loan quote.**

| Program | Reserve convention | Typical floor / basis |
|---|---|---|
| Fannie Mae DUS (MF) | Underwritten replacement reserve, PUPY | Often ~$250 - $300 / unit / yr floor; can be higher for older assets |
| Freddie Mac Optigo (MF) | Underwritten replacement reserve, PUPY | Similar PUPY floors; PCA-driven adjustments |
| HUD / FHA (221(d)(4), 223(f)) | R4R deposit from 20-yr PNA | PNA-driven; commonly higher because it funds a 20-yr horizon |
| CMBS | Ongoing monthly reserve, often springing | Engineer-recommended; may be waived above a debt-yield/quality threshold |
| Life co / bank | Negotiated; often lighter or waived | Balance-sheet discretion; smallest reserve burden, most diligence risk on buyer |

Gap interpretation:
- Lender reserve **materially below** implied → proforma under-reserves; NOI and value overstated.
  Quantify: `gap_$ = (implied_PUPY - lender_PUPY) * units`; value impact `= NOI_impact / cap_rate`.
- Lender reserve **above** implied → conservative (often agency/HUD) sizing; compresses cash-on-cash but
  de-risks capital. Note as conservative, not as error.

---

## 8. Contingency guidance on the immediate-repair total

| PCA report quality | Contingency on immediate total |
|---|---|
| Detailed PCA with quantities + unit costs | 5 - 10% |
| Limited PCA, partial quantities | 10 - 15% |
| Walk-through only, no quantities | 15 - 25% (and label costs order-of-magnitude) |

Lender escrow at closing for immediates is commonly 100 - 125% of the estimate; show both the estimate
and the escrow figure.

---

## 9. Common PCA scope exclusions (treat as diligence issues, not zeros)

Absence of a line in the PCA is not absence of cost. Frequently out of scope:
- Roof interior / underlayment condition (only surface observed)
- In-unit components (residential), unless a unit-by-unit was commissioned
- Structural adequacy / load testing
- Environmental (separate Phase I/II ESA; see `dd-command-center`)
- ADA / accessibility full audit
- MEP capacity / load (often visual only)

For each excluded system, the skill lists a prioritized diligence issue with a recommended specialist
scope rather than recording a $0 cost.
