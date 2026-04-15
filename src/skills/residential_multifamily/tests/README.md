# Tests

Validation tests that run alongside the existing `tests/` tree at repo root. These tests do not replace any existing test; they extend the suite.

## How to run

From the repo root:

```bash
pytest tests/residential_multifamily/ -v
```

The tests do not require live market data. They validate structure, schema conformance, naming, reference manifests, and render-ability against sample data.

## What these tests validate

1. **Reference manifests exist and link correctly.**
   Every pack has `reference_manifest.yaml`; every path listed exists; every path exists in a pack manifest that reads it.

2. **Metric contracts are complete.**
   Every metric in `_core/metrics.md` has every required contract field. Every metric slug used in a pack `metrics_used` or pack body appears in `_core/metrics.md` or in an overlay's `adds`.

3. **No hard-coded market figures in skill prose.**
   Scans role/workflow/overlay `.md` files outside fenced code blocks for numeric density patterns that suggest embedded financial figures (e.g., dollar amounts, occupancy percentages, material prices) not attached to a reference citation.

4. **Routing loads correct overlays.**
   Given a test set of scenario inputs, the router resolves axes and selects the expected pack + overlay stack.

5. **Missing data fails gracefully.**
   Reference files with deliberately removed required scopes produce the declared fallback behavior, not silent defaults.

6. **Naming conflicts are detected.**
   No duplicate metric slugs, no alias used without registration, no collisions across metric and object namespaces.

7. **Templates render.**
   Every template renders against a sample input without unfilled placeholders.

8. **Update workflows preserve version and as-of fields.**
   A simulated reference update produces a valid `change_log_entry` and preserves prior in `archives/`.

9. **Segment stubs do not override middle-market behavior.**
   The luxury and affordable overlays do not silently alter `middle_market` target bands.

10. **Fair-housing scans on resident-facing template output.**
    Rendered resident templates are scanned for forbidden phrases (preference signaling, protected-class references). Unregistered flagged phrases fail.

## File map

```
tests/residential_multifamily/
  __init__.py
  conftest.py
  test_metric_contracts.py
  test_alias_registry.py
  test_skill_manifests.py
  test_reference_manifests.py
  test_no_hardcoded_figures.py
  test_routing.py
  test_naming_collisions.py
  test_template_rendering.py
  test_change_log.py
  test_segment_overlay_integrity.py
  test_fair_housing_banner.py
  fixtures/
    properties/           # sample property master rows
    rent_rolls/           # sample rent roll snapshots
    funnel/               # sample CRM funnel snapshots
    work_orders/          # sample WO exports
    scenarios/            # routing scenario inputs and expected outputs
```

## Conventions

- Tests use PyYAML for YAML loading and plain CSV reader for CSVs.
- Tests rely only on the standard library + PyYAML. No live-service dependencies.
- Fixtures are sample data tagged `status: sample`.
- Tests that compare outputs to expected strings prefer regex patterns and structural assertions over exact text.
