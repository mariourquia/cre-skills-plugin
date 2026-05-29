"""Document-to-database ingestion: shared, stdlib-only support package.

This subpackage is the single internal source of truth shared by every
``*-to-database`` ingestion calculator in ``src/calculators/``:

- ``schema``      canonical field enums + record builders (charge schedule,
                  operating-statement line, unit/lease status, line types).
- ``accounts``    canonical chart-of-accounts slugs + charge-code/account
                  mapping. Mirrors ``residential_multifamily`` GL crosswalk;
                  parity enforced by ``tests/test_ingestion_canonical_sources.py``.
- ``rubric``      executable realization of ``rent-roll-analyzer``'s
                  ``data-quality-rubric.yaml`` (weakest-link A/B/C + 0-100).
- ``pii``         PII field classification, pseudonymization, leak scanning;
                  mirrors ``document-to-data-room-extractor``'s
                  ``pii-redaction-policy.yaml`` hard-stop boundary.
- ``provenance``  the canonical provenance bundle (superset of the 8-column
                  warehouse contract) and the ``data-room/<doc>#<anchor>`` ref.
- ``profiles``    target-model adapters (raw / normalized / star / vault /
                  hybrid) consumed by ``map_to_target_model`` / ``emit_sql_ddl``
                  / ``emit_load_plan``.
- ``tolerances``  dimension-specific reconciliation/validation tolerances.
- ``determinism`` rounding + run-context helpers. NOTHING in this package
                  imports ``datetime`` / ``time``; timestamps are supplied by
                  the caller via ``as_of`` so output is byte-reproducible
                  (the ZDR / golden-snapshot guarantee, ADR-0002).

This subpackage lives BELOW the top-level ``*.py`` calculators on purpose:
the catalog/registry calculator-count globs only ``src/calculators/*.py`` (not
subdirectories), so these helpers are not miscounted as calculators.
"""

PACKAGE_VERSION = "0.1.0"
