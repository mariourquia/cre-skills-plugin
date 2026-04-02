# Stacking Plan Format Guide

## Purpose

A stacking plan is a floor-by-floor visual representation of a building's tenant occupancy, lease terms, and space utilization. In text-based format, it provides a quick snapshot of the building without requiring CAD or graphical software. This guide defines the standard text-based format with color-coding conventions and includes a worked 10-floor example.

## Format Structure

### Building Header
```
==================================================================
STACKING PLAN: [Property Name]
Address: [Full address]
Total SF: [Rentable SF]  |  Floors: [Count]  |  Date: [YYYY-MM-DD]
Occupancy: [Phys %] Physical / [Econ %] Economic
WALE: [X.X] years  |  Top Tenant: [Name] ([%] of NRA)
==================================================================
```

### Floor Block Format

Each floor is represented as a horizontal block. Tenants occupy proportional width based on their share of the floor's rentable SF. The block reads left-to-right.

```
Floor [N] | [Total SF] SF | [Occupied %]%
|--- Tenant A (Suite XXX) ---|--- Tenant B (Suite YYY) ---|- VACANT -|
|   [SF] SF | $[Rent]/SF    |   [SF] SF | $[Rent]/SF     | [SF] SF  |
|   Exp: [MM/YY]            |   Exp: [MM/YY]              |          |
```

### Width Proportionality

Tenant width in the diagram is proportional to their share of floor SF. Guidelines:
- Minimum display width: 20 characters (even for small suites)
- Maximum display width: 70 characters (even for full-floor tenants)
- Total floor width: 70 characters

### Color Coding Conventions (for terminals and text with ANSI support)

Since this is text-based, use status markers instead of colors when ANSI is not available:

| Status | Marker | ANSI Color | Meaning |
|---|---|---|---|
| Long-term occupied (3+ yr remaining) | `[+]` | Green | Stable income, low rollover risk |
| Mid-term occupied (1-3 yr remaining) | `[~]` | Blue | Monitor for renewal |
| Short-term occupied (<1 yr remaining) | `[!]` | Yellow | Imminent rollover risk |
| Month-to-month | `[M]` | Orange | No lease security |
| Vacant - available | `[V]` | Red | No income, actively marketing |
| Vacant - down for renovation | `[D]` | Gray | No income, planned return |
| Sublet / sublease | `[S]` | Purple | Tenant risk (not direct relationship) |
| Owner-occupied / management | `[O]` | White | Non-revenue space |

### Information Density Levels

**Level 1: Summary (for executive reports)**
- Floor number, total SF, occupancy %, largest tenant name

**Level 2: Standard (for asset management)**
- Floor number, all tenants with suite, SF, rent/SF, expiration date, status marker

**Level 3: Detailed (for leasing and DD)**
- Everything in Level 2 plus: escalation terms, renewal options, TI remaining, tenant credit rating

## Worked Example: 10-Floor Office Building

### Property Summary
```
==================================================================
STACKING PLAN: Metropolitan Tower
Address: 500 Commerce Street, Nashville, TN 37203
Total SF: 185,000 RSF  |  Floors: 10  |  Date: 2026-03-17
Occupancy: 87.6% Physical / 84.2% Economic
WALE: 4.2 years  |  Top Tenant: Pinnacle Financial (22.2% of NRA)
Avg In-Place Rent: $28.50/SF NNN  |  Market Rent: $32.00/SF NNN
==================================================================
```

### Floor-by-Floor Stacking Plan (Level 2)

```
FLOOR 10 | Penthouse | 15,000 SF | 100% Occupied
+----------------------------------------------------------------------+
| [+] PINNACLE FINANCIAL PARTNERS - Suite 1000                         |
|     15,000 SF | $34.00/SF NNN | Exp: 12/2030 | 4.8 yr remaining     |
|     Full floor. Renewed 2025. 2x5yr options at 95% FMV.              |
+----------------------------------------------------------------------+

FLOOR 9 | 18,000 SF | 100% Occupied
+----------------------------------------------------------------------+
| [+] PINNACLE FINANCIAL PARTNERS - Suite 900                          |
|     18,000 SF | $33.50/SF NNN | Exp: 12/2030 | 4.8 yr remaining     |
|     Full floor. Contiguous with Floor 10. Same lease.                 |
+----------------------------------------------------------------------+

FLOOR 8 | 18,000 SF | 100% Occupied
+----------------------------------------------------------------------+
| [~] BASS BERRY & SIMS LLP - Suite 800          | [+] WALLER LLP     |
|     12,000 SF | $31.00/SF NNN | Exp: 06/2028   | 6,000 SF           |
|     2.3 yr remaining. 1x5yr option at FMV.      | $32.50/SF NNN      |
|                                                  | Exp: 03/2031       |
|                                                  | 5.0 yr remaining   |
+----------------------------------------------------------------------+

FLOOR 7 | 18,000 SF | 83.3% Occupied
+-------------------------------------------------+--------------------+
| [!] DELOITTE - Suite 700                        | [V] VACANT         |
|     15,000 SF | $29.00/SF NNN | Exp: 09/2026   |     3,000 SF       |
|     0.5 yr remaining. No renewal indication.    |     Suite 710      |
|     RISK: May downsize or relocate.             |     Asking $32/SF  |
|     Subletting 2,000 SF (Suite 705).            |     Available now   |
+-------------------------------------------------+--------------------+

FLOOR 6 | 20,000 SF | 100% Occupied
+----------------------------------------------------------------------+
| [+] HEALTHCARE REALTY TRUST - Suite 600                              |
|     20,000 SF | $30.00/SF NNN | Exp: 08/2029 | 3.4 yr remaining     |
|     Full floor. REIT HQ. Critical operations. High renewal prob.     |
+----------------------------------------------------------------------+

FLOOR 5 | 20,000 SF | 75.0% Occupied
+---------------------------------+---------------------------------+---+
| [~] FROST BROWN TODD - Ste 500 | [V] VACANT                     |   |
|     10,000 SF | $28.00/SF NNN  |     8,000 SF | Suite 510        |   |
|     Exp: 12/2027               |     Asking $31.00/SF NNN        |   |
|     1.8 yr remaining           |     Available now                |   |
|     1x3yr option at CPI adj.   |     Showing activity: 3 tours   |   |
+---------------------------------+                                 |   |
| [M] STARTUP CO - Suite 520                                        |   |
|     2,000 SF | $26.00/SF NNN | Month-to-month                    |   |
|     Converted from 12-mo lease. May vacate with 30-day notice.    |   |
+-------------------------------------------------------------------+---+

FLOOR 4 | 20,000 SF | 100% Occupied
+----------------------------------------------------------------------+
| [+] PINNACLE FINANCIAL PARTNERS - Suite 400                          |
|     8,000 SF | $29.00/SF NNN | Exp: 12/2030 | 4.8 yr remaining      |
|     Back office / operations. Same master lease as Fl 9-10.          |
+--------------------------------------+-------------------------------+
| [~] GRANT THORNTON - Suite 410       | [!] REGUS / IWG - Suite 420  |
|     7,000 SF | $27.50/SF NNN         |     5,000 SF | $25.00/SF NNN |
|     Exp: 03/2028 | 2.0 yr remaining  |     Exp: 06/2026             |
|     Audit practice. Stable.          |     0.3 yr remaining          |
|                                      |     Coworking sublicense.     |
|                                      |     RISK: Will not renew.     |
+--------------------------------------+-------------------------------+

FLOOR 3 | 20,000 SF | 85.0% Occupied
+--------------------------------------+-------------------------------+
| [~] BONE MCALLESTER NORTON - Ste 300 | [!] KPMG - Suite 310         |
|     10,000 SF | $27.00/SF NNN        |     7,000 SF | $26.00/SF NNN |
|     Exp: 09/2028 | 2.5 yr remaining  |     Exp: 12/2026             |
|     Law firm. 20-yr occupant.        |     0.8 yr remaining          |
|     High renewal probability.        |     Downsizing from 7k to 4k  |
|                                      |     or relocating. LOI out.   |
+--------------------------------------+-------------------------------+
| [V] VACANT - Suite 320                                               |
|     3,000 SF | Asking $30.00/SF NNN | Available now                  |
|     Previously occupied by small law firm (vacated 01/2026).          |
+----------------------------------------------------------------------+

FLOOR 2 | 18,000 SF | 72.2% Occupied
+---------------------------------+------------------------------------+
| [+] NASHVILLE SURGICAL CTR     | [V] VACANT                        |
|     Suite 200                   |     5,000 SF | Suite 210           |
|     13,000 SF | $26.00/SF MG   |     Asking $29.00/SF NNN           |
|     Exp: 05/2031               |     Available now                   |
|     5.2 yr remaining            |     Build-out required ($35/SF TI) |
|     Medical use. Specialized    |     Targeting medical/dental user   |
|     build-out. Very sticky.     |                                    |
+---------------------------------+------------------------------------+

FLOOR 1 | 18,000 SF | 88.9% Occupied
+--------------------------------------------+-------------------------+
| [+] LOBBY + MANAGEMENT OFFICE              | [~] CORNER BAKERY CAFE  |
|     [O] 6,000 SF | Non-revenue             |     Suite 110           |
|     Building lobby, mailroom, security,     |     4,000 SF            |
|     management office, fitness center.      |     $38.00/SF NNN       |
|                                             |     Exp: 12/2028        |
+--------------------------------------------+     2.8 yr remaining   |
| [~] REGIONS BANK - Suite 120               |     Pct rent above $2M  |
|     6,000 SF | $36.00/SF NNN               |     F&B amenity value.  |
|     Exp: 06/2028 | 2.3 yr remaining        |                         |
|     Branch operations. Drive-thru access.   |                         |
|     1x5yr option at FMV.                    |                         |
+--------------------------------------------+-------------------------+
| [V] VACANT - Suite 130                                                |
|     2,000 SF | Asking $35.00/SF NNN | Ground-floor retail frontage   |
|     Street visibility. Targeting service retail or F&B.               |
+----------------------------------------------------------------------+
```

### Summary Statistics
```
==================================================================
ROLLOVER SCHEDULE (by year)
------------------------------------------------------------------
Year     | SF Expiring | % of NRA | Revenue at Risk | Weighted Rent
---------|-------------|----------|-----------------|-------------
2026     | 27,000      | 14.6%    | $726,000        | $26.89/SF
2027     | 10,000      | 5.4%     | $280,000        | $28.00/SF
2028     | 39,000      | 21.1%    | $1,137,500      | $29.17/SF
2029     | 20,000      | 10.8%    | $600,000        | $30.00/SF
2030     | 41,000      | 22.2%    | $1,319,500      | $32.18/SF
2031     | 13,000      | 7.0%     | $338,000        | $26.00/SF
M-T-M    | 2,000       | 1.1%     | $52,000         | $26.00/SF
Vacant   | 21,000      | 11.4%    | --              | --
No Lease | 6,000       | 3.2%     | --              | (mgmt/lobby)
---------|-------------|----------|-----------------|-------------
Total    | 185,000     | 100%     | $4,453,000      | $28.50/SF

TENANT CONCENTRATION
------------------------------------------------------------------
Tenant                    | SF      | % NRA  | Annual Rent | % Rev
--------------------------|---------|--------|-------------|------
Pinnacle Financial        | 41,000  | 22.2%  | $1,319,500  | 29.6%
Healthcare Realty Trust   | 20,000  | 10.8%  | $600,000    | 13.5%
Deloitte                  | 15,000  | 8.1%   | $435,000    | 9.8%
Bass Berry & Sims         | 12,000  | 6.5%   | $372,000    | 8.4%
Nashville Surgical Center | 13,000  | 7.0%   | $338,000    | 7.6%
All others                | 63,000  | 34.1%  | $1,388,500  | 31.2%
Vacant                    | 21,000  | 11.4%  | --          | --
==================================================================

KEY RISKS
------------------------------------------------------------------
[!] Deloitte (Fl 7, 15,000 SF) - Expires 09/2026, no renewal signal
[!] Regus/IWG (Fl 4, 5,000 SF) - Expires 06/2026, will not renew
[!] KPMG (Fl 3, 7,000 SF) - Expires 12/2026, downsizing/relocating
[M] Startup Co (Fl 5, 2,000 SF) - Month-to-month, flight risk

Total at-risk SF (12 months): 29,000 SF (15.7% of NRA)
Worst-case vacancy if all at-risk vacate: 50,000 SF (27.0%)
==================================================================
```

## Layout Guidelines

### Proportional Width Rules
- Each floor line is 70 characters wide (excluding border characters)
- Tenant width = ROUND(tenant_sf / floor_sf * 70) characters
- Minimum tenant display width: 20 characters
- If a tenant occupies less than 20 characters worth of proportional space, expand to 20 and compress the largest tenant

### Multi-Tenant Floor Layout
- Separate tenants with `|` (pipe) characters
- Place tenants left-to-right in suite number order
- Vacant spaces always displayed on the right side
- If more than 4 tenants on a floor, use a condensed format:

```
FLOOR N | XX,000 SF | XX% Occupied
| Tenant A (5,000 SF) | Tenant B (3,000 SF) | Tenant C (2,000 SF) | VACANT (2,000 SF) |
| $28/SF Exp:12/28 [~]| $30/SF Exp:03/29 [+]| $25/SF MTM [M]      | Asking $30/SF     |
```

### Building Orientation
- Stack floors top-to-bottom (highest floor at top of diagram)
- This mirrors the physical building and is the industry convention
- Basement/parking levels can be shown below Floor 1 if relevant

### Information Hierarchy
For each tenant, display in this order:
1. Status marker and tenant name
2. Suite number
3. Square footage
4. Rent per SF and lease type
5. Expiration date and remaining term
6. Key notes (renewal options, risk flags, special terms)

### Highlighting Risk
Use inline annotations for risk items:
- `RISK:` prefix for items requiring attention
- `NOTE:` prefix for informational items
- `OPP:` prefix for opportunity items (below-market rent, expansion potential)
