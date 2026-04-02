# Settlement Statement Template

Reference for the funds-flow-calculator skill. ALTA settlement statement format with line-by-line annotations. Use this structure for all commercial real estate acquisition closings. The HUD-1 form is legacy (residential); commercial transactions use ALTA or custom closing statements. Both have the same two-column logic: buyer debits/credits and seller debits/credits.

---

## Part I: Statement Header

```
CLOSING / SETTLEMENT STATEMENT
================================================================================
Property Address:    123 Main Street, New York, NY 10001
Closing Date:        March 15, 2026
Closing Location:    [Title Company or Attorney Office]
Prepared By:         [Title Company Name]
Settlement Agent:    [Agent Name and License Number]
File Number:         [Title File #]
================================================================================
BUYER:               123 Main Acquisition LLC (a Delaware limited liability company)
Buyer's Counsel:     [Law Firm, Atty Name, Address]
Buyer's Lender:      [Lender Name]
Loan Amount:         $11,250,000
Loan Number:         [Lender Loan #]

SELLER:              123 Main Holdings LLC (a New York limited liability company)
Seller's Counsel:    [Law Firm, Atty Name, Address]
================================================================================
PURCHASE PRICE:      $15,000,000.00
CLOSING DATE:        March 15, 2026
```

---

## Part II: Full Statement (Buyer Column + Seller Column)

The statement is divided into two columns. Every line shows the buyer's impact (Debit = buyer pays more; Credit = buyer pays less) and the seller's impact (Debit = seller receives less; Credit = seller receives more).

```
                                                BUYER                SELLER
LINE ITEM                              DEBIT       CREDIT     DEBIT       CREDIT
================================================================================
PURCHASE PRICE AND CONTRACT TERMS
================================================================================
100. Gross purchase price             $15,000,000.00           -        $15,000,000.00
     [Purchase price is a buyer debit (buyer owes) and a seller credit (seller receives)]

================================================================================
200. AMOUNTS PAID BY OR ON BEHALF OF BUYER (CREDITS TO BUYER)
================================================================================
201. Loan amount (senior mortgage)                $11,250,000.00
     [Lender funds this; reduces buyer's equity requirement]

202. Earnest money paid               -           $300,000.00
     [Buyer already wired earnest money; credited against purchase price at closing]

203. Rent proration (credit from seller)           $68,548.00
     [Seller collected March rent; buyer's share for Mar 15-31]

204. Security deposit transfer         -           $67,500.00
     [Seller transfers cash deposits; buyer assumes liability to tenants]

205. Seller credit: [DD concession]    -                 $0
     [If applicable; describe nature of credit]

SUBTOTAL BUYER CREDITS:              $11,686,048.00

================================================================================
300. AMOUNTS OWED BY BUYER (DEBITS TO BUYER)
================================================================================
301. Loan origination fee (1.0%)      $112,500.00
302. Tax reserve escrow (3 months)     $45,000.00
303. Insurance reserve (2 months)       $1,500.00
304. DSCR / replacement reserve        $30,938.00
305. Prepaid interest (17 days)        $29,219.00
     [Mar 15-31; $11.25M * 5.5% / 360 * 17 = $29,219 bank method]
306. Owner's title insurance            $42,000.00
307. Lender's title insurance           $18,750.00
308. Recording fee -- deed               $1,500.00
309. Recording fee -- mortgage             $500.00
310. Legal fees -- buyer counsel        $15,000.00
311. Survey                              $4,500.00
312. Phase I Environmental               $4,500.00
313. Appraisal                           $8,500.00
314. UCC search                            $800.00
315. Tax certificate                       $400.00
316. Settlement fee (50%)               $1,500.00
317. Property tax proration              $36,000.00
     [Seller's period Jan 1 - Mar 14; seller credits buyer this amount;
      shown as buyer debit here = seller owes buyer; sign convention varies by form]

SUBTOTAL BUYER DEBITS (excl. purchase price): $352,607.00

================================================================================
BUYER CASH TO CLOSE CALCULATION
================================================================================
Gross amount owed by buyer:                       $15,352,607.00
Less: buyer credits (line 200 subtotal):          $11,686,048.00
                                                  ---------------
NET CASH TO CLOSE (buyer must wire):               $3,666,559.00
Less: earnest money (already wired):                ($300,000.00)
                                                  ---------------
ADDITIONAL WIRE REQUIRED AT CLOSING:               $3,366,559.00
================================================================================

================================================================================
400. AMOUNTS OWED BY SELLER (DEBITS TO SELLER)
================================================================================
401. Existing mortgage payoff          $8,757,290.00
     [Per payoff letter including per diem for 5 extra days]
402. Prepayment penalty                       $0.00
     [In this example, loan in open period; no prepayment]
403. Broker commission (2.5%)            $375,000.00
404. Transfer tax -- NY State             $60,000.00
     [$15M * 0.40%]
405. Transfer tax -- NYC                 $213,750.00
     [$15M * 1.425%]
406. Legal fees -- seller counsel         $12,000.00
407. Settlement fee (50%)                  $1,500.00
408. Mortgage satisfaction recording fee     $500.00
     [Fee to record release of seller's mortgage]
409. Property tax proration               $36,000.00
     [Seller owes buyer for Jan 1 - Mar 14 period (73 days)]
410. Rent proration                       $68,548.00
     [Seller collected full March rent; must remit buyer's share]
411. Security deposit transfer            $67,500.00
     [Seller transfers cash deposits to buyer]

SUBTOTAL SELLER DEBITS:              $9,592,088.00

================================================================================
500. AMOUNTS OWED TO SELLER (CREDITS TO SELLER)
================================================================================
[No additional credits to seller in this transaction]
Gross sale price (from line 100):   $15,000,000.00

================================================================================
SELLER NET PROCEEDS CALCULATION
================================================================================
Gross sale price:                                 $15,000,000.00
Less: seller debits (line 400 subtotal):          ($9,592,088.00)
                                                  ---------------
NET PROCEEDS TO SELLER:                            $5,407,912.00
[Wire to seller entity or to QI if 1031 exchange]
================================================================================

================================================================================
SOURCES AND USES VERIFICATION
================================================================================
TOTAL INTO ESCROW:
  Buyer equity wire (additional):                 $3,366,559
  Earnest money (already in escrow):               $300,000
  Loan proceeds (lender wire):                  $11,250,000
  --------------------------------------------------------
  TOTAL SOURCES:                                $14,916,559

TOTAL OUT OF ESCROW:
  Net proceeds to seller:                        $5,407,912
  Existing mortgage payoff:                      $8,757,290
  Broker commission:                               $375,000
  Transfer taxes (title remits):                   $273,750
  Settlement fee:                                   $3,000
  Recording fees:                                   $2,500
  Mortgage satisfaction recording:                    $500
  Buyer costs advanced through title:                96,607
  [Origination, reserves, insurance, survey, Phase I,
   legal, appraisal, UCC, tax cert = $96,607]
  --------------------------------------------------------
  TOTAL DISBURSEMENTS:                          $14,916,559

BALANCE:                                                 $0  [VERIFIED]
```

---

## Part III: Line-Item Annotations

The annotations below explain the logic of each section for audit purposes.

### Purchase Price (Lines 100-199)

The purchase price simultaneously creates the largest debit on the buyer side (what buyer owes) and the largest credit on the seller side (what seller will receive). Every other line modifies this starting point.

### Buyer Credits (Lines 200-299)

Credits reduce the buyer's cash-to-close obligation. The three primary credits are:
1. **Loan proceeds**: lender provides this; dramatically reduces buyer's equity requirement
2. **Earnest money**: already paid; buyer gets credit to avoid paying twice
3. **Prorations and deposits**: seller-owed adjustments that flow as credits to buyer

A credit to buyer is simultaneously a debit to the escrow disbursement (the money source changes, not the total).

### Buyer Debits (Lines 300-399)

Every buyer cost beyond the purchase price is listed here. The sum of purchase price + buyer debits = buyer's total obligation. Subtracting all buyer credits = net cash to close.

**Prepaid interest calculation detail**:
```
Formula: Loan balance * annual rate / days-in-year * days in stub period

Stub period: from closing day through last day of closing month
If closing March 15: stub period = 17 days (March 15 through March 31)
First full monthly payment due May 1 (covers April 1-30)
Prepaid covers the closing-month stub

Actual/365: $11,250,000 * 5.50% / 365 * 17 = $28,836
Actual/360: $11,250,000 * 5.50% / 360 * 17 = $29,219
Confirm method with lender payoff/closing instructions.
```

### Seller Debits (Lines 400-499)

Every cost charged against the seller's proceeds. The mortgage payoff is usually the largest line item. Together these define what is deducted from the sale price before the seller receives net proceeds.

**Payoff letter reconciliation**:
```
Payoff letter good-through: March 10, 2026
Payoff amount as of March 10: [stated in payoff letter]
Per diem: $X/day
Closing date: March 15 (5 days after good-through)
Adjustment: 5 * per diem = additional interest owed
Adjusted payoff = letter amount + additional interest
Enter adjusted payoff on Line 401.
```

### Net Proceeds to Seller (Lines 500-599)

After all seller debits, the remaining balance is the seller's net proceeds. This is the wire amount to seller (or QI if 1031 exchange).

---

## Part IV: Proration Line Detail

Always show the proration calculation methodology in a supporting schedule. The settlement statement line item only shows the net dollar amount; the supporting schedule shows the arithmetic.

```
PRORATION SUPPORTING SCHEDULE
=============================
Method: Actual/365 per PSA Section __

Item 1: Property Tax Proration
  Annual tax bill: $180,000 (2026 calendar year, paid in arrears)
  Daily rate: $180,000 / 365 = $493.15
  Seller period: January 1 - March 14, 2026 = 73 days
  Seller's share: 73 * $493.15 = $36,000 (rounded)
  Direction: SELLER DEBIT / BUYER CREDIT

Item 2: Rent Proration -- all units
  Total monthly rent collected: $125,000 (March 1, 2026)
  Seller period: March 1-14 = 14 days
  Buyer period: March 15-31 = 17 days
  Days in March: 31
  Buyer's portion: $125,000 * 17/31 = $68,548 (rounded)
  Direction: SELLER DEBIT / BUYER CREDIT

Item 3: Security Deposit Transfer
  45 tenants, $1,500 average: $67,500 total (all cash)
  All matched to estoppels: no discrepancies
  Direction: SELLER DEBIT / BUYER CREDIT (buyer assumes liability)

PRORATION TOTAL (SELLER DEBITS / BUYER CREDITS):
  Property tax:     $36,000
  Rent:            $68,548
  Security deposits: $67,500
  TOTAL:          $172,048
```

---

## Part V: Wire Disbursement Schedule

After settlement statement is approved, title company prepares disbursement schedule:

```
DISBURSEMENT AUTHORIZATION
==========================
Authorized by: [Buyer counsel] and [Seller counsel]
Date authorized: March 15, 2026

Wire 1: Net proceeds to seller
  Payee: 123 Main Holdings LLC
  ABA: [routing number]
  Account: [account number]
  Amount: $5,407,912.00
  Reference: 123 Main Street closing 3/15/2026
  Timing: Same day after recording confirmed

Wire 2: Existing mortgage payoff
  Payee: [Existing Lender Name]
  ABA: [routing number]
  Account: [payoff account per payoff letter]
  Amount: $8,757,290.00
  Reference: Loan # [xxxx] payoff
  Timing: Before seller proceeds wire

Wire 3: Broker commission
  Payee: [Brokerage Name]
  ABA: [routing number]
  Account: [account number]
  Amount: $375,000.00
  Reference: Commission -- 123 Main Street
  Timing: Same day

Wire 4: Transfer tax (NYC)
  Payee: NYC Department of Finance
  Amount: $213,750.00
  Method: [Per title company filing procedure]
  Timing: At recording

Wire 5: Transfer tax (NY State)
  Payee: NYS Tax and Finance
  Amount: $60,000.00
  Method: Per title company
  Timing: At recording

[Additional wires for legal fees, etc. per payee invoice instructions]
```

---

## Part VI: Execution and Approval

The settlement statement must be reviewed and approved by both buyer and seller (or their counsel) before any documents are released for recording or any wires are sent.

```
APPROVAL SIGNATURES
===================
BUYER acknowledges and approves this settlement statement:

Signature: ______________________ Date: __________
Name:      ______________________ Title: __________
Entity:    123 Main Acquisition LLC

SELLER acknowledges and approves this settlement statement:

Signature: ______________________ Date: __________
Name:      ______________________ Title: __________
Entity:    123 Main Holdings LLC

Prepared by:
[Title Company Name]
Settlement Agent: ______________________
License #: ______________________________
Date Prepared: March 14, 2026 (final draft)
Date of Closing: March 15, 2026
```

---

## Part VII: Common Settlement Statement Errors

| Error Type | Description | Detection | Resolution |
|---|---|---|---|
| Proration sign reversal | Tax proration shown as seller credit instead of debit | Cross-check: taxes in arrears = seller debit | Flip sign; re-verify balance |
| Double-counted earnest money | Earnest money listed as both a source and a buyer credit | Sources and uses don't balance | Remove from sources OR credits (not both) |
| Missing reserve line | Lender reserve not included in buyer debits | Cash-to-close understated; lender will flag | Add reserve lines per lender commitment |
| Wrong payoff amount | Using payoff letter amount without per-diem adjustment | Payoff letter good-through date is before closing | Apply per-diem for additional days |
| Transfer tax on wrong party | State convention differs from PSA allocation | Seller/buyer both think the other pays | Cross-reference PSA and state law |
| LOC deposits shown as cash credit | LOC deposits not yet transferred; buyer receives cash credit without asset | Deposit schedule shows LOC, not cash | Remove LOC from cash credit; add escrow for pending transfer |
| Rounding error cumulation | Many small rounding errors aggregate to >$100 | Final balance check | Round each line consistently; reconcile total |
| Prepaid interest wrong stub period | Counting days of prepaid from wrong start date | Calendar day count | Count from actual closing day through month-end |
