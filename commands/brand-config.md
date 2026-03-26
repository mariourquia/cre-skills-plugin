---
name: brand-config
description: "Configure or update your organization's brand guidelines for CRE deliverables (pitch decks, IC memos, investor updates, offering packages). Saved locally at ~/.cre-skills/brand-guidelines.json for automatic reuse across all deliverable skills."
---

# Brand Guidelines Configurator

You are setting up or updating brand guidelines for CRE deliverable production. These settings are saved locally at `~/.cre-skills/brand-guidelines.json` and auto-loaded by all skills that produce investor-facing documents: pitch decks, IC memos, quarterly LP updates, capital raise materials, offering packages, and leasing marketing materials.

## Step 1: Check Existing Configuration

Check whether `~/.cre-skills/brand-guidelines.json` exists:

```bash
cat ~/.cre-skills/brand-guidelines.json 2>/dev/null
```

**If the file exists**, display the current settings in a readable summary table:

| Setting | Current Value |
|---------|--------------|
| Company/Fund Name | ... |
| Primary Color | ... |
| Secondary Color | ... |
| Accent Color | ... |
| Heading Font | ... |
| Body Font | ... |
| Layout Style | ... |
| Number Format | ... |
| Units Preference | ... |
| Logo Path | ... |
| Tagline | ... |
| Disclaimer | (truncated to 80 chars) |
| Confidentiality Notice | (truncated to 80 chars) |
| Contact Block | ... |

Then ask: **"What would you like to update? You can say a field name, 'all' to redo the full setup, or 'done' to keep current settings."**

Handle partial updates: only re-ask for fields the user specifies, then merge with existing JSON before saving.

**If the file does not exist**, proceed with the full guided setup below.

---

## Step 2: Guided Setup (New Configuration)

Walk through the following questions one section at a time. Do not ask all questions at once -- group them into logical sections and wait for user responses before proceeding.

### Section A: Identity

1. **Company or fund name**: What is your company or fund name as it should appear on all deliverables?
   - Example: "Apex Capital Partners" or "Mesa Verde Fund III"

2. **Tagline or motto** *(optional)*: Do you have a tagline or positioning statement for your firm?
   - Example: "Institutional-Grade Real Estate for the Modern Investor"
   - Press Enter to skip.

### Section B: Visual Identity

3. **Primary color** (hex code): What is your primary brand color?
   - Example: `#1B365D` (navy), `#2C5F2E` (forest green), `#8B0000` (dark red)
   - If unsure, enter `default` to use institutional navy `#1B365D`.

4. **Secondary color** (hex code): What is your secondary brand color?
   - Example: `#FFFFFF` (white), `#F5F5F5` (off-white), `#C9A84C` (gold)
   - If unsure, enter `default` for white `#FFFFFF`.

5. **Accent color** (hex code): What is your accent/highlight color (used for callouts, key numbers, headings)?
   - Example: `#C9A84C` (gold), `#4A90D9` (blue), `#E8633A` (terracotta)
   - If unsure, enter `default` for gold `#C9A84C`.

6. **Logo file path** *(optional)*: What is the local file path to your logo? (Used as a reference -- not embedded in output.)
   - Example: `~/Documents/brand/logo.png`
   - Press Enter to skip.

### Section C: Typography

7. **Font preferences**: Do you have specific font preferences, or use defaults?
   - Enter `default` to use Helvetica Neue (headings) / Arial (body) -- universally available.
   - Or specify: heading font name, body font name.
   - Example: `Garamond, Calibri` or `Montserrat, Open Sans`

### Section D: Layout Style

8. **Preferred layout style**: Which describes your firm's presentation aesthetic?
   - `minimal` -- clean white space, data-forward, minimal graphics
   - `corporate` -- structured, grid-based, heavy use of tables and charts
   - `boutique` -- editorial feel, larger type, bold section breaks, some imagery guidance
   - `institutional` -- dense, comprehensive, GIPS-style reporting with full disclosure blocks
   - Enter the keyword or press Enter for `corporate` (default).

### Section E: Number Formatting

9. **Number format preference**: How do you prefer to display dollar amounts?
   - `full` -- $1,234,567 (full numbers, best for IC memos and precise documents)
   - `abbreviated` -- $1.2M / $2.5B (best for pitch decks and summaries)
   - `both` -- show abbreviated in headers/callouts, full in tables (recommended)
   - Enter the keyword or press Enter for `both` (default).

10. **Units preference**: When reporting commercial RE metrics, do you prefer:
    - `psf` -- per square foot ($/SF) for all commercial asset types
    - `per_unit` -- per unit for multifamily, $/SF for commercial
    - `auto` -- auto-select based on asset type (recommended)
    - Enter the keyword or press Enter for `auto` (default).

### Section F: Legal & Compliance Language

11. **Disclaimer / legal footer text**: Enter the standard disclaimer text to appear at the bottom of every investor-facing document.
    - Press Enter to use the professional default:
      > "This document is for informational purposes only and does not constitute an offer to sell or a solicitation of an offer to buy any security. Past performance is not indicative of future results. All projections are forward-looking and subject to change."

12. **Confidentiality notice**: Enter the confidentiality notice to appear on the cover/first page of sensitive materials.
    - Press Enter to use the professional default:
      > "CONFIDENTIAL -- This document contains proprietary and confidential information. Distribution or reproduction without prior written consent is prohibited."

### Section G: Contact Information

13. **Contact information block**: Enter the contact block to appear on the final page of deliverables.
    Format as:
    ```
    Name: [Your Name]
    Title: [Your Title]
    Phone: [Phone Number]
    Email: [Email Address]
    Address: [Office Address]
    Website: [Website URL]
    ```
    Press Enter to skip (contact block will be omitted from deliverables).

---

## Step 3: Save Configuration

After collecting all responses, construct the JSON and save it:

```bash
mkdir -p ~/.cre-skills
```

Write the following structure to `~/.cre-skills/brand-guidelines.json`:

```json
{
  "version": "1.0",
  "last_updated": "<ISO 8601 date>",
  "identity": {
    "company_name": "<value or null>",
    "tagline": "<value or null>"
  },
  "colors": {
    "primary": "<hex or #1B365D>",
    "secondary": "<hex or #FFFFFF>",
    "accent": "<hex or #C9A84C>"
  },
  "typography": {
    "heading_font": "<value or Helvetica Neue>",
    "body_font": "<value or Arial>"
  },
  "logo_path": "<path or null>",
  "layout_style": "<minimal|corporate|boutique|institutional>",
  "number_format": "<full|abbreviated|both>",
  "units_preference": "<psf|per_unit|auto>",
  "legal": {
    "disclaimer": "<text>",
    "confidentiality_notice": "<text>"
  },
  "contact": {
    "name": "<value or null>",
    "title": "<value or null>",
    "phone": "<value or null>",
    "email": "<value or null>",
    "address": "<value or null>",
    "website": "<value or null>"
  }
}
```

Run the write command:

```bash
cat > ~/.cre-skills/brand-guidelines.json << 'BRAND_EOF'
<constructed JSON>
BRAND_EOF
```

---

## Step 4: Confirm and Summarize

After saving, display a confirmation:

> "Brand guidelines saved to `~/.cre-skills/brand-guidelines.json`."

Then show a clean summary table of all saved values.

Finally, show which skills will now auto-load these guidelines:

> "These guidelines will be auto-applied to: **LP Pitch Deck Builder**, **IC Memo Generator**, **Quarterly Investor Update**, **Capital Raise Machine**, **Fund Formation Toolkit**, **Disposition Prep Kit**, **Investor Lifecycle Manager**, and **Leasing Strategy & Marketing Planner**."

---

## Notes

- The file is local to the user's machine and never transmitted anywhere.
- To reset to defaults, delete `~/.cre-skills/brand-guidelines.json` and re-run `/cre-skills:brand-config`.
- Individual skills can accept inline `brand_guidelines` overrides at invocation time, which take precedence over the saved file.
- The `version` field allows future migrations when the schema evolves.
