# PII Sample Policy - Synthetic Only, No Real Data, Ever

Every sample payload in this repo - `sample_input.json`, `sample_normalized.json`, `example_raw_payload.jsonl`, any test fixture, any illustrative snippet inside any doc - uses synthetic content. No real names. No real addresses. No real phone numbers. No real emails. No real SSNs. No real DOBs. No real vendor names that could trace to a real business. No real tenant ids.

This policy exists because any real record committed to this repo becomes a compliance incident the moment the repo is cloned, pushed to a public mirror, or shared with a third-party reviewer.

## Scope

Applies to:

- Every file under `reference/connectors/<domain>/sample_input.json`.
- Every file under `reference/connectors/<domain>/sample_normalized.json`.
- Every file under `reference/connectors/<domain>/example_raw_payload.jsonl`.
- Every file under `tests/fixtures/**` that represents an inbound record.
- Every illustrative snippet inside any `.md` file in `reference/connectors/**`.
- Every example in overlays, tailoring question banks, workflow docs, and role guides.

Does not apply to the operator's own test data outside the repo.

## Synthetic identifier conventions

Use these patterns when building sample data. They are easy to scan for, unlikely to collide with real identities, and recognizably fake.

### Resident and employee names

Use name patterns that read as obviously synthetic:

- `alpha_resident_one`, `alpha_resident_two`, `beta_resident_one`
- `sample_tenant_alpha`, `sample_tenant_beta`
- `test_employee_alpha`, `test_employee_beta`

Or use clearly-fictional first-last combinations that do not match any real person (for example, `Sample Alpha`, `Example Beta`). Do not use names pulled from real directories, social media, or third-party services.

### Emails

Use non-routable example domains:

- `alpha@example.test`
- `resident.alpha@sample.test`
- `employee.beta@fixture.test`

The `.test`, `.example`, and `.invalid` TLDs are reserved for this purpose. Do not use `gmail.com`, `yahoo.com`, or any real corporate domain.

### Phone numbers

Use the North American "555" reserved range:

- `+1-555-555-0100`
- `+1-555-555-0101`

Or, for international samples, use documented-example ranges. Never use a real number.

### Physical addresses

Use addresses that cannot resolve to a real building:

- `100 Example Street, Sample City, Example State 00000`
- `200 Sample Avenue, Fixture City, Test State 00000`

Do not copy real addresses from Google Maps, listing sites, or property records.

### Unit numbers

Unit numbers are low-sensitivity when scoped to a synthetic property. Use patterns like `unit_alpha_101`, `unit_beta_202`.

### Dates of birth and ages

`date_of_birth` is classified `high` and `allowed_in_sample: false`. Do not include DOB in any sample. Use `age_bucket: adult` or a similar coded form if the record type requires age reasoning.

### SSN and government ID

`ssn` and `government_id` are `restricted` and `allowed_in_sample: false`. Never appear in any sample. Under no circumstances. Not even as `000-00-0000` or any other "obviously fake" value - the secret-scan test will flag SSN-shaped strings regardless of whether the digits are plausible.

### Credit scores and background checks

`credit_score` and `background_check_result` are `high` and `allowed_in_sample: false`. If a sample must illustrate the schema shape, render the field name with a placeholder such as `credit_score_bucket: sample_bucket_alpha` and a note that the real field is not represented in sample data.

### Payment instrument detail

`payment_instrument_detail` is `high` and `allowed_in_sample: false`. Do not include account numbers, routing numbers, or card numbers in samples. Use tokenized placeholders: `payment_instrument_token: sample_token_alpha`.

### Vendor names

`vendor_legal_name` is `low` but names that match a real business are prohibited. Use `sample_vendor_alpha`, `fixture_vendor_beta`, `test_vendor_gamma`. Do not use the name of any real company, even one that does not do residential-multifamily work.

### Vendor tax ids

`vendor_tax_id` is `high` and `allowed_in_sample: false`. Do not include real or fake EINs in samples.

### Account numbers and bank routing

`account_number` and `bank_routing` are `high` and `allowed_in_sample: false`. The sample-scan test will flag 9-digit strings that look routing-shaped and 12-to-17-digit strings that look account-shaped.

### Employee compensation

`compensation_detail` is `high` and `allowed_in_sample: false`. Samples that illustrate payroll shape may carry a `compensation_band: sample_band_alpha` token but never a dollar figure (which also breaks the prose numeric-density rule in `_core/DESIGN_RULES.md`).

### Eviction and fair-housing narratives

`eviction_detail` and `fair_housing_complaint_detail` carry free-text narratives that may leak details even when the names are synthetic. Samples may include a status code only (`status_code: notice_served`, `status_code: case_filed`), never a narrative.

## Sample-data redaction checklist

Before committing or reviewing any sample file, run this checklist:

- [ ] All names are synthetic, using `alpha/beta/gamma` or `sample/example/fixture` conventions.
- [ ] All emails use `.test`, `.example`, or `.invalid` TLDs.
- [ ] All phones use `+1-555-555-01xx` or a documented-example equivalent.
- [ ] All addresses use `Sample City / Example State / ZIP 00000`-style placeholders.
- [ ] No `date_of_birth` field appears. No date that could be a DOB appears under a differently-named field.
- [ ] No string matches the SSN regex (`\d{3}-?\d{2}-?\d{4}`) anywhere in the file.
- [ ] No string matches the routing regex (`\b\d{9}\b`) or the account regex (`\b\d{12,17}\b`) anywhere in the file.
- [ ] No real company name, real property name, or real tenant name appears.
- [ ] No credit_score, no background_check_result, no compensation_detail numeric value appears.
- [ ] No eviction or fair-housing narrative appears - only status codes.
- [ ] File header comment states the file is a synthetic sample and cites this policy.

## File header convention

Every sample file carries a header block that states synthetic status and cites this policy. Example for a JSONL file:

```
// synthetic sample - no real PII, no real credentials, no real business names.
// all values are fixture content; see pii_sample_policy.md.
```

Or for a YAML file:

```
# synthetic sample - no real PII, no real credentials, no real business names.
# all values are fixture content; see pii_sample_policy.md.
```

## Reviewer scan

Reviewers scan every sample-bearing PR for the patterns above. A sample file that fails the checklist is rejected. A sample file that slips through and is discovered later triggers the secret-leakage incident protocol in `secrets_handling.md`, scaled to PII rather than credential material, with the same shred-and-replace handling of the raw file.

## Illustrative-only examples

The allowed synthetic example for a minimal PMS lease record:

```json
{
  "entity": "lease",
  "lease_id": "sample_lease_alpha_001",
  "property_id": "sample_property_alpha",
  "unit_number": "unit_alpha_101",
  "resident_name": "alpha_resident_one",
  "email": "resident.alpha@example.test",
  "phone": "+1-555-555-0100",
  "lease_start": "2025-01-01",
  "lease_end": "2025-12-31",
  "source_name": "sample_source",
  "source_type": "pms",
  "source_date": "2025-04-01",
  "extracted_at": "2025-04-01T00:00:00Z",
  "extractor_version": "sample-0.0.1",
  "source_row_id": "sample_row_alpha_001"
}
```

The same record in an unallowed real-data form would carry a real name, real email, real phone, real address, and real dates tied to a real person. That form is prohibited regardless of whether the person has consented or is an employee of the operator.

## Related enforcement

- `security_testing_guidance.md` - defines the sample-scan test set.
- `pii_classification.md` - canonical `allowed_in_sample` values per field.
- `unsafe_defaults_registry.md` - the PII-in-samples entry.
- `_core/DESIGN_RULES.md` - the no-real-PII rule at the subsystem level.
