"""Target-model profiles (database adapters).

Five profiles, each a declarative table catalog that drives ``map_to_target_model``
(shape), ``emit_sql_ddl`` (CREATE TABLE), and ``emit_load_plan`` (FK-ordered
load). These describe a TARGET WAREHOUSE schema and are NOT executed by the
amos-prototype runtime: the AMOS staging tables (migration 005) are a flatter,
FK-free, session-scoped subset on purpose (the Neon HTTP driver runs one
statement per round-trip and the house schema carries no foreign keys).

Profiles:
  raw_landing         preserve raw extraction + hash + provenance (audit tier).
  normalized_relational  AMOS-app-shaped entities (the cash-flow spine).
  star_schema         analytics dims + facts.
  data_vault          enterprise lineage (hubs / links / satellites).
  hybrid_recommended  composition: raw -> normalized -> star (+ optional vault).

A table entry: {grain, primary_key, columns:[(name, sql_type, nullable)],
foreign_keys:[(col, ref_table, ref_col)], load_order}.
"""
from __future__ import annotations

TARGET_PROFILES = (
    "raw_landing",
    "normalized_relational",
    "star_schema",
    "data_vault",
    "hybrid_recommended",
)

NUMERIC_MONEY = "numeric(18,2)"
NUMERIC_RATE = "numeric(12,6)"

# Provenance columns appended to landing/fact rows (superset of the 8-col
# warehouse contract). Kept FK-free.
_PROV = [
    ("source_doc", "text", False),
    ("locator", "text", True),
    ("source_ref", "text", False),
    ("extracted_by", "text", True),
    ("classification", "text", True),
    ("confidence", "text", True),
    ("review_status", "text", True),
    ("extracted_at", "timestamptz", True),
    ("extraction_run_id", "text", False),
    ("skill_version", "text", True),
    ("pii_class", "text", True),
    ("redaction_status", "text", True),
    ("tenant_id_or_workspace_id", "text", True),
]


def _t(grain, pk, columns, load_order, foreign_keys=None):
    return {
        "grain": grain,
        "primary_key": pk,
        "columns": columns,
        "foreign_keys": foreign_keys or [],
        "load_order": load_order,
    }


RAW_LANDING = {
    "cre_raw_extraction_record": _t(
        "one row per extracted record, raw payload preserved",
        ["raw_id"],
        [
            ("raw_id", "text", False),
            ("doc_type", "text", False),
            ("document_hash", "text", False),
            ("raw_payload", "jsonb", False),
        ]
        + _PROV,
        load_order=1,
    ),
}

NORMALIZED_RELATIONAL = {
    "cre_fund": _t("one row per fund", ["fund_id"],
                   [("fund_id", "text", False), ("fund_name", "text", True)], 1),
    "cre_property": _t("one row per property", ["property_id"],
                       [("property_id", "text", False), ("fund_id", "text", True),
                        ("property_name", "text", True), ("address", "text", True),
                        ("market", "text", True), ("property_type", "text", True),
                        ("units", "integer", True), ("rentable_sf", "numeric(18,2)", True)],
                       2, [("fund_id", "cre_fund", "fund_id")]),
    "cre_document": _t("one row per source document", ["document_id"],
                       [("document_id", "text", False), ("property_id", "text", True),
                        ("doc_type", "text", True), ("as_of", "date", True),
                        ("document_hash", "text", True)],
                       3, [("property_id", "cre_property", "property_id")]),
    "cre_unit": _t("one row per unit/suite/space", ["unit_id"],
                   [("unit_id", "text", False), ("property_id", "text", False),
                    ("building", "text", True), ("floor", "text", True),
                    ("suite", "text", True), ("unit_type", "text", True),
                    ("rentable_sf", "numeric(18,2)", True), ("unit_status", "text", True)],
                   3, [("property_id", "cre_property", "property_id")]),
    "cre_tenant": _t("one row per (pseudonymized) tenant", ["tenant_id"],
                     [("tenant_id", "text", False), ("property_id", "text", True),
                      ("tenant_code", "text", False), ("normalized_name", "text", True),
                      ("industry", "text", True)],
                     3, [("property_id", "cre_property", "property_id")]),
    "cre_lease": _t("one row per lease", ["lease_id"],
                    [("lease_id", "text", False), ("tenant_id", "text", True),
                     ("unit_id", "text", True), ("lease_status", "text", True),
                     ("lease_type", "text", True), ("lease_start", "date", True),
                     ("lease_expire", "date", True), ("recovery_method", "text", True),
                     ("base_year", "integer", True), ("expense_stop_psf", NUMERIC_MONEY, True),
                     ("free_rent_months", "numeric(6,2)", True), ("security_deposit", NUMERIC_MONEY, True)],
                    4, [("tenant_id", "cre_tenant", "tenant_id"), ("unit_id", "cre_unit", "unit_id")]),
    "cre_charge_schedule": _t("one row per lease charge line", ["charge_line_id"],
                              [("charge_line_id", "text", False), ("lease_id", "text", False),
                               ("charge_code", "text", True), ("charge_category", "text", True),
                               ("canonical_account", "text", True), ("monthly_amount", NUMERIC_MONEY, True),
                               ("annual_amount", NUMERIC_MONEY, True), ("frequency", "text", True),
                               ("is_recoverable", "boolean", True), ("is_estimate", "boolean", True),
                               ("effective_start", "date", True), ("effective_end", "date", True)],
                              5, [("lease_id", "cre_lease", "lease_id")]),
    "cre_account": _t("one row per canonical account", ["canonical_account"],
                      [("canonical_account", "text", False), ("account_type", "text", True),
                       ("normal_balance", "text", True), ("statement_section", "text", True)],
                      2),
    "cre_account_mapping": _t("one row per source account -> canonical", ["source_account_id", "canonical_account"],
                              [("source_account_id", "text", False), ("canonical_account", "text", False),
                               ("match_method", "text", True), ("match_confidence", "text", True)],
                              3, [("canonical_account", "cre_account", "canonical_account")]),
    "cre_operating_statement_line": _t("one row per account x period x scenario", ["os_line_id"],
                                       [("os_line_id", "text", False), ("property_id", "text", False),
                                        ("canonical_account", "text", True), ("statement_section", "text", True),
                                        ("line_type", "text", True), ("fiscal_period", "text", True),
                                        ("amount", NUMERIC_MONEY, True)],
                                       5, [("property_id", "cre_property", "property_id"),
                                           ("canonical_account", "cre_account", "canonical_account")]),
    "cre_ingestion_run": _t("one row per ingestion run", ["ingestion_run_id"],
                            [("ingestion_run_id", "text", False), ("doc_type", "text", True),
                             ("as_of", "date", True), ("grade", "text", True),
                             ("score_100", NUMERIC_RATE, True), ("status", "text", True)],
                            1),
    "cre_validation_issue": _t("one row per validation issue", ["issue_id"],
                               [("issue_id", "text", False), ("ingestion_run_id", "text", False),
                                ("code", "text", True), ("severity", "text", True),
                                ("field_path", "text", True), ("detail", "text", True)],
                               6, [("ingestion_run_id", "cre_ingestion_run", "ingestion_run_id")]),
    "cre_human_review_item": _t("one row per human-review item", ["review_id"],
                                [("review_id", "text", False), ("ingestion_run_id", "text", False),
                                 ("reason", "text", True), ("field_path", "text", True),
                                 ("confidence", "text", True), ("status", "text", True)],
                                6, [("ingestion_run_id", "cre_ingestion_run", "ingestion_run_id")]),
    "cre_reconciliation_result": _t("one row per tie-out dimension", ["recon_id"],
                                    [("recon_id", "text", False), ("ingestion_run_id", "text", True),
                                     ("dimension", "text", True), ("rent_roll_value", NUMERIC_MONEY, True),
                                     ("t12_value", NUMERIC_MONEY, True), ("variance", NUMERIC_MONEY, True),
                                     ("variance_pct", NUMERIC_RATE, True), ("difference_type", "text", True),
                                     ("tie_status", "text", True), ("residual_unexplained", NUMERIC_MONEY, True),
                                     ("basis", "text", True)],
                                    6),
}

STAR_SCHEMA = {
    "dim_property": _t("property dimension", ["property_key"],
                       [("property_key", "text", False), ("property_id", "text", False),
                        ("property_name", "text", True), ("market", "text", True),
                        ("property_type", "text", True)], 1),
    "dim_tenant": _t("tenant dimension (pseudonymized)", ["tenant_key"],
                     [("tenant_key", "text", False), ("tenant_code", "text", False),
                      ("industry", "text", True)], 1),
    "dim_lease": _t("lease dimension", ["lease_key"],
                    [("lease_key", "text", False), ("lease_id", "text", False),
                     ("lease_type", "text", True), ("recovery_method", "text", True)], 1),
    "dim_unit": _t("unit dimension", ["unit_key"],
                   [("unit_key", "text", False), ("unit_id", "text", False),
                    ("unit_type", "text", True), ("unit_status", "text", True)], 1),
    "dim_account": _t("account dimension", ["account_key"],
                      [("account_key", "text", False), ("canonical_account", "text", False),
                       ("account_type", "text", True), ("statement_section", "text", True)], 1),
    "dim_charge_code": _t("charge-code dimension", ["charge_code_key"],
                          [("charge_code_key", "text", False), ("charge_code", "text", True),
                           ("charge_category", "text", True)], 1),
    "dim_time": _t("period dimension", ["time_key"],
                   [("time_key", "text", False), ("fiscal_period", "text", False),
                    ("year", "integer", True), ("month", "integer", True)], 1),
    "dim_document": _t("document dimension", ["document_key"],
                       [("document_key", "text", False), ("document_id", "text", False),
                        ("doc_type", "text", True)], 1),
    "fact_lease_charge": _t("grain: lease x charge x period", ["lease_charge_fact_id"],
                            [("lease_charge_fact_id", "text", False), ("lease_key", "text", True),
                             ("charge_code_key", "text", True), ("account_key", "text", True),
                             ("time_key", "text", True), ("monthly_amount", NUMERIC_MONEY, True),
                             ("annual_amount", NUMERIC_MONEY, True)],
                            2, [("lease_key", "dim_lease", "lease_key"),
                                ("account_key", "dim_account", "account_key"),
                                ("time_key", "dim_time", "time_key")]),
    "fact_operating_statement": _t("grain: property x account x period x line_type", ["os_fact_id"],
                                   [("os_fact_id", "text", False), ("property_key", "text", True),
                                    ("account_key", "text", True), ("time_key", "text", True),
                                    ("line_type", "text", True), ("amount", NUMERIC_MONEY, True)],
                                   2, [("property_key", "dim_property", "property_key"),
                                       ("account_key", "dim_account", "account_key"),
                                       ("time_key", "dim_time", "time_key")]),
    "fact_reconciliation_variance": _t("grain: property x dimension x period", ["recon_fact_id"],
                                       [("recon_fact_id", "text", False), ("property_key", "text", True),
                                        ("time_key", "text", True), ("dimension", "text", True),
                                        ("variance", NUMERIC_MONEY, True), ("variance_pct", NUMERIC_RATE, True),
                                        ("difference_type", "text", True), ("residual_unexplained", NUMERIC_MONEY, True)],
                                       2, [("property_key", "dim_property", "property_key"),
                                           ("time_key", "dim_time", "time_key")]),
}

DATA_VAULT = {
    "hub_property": _t("property hub", ["property_hk"],
                       [("property_hk", "text", False), ("property_bk", "text", False),
                        ("load_dts", "timestamptz", True), ("record_source", "text", True)], 1),
    "hub_tenant": _t("tenant hub", ["tenant_hk"],
                     [("tenant_hk", "text", False), ("tenant_bk", "text", False),
                      ("load_dts", "timestamptz", True), ("record_source", "text", True)], 1),
    "hub_lease": _t("lease hub", ["lease_hk"],
                    [("lease_hk", "text", False), ("lease_bk", "text", False),
                     ("load_dts", "timestamptz", True), ("record_source", "text", True)], 1),
    "hub_unit": _t("unit hub", ["unit_hk"],
                   [("unit_hk", "text", False), ("unit_bk", "text", False),
                    ("load_dts", "timestamptz", True), ("record_source", "text", True)], 1),
    "hub_account": _t("account hub", ["account_hk"],
                      [("account_hk", "text", False), ("account_bk", "text", False),
                       ("load_dts", "timestamptz", True), ("record_source", "text", True)], 1),
    "hub_charge_code": _t("charge-code hub", ["charge_code_hk"],
                          [("charge_code_hk", "text", False), ("charge_code_bk", "text", False),
                           ("load_dts", "timestamptz", True), ("record_source", "text", True)], 1),
    "hub_document": _t("document hub", ["document_hk"],
                       [("document_hk", "text", False), ("document_bk", "text", False),
                        ("load_dts", "timestamptz", True), ("record_source", "text", True)], 1),
    "link_tenant_lease": _t("tenant<->lease link", ["tenant_lease_hk"],
                            [("tenant_lease_hk", "text", False), ("tenant_hk", "text", False),
                             ("lease_hk", "text", False), ("load_dts", "timestamptz", True)],
                            2, [("tenant_hk", "hub_tenant", "tenant_hk"), ("lease_hk", "hub_lease", "lease_hk")]),
    "link_lease_unit": _t("lease<->unit link", ["lease_unit_hk"],
                          [("lease_unit_hk", "text", False), ("lease_hk", "text", False),
                           ("unit_hk", "text", False), ("load_dts", "timestamptz", True)],
                          2, [("lease_hk", "hub_lease", "lease_hk"), ("unit_hk", "hub_unit", "unit_hk")]),
    "link_lease_charge_code": _t("lease<->charge-code link", ["lease_charge_hk"],
                                 [("lease_charge_hk", "text", False), ("lease_hk", "text", False),
                                  ("charge_code_hk", "text", False), ("load_dts", "timestamptz", True)],
                                 2, [("lease_hk", "hub_lease", "lease_hk"), ("charge_code_hk", "hub_charge_code", "charge_code_hk")]),
    "link_charge_code_account": _t("charge-code<->account link", ["charge_account_hk"],
                                   [("charge_account_hk", "text", False), ("charge_code_hk", "text", False),
                                    ("account_hk", "text", False), ("load_dts", "timestamptz", True)],
                                   2, [("charge_code_hk", "hub_charge_code", "charge_code_hk"), ("account_hk", "hub_account", "account_hk")]),
    "link_rent_roll_t12_reconciliation": _t("rent-roll<->t12 reconciliation link", ["recon_hk"],
                                            [("recon_hk", "text", False), ("property_hk", "text", False),
                                             ("account_hk", "text", True), ("load_dts", "timestamptz", True)],
                                            2, [("property_hk", "hub_property", "property_hk")]),
    "sat_lease_terms": _t("lease-terms satellite", ["lease_hk", "load_dts"],
                          [("lease_hk", "text", False), ("load_dts", "timestamptz", False),
                           ("lease_type", "text", True), ("recovery_method", "text", True),
                           ("base_year", "integer", True), ("free_rent_months", "numeric(6,2)", True),
                           ("hash_diff", "text", True)],
                          3, [("lease_hk", "hub_lease", "lease_hk")]),
    "sat_charge_schedule": _t("charge-schedule satellite", ["charge_code_hk", "load_dts"],
                              [("charge_code_hk", "text", False), ("load_dts", "timestamptz", False),
                               ("monthly_amount", NUMERIC_MONEY, True), ("is_recoverable", "boolean", True),
                               ("hash_diff", "text", True)],
                              3, [("charge_code_hk", "hub_charge_code", "charge_code_hk")]),
    "sat_document_extraction": _t("document-extraction satellite", ["document_hk", "load_dts"],
                                  [("document_hk", "text", False), ("load_dts", "timestamptz", False),
                                   ("extraction_run_id", "text", True), ("confidence", "text", True),
                                   ("redaction_status", "text", True), ("hash_diff", "text", True)],
                                  3, [("document_hk", "hub_document", "document_hk")]),
    "sat_validation_results": _t("validation-results satellite", ["property_hk", "load_dts"],
                                 [("property_hk", "text", False), ("load_dts", "timestamptz", False),
                                  ("grade", "text", True), ("score_100", NUMERIC_RATE, True),
                                  ("hash_diff", "text", True)],
                                 3, [("property_hk", "hub_property", "property_hk")]),
}

PROFILE_TABLES = {
    "raw_landing": RAW_LANDING,
    "normalized_relational": NORMALIZED_RELATIONAL,
    "star_schema": STAR_SCHEMA,
    "data_vault": DATA_VAULT,
}

# The recommended hybrid is a composition, not a new table set.
HYBRID_COMPOSITION = ("raw_landing", "normalized_relational", "star_schema")


def profile_tables(profile: str) -> dict:
    """Resolve a profile to its table catalog. hybrid_recommended composes
    raw + normalized + star (vault is opt-in for enterprise lineage)."""
    if profile == "hybrid_recommended":
        merged: dict = {}
        for p in HYBRID_COMPOSITION:
            merged.update(PROFILE_TABLES[p])
        return merged
    return PROFILE_TABLES.get(profile, {})
