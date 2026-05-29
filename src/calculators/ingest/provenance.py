"""Canonical provenance bundle for every emitted record.

This is a strict SUPERSET of the existing 8-column warehouse provenance
contract (``document-to-warehouse-pipeline/references/warehouse-schema-conventions.md``):
``source_doc, locator, source_ref, extracted_by, classification, confidence,
review_status, extracted_at`` are all preserved (with the same allowed values
and the canonical ``data-room/<doc>#<anchor>`` join key) so the new layer joins
cleanly with the prose chain and the AMOS source manifest.

It additionally carries the granular locator components the brief requires
(page / section / table / row / column / cell address), the run/skill/parser
identity, the tenancy label, and two governance fields:

- ``pii_class``        natural_person | identifier | contact | financial |
                       aggregate_safe (from :func:`pii.classify_field`).
- ``redaction_status`` raw | pseudonymized | redacted | aggregate-only.

``source_text_span`` (a VERBATIM value) is retained ONLY for non-PII
(aggregate-safe) fields. For PII-classified fields the cell ADDRESS is kept
but the value is never stored -- this is the locator-not-value rule.
"""
from __future__ import annotations

from typing import Any

from . import pii as _pii

CLASSIFICATIONS = ("source-fact", "calculated", "modeled-assumption", "requires-review")
CONFIDENCE_BANDS = ("high", "medium", "low")
REVIEW_STATUSES = ("accepted", "needs-review", "flagged")
REDACTION_STATUSES = ("raw", "pseudonymized", "redacted", "aggregate-only")

# The 8-column warehouse contract this bundle must remain a superset of.
WAREHOUSE_PROVENANCE_COLUMNS = (
    "source_doc",
    "locator",
    "source_ref",
    "extracted_by",
    "classification",
    "confidence",
    "review_status",
    "extracted_at",
)


def source_ref(doc: str, anchor: str) -> str:
    """Canonical join key back to the data room: data-room/<doc>#<anchor>."""
    return "data-room/%s#%s" % (doc, anchor)


def build_provenance(
    *,
    field_name: str,
    source_document_id: str,
    source_ref_anchor: str,
    skill_name: str,
    skill_version: str,
    run_id: str,
    as_of: str,
    classification: str = "source-fact",
    confidence: str = "medium",
    review_status: str = "needs-review",
    validation_status: str = "pass",
    tenant_id: Any = None,
    source_file_name: str | None = None,
    source_document_type: str | None = None,
    source_page: Any = None,
    source_section: str | None = None,
    source_table_id: str | None = None,
    source_row_number: Any = None,
    source_column_name: str | None = None,
    source_cell_address: str | None = None,
    extraction_method: str = "extracted",
    parser_version: str = "ingest-0.1.0",
    source_text_span: str | None = None,
    extracted_by: str | None = None,
) -> dict:
    """Assemble the provenance bundle for one record/field.

    Enforces the PII rule: if ``field_name`` classifies as PII, the verbatim
    ``source_text_span`` is dropped and ``redaction_status`` becomes
    ``redacted`` (the cell address locator is still kept).
    """
    pii_class = _pii.classify_field(field_name)
    locator = source_cell_address or source_section or source_page or source_ref_anchor

    if pii_class != "aggregate_safe":
        # Never retain a verbatim value for PII fields.
        span = None
        redaction_status = "redacted"
    else:
        span = source_text_span
        redaction_status = "raw"

    return {
        # --- 8-column warehouse superset (exact names/values preserved) ---
        "source_doc": source_document_id,
        "locator": locator,
        "source_ref": source_ref(source_document_id, source_ref_anchor),
        "extracted_by": extracted_by or skill_name,
        "classification": classification,
        "confidence": confidence,
        "review_status": review_status,
        "extracted_at": as_of,
        # --- granular locator components ---
        "source_document_id": source_document_id,
        "source_file_name": source_file_name,
        "source_document_type": source_document_type,
        "source_page": source_page,
        "source_section": source_section,
        "source_table_id": source_table_id,
        "source_row_number": source_row_number,
        "source_column_name": source_column_name,
        "source_cell_address": source_cell_address,
        "source_text_span": span,
        # --- run / skill / parser identity ---
        "extraction_method": extraction_method,
        "extraction_run_id": run_id,
        "skill_name": skill_name,
        "skill_version": skill_version,
        "parser_version": parser_version,
        # --- quality + lifecycle ---
        "confidence_score": _confidence_to_score(confidence),
        "validation_status": validation_status,
        "created_at": as_of,
        "updated_at": as_of,
        # --- tenancy + governance ---
        "tenant_id_or_workspace_id": tenant_id,
        "pii_class": pii_class,
        "redaction_status": redaction_status,
    }


def _confidence_to_score(band: str) -> float:
    """Deterministic band -> score (high=0.95, medium=0.75, low=0.4)."""
    return {"high": 0.95, "medium": 0.75, "low": 0.4}.get(band, 0.4)
