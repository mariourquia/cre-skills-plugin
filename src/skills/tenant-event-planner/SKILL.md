---
name: tenant-event-planner
slug: tenant-event-planner
version: 0.1.0
status: deployed
category: reit-cre
description: "Plans, budgets, and executes tenant appreciation events, seasonal programming, and community engagement for CRE properties. Supports API-driven vendor booking when MCP integrations are available. Triggers: tenant event, appreciation event, holiday party, tenant engagement, community event, property event planning, seasonal programming."
targets:
  - claude_code
---

# Tenant Event Planner

Plans, budgets, and coordinates tenant appreciation events, seasonal programming, and community engagement activities for commercial real estate properties. Operates in two modes: plan-only (current) and plan-and-book (future API-integrated via MCP servers).

## When to Activate

Trigger this skill when the user asks about:
- Tenant appreciation events or programming
- Holiday parties or seasonal events at a property
- Community engagement or tenant retention through events
- Event budgeting for CRE properties
- Vendor booking or coordination for property events
- Move-in welcome packages or milestone celebrations
- Wellness fairs, food trucks, networking mixers
- ROI analysis for tenant event spending

Keywords: tenant event, appreciation event, holiday party, tenant engagement, community event, property event planning, seasonal programming, tenant retention events, vendor booking.

## Input Schema

```yaml
property:
  name: string                    # Property name
  type: enum [multifamily, office, mixed_use, retail, industrial]
  units_or_tenants: integer       # Number of units (MF) or tenant companies (office)
  total_occupants: integer        # Estimated headcount across all tenants
  sf: integer                     # Total leasable SF
  class: enum [A, B, C]           # Property class
  amenity_spaces: list[string]    # Available on-site spaces (lobby, rooftop, courtyard, conference center, pool deck)
  location_metro: string          # Metro area for vendor search radius

event_request:
  event_type: enum [appreciation, seasonal, wellness, networking, community, holiday, move_in_welcome, milestone, food_truck, pet_friendly, kids_family, outdoor_movie, charity, decoration_reveal]
  budget:
    total: float                  # Total budget in USD
    # OR
    per_unit: float               # Budget per unit/tenant
    currency: string              # Default USD
  target_date: date               # Preferred event date
  season: enum [spring, summer, fall, winter]  # If no specific date
  duration_hours: float           # Expected event duration
  indoor_outdoor: enum [indoor, outdoor, hybrid]

tenant_demographics:              # Optional
  type: enum [residential, commercial, mixed]
  family_friendly: boolean
  corporate_formality: enum [casual, business_casual, formal]
  pet_friendly: boolean
  dietary_considerations: list[string]  # vegetarian, vegan, halal, kosher, gluten-free, nut-free
  age_distribution: enum [young_professional, mixed_age, family_heavy, senior]

execution_mode: enum [plan_only, plan_and_book]
# plan_only: generate full event plan with vendor specs and RFP templates
# plan_and_book: (future) execute vendor search, quoting, and booking via MCP tools

vendor_preferences:               # Optional
  preferred_vendors: list[string] # Vendor names to prioritize
  excluded_vendors: list[string]  # Vendors to avoid
  max_vendor_count: integer       # Cap on number of vendors to engage
  local_radius_miles: integer     # Search radius for local vendors, default 25
```

## Process

### Mode A: Plan Only (Current)

This is the active mode. All output is advisory; no external API calls are made.

**Step 1 -- Event Concept Generation**
- Match event type to property type, season, budget, and tenant demographics
- Generate 2-3 concept options with varying budget allocations
- Each concept includes: theme, description, target attendance, space requirements, weather contingency (if outdoor)
- Reference `references/event-playbook.md` for type-specific benchmarks

**Step 2 -- Budget Breakdown**
- Allocate budget across standard line items:
  - Venue/space preparation: 5-15% (on-site) or 25-35% (off-site rental)
  - Catering/food & beverage: 35-45%
  - Entertainment/activities: 10-20%
  - Decor/ambiance: 5-10%
  - Staffing (event coordinator, setup/teardown): 5-10%
  - Marketing/communications (signage, invites, swag): 5-10%
  - Contingency: 10%
- Flag if budget per attendee is below $8 (hard to deliver quality) or above $50 (diminishing returns for non-corporate)
- Provide unit-cost breakdown for each line item

**Step 3 -- Timeline**
- Major events (holiday party, annual appreciation): 8-week countdown
- Standard events (BBQ, mixer, wellness fair): 4-week countdown
- Minor events (food truck, decoration reveal): 2-week countdown
- Each timeline includes: vendor outreach, booking deadlines, communication milestones, setup logistics, day-of schedule

**Step 4 -- Vendor Requirements Specification**
- For each vendor category needed, produce:
  - Scope of work description
  - Quantity and headcount estimates (plan for 60-70% of invited for MF, 50-60% for office)
  - Dietary and accessibility requirements
  - Setup/teardown time windows
  - Insurance and liability requirements
  - RFP template ready to send to vendors
- Reference `references/vendor-booking-schemas.yaml` for structured specs

**Step 5 -- Tenant Communication Plan**
- Save-the-date: 4 weeks out (major) or 2 weeks (minor)
- Formal invitation with RSVP: 2-3 weeks out
- Reminder: 3 days out
- Day-of signage and wayfinding
- Post-event thank-you with photos: within 48 hours
- Include channel recommendations: building app, email, lobby signage, door hangers (MF), elevator screens

**Step 6 -- ROI Projection**
- Forecast attendance based on event type and property benchmarks
- Estimate retention impact using methodology from `references/event-roi-model.md`
- Calculate cost-per-attendee and cost-per-unit
- Project satisfaction score lift (NPS or equivalent)
- Compare to benchmark spending for property class and type

**Step 7 -- Post-Event Debrief Template**
- Attendance vs. forecast
- Budget actual vs. planned
- Tenant feedback summary (survey template included)
- Vendor performance rating
- Recommendations for next event
- Photos/documentation for marketing use

### Mode B: Plan and Book (Future, API-Integrated)

Activates when `execution_mode: plan_and_book` and required MCP servers are connected. Includes all Mode A steps plus automated vendor engagement.

**Step 8 -- Vendor Search via MCP**
- Query connected vendor MCP servers (catering, entertainment, rentals)
- Filter by location, availability, capacity, budget range
- Return ranked list with ratings, pricing, availability

**Step 9 -- Quote Comparison**
- Request formal quotes from top 3 vendors per category
- Normalize pricing to per-attendee basis for comparison
- Present comparison table with: price, included items, reviews, availability, cancellation terms

**Step 10 -- Approval Gate**
- Present full plan with selected vendors and total cost to user
- REQUIRE explicit human approval before any financial commitment
- No booking proceeds without written confirmation

**Step 11 -- Booking Confirmation**
- Execute bookings via MCP tool calls
- Capture confirmation numbers, contracts, payment terms
- Generate consolidated event order with all vendor details

**Step 12 -- Vendor Coordination**
- Automated reminder timeline for each vendor (1 week, 3 days, day-of)
- Setup/delivery time coordination across vendors
- Contact sheet for day-of communications

**Step 13 -- Day-of Logistics**
- Consolidated run-of-show document
- Vendor arrival schedule
- Contingency contact list
- Real-time issue escalation protocol

**Step 14 -- Post-Event Settlement**
- Vendor invoice collection and reconciliation
- Vendor performance rating (stored for future events)
- Payment approval workflow
- Final budget reconciliation

## API Integration Architecture

This section defines how the skill transitions from Mode A to Mode B when MCP servers become available for vendor services.

### Integration Points

```yaml
mcp_integrations:
  catering:
    providers: [ezCater, CaterCow, Fooda, local_vendors]
    actions:
      - search_menus:
          input: {location, date, headcount, dietary_reqs, budget_range, cuisine_type}
          output: {vendor_list: [{name, menu_options, price_per_head, rating, min_order}]}
      - get_quotes:
          input: {vendor_id, menu_selections, headcount, date, time, delivery_address}
          output: {quote_id, line_items, total, tax, delivery_fee, cancellation_policy}
      - place_order:
          input: {quote_id, payment_method, contact_info, special_instructions}
          output: {order_id, confirmation, estimated_delivery, vendor_contact}
          approval_gate: true
      - modify_order:
          input: {order_id, changes}
          output: {updated_order, price_delta, confirmation}
      - cancel_order:
          input: {order_id, reason}
          output: {cancellation_confirmation, refund_amount, refund_timeline}
    data_flow: event_spec -> menu_search -> quote_comparison -> approval -> booking -> confirmation

  entertainment:
    providers: [GigSalad, Thumbtack, local_agencies]
    actions:
      - search_performers:
          input: {location, date, event_type, genre_or_category, duration, budget_range}
          output: {performer_list: [{name, category, price, rating, availability, media_samples}]}
      - check_availability:
          input: {performer_id, date, time, duration}
          output: {available, alternate_dates}
      - get_quotes:
          input: {performer_id, date, time, duration, venue_details, requirements}
          output: {quote_id, price, includes, rider_requirements, cancellation_terms}
      - book:
          input: {quote_id, payment_method, contact_info, venue_access_details}
          output: {booking_id, confirmation, performer_contact, setup_requirements}
          approval_gate: true
    data_flow: event_spec -> performer_search -> availability_check -> quote -> approval -> book

  rentals:
    providers: [CORT_Events, Party_Rental_Ltd, local_rental_companies]
    actions:
      - search_inventory:
          input: {location, date, items_needed: [{category, quantity, style_preference}]}
          output: {available_items: [{item, options, price_per_unit, delivery_fee}]}
      - check_availability:
          input: {item_ids, date_range}
          output: {availability_status, alternatives_if_unavailable}
      - get_quotes:
          input: {item_selections, delivery_date, pickup_date, delivery_address}
          output: {quote_id, line_items, delivery_fee, total, damage_waiver}
      - reserve:
          input: {quote_id, payment_method, contact_info, access_instructions}
          output: {reservation_id, confirmation, delivery_window, pickup_window}
          approval_gate: true
    data_flow: event_spec -> inventory_search -> availability -> quote -> approval -> reserve

  venue_services:
    providers: [building_amenity_system, common_area_booking]
    actions:
      - check_availability:
          input: {space_id, date, start_time, end_time, setup_buffer, teardown_buffer}
          output: {available, conflicts, alternate_times}
      - reserve_space:
          input: {space_id, date, time_range, event_description, setup_requirements}
          output: {reservation_id, confirmation, rules_and_restrictions}
      - setup_requirements:
          input: {reservation_id, furniture_config, av_needs, power_requirements}
          output: {work_order_id, estimated_cost, scheduling_confirmation}
    data_flow: event_spec -> space_search -> availability -> reserve -> setup_order

  communications:
    providers: [Mailchimp, building_app, AppFolio, Yardi]
    actions:
      - create_invite:
          input: {event_details, template_style, recipient_list_or_segment, rsvp_enabled}
          output: {draft_id, preview_url}
      - send_blast:
          input: {draft_id, send_time, channels: [email, app_push, sms]}
          output: {send_confirmation, recipient_count, delivery_stats}
          approval_gate: true
      - track_rsvps:
          input: {event_id}
          output: {total_invited, rsvps_yes, rsvps_no, rsvps_pending, dietary_responses}
      - send_reminders:
          input: {event_id, reminder_type: [3_day, day_of, post_event_thanks]}
          output: {send_confirmation, recipient_count}
    data_flow: event_plan -> invite_draft -> approval -> send -> track_rsvps -> reminders
```

### Fallback Behavior

When an MCP integration is unavailable, the skill degrades gracefully:

| Integration | Available | Unavailable Fallback |
|---|---|---|
| Catering | Search menus, get quotes, book | Generate RFP with specs, suggest local vendors to contact manually |
| Entertainment | Search performers, book | Generate performer requirements brief, suggest booking platforms |
| Rentals | Search inventory, reserve | Generate rental list with quantities, suggest rental companies |
| Venue services | Check/reserve building spaces | Generate space reservation request for property management |
| Communications | Send invites, track RSVPs | Generate email/flyer copy, provide RSVP tracking spreadsheet template |

### Approval Gates

Every action involving financial commitment requires explicit human approval:

```
1. Plan generated -> user reviews plan
2. Vendors selected -> user approves vendor shortlist
3. Quotes received -> user approves specific quote
4. Booking initiated -> user confirms booking (BLOCKING)
5. Payment processed -> user authorizes payment (BLOCKING)
```

No autonomous spending. The skill recommends; the human decides.

## Output Format

The final deliverable is a structured event plan document:

```
# [Event Name] -- Event Plan
## Property: [name] | Date: [date] | Budget: [$total]

### 1. Event Concept
- Theme and description
- Target attendance and demographics
- Space and layout plan
- Weather contingency (if applicable)

### 2. Budget
| Line Item | Budgeted | % of Total | Notes |
|---|---|---|---|
| Catering | $X | X% | [details] |
| Entertainment | $X | X% | [details] |
| ... | ... | ... | ... |
| **Total** | **$X** | **100%** | |

### 3. Timeline
[Week-by-week countdown with milestones]

### 4. Vendor Specifications
[Per-vendor scope, RFP template or booking confirmation]

### 5. Communications Plan
[Message schedule with draft copy]

### 6. ROI Projection
[Attendance forecast, retention impact, cost-per-attendee, ROI calculation]

### 7. Post-Event Debrief Template
[Survey questions, metrics to capture, vendor evaluation form]
```

## Red Flags

Flag and warn the user about:
- **Budget too low**: Below $8/attendee makes quality delivery difficult; recommend scaling scope
- **Budget too high**: Above $50/attendee for non-corporate events shows diminishing returns
- **Insufficient lead time**: Major event with less than 4 weeks; minor with less than 1 week
- **Operations conflict**: Event during building maintenance, move-in/move-out heavy periods, or other scheduled property activity
- **Accessibility omissions**: No dietary accommodation plan, no ADA compliance check, no weather backup for outdoor events
- **Seasonal mismatch**: Outdoor event planned for winter in cold climates, ice cream social in January
- **Insurance gap**: Events with alcohol, bouncy houses, or open flame without additional insurance coverage
- **Over-frequency**: More than one major event per month risks fatigue and budget strain
- **Under-frequency**: Fewer than 4 events per year provides no meaningful retention benefit

## Chain Notes

This skill connects to other CRE skills in the ecosystem:

- **Upstream**: Property data, tenant roster, lease terms feed into event planning decisions
- **Downstream**:
  - `tenant-retention-engine`: Event attendance and satisfaction data feed retention scoring
  - `property-operations-admin-toolkit`: Event logistics coordinate with building operations (elevator holds, parking, security, cleaning)
  - `property-performance-dashboard`: Event spending and tenant satisfaction metrics roll into property-level KPIs
- **Parallel**: `annual-budget-planner` allocates the tenant events line item that this skill spends against

## Version History

- 0.1.0: Initial release. Mode A (plan-only) fully specified. Mode B (plan-and-book) architecture defined, pending MCP server availability.
